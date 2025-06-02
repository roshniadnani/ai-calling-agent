#!/bin/bash

echo "🔧 Updating pip..."
pip install --upgrade pip

echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "🔁 Ensuring vonage is installed..."
pip install vonage==2.6.0

echo "✅ All dependencies installed. Build complete!"
