#!/bin/bash

echo "Installing packages manually..."
pip install --upgrade pip
pip install uvicorn
pip install vonage==2.6.0
pip install -r requirements.txt
