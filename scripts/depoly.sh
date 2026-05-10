#!/bin/bash
# ─────────────────────────────────────────────────────────
#  AI_IOS  –  Deployment Script
#  Usage:  bash scripts/deploy.sh [prod|dev]
# ─────────────────────────────────────────────────────────
set -e

ENV=${1:-dev}
echo "🚀 Deploying AI_IOS in [$ENV] mode..."

# 1. Install / update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet

# 2. Init DB
echo "🗄️  Initialising database..."
cd backend
python ../scripts/init_db.py
cd ..

# 3. Train ML models (only if .pkl files don't exist)
if [ ! -f "backend/app/ml/models/intent_classifier.pkl" ]; then
  echo "🧠 Training intent classifier..."
  cd backend
  python app/ml/train_intent.py
  python app/ml/train_sentiment.py
  python app/ml/recommend.py
  cd ..
fi

# 4. Start server
if [ "$ENV" = "prod" ]; then
  echo "🌐 Starting production server..."
  cd backend
  uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
else
  echo "🔧 Starting dev server with hot-reload..."
  cd backend
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
fi