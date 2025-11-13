@echo off
REM TrustNet 2.0 - Quick Start Script for Windows
REM This script starts all required services

echo.
echo ================================================================================
echo   TrustNet 2.0 - Real-Time Production System
echo ================================================================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed or not in PATH
    echo Please install Docker Desktop: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [1/5] Checking environment variables...
if not exist .env (
    echo [WARNING] .env file not found!
    echo Creating .env from template...
    copy .env.example .env
    echo.
    echo [ACTION REQUIRED] Please edit .env file and add your API keys:
    echo   - OPENAI_API_KEY
    echo   - GOOGLE_FACTCHECK_API_KEY
    echo   - TWITTER_API_KEY (optional for real-time streaming)
    echo.
    notepad .env
    echo.
    echo Press any key after you've added your API keys...
    pause
)

echo [2/5] Starting infrastructure services (Docker)...
docker-compose up -d
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start Docker services
    pause
    exit /b 1
)

echo [3/5] Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo [4/5] Checking service health...
docker-compose ps

echo [5/5] Services are ready!
echo.
echo ================================================================================
echo   Infrastructure Status:
echo ================================================================================
docker-compose ps
echo.
echo ================================================================================
echo   Next Steps:
echo ================================================================================
echo.
echo   1. Start Backend (in this terminal):
echo      python main.py
echo.
echo   2. Start Dashboard (in new terminal):
echo      cd dashboard
echo      npm install
echo      npm run dev
echo.
echo   3. Open Dashboard:
echo      http://localhost:3000
echo.
echo ================================================================================
echo.
echo Press any key to start the backend system...
pause

echo.
echo Starting TrustNet 2.0 backend...
python main.py
