#!/bin/bash

# VeriTrueAI2.0 Backend Deployment Script

echo "🚀 VeriTrueAI2.0 Backend Deployment Script"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this script from the project root."
    exit 1
fi

# Create uploads directory if it doesn't exist
echo "📁 Creating uploads directory..."
mkdir -p uploads

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -v

if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Please fix issues before deploying."
    exit 1
fi

echo "✅ Tests passed!"

# Check deployment type
if [ "$1" = "local" ]; then
    echo "🏠 Starting local development server..."
    python main.py
elif [ "$1" = "docker" ]; then
    echo "🐳 Building and running Docker container..."
    docker build -t veritrue-ai-backend .
    docker run -p 8000:8000 --env-file .env veritrue-ai-backend
elif [ "$1" = "gcloud" ]; then
    echo "☁️ Deploying to Google Cloud..."
    gcloud app deploy app.yaml --quiet
    gcloud app browse
else
    echo "📖 Usage: $0 [local|docker|gcloud]"
    echo ""
    echo "Options:"
    echo "  local   - Start local development server"
    echo "  docker  - Build and run Docker container"
    echo "  gcloud  - Deploy to Google Cloud App Engine"
    echo ""
    echo "Example: $0 local"
fi