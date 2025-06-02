#!/bin/bash

echo "🔧 Updating pip..."
pip install --upgrade pip

echo "📦 Installing dependencies from requirements.txt inside venv..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "📦 Installing vonage manually again (safe fallback)..."
python -m pip install vonage==2.6.3

echo "✅ Build complete."
