#!/usr/bin/env bash
set -euo pipefail

# Create venv if not present
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Upgrade pip and install deps
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "If you plan to use gTTS playback, ensure ffmpeg is installed on your system."
echo "On Ubuntu/Debian: sudo apt-get install ffmpeg"
echo "On macOS (brew):  brew install ffmpeg"
echo "On Windows (choco): choco install ffmpeg"

# Run the app
python src/main.py
