#!/bin/bash

echo "========================================"
echo "  BioReport Copilot - One-Click Launch"
echo "========================================"
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js not found, please install Node.js first"
    echo "Download: https://nodejs.org/"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found, please install Python first"
    exit 1
fi

echo "[1/4] Checking dependencies..."

# Check frontend dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies, please wait..."
    npm install
    if [ $? -ne 0 ]; then
        echo "[ERROR] Frontend dependency installation failed"
        exit 1
    fi
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
        exit 1
    fi
fi
cd ..

echo "[2/4] Starting backend server..."
cd backend
python3 -m uvicorn main:app --reload > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo "[3/4] Waiting for backend to start..."
sleep 3

echo "[4/4] Starting frontend server..."
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "  Launch Complete!"
echo "========================================"
echo ""
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Browser will open automatically..."
sleep 2

# Try to open browser
if command -v open &> /dev/null; then
    # macOS
    open http://localhost:5173
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open http://localhost:5173
fi

echo ""
echo "Press Ctrl+C to stop servers"
echo ""

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait

