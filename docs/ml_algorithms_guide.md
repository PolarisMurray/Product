# 🤖 Machine Learning Algorithms Guide

## 📋 Overview

BioReport Copilot now integrates multiple machine learning algorithms for sample classification, clustering analysis, and feature selection. All algorithms automatically generate visualization charts.

---

## 🔬 Implemented Algorithms

### 1. Sample Classification

#### 1.1 Support Vector Machine (SVM)
- **Algorithm**: Support Vector Machine with RBF kernel
- **Function**: Predict sample categories based on full gene expression profiles
- **Visualization**:
  - Classification result scatter plot (PCA reduced to 2D)
  - Confusion matrix heatmap
- **Output Metrics**:
  - Classification accuracy
  - Cross-validation accuracy
  - Confusion matrix

#### 1.2 Random Forest
- **Algorithm**: Random Forest Classifier
- **Function**: Predict sample categories based on full gene expression profiles, while identifying important features
- **Visualization**:
  - Classification result scatter plot
  - Top 20 feature importance bar chart
  - Confusion matrix heatmap
  - Feature importance distribution histogram
- **Output Metrics**:
  - Classification accuracy
  - Cross-validation accuracy
  - Feature importance scores
  - Confusion matrix

---

### 2. Clustering Analysis

#### 2.1 Hierarchical Clustering
- **Algorithm**: Agglomerative Clustering
- **Function**: Identify sample groups with similar expression patterns
- **Parameters**:
  - `n_clusters`: Number of clusters (default 3)
  - `linkage`: Linkage method ('ward', 'complete', 'average', 'single')
- **Visualization**:
  - Clustering result scatter plot (PCA reduced to 2D)
  - Dendrogram
- **Output Metrics**:
  - Cluster labels
  - Silhouette Score

#### 2.2 K-Means Clustering
- **Algorithm**: K-Means Clustering
- **Function**: Identify sample groups with similar expression patterns
- **Parameters**:
  - `n_clusters`: Number of clusters (default 3)
- **Visualization**:
  - Clustering result scatter plot (with cluster centers)
  - Cluster size distribution bar chart
- **Output Metrics**:
  - Cluster labels
  - Cluster centers
  - Silhouette Score
  - Within-cluster sum of squares (Inertia)

---

### 3. Feature Selection/Dimensionality Reduction

#### 3.1 Principal Component Analysis (PCA)
- **Algorithm**: Principal Component Analysis
- **Function**: Reduce data dimensionality, identify main variation directions
- **Visualization**:
  - PCA scatter plot (PC1 vs PC2)
  - Display explained variance ratio
- **Output Metrics**:
  - Principal component scores
  - Explained variance ratio

#### 3.2 Lasso Regression
- **Algorithm**: Lasso Regression (L1 Regularization)
- **Function**: Feature selection, identify most important gene subsets
- **Parameters**:
  - `alpha`: Regularization strength (default 0.1)
- **Visualization**:
  - Coefficient value line chart
  - Top 20 selected features bar chart
  - Coefficient distribution histogram
  - Feature selection statistics bar chart
- **Output Metrics**:
  - Regression coefficients
  - Number of selected features
  - Coefficient values of selected features

#### 3.3 Ridge Regression
- **Algorithm**: Ridge Regression (L2 Regularization)
- **Function**: Feature selection and regularization
- **Parameters**:
  - `alpha`: Regularization strength (default 1.0)
- **Visualization**:
  - Coefficient value line chart
  - Top 20 features (by absolute value) bar chart
  - Coefficient distribution histogram
  - Absolute coefficient value line chart
- **Output Metrics**:
  - Regression coefficients
  - Top feature indices and coefficient values

---

## 📊 Chart Type Summary

| Algorithm | Number of Charts | Chart Types |
|-----------|------------------|-------------|
| SVM | 2 | Classification scatter, Confusion matrix |
| Random Forest | 4 | Classification scatter, Feature importance, Confusion matrix, Importance distribution |
| Hierarchical Clustering | 2 | Clustering scatter, Dendrogram |
| K-Means | 2 | Clustering scatter (with centers), Cluster size distribution |
| PCA | 1 | PCA scatter plot |
| Lasso | 4 | Coefficient chart, Selected features, Coefficient distribution, Statistics chart |
| Ridge | 4 | Coefficient chart, Top features, Coefficient distribution, Absolute coefficient chart |

**Total**: 19 different visualization charts

---

## 🔄 Workflow

### Automatic Execution Flow

After users upload DEG files, the system automatically executes the following analyses:

1. **Basic Analysis**
   - Volcano Plot
   - PCA Analysis
   - Heatmap

2. **Sample Classification** (automatic execution)
   - SVM Classification
   - Random Forest Classification

3. **Clustering Analysis** (automatic execution)
   - Hierarchical Clustering
   - K-Means Clustering

4. **Feature Selection** (automatic execution)
   - Lasso Feature Selection
   - Ridge Regression

