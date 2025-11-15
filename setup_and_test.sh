#!/bin/bash

echo "=== BioReport Copilot - 安装和测试脚本 ==="
echo ""

# 检查并安装后端依赖
echo "📦 步骤1: 安装后端依赖..."
cd backend
if python3 -c "import fastapi" 2>/dev/null; then
    echo "✅ 后端依赖已安装"
else
    echo "正在安装后端依赖..."
    pip3 install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "✅ 后端依赖安装成功"
    else
        echo "❌ 后端依赖安装失败"
        exit 1
    fi
fi
cd ..

echo ""

# 检查并安装前端依赖
echo "📦 步骤2: 安装前端依赖..."
if [ -d "node_modules" ]; then
    echo "✅ 前端依赖已安装"
else
    echo "正在安装前端依赖..."
    npm install
    if [ $? -eq 0 ]; then
        echo "✅ 前端依赖安装成功"
    else
        echo "❌ 前端依赖安装失败"
        exit 1
    fi
fi

echo ""

# 测试后端导入
echo "🧪 步骤3: 测试后端代码..."
cd backend
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from routers.research import router
    from routers.personal import router as personal_router
    from routers.report import router as report_router
    from models.schemas import ResearchAnalyzeResponse
    print('✅ 后端代码导入测试通过')
except Exception as e:
    print(f'❌ 后端代码导入失败: {e}')
    sys.exit(1)
"
BACKEND_TEST=$?
cd ..

if [ $BACKEND_TEST -eq 0 ]; then
    echo "✅ 后端代码检查通过"
else
    echo "❌ 后端代码检查失败"
fi

echo ""

# 测试前端构建
echo "🧪 步骤4: 测试前端代码..."
if npm run build --dry-run 2>/dev/null || npx vite build --help >/dev/null 2>&1; then
    echo "✅ 前端构建工具可用"
else
    echo "⚠️  无法测试前端构建（需要实际运行npm run dev）"
fi

echo ""
echo "=== 安装和测试完成 ==="
echo ""
echo "🚀 启动说明:"
echo ""
echo "终端1 - 启动后端:"
echo "  cd backend"
echo "  uvicorn main:app --reload"
echo ""
echo "终端2 - 启动前端:"
echo "  npm run dev"
echo ""
echo "然后打开浏览器访问: http://localhost:5173"

