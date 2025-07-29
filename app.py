# app.py

# -------------------------
# 📦 Importations
# -------------------------
import streamlit as st
import time, threading

# Importation des fonctions de traitement depuis backend.py
from backend import (
    load_models, build_or_load_faiss, add_documents, search,
    summarize, cached_evaluation
)

# -------------------------
# 🎛️ Configuration de la page Streamlit
# -------------------------
st.set_page_config(
    page_title="🔍 RAG CPU AutoEval",  # Titre de l'onglet du navigateur
    layout="wide"                      # Mise en page large
)

# Titre principal de la page
st.title("📄 RAG Optimisé : Upload + Recherche + Résumé")


# -------------------------
# 🚀 Chargement des modèles + index FAISS
# -------------------------
# Charge le modèle d'embedding (MiniLM) et le modèle de résumé (T5)
emb, summ = load_models()

# Charge ou initialise l’index FAISS (vecteurs + métadonnées)
index, meta = build_or_load_faiss(emb)


# -------------------------
# 📁 Section : Ajout de documents
# -------------------------
st.header("📁 Ajout de documents")

# Permet à l'utilisateur d'uploader un ou plusieurs fichiers
files = st.file_uploader(
    "Ajoutez vos documents (formats pris en charge : PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

# Lorsqu’un ou plusieurs fichiers sont ajoutés
if files:
    with st.spinner("🔄 Indexation automatique en cours..."):
        # Envoie les fichiers au backend pour extraire, segmenter et indexer
        added = add_documents(files, emb, index, meta)

        # Réinitialise les anciens résultats de recherche et le résumé affiché
        st.session_state.results = []
        st.session_state.summary = ""
        st.session_state.eval_cache = {}

    # Affiche les fichiers nouvellement indexés
    if added:
        st.success(f"✅ Fichiers indexés : {', '.join(added)}")
    else:
        st.info("📎 Tous les fichiers étaient déjà présents dans l’index")


# -------------------------
# 🔍 Section : Recherche & Résumé
# -------------------------
st.header("🔍 Recherche et Résumé")

# Champ de saisie pour la question de l'utilisateur
query = st.text_input("Posez une question")

# Lorsque l'utilisateur clique sur "Chercher"
if st.button("Chercher"):
    if not query.strip():
        st.warning("⚠️ Veuillez entrer une requête.")
    else:
        with st.spinner("🔍 Recherche en cours..."):
            # Recherche les segments les plus pertinents dans l’index vectoriel
            res = search(query, emb, index, meta)

            # Sauvegarde les résultats pour affichage
            st.session_state.results = res

            # Réinitialise le cache d’évaluation
            st.session_state.eval_cache = {}

            # Prépare le texte à résumer
            valid = [r["text"] for r in res if r.get("text", "").strip()]

            # Génère le résumé si du texte valide a été trouvé
            st.session_state.summary = summarize(valid, summ) if valid else ""


# -------------------------
# 📑 Affichage des résultats de recherche
# -------------------------
if st.session_state.get("results"):
    st.subheader("📑 Segments pertinents")
    for r in st.session_state.results:
        # Affiche chaque segment dans un volet déroulant
        with st.expander(f"{r['file']} §{r['segment_id']}"):
            st.write(r["text"])


# -------------------------
# 📝 Affichage du résumé généré
# -------------------------
if st.session_state.get("summary", "").strip():
    st.subheader("📝 Résumé généré automatiquement")
    st.write(st.session_state.summary)


    # -------------------------
    # 📊 Section : Évaluation du résumé
    # -------------------------
    st.header("📊 Évaluation du résumé")

    # Initialisation des timers et du cache
    if "last_edit" not in st.session_state:
        st.session_state.last_edit = time.time()
    if "eval_ready" not in st.session_state:
        st.session_state.eval_ready = False

    # Zone de texte pour que l'utilisateur colle un résumé de référence
    ref = st.text_area(
        "📄 Collez un résumé de référence pour comparer avec celui généré",
        placeholder="Tapez ici...",
        key="ref_input"
    )

    # Met à jour le timestamp de la dernière saisie
    st.session_state.last_edit = time.time()

    # Fonction appelée en arrière-plan pour attendre 5s après la dernière frappe
    def trigger_eval():
        time.sleep(5)
        if time.time() - st.session_state.last_edit >= 5:
            st.session_state.eval_ready = True

    # Démarre la vérification différée si un texte est présent
    if ref.strip():
        threading.Thread(target=trigger_eval, daemon=True).start()

    # Affichage des scores BLEU / ROUGE
    if st.session_state.get("eval_ready"):
        status = st.info("🔍 Calcul des scores BLEU / ROUGE…")
        bar = st.progress(0)
        for pct in range(0, 101, 20):
            time.sleep(0.15)
            bar.progress(pct)

        # Calcule et affiche les scores
        b, r = cached_evaluation(st.session_state.summary, ref)
        status.empty()
        bar.empty()

        # Affichage formaté avec couleurs
        st.markdown(f"""
            <div style="display: flex; justify-content: space-around; gap: 1rem; margin-top: 1rem;">
                <div style="flex: 1; background:#3498db; color:white; padding:1em; border-radius:8px; text-align:center;">
                    <strong>🔵 BLEU</strong><br>{b:.3f}
                </div>
                <div style="flex: 1; background:#e74c3c; color:white; padding:1em; border-radius:8px; text-align:center;">
                    <strong>🔴 ROUGE-1</strong><br>{r['rouge1']:.3f}
                </div>
                <div style="flex: 1; background:#c0392b; color:white; padding:1em; border-radius:8px; text-align:center;">
                    <strong>🔴 ROUGE-L</strong><br>{r['rougeL']:.3f}
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("🕐 Entrez un résumé de référence pour lancer l’évaluation.")
