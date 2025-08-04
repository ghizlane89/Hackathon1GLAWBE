
# 🧠 RAG T5 – Application Streamlit pour la génération et l’évaluation de résumés

Cette application **Streamlit** permet :
- d'**ingérer et indexer** des documents (PDF, DOCX, TXT),
- de faire une **recherche sémantique** (avec FAISS + SentenceTransformers),
- de générer un **résumé automatique** à l’aide du modèle `T5-small`,
- et d’**évaluer** ce résumé avec les métriques **BLEU** et **ROUGE**.

---

## 🚀 Fonctionnalités

- 📄 **Upload** de documents (PDF, DOCX, TXT)
- 🧠 **Indexation vectorielle** avec FAISS (similarité sémantique)
- 🔍 **Recherche intelligente** de segments pertinents
- ✂️ **Découpage automatique** du texte en segments
- 📝 **Génération de résumé** avec `T5-small` (multi-langue)
- 📊 **Évaluation automatique** du résumé généré vs un résumé de référence
- 💾 **Cache d’évaluation BLEU / ROUGE**
- ☁️ Accès via **tunnel Cloudflare**

---

## 🛠️ Dépendances

Les dépendances suivantes sont installées automatiquement au lancement :

- `streamlit`
- `PyPDF2`
- `python-docx`
- `sentence-transformers`
- `faiss-cpu`
- `transformers`
- `torch`
- `evaluate`
- `sacrebleu`
- `rouge_score`
- `spacy` (avec modèle `en_core_web_sm`)

---

## 📁 Structure du projet

```
├── app.py                  ← Interface Streamlit
├── cloudflared            ← Tunnel Cloudflare (exécutable)
├── faiss_index.idx        ← Index vectoriel FAISS
├── metadata.json          ← Métadonnées associées aux segments
├── .cache_eval/           ← Dossier de cache pour l’évaluation BLEU/ROUGE
├── README.md              ← Ce fichier
```

---

## ⚙️ Lancement de l'application

### 1. Cloner le repo (si applicable)
```bash
git clone <URL_DU_REPO>
cd <nom_du_dossier>
```

### 2. Exécuter le script de démarrage (inclus dans le notebook ou fichier `.py`)
Cela :
- installe toutes les dépendances
- télécharge `cloudflared`
- génère automatiquement `app.py`
- démarre Streamlit et expose l’URL publique

```bash
python nom_du_script.py
```

📎 **Note** : le lien public est affiché en console une fois le tunnel Cloudflare actif.

---

## 🌐 Accès distant à l’application

Une URL comme :

```
https://tunnel-xxxx.trycloudflare.com
```

sera générée automatiquement pour accéder à l’interface Streamlit depuis n’importe où.

---

## 📊 Exemple de flux utilisateur

1. Ajouter des documents via l’interface
2. Poser une question dans le champ de recherche
3. Voir les segments pertinents affichés
4. Lire le résumé généré automatiquement
5. Coller un résumé de référence (manuel ou externe)
6. Calculer les scores BLEU / ROUGE

---

## 📦 Modèles utilisés

- **Embedding** : `sentence-transformers/all-MiniLM-L6-v2`
- **Résumé** : `t5-small` (via `transformers.pipeline`)
- **Évaluation** : 
  - BLEU via `sacrebleu`
  - ROUGE via `rouge_score`

---

## ✅ TODO (optionnel)

- [ ] Ajouter support multilingue complet (français, espagnol…)
- [ ] Possibilité de télécharger le résumé généré
- [ ] Interface utilisateur personnalisée
- [ ] Support de fichiers HTML / Markdown

---

## 📜 Licence

Projet à usage personnel ou académique. Libre d’être modifié et distribué avec mention de l’auteur original.

---

## 🙏 Remerciements

- [Hugging Face](https://huggingface.co)
- [FAISS by Facebook AI](https://github.com/facebookresearch/faiss)
- [SpaCy](https://spacy.io)
- [Streamlit](https://streamlit.io)
