# 📁 File Path Information

## Quick Reference

### Example Data Files
- **Location**: `backend/example_data/`
- **Files**: 
  - `example_deg.csv` - DEG file example
  - `example_enrichment.csv` - Enrichment analysis file example

### Generated Reports
- **Save Location**: `backend/static/reports/`
- **File Naming**: `{mode}-{timestamp}.{format}`
  - Example: `research-1704067200.pdf`
  - Example: `personal-1704067300.docx`
- **Access URL**: `http://localhost:8000/static/reports/{filename}`

### Uploaded Files
- **Current**: Not saved to disk, processed in memory only
- **Reason**: Privacy protection, reduce disk usage

---

## Directory Structure

```
backend/
├── example_data/          # Example data
│   ├── example_deg.csv
│   └── example_enrichment.csv
├── static/                # Static files
│   └── reports/          # Generated reports
├── report_templates/      # Report templates (future use)
└── ...
```

---

## Detailed Information

See full documentation: `docs/file_paths_guide.md`

