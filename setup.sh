#!/bin/bash

echo "===> Starting AI Wordlist Generator Setup..."

# Exit immediately if any command fails
set -e

# --- Config ---
VENV_DIR="venv"
USE_VENV=true  # Set to false if you don’t want a virtual environment
KAONASHI_REPO="https://github.com/kaonashi-passwords/Kaonashi"
KAONASHI_DIR="Kaonashi"

# --- Functions ---
install_requirements() {
    echo "===> Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
}

check_command() {
    if ! command -v "$1" &>/dev/null; then
        echo "❌ $1 is not installed."
        return 1
    else
        echo "✅ $1 is installed."
        return 0
    fi
}

install_git() {
    echo "===> Installing Git..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update && sudo apt install -y git
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install git
    else
        echo "⚠️ Please install Git manually for your OS."
    fi
}

install_tkinter() {
    echo "===> Installing tkinter..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update && sudo apt install -y python3-tk
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS usually includes tkinter. If not, install with Homebrew Python."
    else
        echo "⚠️ Please install tkinter manually for your OS."
    fi
}

clone_kaonashi() {
    if [ -d "$KAONASHI_DIR" ]; then
        echo "===> Kaonashi repo already exists. Updating..."
        git -C "$KAONASHI_DIR" pull
    else
        echo "===> Cloning Kaonashi repo..."
        git clone "$KAONASHI_REPO" "$KAONASHI_DIR"
    fi
}

# --- Check Environment ---
check_command git || install_git
check_command python3 || (echo "❌ Python3 is required. Please install it." && exit 1)
check_command pip || (echo "❌ pip is required. Please install it." && exit 1)

# --- Tkinter Check (best-effort) ---
python3 -c "import tkinter" 2>/dev/null || install_tkinter

# --- Virtual Env Setup (Optional) ---
if $USE_VENV; then
    if [ ! -d "$VENV_DIR" ]; then
        echo "===> Creating virtual environment in $VENV_DIR"
        python3 -m venv "$VENV_DIR"
    fi
    echo "===> Activating virtual environment"
    source "$VENV_DIR/bin/activate"
fi

# --- Requirements File ---
if [ ! -f requirements.txt ]; then
    echo "Creating requirements.txt..."
    echo "requests" > requirements.txt
fi

install_requirements
clone_kaonashi

echo "✅ Setup complete!"
echo "You can now run your app with: python3 vllwl.py"
