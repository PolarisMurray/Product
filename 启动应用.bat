@echo off
chcp 65001 >nul
echo ========================================
echo   BioReport Copilot - 一键启动
echo ========================================
echo.

REM 检查Node.js
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Node.js，请先安装 Node.js
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)

REM 检查Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    where python3 >nul 2>&1
    if %errorlevel% neq 0 (
        echo [错误] 未找到 Python，请先安装 Python
        pause
        exit /b 1
    )
    set PYTHON_CMD=python3
) else (
    set PYTHON_CMD=python
)

echo [1/4] 检查依赖...
if not exist "node_modules" (
    echo 正在安装前端依赖，请稍候...
    call npm install
    if %errorlevel% neq 0 (
        echo [错误] 前端依赖安装失败
        pause
        exit /b 1
    )
)

cd backend
%PYTHON_CMD% -c "import fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装后端依赖，请稍候...
    %PYTHON_CMD% -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [错误] 后端依赖安装失败
        cd ..
        pause
        exit /b 1
    )
)
cd ..

echo [2/4] 启动后端服务器...
start "BioReport后端" cmd /k "cd backend && %PYTHON_CMD% -m uvicorn main:app --reload"

echo [3/4] 等待后端启动...
timeout /t 3 /nobreak >nul

echo [4/4] 启动前端服务器...
start "BioReport前端" cmd /k "npm run dev"

echo.
echo ========================================
echo   启动完成！
echo ========================================
echo.
echo 前端地址: http://localhost:5173
echo 后端API: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo.
echo 浏览器将自动打开...
echo.
timeout /t 2 /nobreak >nul
start http://localhost:5173

echo 按任意键关闭此窗口（服务器将继续运行）
pause >nul

