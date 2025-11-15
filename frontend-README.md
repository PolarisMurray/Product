# Research Mode UI/UX - Installation and Running Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

Application will start at `http://localhost:5173`

### 3. Build Production Version

```bash
npm run build
```

## 📁 Project Structure

```
src/
├── components/          # UI Components
│   ├── FileUploadArea.jsx      # File upload area (Phase 2)
│   ├── ActionButtons.jsx       # Action buttons (Phase 3)
│   ├── ResultView.jsx          # Result display area (Phase 4)
│   ├── ExportButtons.jsx       # Export buttons (Phase 5)
│   └── LoadingSkeleton.jsx     # Loading skeleton screen
│
└── pages/
    └── ResearchMode.jsx        # Research mode main page
```

## ✨ Implemented Features

### Phase 1 - Page Framework ✅
- ✅ Research mode main page layout
- ✅ Page header title "Research Mode"
- ✅ Main content area (upload area + result display area)
- ✅ Empty state prompt

### Phase 2 - File Upload Area ✅
- ✅ Drag & Drop file box
- ✅ File type validation (CSV / TSV / XLSX)
- ✅ Uploaded file list display
- ✅ File information (filename, type, size)
- ✅ Delete button
- ✅ Upload status feedback (success/error)

### Phase 3 - Action Buttons Area ✅
- ✅ Generate report button
- ✅ Button state management (disabled/active/loading)
- ✅ Loading spinner animation

### Phase 4 - Result Display Area ✅
- ✅ Chart display cards (2-column grid layout)
- ✅ Chart placeholder
- ✅ Download button
- ✅ Results text area (editable)
- ✅ Discussion text area (editable)
- ✅ Copy button functionality

### Phase 5 - Report Export UI ✅
- ✅ PDF export button
- ✅ DOCX export button
- ✅ Export state management (loading/complete)

### Phase 6 - UI Polish ✅
- ✅ Unified color system (research-blue blue theme)
- ✅ Card rounded corners and shadows
- ✅ Text font hierarchy
- ✅ Loading effects (skeleton screen)
- ✅ Responsive layout (mobile + desktop)

## 🎨 Design Features

- **Color System**: Uses research-blue blue theme, reflecting scientific style
- **Interaction Feedback**: All buttons have hover and active states
- **Loading States**: Uses skeleton screen (Skeleton) for smooth loading experience
- **Responsive**: Supports mobile, tablet, and desktop
- **Accessibility**: Uses semantic HTML and ARIA labels

## 🔌 API Integration Preparation

Currently pure frontend implementation using mock data. To connect to backend API, need to:

1. Replace mock API call in `ResearchMode.jsx`'s `handleGenerateReport`
2. Connect to real export API in `ExportButtons.jsx`'s `handleExport`
3. Add actual upload logic in `FileUploadArea.jsx` (if needed)

## 📝 Next Steps

- [ ] Connect to backend API
- [ ] Implement real chart rendering (Plotly/Chart.js)
- [ ] Add error handling and Toast notifications
- [ ] Implement file preview functionality
- [ ] Add dark mode support
