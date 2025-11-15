# 📊 Data Format Guide

This document details the data format requirements for the BioReport Copilot system.

---

## 🔬 Research Mode Data Format

### DEG File Format

**Supported File Formats**:
- CSV (`.csv`)
- TSV (`.tsv`)
- Excel (`.xlsx`)

**Required Columns**:
- `log2FC` or `log2_FC` or `logFC` or `log_fold_change` or `fold_change` or `FC` - Log2 fold change value
- `pvalue` or `p_value` or `pval` or `p` - P-value
- `padj` or `p_adj` or `adjusted_pvalue` or `fdr` or `adj_pval` - Adjusted P-value (optional, preferred if available)

**Recommended Columns**:
- `gene_id` or `gene` or `Gene` or `gene_name` or `geneid` - Gene ID/name

**Optional Columns**:
- Expression matrix columns (for PCA and Heatmap): `Sample_1`, `Sample_2`, `Sample_3`, etc.

### DEG File Examples

#### CSV Format Example:

```csv
gene_id,log2FC,pvalue,padj
GENE1,2.5,0.001,0.01
GENE2,-1.8,0.002,0.015
GENE3,0.3,0.5,0.8
GENE4,3.2,0.0001,0.005
GENE5,-2.1,0.0015,0.012
```

#### CSV Format with Expression Matrix:

```csv
gene_id,log2FC,pvalue,padj,Sample_A1,Sample_A2,Sample_B1,Sample_B2
GENE1,2.5,0.001,0.01,10.2,11.5,8.1,7.9
GENE2,-1.8,0.002,0.015,5.3,5.1,7.2,7.5
GENE3,0.3,0.5,0.8,6.1,6.3,5.9,6.0
GENE4,3.2,0.0001,0.005,12.5,13.1,9.2,9.0
GENE5,-2.1,0.0015,0.012,4.8,4.9,7.1,7.3
```

### Column Name Variants Support

The system automatically recognizes the following column name variants:

**Log2FC Column**:
- `log2FC`, `log2_FC`, `logFC`, `log_fold_change`, `fold_change`, `FC`

**P-value Column**:
- `pvalue`, `p_value`, `pval`, `p`

**Adjusted P-value Column**:
- `padj`, `p_adj`, `adjusted_pvalue`, `fdr`, `adj_pval`

**Gene ID Column**:
- `gene_id`, `gene`, `Gene`, `gene_name`, `geneid`

### Enrichment Analysis File Format (Optional)

**Supported File Formats**:
- CSV (`.csv`)
- TSV (`.tsv`)
- Excel (`.xlsx`)

**Recommended Columns**:
- `pathway` or `term` or `description` or `name` - Pathway/term name
- `pvalue` or `p_value` or `pval` or `padj` or `p_adj` or `fdr` - P-value
- `count` or `gene_count` or `size` or `genes` - Gene count (optional)

**Example**:

```csv
pathway,pvalue,count
GO:0008150,0.001,25
GO:0008152,0.002,18
KEGG:04010,0.0005,32
```

---

## 🧬 Personal Mode Data Format

### API Request Format (JSON)

**Required Fields**:
- `snps`: Array of SNPs, each containing:
  - `rsid`: SNP rsID (string, e.g., "rs762551")
  - `genotype`: Genotype (string, e.g., "AA", "AG", "GG", "CC", "TT")

**Optional Fields**:
- `lifestyle`: Lifestyle object containing:
  - `caffeine_intake`: Caffeine intake (string, e.g., "low", "moderate", "high")
  - `exercise_frequency`: Exercise frequency (string, e.g., "daily", "weekly", "monthly", "rarely")
  - `sleep_duration_hours`: Sleep duration (number, hours)
  - `diet_pattern`: Diet pattern (string, e.g., "vegetarian", "vegan", "omnivore")

### JSON Request Examples

#### Basic SNP Analysis:

```json
{
  "snps": [
    {
      "rsid": "rs762551",
      "genotype": "CC"
    },
    {
      "rsid": "rs4988235",
      "genotype": "CT"
    }
  ]
}
```

#### With Lifestyle Factors:

```json
{
  "snps": [
    {
      "rsid": "rs762551",
      "genotype": "CC"
    },
    {
      "rsid": "rs4988235",
      "genotype": "CT"
    },
    {
      "rsid": "rs7412",
      "genotype": "CC"
    }
  ],
  "lifestyle": {
    "caffeine_intake": "moderate",
    "exercise_frequency": "weekly",
    "sleep_duration_hours": 7.5,
    "diet_pattern": "omnivore"
  }
}
```

### Supported SNP List

The system currently supports detailed interpretation for the following SNPs:

