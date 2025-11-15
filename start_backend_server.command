#!/bin/bash

# Get script directory
cd "$(dirname "$0")"

echo "========================================"
echo "  BioReport Copilot - Backend Server"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found, please install Python first"
    echo ""
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

# Check backend dependencies
cd backend
python3 -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing backend dependencies, please wait..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Backend dependency installation failed"
        cd ..
        echo ""
        echo "Press any key to exit..."
        read -n 1
        exit 1
    fi
fi

echo "Starting backend server..."
echo ""
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start backend server
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

