@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo ========================================
echo   BioReport Copilot - One-Click Launch
echo ========================================
echo.

REM Check Node.js
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found, please install Node.js first
    echo Download: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

REM Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found, please install Python first
    echo.
    pause
    exit /b 1
)

echo [1/4] Checking dependencies...

REM Check frontend dependencies
if not exist "node_modules" (
    echo Installing frontend dependencies, please wait...
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Frontend dependency installation failed
        echo.
        pause
        exit /b 1
    )
)

REM Check backend dependencies
cd backend
python -c "import fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing backend dependencies, please wait...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Backend dependency installation failed
        cd ..
        echo.
        pause
        exit /b 1
    )
)
cd ..

echo [2/4] Starting backend server...
cd backend
start /b python -m uvicorn main:app --reload > ..\backend.log 2>&1
cd ..

echo [3/4] Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo [4/4] Starting frontend server...
start /b npm run dev > frontend.log 2>&1

echo.
echo ========================================
echo   Launch Complete!
echo ========================================
echo.
echo Frontend: http://localhost:5173
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Browser will open automatically...
timeout /t 2 /nobreak >nul

REM Open browser
start http://localhost:5173

echo.
echo ========================================
echo   Servers are running...
echo ========================================
echo.
echo ⚠️  Please keep this window open, closing will stop the servers
echo.
echo Press Ctrl+C to stop servers
echo.
pause

