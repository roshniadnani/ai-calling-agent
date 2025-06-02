#!/bin/bash

echo "🔧 Updating pip..."
pip install --upgrade pip

echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "🔁 Installing vonage manually to fix Render issue..."
pip install vonage==2.6.0

echo "🚀 Build complete!"
