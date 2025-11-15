# 🔬 Backend Analysis Logic

## 📋 Current Implementation Status

**✅ Real data analysis functions have been fully implemented!**

The backend now includes complete data analysis capabilities:
- ✅ Real parsing and analysis of DEG files
- ✅ Generation of real bioinformatics charts
- ✅ Scientific text generation based on real data
- ✅ Extended SNP rule database and interpretation engine
- ✅ Real percentile calculation

**For detailed implementation information, please refer to**: `docs/implementation_complete.md`

---

## 🔬 Research Mode Analysis Flow

### ✅ Current Implementation (Real Analysis)

**File Locations**: 
- `backend/routers/research.py` - API endpoint
- `backend/services/deg_analyzer.py` - DEG file parsing and analysis
- `backend/services/plot_generator.py` - Chart generation
- `backend/services/research_service.py` - Text generation
- `backend/services/ml_analyzer.py` - Machine learning algorithms

**Current Flow**:
1. ✅ **Receive Files**: Read uploaded DEG file and optional enrichment file
2. ✅ **Parse Files**: Use `parse_deg_file()` to parse CSV/TSV/XLSX files
3. ✅ **Normalize Column Names**: Automatically recognize various column name variants (log2FC, log2_FC, logFC, etc.)
4. ✅ **Data Analysis**: Use `analyze_deg_data()` to calculate real statistics
   - DEG count (based on pvalue/padj and log2FC thresholds)
   - Up and down-regulated gene classification
   - Percentage and average calculations
5. ✅ **Generate Real Charts**: 
   - Volcano Plot (based on real data)
   - PCA Plot (if expression matrix available)
   - Heatmap (top DEGs)
   - Pathway Enrichment (if enrichment file provided)
6. ✅ **Machine Learning Analysis** (automatic):
   - SVM Classification
   - Random Forest Classification
   - Hierarchical Clustering
   - K-Means Clustering
   - Lasso Feature Selection
   - Ridge Regression
7. ✅ **Generate Real Text**: Dynamically generate Results and Discussion based on statistical results
8. ✅ **Return Results**: Return response containing real analysis data

### ✅ Implemented Features

**Real Analysis Functions**:

1. ✅ **Read and Parse DEG Files**
   - Support CSV, TSV, XLSX formats
   - Automatic column name normalization
   - Parse gene_id, log2FC, pvalue, padj columns

2. ✅ **Statistical Analysis**
   - Calculate DEG count (based on pvalue/padj and log2FC thresholds)
   - Classify up and down-regulated genes
   - Calculate percentages, averages, medians
   - Extract top DEGs

3. ✅ **Generate Real Charts**
   - **Volcano Plot**: Draw real data using matplotlib/seaborn
   - **PCA Plot**: Support expression matrix data
   - **Heatmap**: Display expression patterns of top DEGs
   - **Pathway Enrichment**: Visualize enrichment analysis results

4. ✅ **Machine Learning Analysis**
   - **Sample Classification**: SVM, Random Forest
   - **Clustering**: Hierarchical, K-Means
   - **Feature Selection**: Lasso, Ridge Regression

5. ✅ **Text Generation** (`services/research_service.py`)
   - Generate Results and Discussion based on real statistical data
   - Dynamically reflect analysis results
   - Include key findings and biological interpretations

**Future Improvements**:
- 🔮 Integrate OpenAI API or LLM for more intelligent text generation
- 🔮 Improve PCA and Heatmap to better handle expression matrices
- 🔮 Add more statistical analysis and visualization options

---

## 🧬 Personal Mode Analysis Flow

### ✅ Current Implementation (Extended Rule Engine)

**File Locations**: 
- `backend/routers/personal.py` - API endpoint
- `backend/services/genetics_engine.py` - SNP rule engine
- `backend/services/personal_service.py` - Percentile calculation

**Current Flow**:
1. ✅ **Receive SNP Data**: Parse rsID and genotype
2. ✅ **Rule Matching**: Use extended SNP rule database
   - Support 5+ SNPs (rs762551, rs4988235, rs7412, rs1800566, rs1042713)
   - Each SNP contains detailed interpretations for multiple genotypes
   - Unknown SNPs return generic interpretation
3. ✅ **Generate Insight Cards**: Generate personalized interpretations and recommendations based on rule database
4. ✅ **Generate Peer Comparison**: Calculate real percentiles using statistical distributions
5. ✅ **Generate BioCard**: Generate comprehensive card based on analysis results

**SNP Rule Database**:
- Caffeine Metabolism (rs762551)
- Lactose Tolerance (rs4988235)
- Cardiovascular Health (rs7412)
- Drug Metabolism (rs1800566)
- Exercise Response (rs1042713)

### ✅ Implemented Features

**Real Analysis Functions**:

1. ✅ **SNP Rule Database**
   - Extended SNP rule library (5+ SNPs)
   - Each SNP contains gene information, genotype interpretation, scores, and recommendations
   - Support generic interpretation for unknown SNPs

2. ✅ **Rule Engine** (`services/genetics_engine.py`)
   - Intelligent SNP matching and interpretation
   - Generate personalized Insight Cards
   - Integrate lifestyle factors

3. ✅ **Percentile Calculation** (`services/personal_service.py`)
   - Calculate percentiles using statistical distributions (normal distribution, Beta distribution)
   - Support trait-specific distributions
   - Implemented using scipy.stats

4. ✅ **Personalized Recommendation Generation**
   - Generate personalized recommendations based on SNP results
   - Integrate lifestyle factors into BioCard
   - Generate peer comparison metrics

**Future Improvements**:
- 🔮 Connect to real population databases (1000 Genomes, gnomAD)
- 🔮 Extend SNP rule database
- 🔮 Support multi-SNP interaction analysis
- 🔮 AI-generated more personalized recommendations

---

## 📊 Data Analysis Module Structure

### Current Structure

```
backend/
├── routers/
│   ├── research.py      # Research mode API (real implementation)
│   └── personal.py      # Personal mode API (extended rules)
├── services/
│   ├── deg_analyzer.py          # DEG data analysis
│   ├── plot_generator.py        # Chart generation
│   ├── ml_analyzer.py           # Machine learning algorithms
│   ├── enrichment_analyzer.py   # Enrichment analysis (via plot_generator)
│   ├── research_service.py      # Text generation
│   └── personal_service.py      # Percentile calculation
└── models/
    └── schemas.py       # Data model definitions
```

---

## 🎯 Summary

**Current Status**:
- ✅ API interfaces complete
- ✅ Data structure definitions complete
- ✅ Frontend-backend integration normal
- ✅ **Real data analysis: Fully implemented!**

**Implemented Features**:
1. ✅ DEG file parsing and statistical analysis
2. ✅ Generate real charts using matplotlib/seaborn
3. ✅ Generate scientific text based on real data
4. ✅ Extended SNP rule database (5+ SNPs)
5. ✅ Real percentile calculation (based on statistical distributions)
6. ✅ Machine learning analysis (7 algorithms)

**For detailed implementation information**: Please refer to `docs/implementation_complete.md`

**Future Improvement Directions**:
- 🔮 Integrate OpenAI API for more intelligent text generation
- 🔮 Use real population databases to calculate percentiles
- 🔮 Extend more SNP rules
- 🔮 Improve expression matrix processing

