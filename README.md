# 🧪 AI-Powered Document Search & Summarization System

Ce projet a été réalisé dans le cadre d’un **hackathon IA Générative**. Il s'agit d'une application Streamlit permettant de :

- 📥 Uploader des documents (PDF, DOCX, TXT)
- 🔎 Rechercher dans leur contenu via des embeddings sémantiques
- 📝 Générer un résumé multilingue avec T5
- 📊 Évaluer la qualité du résumé via BLEU & ROUGE
- 🌐 Partager l’interface en ligne via Cloudflare Tunnel

---

## ⚙️ Installation et Lancement

Tout est automatisé dans le fichier Colab :

1. Installation des dépendances (transformers, faiss, PyPDF2…)
2. Téléchargement de l’exécutable cloudflared
3. Génération automatique du script `app.py`
4. Lancement de Streamlit + ouverture d’un tunnel Cloudflare

À la fin, une URL publique est affichée pour accéder à l'app.

---

## 🧠 Fonctionnalités

### 🔍 Recherche Sémantique
- Index FAISS
- Encodage avec `all-MiniLM-L6-v2`
- Résultats sans doublons

### 📝 Résumé Automatique
- Modèle T5 (`t5-small`)
- Langue détectée automatiquement
- Résumé fluide, structuré et court

### 📊 Évaluation BLEU / ROUGE
- Tokenisation avec spaCy
- Scores calculés avec Hugging Face `evaluate`
- Résultats visuellement présentés

---

## 📂 Fichiers supportés

- `.pdf` via PyPDF2
- `.docx` via python-docx
- `.txt` brut

---

## 🧰 Stack technique

| Outil / Librairie        | Rôle                                     |
|--------------------------|------------------------------------------|
| Streamlit                | Interface web                            |
| FAISS                    | Recherche vectorielle                    |
| SentenceTransformers     | Embeddings (MiniLM)                      |
| Transformers (T5)        | Génération de résumé                     |
| Evaluate (HF)            | Scores BLEU et ROUGE                     |
| spaCy                    | Tokenisation pour l’évaluation           |
| Cloudflared              | Tunnel sécurisé via internet             |

---

## 🏁 Exécution dans Google Colab

> 📌 Recommandé : exécuter dans Colab avec CPU (pas besoin de GPU).

Lancez les cellules une par une. L’URL d’accès s’affichera automatiquement.

---

## 👤 Auteur

Développé par [TON NOM] — Hackathon AI Gen 2025

---

## 📌 À venir (idées d’amélioration)

- Authentification utilisateur
- Résumé par chapitre
- Visualisation des documents PDF