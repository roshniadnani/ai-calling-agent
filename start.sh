#!/bin/bash

echo "🔧 Ensuring pip is updated..."
pip install --upgrade pip

echo "📦 Installing all dependencies..."
pip install -r requirements.txt

echo "✅ Verifying vonage installation..."
pip install vonage==2.6.0

echo "🚀 Starting server..."
uvicorn main:app --host=0.0.0.0 --port=8000
