#!/bin/bash

echo "🔧 Updating pip..."
pip install --upgrade pip

echo "📦 Installing all dependencies..."
pip install -r requirements.txt

echo "📦 Manually installing vonage in case Render skips it..."
pip install vonage==2.6.0

echo "✅ Build complete!"
