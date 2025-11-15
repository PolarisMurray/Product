# 📁 File Paths Guide

This document explains the file save paths for all files in the BioReport Copilot system.

---

## 📂 Directory Structure

```
Product/
├── backend/
│   ├── example_data/          # Example data files
│   │   ├── example_deg.csv
│   │   └── example_enrichment.csv
│   ├── report_templates/      # Report templates (future use)
│   ├── static/                # Static files directory (needs to be created)
│   │   └── reports/           # Generated report files
│   └── ...
└── ...
```

---

## 📊 Data File Paths

### 1. Example Data Files

**Location**: `backend/example_data/`

**Files**:
- `example_deg.csv` - DEG file example
- `example_enrichment.csv` - Enrichment analysis file example

**Purpose**: For testing and demonstration

**Access Method**: Use file path directly

---

### 2. Uploaded Data Files

**Current Implementation**: 
- ⚠️ **Uploaded files are NOT saved to disk**
- File content is read into memory for processing
- Memory is released after processing

**Reason**: 
- Protect user data privacy
- Reduce disk usage
- Temporary processing, no need for persistence

**Future Improvement** (optional):
- If file saving is needed, can save to:
  ```
  backend/uploads/
  ├── {user_id}/
  │   ├── {timestamp}_deg_file.csv
  │   └── {timestamp}_enrichment_file.csv
  ```

---

## 📄 Generated Report Paths

### Report Save Location

**Path**: `backend/static/reports/`

**File Naming Format**:
- Research Mode: `research-{timestamp}.pdf` or `research-{timestamp}.docx`
- Personal Mode: `personal-{timestamp}.pdf` or `personal-{timestamp}.docx`

**Examples**:
```
backend/static/reports/
├── research-1704067200.pdf
├── research-1704067300.docx
├── personal-1704067400.pdf
└── personal-1704067500.docx
```

**Access URL**: 
- Local: `http://localhost:8000/static/reports/{filename}`
- Production: `https://yourdomain.com/static/reports/{filename}`

**Note**: 
- ⚠️ Current report generation is placeholder implementation
- Actual file generation functionality pending
- Currently only returns placeholder URL

---

## 🔧 Configure Static File Service

### FastAPI Static File Configuration

Need to add static file service in `backend/main.py` (if not already added):

```python
from fastapi.staticfiles import StaticFiles

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")
```

### Create Directories

If directories don't exist, need to create:

```bash
cd backend
mkdir -p static/reports
```

---

## 📝 Path Configuration Notes

### 1. Example Data Path

**Code Location**: No hardcoded paths, use relative paths directly

**Usage**:
```python
# Reference example file in code
example_file = "backend/example_data/example_deg.csv"
```

### 2. Report Save Path

**Code Location**: `backend/routers/report.py`

**Current Implementation**:
```python
download_url = f"/static/reports/{filename}"
```

**Actual Save Path** (to be implemented):
```python
import os
from pathlib import Path

# Create reports directory (if doesn't exist)
reports_dir = Path("static/reports")
reports_dir.mkdir(parents=True, exist_ok=True)

# Save file
file_path = reports_dir / filename
# ... save file to file_path ...
```

### 3. Upload File Path (Future)

If file saving is needed in the future:

```python
import os
from pathlib import Path
from datetime import datetime

# Create uploads directory
uploads_dir = Path("backend/uploads")
uploads_dir.mkdir(parents=True, exist_ok=True)

# Save file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_path = uploads_dir / f"{timestamp}_{filename}"
```

---

## 🛠️ Setup File Paths

### Create Necessary Directories

Run the following commands to create directory structure:

```bash
cd backend

# Create static files directory
mkdir -p static/reports

# Ensure example_data directory exists
mkdir -p example_data
```

### Verify Directory Structure

```bash
# Check directories
ls -la backend/static/reports/
ls -la backend/example_data/
```

---

## 📋 Path Summary Table

| File Type | Path | Description |
|-----------|------|-------------|
| Example DEG File | `backend/example_data/example_deg.csv` | Test example data |
| Example Enrichment File | `backend/example_data/example_enrichment.csv` | Test example data |
| Generated Reports | `backend/static/reports/{mode}-{timestamp}.{format}` | PDF/DOCX reports |
| Report Templates | `backend/report_templates/` | Report templates (future use) |
| Uploaded Files | In memory (not saved) | Temporary processing |

---

## 🔐 Security Notes

### 1. File Permissions

Ensure report directory has appropriate permissions:

```bash
# Set directory permissions (Linux/Mac)
chmod 755 backend/static/reports
```

### 2. File Cleanup

Recommend regular cleanup of old report files:

```python
# Clean up report files older than 7 days
import os
import time
from pathlib import Path

reports_dir = Path("backend/static/reports")
current_time = time.time()
max_age = 7 * 24 * 60 * 60  # 7 days

for file in reports_dir.glob("*"):
    if file.is_file():
        file_age = current_time - file.stat().st_mtime
        if file_age > max_age:
            file.unlink()
```

### 3. Disk Space

Monitor disk usage of `static/reports/` directory to avoid filling up the disk.

---

## 🚀 Quick Setup

### One-Click Directory Creation

Create script `setup_directories.sh`:

```bash
#!/bin/bash
cd backend
mkdir -p static/reports
mkdir -p example_data
mkdir -p report_templates
echo "✅ Directory structure created"
```

Run:
```bash
chmod +x setup_directories.sh
./setup_directories.sh
```

---

## ❓ FAQ

**Q: Where are uploaded files saved?**
A: Currently not saved to disk, only processed in memory. If saving is needed, code modification is required.

**Q: How to access generated reports?**
A: Through the returned URL, e.g., `http://localhost:8000/static/reports/research-1234567890.pdf`

**Q: Will report files be saved permanently?**
A: Current is placeholder implementation. After actual implementation, recommend adding automatic cleanup mechanism.

**Q: Can I modify the save path?**
A: Yes, modify the path configuration in `backend/routers/report.py`.

---

## 📚 Related Documentation

- **Data Format Guide**: `docs/data_format_guide.md`
- **API Interface Documentation**: `docs/api_contract.md`
- **Running Instructions**: See project README.md

