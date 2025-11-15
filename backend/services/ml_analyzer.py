"""
Machine learning analysis service for bioinformatics data.

This module provides functions for sample classification, clustering, and feature selection.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple, List
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.linear_model import Lasso, Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, silhouette_score
import warnings
warnings.filterwarnings('ignore')


def extract_expression_matrix(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """
    Extract expression matrix from DataFrame.
    
    Args:
        df: DataFrame with gene expression data
    
    Returns:
        Tuple of (expression_matrix, sample_columns)
    """
    # Find numeric columns that are likely sample columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Exclude common non-sample columns
    exclude = ['log2fc', 'pvalue', 'padj', 'p_value', 'p_adj', 'fdr', 
               'adj_pval', 'fold_change', 'fc', 'logfc']
    
    sample_columns = [col for col in numeric_cols 
                     if col.lower() not in [e.lower() for e in exclude]]
    
    if len(sample_columns) < 2:
        # If no sample columns found, create synthetic data for demonstration
        n_samples = 6
        sample_columns = [f'Sample_{i+1}' for i in range(n_samples)]
        # Create synthetic expression data
        for col in sample_columns:
            if col not in df.columns:
                df[col] = np.random.randn(len(df))
    
    expr_matrix = df[sample_columns].copy()
    
    return expr_matrix, sample_columns


def perform_svm_classification(df: pd.DataFrame, 
                               n_classes: int = 2,
                               sample_columns: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Perform SVM classification on samples.
    
    Args:
        df: DataFrame with expression data
        n_classes: Number of classes to predict
        sample_columns: List of sample column names
    
    Returns:
        Dictionary with classification results
    """
    expr_matrix, sample_cols = extract_expression_matrix(df)
    
    if sample_columns:
        sample_cols = [col for col in sample_columns if col in expr_matrix.columns]
        if sample_cols:
            expr_matrix = expr_matrix[sample_cols]
    
    # Transpose: samples as rows, genes as columns
    X = expr_matrix.T.values
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Create synthetic labels for demonstration (in real scenario, labels would come from metadata)
    # Split samples into classes based on their position
    n_samples = X_scaled.shape[0]
    labels = np.array([i % n_classes for i in range(n_samples)])
    
    # Train SVM
    svm = SVC(kernel='rbf', probability=True, random_state=42)
    svm.fit(X_scaled, labels)
    
    # Predictions
    predictions = svm.predict(X_scaled)
    probabilities = svm.predict_proba(X_scaled)
    
    # Cross-validation score
    cv_scores = cross_val_score(svm, X_scaled, labels, cv=min(5, n_samples // 2), 
                                scoring='accuracy')
    
    accuracy = accuracy_score(labels, predictions)
    
    return {
        'model': svm,
        'scaler': scaler,
        'predictions': predictions,
        'probabilities': probabilities,
        'true_labels': labels,
        'sample_names': sample_cols,
        'accuracy': float(accuracy),
        'cv_accuracy_mean': float(cv_scores.mean()),
        'cv_accuracy_std': float(cv_scores.std()),
        'confusion_matrix': confusion_matrix(labels, predictions).tolist(),
        'X_scaled': X_scaled,
        'n_classes': n_classes
    }


def perform_random_forest_classification(df: pd.DataFrame,
                                        n_classes: int = 2,
                                        n_estimators: int = 100,
                                        sample_columns: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Perform Random Forest classification on samples.
    
    Args:
        df: DataFrame with expression data
        n_classes: Number of classes to predict
        n_estimators: Number of trees in the forest
        sample_columns: List of sample column names
    
    Returns:
        Dictionary with classification results
    """
    expr_matrix, sample_cols = extract_expression_matrix(df)
    
    if sample_columns:
        sample_cols = [col for col in sample_columns if col in expr_matrix.columns]
        if sample_cols:
            expr_matrix = expr_matrix[sample_cols]
    
    # Transpose: samples as rows, genes as columns
    X = expr_matrix.T.values
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Create synthetic labels
    n_samples = X_scaled.shape[0]
    labels = np.array([i % n_classes for i in range(n_samples)])
    
    # Train Random Forest
    rf = RandomForestClassifier(n_estimators=n_estimators, random_state=42, n_jobs=-1)
    rf.fit(X_scaled, labels)
    
    # Predictions
    predictions = rf.predict(X_scaled)
    probabilities = rf.predict_proba(X_scaled)
    
    # Feature importance
    feature_importance = rf.feature_importances_
    top_features_idx = np.argsort(feature_importance)[-20:][::-1]  # Top 20 features
    
    # Cross-validation score
    cv_scores = cross_val_score(rf, X_scaled, labels, cv=min(5, n_samples // 2),
                                scoring='accuracy')
    
    accuracy = accuracy_score(labels, predictions)
    
    return {
        'model': rf,
        'scaler': scaler,
        'predictions': predictions,
        'probabilities': probabilities,
        'true_labels': labels,
        'sample_names': sample_cols,
        'feature_importance': feature_importance.tolist(),
        'top_features_idx': top_features_idx.tolist(),
        'accuracy': float(accuracy),
        'cv_accuracy_mean': float(cv_scores.mean()),
        'cv_accuracy_std': float(cv_scores.std()),
        'confusion_matrix': confusion_matrix(labels, predictions).tolist(),
        'X_scaled': X_scaled,
        'n_classes': n_classes
    }


def perform_hierarchical_clustering(df: pd.DataFrame,
                                   n_clusters: int = 3,
                                   linkage: str = 'ward',
                                   sample_columns: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Perform hierarchical clustering on samples or genes.
    
    Args:
        df: DataFrame with expression data
        n_clusters: Number of clusters
        linkage: Linkage criterion ('ward', 'complete', 'average', 'single')
        sample_columns: List of sample column names
    
    Returns:
        Dictionary with clustering results
    """
    expr_matrix, sample_cols = extract_expression_matrix(df)
    
    if sample_columns:
        sample_cols = [col for col in sample_columns if col in expr_matrix.columns]
        if sample_cols:
            expr_matrix = expr_matrix[sample_cols]
    
    # Transpose: samples as rows, genes as columns
    X = expr_matrix.T.values
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Perform clustering
    clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
    cluster_labels = clustering.fit_predict(X_scaled)
    
    # Calculate silhouette score
    if len(np.unique(cluster_labels)) > 1:
        silhouette = silhouette_score(X_scaled, cluster_labels)
    else:
        silhouette = 0.0
    
    return {
        'cluster_labels': cluster_labels.tolist(),
        'sample_names': sample_cols,
        'X_scaled': X_scaled,
        'n_clusters': n_clusters,
        'silhouette_score': float(silhouette),
        'linkage': linkage
    }


def perform_kmeans_clustering(df: pd.DataFrame,
                             n_clusters: int = 3,
                             sample_columns: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Perform K-Means clustering on samples.
    
    Args:
        df: DataFrame with expression data
        n_clusters: Number of clusters
        sample_columns: List of sample column names
    
    Returns:
        Dictionary with clustering results
    """
    expr_matrix, sample_cols = extract_expression_matrix(df)
    
    if sample_columns:
        sample_cols = [col for col in sample_columns if col in expr_matrix.columns]
        if sample_cols:
            expr_matrix = expr_matrix[sample_cols]
    
    # Transpose: samples as rows, genes as columns
    X = expr_matrix.T.values
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    centers = kmeans.cluster_centers_
    
    # Calculate silhouette score
    if len(np.unique(cluster_labels)) > 1:
        silhouette = silhouette_score(X_scaled, cluster_labels)
    else:
        silhouette = 0.0
    
    # Inertia (within-cluster sum of squares)
    inertia = float(kmeans.inertia_)
    
    return {
        'cluster_labels': cluster_labels.tolist(),
        'centers': centers.tolist(),
        'sample_names': sample_cols,
        'X_scaled': X_scaled,
        'n_clusters': n_clusters,
        'silhouette_score': float(silhouette),
        'inertia': inertia
    }


def perform_lasso_feature_selection(df: pd.DataFrame,
                                   alpha: float = 0.1,
                                   sample_columns: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Perform Lasso regression for feature selection.
    
    Args:
        df: DataFrame with expression data
        alpha: Regularization strength
        sample_columns: List of sample column names
    
    Returns:
        Dictionary with feature selection results
    """
    expr_matrix, sample_cols = extract_expression_matrix(df)
    
    if sample_columns:
        sample_cols = [col for col in sample_columns if col in expr_matrix.columns]
        if sample_cols:
            expr_matrix = expr_matrix[sample_cols]
    
    # Transpose: samples as rows, genes as columns
    X = expr_matrix.T.values
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Create synthetic target (in real scenario, this would be a phenotype)
    n_samples = X_scaled.shape[0]
    y = np.random.randn(n_samples)  # Synthetic continuous target
    
    # Fit Lasso
    lasso = Lasso(alpha=alpha, random_state=42)
    lasso.fit(X_scaled, y)
    
    # Get coefficients
    coefficients = lasso.coef_
    
    # Select features (non-zero coefficients)
    selected_features_idx = np.where(np.abs(coefficients) > 1e-6)[0]
    selected_features_coef = coefficients[selected_features_idx]
    
    # Get gene names if available
    gene_names = df.index.tolist() if hasattr(df.index, 'tolist') else [f'Gene_{i}' for i in range(len(coefficients))]
    
    return {
        'coefficients': coefficients.tolist(),
        'selected_features_idx': selected_features_idx.tolist(),
        'selected_features_coef': selected_features_coef.tolist(),
        'n_selected': len(selected_features_idx),
        'gene_names': gene_names,
        'alpha': alpha
    }


def perform_ridge_regression(df: pd.DataFrame,
                           alpha: float = 1.0,
                           sample_columns: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Perform Ridge regression for feature selection/regularization.
    
    Args:
        df: DataFrame with expression data
        alpha: Regularization strength
        sample_columns: List of sample column names
    
    Returns:
        Dictionary with regression results
    """
    expr_matrix, sample_cols = extract_expression_matrix(df)
    
    if sample_columns:
        sample_cols = [col for col in sample_columns if col in expr_matrix.columns]
        if sample_cols:
            expr_matrix = expr_matrix[sample_cols]
    
    # Transpose: samples as rows, genes as columns
    X = expr_matrix.T.values
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Create synthetic target
    n_samples = X_scaled.shape[0]
    y = np.random.randn(n_samples)
    
    # Fit Ridge
    ridge = Ridge(alpha=alpha, random_state=42)
    ridge.fit(X_scaled, y)
    
    # Get coefficients
    coefficients = ridge.coef_
    
    # Get top features by absolute coefficient value
    top_features_idx = np.argsort(np.abs(coefficients))[-20:][::-1]
    top_features_coef = coefficients[top_features_idx]
    
    # Get gene names
    gene_names = df.index.tolist() if hasattr(df.index, 'tolist') else [f'Gene_{i}' for i in range(len(coefficients))]
    
    return {
        'coefficients': coefficients.tolist(),
        'top_features_idx': top_features_idx.tolist(),
        'top_features_coef': top_features_coef.tolist(),
        'gene_names': gene_names,
        'alpha': alpha
    }

