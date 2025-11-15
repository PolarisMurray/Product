# Research Mode UI/UX - 安装与运行指南

## 🚀 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

应用将在 `http://localhost:5173` 启动

### 3. 构建生产版本

```bash
npm run build
```

## 📁 项目结构

```
src/
├── components/          # UI 组件
│   ├── FileUploadArea.jsx      # 文件上传区（Phase 2）
│   ├── ActionButtons.jsx       # 操作按钮（Phase 3）
│   ├── ResultView.jsx          # 结果展示区（Phase 4）
│   ├── ExportButtons.jsx       # 导出按钮（Phase 5）
│   └── LoadingSkeleton.jsx     # 加载骨架屏
├── pages/
│   └── ResearchMode.jsx        # 科研模式主页面
├── App.jsx
├── main.jsx
└── index.css
```

## ✨ 已实现的功能

### Phase 1 - 页面框架 ✅
- ✅ 科研模式主页面布局
- ✅ 页头标题 "Research Mode"
- ✅ 主内容区域（上传区 + 结果展示区）
- ✅ 空状态提示

### Phase 2 - 文件上传区 ✅
- ✅ Drag & Drop 文件框
- ✅ 文件类型验证（CSV / TSV / XLSX）
- ✅ 上传文件列表显示
- ✅ 文件信息（文件名、类型、大小）
- ✅ 删除按钮
- ✅ 上传状态反馈（成功/错误）

### Phase 3 - 操作按钮区 ✅
- ✅ 生成报告按钮
- ✅ 按钮状态管理（禁用/激活/加载中）
- ✅ Loading spinner 动画

### Phase 4 - 结果展示区 ✅
- ✅ 图表展示卡片（2列网格布局）
- ✅ 图表占位符
- ✅ 下载按钮
- ✅ Results 文本区（可编辑）
- ✅ Discussion 文本区（可编辑）
- ✅ 复制按钮功能

### Phase 5 - 报告导出 UI ✅
- ✅ PDF 导出按钮
- ✅ DOCX 导出按钮
- ✅ 导出状态管理（加载中/完成）

### Phase 6 - UI 打磨 ✅
- ✅ 统一色彩系统（research-blue 蓝色系）
- ✅ 卡片圆角与阴影
- ✅ 文本字体层级
- ✅ Loading 效果（骨架屏）
- ✅ 响应式布局（移动端 + 桌面端）

## 🎨 设计特点

- **色彩系统**: 使用 research-blue 蓝色系，体现科研风格
- **交互反馈**: 所有按钮都有 hover 和 active 状态
- **加载状态**: 使用骨架屏（Skeleton）提供流畅的加载体验
- **响应式**: 支持移动端、平板和桌面端
- **可访问性**: 使用语义化 HTML 和 ARIA 标签

## 🔌 API 集成准备

当前为纯前端实现，使用模拟数据。要连接后端 API，需要：

1. 在 `ResearchMode.jsx` 的 `handleGenerateReport` 中替换模拟 API 调用
2. 在 `ExportButtons.jsx` 的 `handleExport` 中连接真实的导出 API
3. 在 `FileUploadArea.jsx` 中添加实际上传逻辑（如需要）

## 📝 下一步

- [ ] 连接后端 API
- [ ] 实现真实的图表渲染（Plotly/Chart.js）
- [ ] 添加错误处理和 Toast 提示
- [ ] 实现文件预览功能
- [ ] 添加暗色模式支持


