# backend.py

# Importations nécessaires
import os, json, hashlib, re, pathlib
import PyPDF2  # Pour lire les fichiers PDF
import docx    # Pour lire les fichiers DOCX
import numpy as np
import faiss   # Indexation vectorielle
import streamlit as st  # Nécessaire pour le cache Streamlit
from sentence_transformers import SentenceTransformer  # Modèle d'embedding
from transformers import pipeline  # Modèle de résumé
from evaluate import load  # Outils d'évaluation BLEU/ROUGE

# 🔧 Paramètres globaux
EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
SUM_MODEL = "t5-small"
EMB_DIM = 384  # Dimension des vecteurs
INDEX_PATH = "faiss.index"
META_PATH = "meta.json"
TARGET_TOK = 150  # Nombre de tokens par segment

# 🚀 Chargement des modèles d'embedding et de résumé
@st.cache_resource(show_spinner=False)
def load_models():
    """
    Charge les modèles d'embedding (MiniLM) et de résumé (T5) une seule fois
    grâce au cache de Streamlit.
    """
    return SentenceTransformer(EMB_MODEL), pipeline("summarization", model=SUM_MODEL)

# 📄 Extraction de texte depuis différents formats de fichiers
def extract_text(file):
    """
    Extrait le texte brut d'un fichier PDF, DOCX ou TXT.
    """
    ext = pathlib.Path(file.name).suffix.lower()
    if ext == ".pdf":
        return "".join(p.extract_text() or "" for p in PyPDF2.PdfReader(file).pages)
    elif ext == ".docx":
        return "\n".join(p.text for p in docx.Document(file).paragraphs)
    else:
        return file.read().decode("utf-8", errors="ignore")

# ✂️ Segmentation du texte en blocs de 150 mots
def segment(text):
    """
    Divise un long texte en segments contenant environ 150 tokens.
    """
    sents = re.split(r"(?<=[.!?])\s*", text.replace("\n", " "))
    out, cur = [], ""
    for s in sents:
        cur += s.strip() + " "
        if len(cur.split()) >= TARGET_TOK:
            out.append(cur.strip())
            cur = ""
    if cur:
        out.append(cur.strip())
    return [re.sub(r"\s+", " ", s) for s in out if s.strip()]

# 📥 Chargement ou création d’un index FAISS
def build_or_load_faiss(emb):
    """
    Si un index FAISS existe, le charge ; sinon, en crée un vide.
    """
    if os.path.exists(INDEX_PATH):
        idx = faiss.read_index(INDEX_PATH)
        meta = json.load(open(META_PATH, encoding="utf-8"))
    else:
        idx = faiss.IndexFlatIP(EMB_DIM)
        meta = []
    return idx, meta

# 💾 Sauvegarde de l’index et des métadonnées
def save_index(index, meta):
    """
    Sauvegarde l’index FAISS et le fichier JSON de métadonnées.
    """
    faiss.write_index(index, INDEX_PATH)
    json.dump(meta, open(META_PATH, "w", encoding="utf-8"), ensure_ascii=False)

# ➕ Ajout de documents à l’index
def add_documents(files, emb, index, meta):
    """
    Indexe tous les segments de tous les fichiers non déjà présents.
    """
    added = []
    for f in files:
        h = hashlib.md5(f.getbuffer()).hexdigest()  # Empreinte pour éviter les doublons
        if any(m["hash"] == h for m in meta): continue
        text = extract_text(f)
        segments = segment(text)
        for i, s in enumerate(segments):
            vec = emb.encode([s], normalize_embeddings=True).astype("float32")
            index.add(vec)
            meta.append({"file": f.name, "segment_id": i, "text": s, "hash": h})
        added.append(f.name)
    if added:
        save_index(index, meta)
    return added

# 🔍 Recherche vectorielle
def search(query, emb, index, meta, top_k=5):
    """
    Recherche les segments les plus proches d’une requête.
    """
    if index.ntotal == 0: return []
    q = emb.encode([query], normalize_embeddings=True)
    D, I = index.search(np.array(q, dtype="float32"), top_k)
    return [meta[i] for i in I[0] if i < len(meta)]

# 📝 Résumé automatique
def summarize(texts, summ):
    """
    Génère un résumé du contenu en concaténant les segments pertinents.
    """
    return summ(" ".join(texts)[:1500], max_length=130, min_length=30, do_sample=False)[0]["summary_text"]

# 📊 Outils d’évaluation
bleu_metric = load("bleu")
rouge_metric = load("rouge")

def cached_evaluation(summary, reference):
    """
    Calcule et met en cache les scores BLEU et ROUGE.
    """
    key = hashlib.md5((summary + reference).encode("utf-8")).hexdigest()
    if not hasattr(st.session_state, "eval_cache"):
        st.session_state.eval_cache = {}
    if key in st.session_state.eval_cache:
        return st.session_state.eval_cache[key]
    b = bleu_metric.compute(predictions=[summary], references=[reference])["bleu"]
    r = rouge_metric.compute(predictions=[summary], references=[reference])
    st.session_state.eval_cache[key] = (b, r)
    return b, r
