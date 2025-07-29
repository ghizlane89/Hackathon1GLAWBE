# 📄 AI-Powered Document Search & Summarization System

Un outil **IA** local permettant d’**ingérer des documents**, de faire une **recherche sémantique** sur leur contenu et de générer un **résumé automatique**, avec en bonus une **évaluation automatique** du résumé généré.

---

## 🚀 Fonctionnalités principales

- 📁 Upload de documents (PDF, DOCX, TXT)
- 🔍 Recherche sémantique avec embeddings (MiniLM)
- 📝 Résumé automatique des segments pertinents (T5)
- 📊 Évaluation des résumés avec les scores **BLEU** et **ROUGE**
- ⚙️ Fonctionne **en local**, sans GPU nécessaire

---

## 🧠 Technologies utilisées

| Composant              | Détail                                   |
|------------------------|-------------------------------------------|
| Frontend               | [Streamlit](https://streamlit.io)        |
| Embeddings             | `all-MiniLM-L6-v2` (via `sentence-transformers`) |
| Résumés                | `t5-small` (via `transformers`)          |
| Recherche sémantique   | `FAISS` (similarité cosinus)             |
| Évaluation             | `evaluate`, `bleu`, `rouge_score`        |

---

## 🗂️ Structure du projet

```
rag_local_project/
├── app.py          # Interface utilisateur Streamlit
├── backend.py      # Fonctions techniques (traitement + IA)
├── faiss.index     # Index vectoriel (auto-généré)
├── meta.json       # Métadonnées des documents (auto-généré)
├── venv/           # Environnement virtuel Python
└── README.md       # Documentation du projet
```

---

## ⚙️ Installation locale (macOS/Linux)

1. **Cloner le repo** ou créer un dossier :
   ```bash
   mkdir rag_local_project && cd rag_local_project
   ```

2. **Créer un environnement virtuel** :
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install streamlit PyPDF2 python-docx sentence-transformers faiss-cpu transformers torch evaluate sacrebleu rouge_score
   ```

4. **Lancer l’application** :
   ```bash
   streamlit run app.py
   ```

5. **Ouvrir dans le navigateur** :  
   [http://localhost:8501](http://localhost:8501)

---

## 🧪 Mode d'emploi

### 🔹 1. Ajout de documents
- Uploadez un ou plusieurs fichiers (`.pdf`, `.docx`, `.txt`)
- Le système extrait, découpe et indexe automatiquement leur contenu

### 🔹 2. Posez une question
- Entrez une requête naturelle dans la zone de recherche
- L'IA renvoie les segments pertinents

### 🔹 3. Résumé généré automatiquement
- L’outil synthétise les segments pour vous donner une vue concise

### 🔹 4. Évaluation (optionnelle)
- Collez un résumé de référence (manuel ou officiel)
- L’outil calcule les scores **BLEU** et **ROUGE**

---

## 🧑‍💻 Pour les hackathons / démonstrations

- ✅ 100 % exécutable en local (pas besoin de GPU ni d’API externe)
- 🧠 Qualité IA maintenue avec des modèles efficaces (MiniLM + T5-small)
- 💾 Index persistant entre sessions (via `faiss.index` et `meta.json`)
- ♻️ Réutilisable facilement : ajoutez vos propres documents, posez vos propres questions

---

## 💡 Prochaines améliorations possibles

- [ ] Ajout de l’upload de dossiers entiers
- [ ] Interface multilingue
- [ ] Extraction automatique de réponses précises en plus du résumé
- [ ] Intégration de modèles LLM plus puissants (TinyLLaMA, Mistral...)

---

## 📜 Licence

Ce projet est mis à disposition dans un cadre éducatif ou hackathon. Vous pouvez le modifier et le partager librement.
