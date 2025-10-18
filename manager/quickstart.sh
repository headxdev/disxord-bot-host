#!/bin/bash
# Discord Bot Manager - Quick Start Script
# Created by headx & the psychon
# For Linux and macOS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Discord Bot Manager - Quick Start      ║${NC}"
echo -e "${BLUE}║  Created by headx & the psychon         ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
echo ""

# Check Python version
echo -e "${BLUE}[1/5]${NC} Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
    PYTHON_CMD="python"
else
    echo -e "${RED}✗${NC} Python not found!"
    echo -e "${YELLOW}Please install Python 3.8 or higher from https://www.python.org${NC}"
    exit 1
fi

# Check if virtual environment exists
echo ""
echo -e "${BLUE}[2/5]${NC} Setting up virtual environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo -e "${BLUE}[3/5]${NC} Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓${NC} Virtual environment activated"

# Install/Update dependencies
echo ""
echo -e "${BLUE}[4/5]${NC} Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
    echo -e "${GREEN}✓${NC} Dependencies installed"
else
    echo -e "${YELLOW}⚠${NC} requirements.txt not found, installing basic dependencies..."
    pip install discord.py python-dotenv aiohttp PyNaCl
    echo -e "${GREEN}✓${NC} Basic dependencies installed"
fi

# Create necessary directories
echo ""
echo -e "${BLUE}[5/5]${NC} Setting up directory structure..."
mkdir -p bots logs cmdtamplates data
echo -e "${GREEN}✓${NC} Directories created"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo -e "${YELLOW}Creating .env configuration file...${NC}"
    cat > .env << EOL
# Discord Bot Manager Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False
LOG_LEVEL=INFO
DEFAULT_PREFIX=!
EOL
    echo -e "${GREEN}✓${NC} Configuration file created"
fi

# Start the server
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Setup Complete! Starting server...     ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Starting Discord Bot Manager...${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Run the server
$PYTHON_CMD start.py
