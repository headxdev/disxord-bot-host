@echo off
REM Discord Bot Manager - Quick Start Script
REM Created by headx & the psychon
REM For Windows

setlocal enabledelayedexpansion

title Discord Bot Manager - Quick Start

echo ========================================
echo   Discord Bot Manager - Quick Start
echo   Created by headx ^& the psychon
echo ========================================
echo.

REM Check Python installation
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python not found!
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [+] Python %PYTHON_VERSION% found
echo.

REM Check if virtual environment exists
echo [2/5] Setting up virtual environment...
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [X] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [+] Virtual environment created
) else (
    echo [+] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [X] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [+] Virtual environment activated
echo.

REM Install/Update dependencies
echo [4/5] Installing dependencies...
if exist "requirements.txt" (
    python -m pip install --upgrade pip --quiet
    python -m pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo [!] Some dependencies failed to install
        echo Trying again with verbose output...
        python -m pip install -r requirements.txt
    ) else (
        echo [+] Dependencies installed
    )
) else (
    echo [!] requirements.txt not found, installing basic dependencies...
    python -m pip install discord.py python-dotenv aiohttp PyNaCl --quiet
    echo [+] Basic dependencies installed
)
echo.

REM Create necessary directories
echo [5/5] Setting up directory structure...
if not exist "bots\" mkdir bots
if not exist "logs\" mkdir logs
if not exist "cmdtamplates\" mkdir cmdtamplates
if not exist "data\" mkdir data
echo [+] Directories created
echo.

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env configuration file...
    (
        echo # Discord Bot Manager Configuration
        echo HOST=0.0.0.0
        echo PORT=8000
        echo DEBUG=False
        echo LOG_LEVEL=INFO
        echo DEFAULT_PREFIX=!
    ) > .env
    echo [+] Configuration file created
    echo.
)

REM Start the server
echo ========================================
echo   Setup Complete! Starting server...
echo ========================================
echo.
echo Starting Discord Bot Manager...
echo Press Ctrl+C to stop the server
echo.

REM Run the server
python start.py

REM Keep window open on error
if errorlevel 1 (
    echo.
    echo [X] Server stopped with an error
    pause
)
