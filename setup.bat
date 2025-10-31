@echo off
REM Database Security CTF - Setup Script for Windows
REM This script initializes the CTF environment

echo ============================================================
echo Database Security CTF - Setup Script
echo ============================================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

echo [+] Docker is running
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.7+
    pause
    exit /b 1
)

echo [+] Python is installed
echo.

REM Generate flags and environment variables
echo [+] Generating flags and environment variables...
cd flag-generator
python .\generate_flags.py
cd ..

if not exist ".env" (
    echo [ERROR] Failed to generate .env file
    pause
    exit /b 1
)

echo [+] Flags generated successfully
echo.

REM Build and start Docker containers
echo [+] Building Docker containers (this may take a few minutes)...
docker-compose build

echo.
echo [+] Starting containers...
docker-compose up -d

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Services are now running:
echo   - CTF Platform:       http://localhost:5000
echo   - Vulnerable Web App: http://localhost:8080
echo   - MySQL Database:     localhost:3306
echo.
echo To view logs:       docker-compose logs -f
echo To stop services:   docker-compose down
echo To restart:         docker-compose restart
echo.
echo IMPORTANT: Check the .env file for database credentials
echo.
pause
