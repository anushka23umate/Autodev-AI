#!/bin/bash

set -e

echo "╔════════════════════════════════════════╗"
echo "║   AutoDev-AI Setup Script              ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi
echo "✓ Docker is installed"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi
echo "✓ Docker Compose is installed"

# Check Ollama
echo ""
echo "Checking Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✓ Ollama is running"
else
    echo "⚠️  Ollama is not running at localhost:11434"
    echo "   Please start Ollama with: ollama serve"
    echo "   Then run this script again."
    exit 1
fi

# Check if models are available
echo ""
echo "Checking AI models..."
if curl -s http://localhost:11434/api/tags | grep -q "deepseek-coder\|codellama\|mistral"; then
    echo "✓ At least one AI model is available"
else
    echo "⚠️  No suitable AI models found. Pulling deepseek-coder..."
    ollama pull deepseek-coder
fi

# Create environment file
echo ""
echo "Setting up environment..."
if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    echo "✓ Created backend/.env"
else
    echo "✓ backend/.env already exists"
fi

# Create projects directory
mkdir -p generated_projects
echo "✓ Created generated_projects directory"

# Build and start services
echo ""
echo "Building and starting services..."
docker-compose up --build -d

echo ""
echo "╔════════════════════════════════════════╗"
echo "║   Setup Complete!                      ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "Services are starting..."
echo ""
echo "Access the application at:"
echo "  🌐 Frontend:    http://localhost:3000"
echo "  🔧 Backend API: http://localhost:8000"
echo "  📚 API Docs:    http://localhost:8000/docs"
echo ""
echo "To stop services:    docker-compose down"
echo "To view logs:        docker-compose logs -f"
echo "To restart:          docker-compose restart"
echo ""
echo "Happy coding! 🚀"
