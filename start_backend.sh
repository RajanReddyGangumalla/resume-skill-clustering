#!/bin/bash

echo "🚀 Starting Resume Clustering Backend..."

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this script from the backend directory."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if model file exists
if [ ! -f "../clustering_model.pkl" ]; then
    echo "⚠️  Warning: clustering_model.pkl not found. Please ensure the model file is in the project root."
    echo "   You may need to run save_model.py first."
fi

# Start the server
echo "🌟 Starting FastAPI server..."
echo "   API will be available at: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Press Ctrl+C to stop the server"
echo ""

python main.py
