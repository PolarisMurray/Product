#!/bin/bash

echo "=== BioReport Copilot Debug Check ==="
echo ""

# Check Python
echo "1. Checking Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python not found!"
    exit 1
fi
echo "✅ Python found"
echo ""

# Check Node.js
echo "2. Checking Node.js..."
node --version
if [ $? -ne 0 ]; then
    echo "❌ Node.js not found!"
    exit 1
fi
echo "✅ Node.js found"
echo ""

# Check npm
echo "3. Checking npm..."
npm --version
if [ $? -ne 0 ]; then
    echo "❌ npm not found!"
    exit 1
fi
echo "✅ npm found"
echo ""

# Check backend dependencies
echo "4. Checking backend dependencies..."
cd backend
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Check if fastapi is installed
python3 -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  FastAPI not installed. Run: pip install -r requirements.txt"
else
    echo "✅ FastAPI installed"
fi
cd ..
echo ""

# Check frontend dependencies
echo "5. Checking frontend dependencies..."
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found!"
    exit 1
fi

if [ ! -d "node_modules" ]; then
    echo "⚠️  node_modules not found. Run: npm install"
else
    echo "✅ node_modules exists"
fi
echo ""

# Check backend code syntax
echo "6. Checking backend code syntax..."
cd backend
python3 -m py_compile main.py 2>&1
if [ $? -eq 0 ]; then
    echo "✅ main.py syntax OK"
else
    echo "❌ main.py has syntax errors"
fi

python3 -m py_compile routers/research.py 2>&1
if [ $? -eq 0 ]; then
    echo "✅ routers/research.py syntax OK"
else
    echo "❌ routers/research.py has syntax errors"
fi

python3 -m py_compile routers/personal.py 2>&1
if [ $? -eq 0 ]; then
    echo "✅ routers/personal.py syntax OK"
else
    echo "❌ routers/personal.py has syntax errors"
fi

python3 -m py_compile routers/report.py 2>&1
if [ $? -eq 0 ]; then
    echo "✅ routers/report.py syntax OK"
else
    echo "❌ routers/report.py has syntax errors"
fi
cd ..
echo ""

# Check frontend files exist
echo "7. Checking frontend files..."
if [ -f "src/App.jsx" ]; then
    echo "✅ src/App.jsx exists"
else
    echo "❌ src/App.jsx not found"
fi

if [ -f "src/main.jsx" ]; then
    echo "✅ src/main.jsx exists"
else
    echo "❌ src/main.jsx not found"
fi

if [ -f "vite.config.js" ]; then
    echo "✅ vite.config.js exists"
else
    echo "❌ vite.config.js not found"
fi
echo ""

echo "=== Debug Check Complete ==="
echo ""
echo "To start the backend:"
echo "  cd backend"
echo "  pip install -r requirements.txt  # if not installed"
echo "  uvicorn main:app --reload"
echo ""
echo "To start the frontend:"
echo "  npm install  # if not installed"
echo "  npm run dev"

