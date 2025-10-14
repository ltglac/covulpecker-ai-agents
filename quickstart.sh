#!/bin/bash

# CoVulPecker Quick Start Script
# This script helps you get started with CoVulPecker quickly

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                   CoVulPecker Setup                       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if dependencies are installed
if ! python -c "import crewai" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

# Check .env configuration
echo ""
echo "🔧 Checking configuration..."
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    exit 1
fi

# Check for API key
if grep -q "your_gemini_api_key_here" .env; then
    echo "⚠️  Warning: Please configure your API key in .env file"
    echo ""
    echo "Edit .env and add your API key:"
    echo "  GEMINI_API_KEY=your_actual_key_here"
    echo ""
    echo "Get your API key from: https://makersuite.google.com/app/apikey"
    exit 1
fi

echo "✅ Configuration looks good!"
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                 Ready to Run!                             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Try these commands:"
echo ""
echo "  1. Run demo analysis:"
echo "     python main.py --demo"
echo ""
echo "  2. Analyze sample file:"
echo "     python main.py --file data/vulnerable_sample.c"
echo ""
echo "  3. Analyze inline code:"
echo "     python main.py --code 'char buf[10]; gets(buf);'"
echo ""
echo "  4. See all options:"
echo "     python main.py --help"
echo ""
