# 🔍 Projet Streamlit – RAG T5 Optimisé

Ce projet est une application Streamlit permettant de :

- Ajouter et indexer des documents (`PDF`, `DOCX`, `TXT`)
- Rechercher du contenu via similarité sémantique (FAISS + embeddings)
- Générer un résumé avec `T5`
- Évaluer le résumé automatiquement (BLEU / ROUGE)

---

## ⚙️ Fonctionnalités

### 📁 1. Ajout de documents
- Extraction du texte à partir de fichiers PDF, Word ou texte brut.
- Segmentation du texte en blocs d’environ 350 tokens.
- Nettoyage et vectorisation via `SentenceTransformer`.
- Indexation dans FAISS (`IndexFlatIP`).

### 🔎 2. Recherche sémantique
- Recherche de segments pertinents via similarité cosinus.
- Affichage des segments extraits.

### 📝 3. Résumé généré
- Utilisation du modèle `t5-small` (transformers).
- Résumé automatique basé sur les segments les plus pertinents.

### 📊 4. Évaluation
- Scores BLEU et ROUGE calculés pour comparer un résumé généré avec un résumé de référence (collé manuellement).
- Mise en cache intelligente des résultats pour éviter les recalculs inutiles.

---

## 🚀 Installation & Lancement

1. Clone ce dépôt ou copie les scripts fournis.
2. Assure-toi d’avoir **Python 3.9+**.
3. Lance simplement le script principal :

```bash
python ton_script.py
```

Ce script :
- Installe automatiquement toutes les dépendances
- Télécharge et configure `cloudflared`
- Lance l’app Streamlit
- Affiche une URL publique via Cloudflare pour accéder à l’app

---

## 📂 Arborescence

```bash
.
├── app.py                  # Interface Streamlit
├── cloudflared             # Binaire Cloudflare (tunnel)
├── faiss_index.idx         # Index FAISS (créé dynamiquement)
├── metadata.json           # Métadonnées des documents indexés
├── .cache_eval/            # Cache des scores BLEU/ROUGE
└── ton_script.py           # Script principal (setup + exécution)
```

---

## 🧠 Modèles utilisés

| Tâche             | Modèle                                 |
|------------------|-----------------------------------------|
| Embeddings       | `sentence-transformers/all-MiniLM-L6-v2` |
| Résumé           | `t5-small`                              |
| Évaluation BLEU  | `evaluate` (sacrebleu)                  |
| Évaluation ROUGE | `evaluate` (rouge_score)                |

---

## ❓ Pourquoi `IndexFlatIP` dans FAISS ?

`IndexFlatIP` est un type d’index FAISS basé sur le **produit scalaire interne** (Inner Product) :

- Utilisé ici avec des vecteurs **normalisés** → l’Inner Product ≈ Cosine Similarity
- ⚡ Très rapide et simple à utiliser
- 🔁 Compatible avec des embeddings générés par SentenceTransformer avec `normalize_embeddings=True`

---

## ✅ À faire (améliorations possibles)

- Ajouter une page FAQ ou documentation intégrée
- Passer à `faiss.IndexHNSWFlat` pour des recherches plus rapides sur grands corpus
- Ajouter une interface d’annotation pour entraîner un modèle de résumé custom
- Enregistrer l’historique des requêtes et des résumés

---

## 📬 Contact

Tu peux me demander des adaptations si tu veux un README en français simplifié, une version technique pour GitHub, ou un README avec visuels intégrés.