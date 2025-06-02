#!/bin/bash

echo "🔧 Updating pip..."
pip install --upgrade pip --no-cache-dir

echo "📦 Installing all requirements..."
pip install -r requirements.txt --no-cache-dir

echo "🔁 Reinstalling vonage explicitly to force dependency..."
pip install vonage==2.6.0 --no-cache-dir

echo "✅ Build script completed successfully."
