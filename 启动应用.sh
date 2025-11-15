#!/bin/bash

echo "========================================"
echo "  BioReport Copilot - 一键启动"
echo "========================================"
echo ""

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "[错误] 未找到 Node.js，请先安装 Node.js"
    echo "下载地址: https://nodejs.org/"
    exit 1
fi

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python3，请先安装 Python"
    exit 1
fi

echo "[1/4] 检查依赖..."

# 检查前端依赖
if [ ! -d "node_modules" ]; then
    echo "正在安装前端依赖，请稍候..."
    npm install
    if [ $? -ne 0 ]; then
        echo "[错误] 前端依赖安装失败"
        exit 1
    fi
fi

# 检查后端依赖
cd backend
python3 -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "正在安装后端依赖，请稍候..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[错误] 后端依赖安装失败"
        cd ..
        exit 1
    fi
fi
cd ..

echo "[2/4] 启动后端服务器..."
cd backend
python3 -m uvicorn main:app --reload > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo "[3/4] 等待后端启动..."
sleep 3

echo "[4/4] 启动前端服务器..."
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "  启动完成！"
echo "========================================"
echo ""
echo "前端地址: http://localhost:5173"
echo "后端API: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "后端进程ID: $BACKEND_PID"
echo "前端进程ID: $FRONTEND_PID"
echo ""
echo "浏览器将自动打开..."
sleep 2

# 尝试打开浏览器
if command -v open &> /dev/null; then
    # macOS
    open http://localhost:5173
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open http://localhost:5173
fi

echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait

