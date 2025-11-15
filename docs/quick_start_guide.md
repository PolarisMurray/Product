# 🚀 Quick Start Guide

This guide helps you quickly prepare test data and start using BioReport Copilot.

---

## 📋 Data Format Quick Reference

### Research Mode

**Required DEG File Columns**:
- `log2FC` (or variants: `log2_FC`, `logFC`, `log_fold_change`, `FC`)
- `pvalue` (or variants: `p_value`, `pval`, `p`)
- `padj` (optional, or variants: `p_adj`, `adjusted_pvalue`, `fdr`)

**Recommended Columns**:
- `gene_id` (or variants: `gene`, `Gene`, `gene_name`)

**Example File Location**: `backend/example_data/example_deg.csv`

### Personal Mode

**JSON Format**:
```json
{
  "snps": [
    {"rsid": "rs762551", "genotype": "CC"},
    {"rsid": "rs4988235", "genotype": "CT"}
  ],
  "lifestyle": {
    "caffeine_intake": "moderate",
    "exercise_frequency": "weekly"
  }
}
```

---

## 🔬 Research Mode Testing Steps

### 1. Prepare DEG File

**Option A: Use Example File**
- Location: `backend/example_data/example_deg.csv`
- Ready to use directly

**Option B: Create Your Own File**

Create a CSV file with the following columns:

```csv
gene_id,log2FC,pvalue,padj
GENE1,2.5,0.001,0.01
GENE2,-1.8,0.002,0.015
GENE3,0.3,0.5,0.8
```

**Column Name Variants Supported**:
- Log2FC: `log2FC`, `log2_FC`, `logFC`, `log_fold_change`, `FC`
- P-value: `pvalue`, `p_value`, `pval`, `p`
- Adjusted P-value: `padj`, `p_adj`, `adjusted_pvalue`, `fdr`
- Gene ID: `gene_id`, `gene`, `Gene`, `gene_name`

### 2. Prepare Enrichment Analysis File (Optional)

**Example File**: `backend/example_data/example_enrichment.csv`

Format:
```csv
pathway,pvalue,count
GO:0007049,0.0001,45
KEGG:04110,0.001,28
```

### 3. Upload and Analyze

1. Start the application (refer to project README.md)
2. Switch to "Research Mode"
3. Fill in project information (optional)
4. Upload DEG file
5. Upload enrichment analysis file (optional)
6. Click "Generate Report"

---

## 🧬 Personal Mode Testing Steps

### 1. Prepare SNP Data

**Supported SNPs**:
- `rs762551` (CYP1A2) - Caffeine Metabolism
- `rs4988235` (LCT) - Lactose Tolerance
- `rs7412` (APOE) - Cardiovascular Health
- `rs1800566` (CYP2D6) - Drug Metabolism
- `rs1042713` (ADRB2) - Exercise Response

**Genotype Format**: Two letters, e.g., `AA`, `AG`, `GG`, `CC`, `TT`

### 2. Test Examples

**Example 1: Caffeine Metabolism Analysis**
```json
{
  "snps": [
    {"rsid": "rs762551", "genotype": "CC"}
  ]
}
```

**Example 2: Multi-SNP Analysis**
```json
{
  "snps": [
    {"rsid": "rs762551", "genotype": "CC"},
    {"rsid": "rs4988235", "genotype": "CT"},
    {"rsid": "rs7412", "genotype": "CC"}
  ],
  "lifestyle": {
    "caffeine_intake": "moderate",
    "exercise_frequency": "weekly",
    "sleep_duration_hours": 7.5,
    "diet_pattern": "omnivore"
  }
}
```

### 3. Analyze

1. Start the application
2. Switch to "Personal Genomics Mode"
3. Input SNP data (through frontend interface or API)
4. Input lifestyle information (optional)
5. Click "Analyze"

---

## 📊 Data Format Checklist

### DEG File Check

- [ ] File format: CSV, TSV, or XLSX
- [ ] Contains `log2FC` column (or variant)
- [ ] Contains `pvalue` column (or variant)
- [ ] Values are numeric format (not text)
- [ ] At least a few rows of data (recommend 10+ rows)

### SNP Data Check

- [ ] rsID format is correct (e.g., `rs762551`)
- [ ] Genotype format is correct (two letters, e.g., `AA`, `CC`)
- [ ] At least one SNP included

---

## 🎯 Quick Testing

### Test Research Mode

1. Use example file: `backend/example_data/example_deg.csv`
2. Upload to frontend interface
3. View generated charts and text

### Test Personal Mode

1. Use the following JSON:
```json
{
  "snps": [
    {"rsid": "rs762551", "genotype": "CC"},
    {"rsid": "rs4988235", "genotype": "CT"}
  ]
}
```
2. Input through frontend interface or call API directly
3. View generated Insight Cards and BioCard

---

## ❓ FAQ

**Q: What if my file has different column names?**
A: The system supports multiple column name variants and will automatically recognize them. If it fails, please rename to standard names.

**Q: Can I upload Excel files?**
A: Yes! Supports `.xlsx` format.

**Q: Do SNP genotypes need to be uppercase?**
A: No, the system will automatically convert.

**Q: How much data is needed for analysis?**
A: 
- DEG file: Recommend at least 10-20 genes
- SNP: At least 1 SNP

**Q: Is the enrichment analysis file required?**
A: No, it's optional, but providing it will generate additional Pathway Enrichment charts.

---

## 📚 More Information

- **Detailed Data Format**: See `docs/data_format_guide.md`
- **API Interface Documentation**: See `docs/api_contract.md`
- **Analysis Logic Explanation**: See `docs/backend_analysis_logic.md`
- **Running Instructions**: See project README.md

---

## 🎉 Start Using

1. Ensure backend and frontend are started
2. Prepare test data (use example files or create your own)
3. Upload data through frontend interface
4. View analysis results!

If you have questions, please refer to detailed documentation or check error messages.

