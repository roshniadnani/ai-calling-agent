#!/bin/bash

echo "🔧 Installing dependencies..."
pip install --upgrade pip
pip install vonage==2.6.0
pip install uvicorn
pip install -r requirements.txt
