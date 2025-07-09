#!/usr/bin/env bash

echo "🧹 Uninstalling old OpenAI..."
pip uninstall -y openai

echo "📦 Installing OpenAI 1.26.0..."
pip install openai==1.26.0

echo "📦 Installing everything else from requirements.txt..."
pip install -r requirements.txt

