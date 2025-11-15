#!/bin/bash

echo "=== BioReport Copilot - Setup and Test Script ==="
echo ""

# Check and install backend dependencies
echo "📦 Step 1: Installing backend dependencies..."
cd backend
if python3 -c "import fastapi" 2>/dev/null; then
    echo "✅ Backend dependencies already installed"
else
    echo "Installing backend dependencies..."
    pip3 install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "✅ Backend dependencies installed successfully"
    else
        echo "❌ Backend dependency installation failed"
        exit 1
    fi
fi
cd ..

# Check and install frontend dependencies
echo "📦 Step 2: Installing frontend dependencies..."
if [ -d "node_modules" ]; then
    echo "✅ Frontend dependencies already installed"
else
    echo "Installing frontend dependencies..."
    npm install
    if [ $? -eq 0 ]; then
        echo "✅ Frontend dependencies installed successfully"
    else
        echo "❌ Frontend dependency installation failed"
        exit 1
    fi
fi

# Test backend imports
echo "🧪 Step 3: Testing backend code..."
cd backend
python3 << EOF
try:
    from routers.research import router as research_router
    from routers.personal import router as personal_router
    from routers.report import router as report_router
    from services.deg_analyzer import parse_deg_file
    from services.ml_analyzer import perform_svm_classification
    print('✅ Backend code import test passed')
except Exception as e:
    print(f'❌ Backend code import failed: {e}')
    exit(1)
EOF

if [ $? -eq 0 ]; then
    echo "✅ Backend code check passed"
else
    echo "❌ Backend code check failed"
    exit 1
fi
cd ..

# Test frontend build
echo "🧪 Step 4: Testing frontend code..."
if command -v npm &> /dev/null; then
    echo "✅ Frontend build tools available"
else
    echo "⚠️  Cannot test frontend build (need to actually run npm run dev)"
fi

echo ""
echo "=== Setup and Test Complete ==="
echo ""
echo "🚀 Startup Instructions:"
echo ""
echo "Terminal 1 - Start Backend:"
echo "  cd backend"
echo "  uvicorn main:app --reload"
echo ""
echo "Terminal 2 - Start Frontend:"
echo "  npm run dev"
echo ""
echo "Then open browser to: http://localhost:5173"
