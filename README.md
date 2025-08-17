AI-powered Wordlist Generator with GUI, LLM support (local/API), and Kaonashi integration for smarter password lists.

<img width="751" height="691" alt="Screenshot from 2025-08-17 21-18-53" src="https://github.com/user-attachments/assets/ac0f48e0-0425-4559-b8a6-642f6c6197cc" />

---

📖 README.md

# OWL – AI Wordlist Generator

**OWL (AI Wordlist Generator)** est un outil avec interface graphique (Tkinter) permettant de créer des listes de mots de passe personnalisées en combinant l’intelligence artificielle (LLMs comme LLaMA via Ollama ou API) et la base de données Kaonashi.  
Il offre un moyen simple et rapide de générer des wordlists uniques adaptées à vos besoins (tests de sécurité éthiques, pentesting autorisé, recherche).

⚠️ **Note légale** : Cet outil est destiné uniquement à un usage éducatif et professionnel (tests de pénétration autorisés). N’utilisez jamais cet outil de manière illégale.

---

## ✨ Fonctionnalités
- Interface graphique (Tkinter).
- Génération de wordlists via :
  - **LLM local** (Ollama).
  - **API externe** (par défaut : `http://localhost:11434/api/generate`).
- Intégration **Kaonashi** (clonage / mise à jour automatique des ressources).
- Support de **masques statiques** (`{word}123`, `123{word}`, etc.).
- Possibilité d’ajouter :
  - des données personnelles/structurées,
  - une base de wordlist existante.
- Export vers fichier `.txt` avec suppression des doublons.

---

## 🛠 Installation

### 1. Cloner le repo

```bash
git clone https://github.com/4lp1ne/OWL.git
cd OWL

2. Lancer le script de setup

chmod +x setup.sh
./setup.sh
```

Ce script :

Vérifie python3, pip, git, et tkinter.

Crée un environnement virtuel (optionnel).

Installe les dépendances (requests).

Clone/Met à jour le repo Kaonashi.



---

🚀 Utilisation

Mode GUI

```bash
python3 llmwl.py
```

Options principales

Prompt : contexte ou type de mots à générer.

Optional Data : infos supplémentaires séparées par des virgules.

Base Wordlist : fichier .txt existant à enrichir.

Masks : sélection de patterns à appliquer.

Iterations : nombre de lots générés.

Model : modèle LLM à utiliser (par défaut llama3).

API Mode : permet d’utiliser une API externe à la place d’Ollama.



---

📂 Structure

OWL/
│── llmwl.py        # Application principale (GUI + logique)
│── setup.sh        # Script d'installation et de configuration
│── requirements.txt # Dépendances Python
│── Kaonashi/       # Repo cloné automatiquement


---

🧑‍💻 Exemple

1. Entrer un prompt :
"Generate password candidates based on sports and music"


2. Ajouter des données perso :
"John, 1990, guitar, football"


3. Sélectionner quelques masks :
{word}123, {word}!


4. Choisir un fichier de sortie output.txt.


5. Lancer → la wordlist finale est générée.




---

⚖️ Disclaimer

L’auteur décline toute responsabilité en cas d’usage abusif.
N’utilisez cet outil que pour des tests éthiques avec autorisation légale explicite.