| rsID | Gene | Trait | Supported Genotypes |
|------|------|-------|---------------------|
| rs762551 | CYP1A2 | Caffeine Metabolism | AA, AC, CC |
| rs4988235 | LCT | Lactose Tolerance | CC, CT, TT |
| rs7412 | APOE | Cardiovascular Health | CC, CT, TT |
| rs1800566 | CYP2D6 | Drug Metabolism | GG, GA, AA |
| rs1042713 | ADRB2 | Exercise Response | GG, AG, AA |

**Note**: If an unlisted SNP is input, the system will return a generic interpretation.

---

## 📝 Data Preparation Guide

### Research Mode Data Preparation

1. **Prepare DEG File**:
   - Ensure the file contains at least `log2FC` and `pvalue`/`padj` columns
   - Column names can be any of the variants listed above
   - Values should be numeric format (not text)

2. **Prepare Enrichment Analysis File (Optional)**:
   - Include pathway/term names and P-values
   - Used for generating Pathway Enrichment charts

3. **File Upload**:
   - Upload files through the frontend interface
   - Or use the API directly

### Personal Mode Data Preparation

1. **Obtain SNP Data**:
   - Get from genetic testing reports or platforms like 23andMe, AncestryDNA
   - Format: rsID + genotype (e.g., rs762551: CC)

2. **Prepare Lifestyle Data (Optional)**:
   - Record caffeine intake, exercise frequency, sleep duration, diet pattern

3. **Build JSON Request**:
   - Build JSON according to the format above
   - Input through frontend interface
   - Or call the API directly

---

## 🔍 Data Validation

### DEG File Validation

The system automatically validates:
- ✅ Required columns exist
- ✅ Numeric format is correct
- ✅ Sufficient gene data is available

**Common Errors**:
- ❌ Missing `log2FC` column → Error: `Required column 'log2fc' not found`
- ❌ Missing `pvalue`/`padj` column → Error: `Required column 'pvalue' not found`
- ❌ Incorrect numeric format → Error: `Data parsing error`

### SNP Data Validation

The system automatically validates:
- ✅ rsID format is correct
- ✅ Genotype format is correct (usually two letters, e.g., AA, AG, GG)

**Common Errors**:
- ❌ Empty SNP list → Error: `At least one SNP must be provided`
- ❌ Invalid rsID format → System will return generic interpretation

---

## 📊 Example Data Files

### Example DEG File (CSV)

Create file `example_deg.csv`:

```csv
gene_id,log2FC,pvalue,padj
BRCA1,2.45,0.0001,0.001
TP53,-1.89,0.0005,0.005
EGFR,1.23,0.01,0.05
MYC,3.12,0.00001,0.0001
KRAS,-2.34,0.001,0.01
```

### Example Enrichment Analysis File (CSV)

Create file `example_enrichment.csv`:

```csv
pathway,pvalue,count
GO:0007049,0.0001,45
GO:0006915,0.0005,32
KEGG:04110,0.001,28
REACTOME:R-HSA-73857,0.002,15
```

### Example SNP JSON

```json
{
  "snps": [
    {"rsid": "rs762551", "genotype": "CC"},
    {"rsid": "rs4988235", "genotype": "CT"},
    {"rsid": "rs7412", "genotype": "CC"}
  ],
  "lifestyle": {
    "caffeine_intake": "high",
    "exercise_frequency": "daily",
    "sleep_duration_hours": 8.0,
    "diet_pattern": "omnivore"
  }
}
```

---

## 🚀 Quick Start

### Research Mode

1. Prepare a CSV file with the following columns:
   ```
   gene_id, log2FC, pvalue
   ```
2. Upload the file through the frontend interface
3. Click "Generate Report" to view analysis results

### Personal Mode

1. Prepare SNP data (rsID + genotype)
2. Input through frontend interface or use JSON API
3. Click "Analyze" to view personalized report

---

## ❓ FAQ

**Q: What if my DEG file has different column names?**
A: The system supports multiple column name variants and will automatically recognize them. If it still fails, please rename columns to standard names.

**Q: Can I upload Excel files?**
A: Yes! The system supports `.xlsx` format.

**Q: Do SNP genotypes need to be uppercase?**
A: No, the system will automatically convert to uppercase.

**Q: How many SNPs can I analyze?**
A: There's no theoretical limit, but we recommend analyzing 10-50 SNPs per session for optimal performance.

**Q: Is the enrichment analysis file required?**
A: No, it's optional, but providing it will generate additional Pathway Enrichment charts.

---

## 📞 Technical Support

If you encounter data format issues, please check:
1. File format is correct (CSV/TSV/XLSX)
2. Required columns exist
3. Numeric format is correct
4. Check error messages for specific hints

For more information, please refer to:
- `docs/api_contract.md` - API interface documentation
- `docs/backend_analysis_logic.md` - Analysis logic explanation

