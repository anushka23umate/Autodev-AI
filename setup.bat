@echo off
setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════╗
echo ║   AutoDev-AI Setup Script (Windows)    ║
echo ╚════════════════════════════════════════╝
echo.

REM Check Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop.
    exit /b 1
)
echo ✓ Docker is installed

REM Check Docker Compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed.
    exit /b 1
)
echo ✓ Docker Compose is installed

REM Check Ollama
echo.
echo Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama is not running at localhost:11434
    echo    Please start Ollama with: ollama serve
    echo    Then run this script again.
    exit /b 1
)
echo ✓ Ollama is running

REM Create environment file
echo.
echo Setting up environment...
if not exist "backend\.env" (
    copy backend\.env.example backend\.env
    echo ✓ Created backend\.env
) else (
    echo ✓ backend\.env already exists
)

REM Create projects directory
if not exist "generated_projects" mkdir generated_projects
echo ✓ Created generated_projects directory

REM Build and start services
echo.
echo Building and starting services...
docker-compose up --build -d

echo.
echo ╔════════════════════════════════════════╗
echo ║   Setup Complete!                      ║
echo ╚════════════════════════════════════════╝
echo.
echo Services are starting...
echo.
echo Access the application at:
echo   🌐 Frontend:    http://localhost:3000
echo   🔧 Backend API: http://localhost:8000
echo   📚 API Docs:    http://localhost:8000/docs
echo.
echo To view logs:        docker-compose logs -f
echo To stop services:    docker-compose down
echo To restart:          docker-compose restart
echo.
echo Happy coding! 🚀