5. **Enrichment Analysis** (if enrichment file provided)
   - Pathway Enrichment Plot

---

## 📝 Technical Implementation

### Data Preprocessing

All algorithms automatically perform:
- **Data Extraction**: Extract expression matrix from DEG files
- **Standardization**: Z-score standardization using StandardScaler
- **Dimension Processing**: Automatically identify sample columns, exclude statistical columns (log2FC, pvalue, etc.)

### Visualization Dimensionality Reduction

For high-dimensional data (>2 dimensions), all scatter plots will:
- Use PCA to reduce to 2D for visualization
- Retain original data for calculations

### Error Handling

- All algorithms have independent try-except blocks
- Failure of a single algorithm does not affect other algorithms
- Error messages are logged and do not interrupt the entire analysis flow

---

## 🎯 Use Cases

### 1. Tumor vs Normal Sample Classification
- Use SVM or Random Forest
- Distinguish tumor and normal samples based on full gene expression profiles

### 2. Drug Sensitive vs Resistant Prediction
- Use SVM or Random Forest
- Predict sample response to drugs

### 3. Sample Subtype Discovery
- Use Hierarchical Clustering or K-Means
- Discover sample groups with similar expression patterns

### 4. Key Gene Identification
- Use Lasso or Ridge Regression
- Identify most important gene subsets for phenotypes

### 5. Data Dimensionality Reduction
- Use PCA
- Visualize main variations in high-dimensional data

---

## 📈 Output Examples

### SVM Classification Results
```
SVM Classification Results
Accuracy: 0.950
Cross-validation Accuracy: 0.920 ± 0.050
```

### Clustering Results
```
Hierarchical Clustering
3 Clusters
Silhouette Score: 0.650
```

### Feature Selection Results
```
Lasso Feature Selection
Selected: 45 features out of 20000
Alpha: 0.1
```

---

## 🔧 Parameter Adjustment

Current implementation uses default parameters. Future versions may support:

1. **User Configurable Parameters**:
   - Number of clusters
   - Regularization strength
   - Number of classification categories

2. **Algorithm Selection**:
   - Allow users to select algorithms to execute
   - Avoid unnecessary computations

---

## 📚 Detailed Algorithm Descriptions

### SVM (Support Vector Machine)
- **Kernel Function**: RBF (Radial Basis Function)
- **Advantages**: Suitable for nonlinear classification, good performance on high-dimensional data
- **Applications**: Sample classification, phenotype prediction

### Random Forest
- **Number of Trees**: 100 (default)
- **Advantages**: Strong interpretability, provides feature importance
- **Applications**: Sample classification, feature selection

### Hierarchical Clustering
- **Linkage Method**: Ward (default)
- **Advantages**: Generates dendrogram, easy to understand clustering hierarchy
- **Applications**: Sample grouping, subtype discovery

### K-Means
- **Initialization**: K-means++
- **Advantages**: Fast computation, suitable for large datasets
- **Applications**: Sample grouping, pattern recognition

### Lasso Regression
- **Regularization**: L1 (Lasso)
- **Advantages**: Automatic feature selection, sparse coefficients
- **Applications**: Key gene identification, dimensionality reduction

### Ridge Regression
- **Regularization**: L2 (Ridge)
- **Advantages**: Prevents overfitting, smooth coefficients
- **Applications**: Feature selection, regression prediction

---

## ⚠️ Notes

1. **Data Requirements**:
   - Expression matrix data (sample columns) required
   - If only DEG statistics are available, some algorithms may not execute

2. **Computation Time**:
   - Large datasets may require longer time
   - Recommend sample count > 3, feature count > 10

3. **Label Generation**:
   - Currently uses synthetic labels for demonstration
   - Real applications require actual sample labels

4. **Parameter Selection**:
   - Default parameters work for most cases
   - Specific scenarios may require parameter adjustment

---

## 🚀 Future Improvements

1. **Real Label Support**:
   - Allow users to upload sample label files
   - Use real labels for classification and evaluation

2. **Parameter Optimization**:
   - Automatically select optimal parameters
   - Grid search or Bayesian optimization

3. **More Algorithms**:
   - Neural network classification
   - t-SNE dimensionality reduction
   - DBSCAN clustering

4. **Interactive Visualization**:
   - 3D scatter plots
   - Interactive charts

---

## 📖 Related Documentation

- **Data Format Guide**: `docs/data_format_guide.md`
- **API Interface Documentation**: `docs/api_contract.md`
- **Backend Analysis Logic**: `docs/backend_analysis_logic.md`

---

## ✅ Summary

The system now supports:
- ✅ 2 classification algorithms (SVM, Random Forest)
- ✅ 2 clustering algorithms (Hierarchical, K-Means)
- ✅ 3 dimensionality reduction/feature selection methods (PCA, Lasso, Ridge)
- ✅ 19 visualization charts
- ✅ Automatic execution of all analyses
- ✅ Complete error handling

All algorithms automatically generate high-quality visualization charts to help users better understand the data!

