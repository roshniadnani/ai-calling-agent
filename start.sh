#!/bin/bash

echo "🔧 Updating pip..."
pip install --upgrade pip

echo "📦 Installing dependencies..."
pip install -r requirements.txt
