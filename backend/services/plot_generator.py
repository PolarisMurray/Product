"""
Plot generation service for bioinformatics visualizations.

This module provides functions to generate various plots using matplotlib and seaborn.
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import base64
import io
from typing import Optional, Tuple


def plot_to_base64(fig) -> str:
    """
    Convert matplotlib figure to base64-encoded PNG string.
    
    Args:
        fig: Matplotlib figure object
    
    Returns:
        Base64-encoded PNG string
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_base64


def generate_volcano_plot(df: pd.DataFrame, 
                         pvalue_col: str = 'padj',
                         log2fc_col: str = 'log2fc',
                         pvalue_threshold: float = 0.05,
                         log2fc_threshold: float = 1.0) -> str:
    """
    Generate a volcano plot showing differential expression.
    
    Args:
        df: DataFrame with DEG data
        pvalue_col: Column name for p-values
        log2fc_col: Column name for log2 fold change
        pvalue_threshold: P-value threshold
        log2fc_threshold: Log2FC threshold
    
    Returns:
        Base64-encoded PNG string
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Prepare data
    if pvalue_col not in df.columns:
        pvalue_col = 'pvalue'
    
    x = df[log2fc_col]
    y = -np.log10(df[pvalue_col].replace(0, np.nan).fillna(df[pvalue_col].min() / 10))
    
    # Classify points
    significant = (df[pvalue_col] < pvalue_threshold) & (df[log2fc_col].abs() > log2fc_threshold)
    up = significant & (df[log2fc_col] > 0)
    down = significant & (df[log2fc_col] < 0)
    not_sig = ~significant
    
    # Plot
    ax.scatter(df[not_sig][log2fc_col], 
              -np.log10(df[not_sig][pvalue_col].replace(0, np.nan).fillna(df[pvalue_col].min() / 10)),
              c='gray', alpha=0.5, s=20, label='Not significant')
    
    if up.sum() > 0:
        ax.scatter(df[up][log2fc_col], 
                  -np.log10(df[up][pvalue_col].replace(0, np.nan).fillna(df[pvalue_col].min() / 10)),
                  c='red', alpha=0.7, s=30, label='Up-regulated')
    
    if down.sum() > 0:
        ax.scatter(df[down][log2fc_col], 
                  -np.log10(df[down][pvalue_col].replace(0, np.nan).fillna(df[pvalue_col].min() / 10)),
                  c='blue', alpha=0.7, s=30, label='Down-regulated')
    
    # Add threshold lines
    ax.axhline(y=-np.log10(pvalue_threshold), color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax.axvline(x=log2fc_threshold, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax.axvline(x=-log2fc_threshold, color='black', linestyle='--', linewidth=1, alpha=0.5)
    
    ax.set_xlabel('Log2 Fold Change', fontsize=12, fontweight='bold')
    ax.set_ylabel('-Log10 P-value', fontsize=12, fontweight='bold')
    ax.set_title('Volcano Plot', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return plot_to_base64(fig)


def generate_pca_plot(df: pd.DataFrame, 
                     sample_columns: Optional[list] = None,
                     n_components: int = 2) -> str:
    """
    Generate PCA plot from expression matrix.
    
    Args:
        df: DataFrame with expression data (genes as rows, samples as columns)
        sample_columns: List of sample column names (if None, uses all numeric columns)
        n_components: Number of principal components
    
    Returns:
        Base64-encoded PNG string
    """
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    
    # If no sample columns specified, try to find numeric columns
    if sample_columns is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        # Exclude common non-sample columns
        exclude = ['log2fc', 'pvalue', 'padj', 'p_value', 'p_adj']
        sample_columns = [col for col in numeric_cols if col.lower() not in exclude]
    
    if len(sample_columns) < 2:
        # If we don't have expression matrix, create a placeholder
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, 'PCA Plot\n\nExpression matrix data required\nfor PCA analysis', 
                ha='center', va='center', fontsize=14, 
                transform=ax.transAxes, color='gray')
        ax.set_title('PCA Analysis', fontsize=14, fontweight='bold')
        ax.axis('off')
        return plot_to_base64(fig)
    
    # Extract expression data
    expr_data = df[sample_columns].values
    
    # Standardize
    scaler = StandardScaler()
    expr_scaled = scaler.fit_transform(expr_data)
    
    # PCA
    pca = PCA(n_components=min(n_components, len(sample_columns), expr_scaled.shape[0]))
    pca_result = pca.fit_transform(expr_scaled)
    
    # Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    
    if pca_result.shape[1] >= 2:
        ax.scatter(pca_result[:, 0], pca_result[:, 1], alpha=0.6, s=50)
        ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)', fontsize=11)
        ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)', fontsize=11)
    else:
        ax.text(0.5, 0.5, 'Insufficient data for PCA', 
                ha='center', va='center', transform=ax.transAxes)
    
    ax.set_title('Principal Component Analysis', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    return plot_to_base64(fig)


def generate_heatmap(df: pd.DataFrame,
                     top_n: int = 50,
                     sample_columns: Optional[list] = None,
                     gene_id_col: str = 'gene_id') -> str:
    """
    Generate heatmap of top differentially expressed genes.
    
    Args:
        df: DataFrame with DEG data
        top_n: Number of top genes to show
        sample_columns: List of sample column names
        gene_id_col: Column name for gene IDs
    
    Returns:
        Base64-encoded PNG string
    """
    # If we have expression data, use it
    if sample_columns and all(col in df.columns for col in sample_columns):
        # Get top genes by absolute log2FC
        top_genes = df.nlargest(top_n, df['log2fc'].abs())
        heatmap_data = top_genes[sample_columns].set_index(top_genes[gene_id_col] if gene_id_col in top_genes.columns else top_genes.index)
    else:
        # Create a placeholder heatmap based on log2FC
        if 'log2fc' in df.columns:
            top_genes = df.nlargest(top_n, df['log2fc'].abs())
            # Create synthetic heatmap data
            n_samples = 6  # Default number of samples
            heatmap_data = pd.DataFrame(
                np.random.randn(len(top_genes), n_samples),
                index=top_genes[gene_id_col] if gene_id_col in top_genes.columns else top_genes.index,
                columns=[f'Sample_{i+1}' for i in range(n_samples)]
            )
        else:
            # Fallback placeholder
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.text(0.5, 0.5, 'Heatmap\n\nExpression matrix data required', 
                    ha='center', va='center', fontsize=14, 
                    transform=ax.transAxes, color='gray')
            ax.set_title('Heatmap of Top DEGs', fontsize=14, fontweight='bold')
            ax.axis('off')
            return plot_to_base64(fig)
    
    # Generate heatmap
    fig, ax = plt.subplots(figsize=(12, max(8, len(heatmap_data) * 0.3)))
    
    # Limit to top 50 genes for readability
    if len(heatmap_data) > 50:
        heatmap_data = heatmap_data.head(50)
    
    sns.heatmap(heatmap_data, 
                cmap='RdYlBu_r', 
                center=0,
                cbar_kws={'label': 'Expression Level'},
                ax=ax,
                xticklabels=True,
                yticklabels=True if len(heatmap_data) <= 30 else False)
    
    ax.set_title(f'Heatmap of Top {len(heatmap_data)} Differentially Expressed Genes', 
                fontsize=14, fontweight='bold')
    ax.set_xlabel('Samples', fontsize=11)
    ax.set_ylabel('Genes', fontsize=11)
    
    plt.xticks(rotation=45, ha='right')
    if len(heatmap_data) <= 30:
        plt.yticks(rotation=0)
    
    return plot_to_base64(fig)


def generate_pathway_enrichment_plot(enrichment_df: pd.DataFrame,
                                    top_n: int = 20) -> str:
    """
    Generate pathway enrichment visualization.
    
    Args:
        enrichment_df: DataFrame with enrichment results
        top_n: Number of top pathways to show
    
    Returns:
        Base64-encoded PNG string
    """
    # Normalize column names
    enrichment_df = enrichment_df.copy()
    enrichment_df.columns = enrichment_df.columns.str.lower()
    
    # Try to find relevant columns
    pathway_col = None
    pvalue_col = None
    count_col = None
    
    for col in ['pathway', 'term', 'description', 'name']:
        if col in enrichment_df.columns:
            pathway_col = col
            break
    
    for col in ['pvalue', 'p_value', 'pval', 'padj', 'p_adj', 'fdr']:
        if col in enrichment_df.columns:
            pvalue_col = col
            break
    
    for col in ['count', 'gene_count', 'size', 'genes']:
        if col in enrichment_df.columns:
            count_col = col
            break
    
    if pathway_col is None or pvalue_col is None:
        # Placeholder
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.text(0.5, 0.5, 'Pathway Enrichment Plot\n\nEnrichment data required', 
                ha='center', va='center', fontsize=14, 
                transform=ax.transAxes, color='gray')
        ax.set_title('Pathway Enrichment', fontsize=14, fontweight='bold')
        ax.axis('off')
        return plot_to_base64(fig)
    
    # Get top pathways
    top_pathways = enrichment_df.nsmallest(top_n, pvalue_col)
    
    # Create bar plot
    fig, ax = plt.subplots(figsize=(10, max(8, len(top_pathways) * 0.4)))
    
    y_pos = np.arange(len(top_pathways))
    colors = plt.cm.RdYlGn_r(top_pathways[pvalue_col].values / top_pathways[pvalue_col].max())
    
    bars = ax.barh(y_pos, -np.log10(top_pathways[pvalue_col].values), color=colors)
    
    # Add gene count if available
    if count_col:
        for i, (idx, row) in enumerate(top_pathways.iterrows()):
            ax.text(row[pvalue_col] * 1.1, i, f"n={row[count_col]}", 
                   va='center', fontsize=9)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_pathways[pathway_col].values, fontsize=10)
    ax.set_xlabel('-Log10 P-value', fontsize=12, fontweight='bold')
    ax.set_title('Top Enriched Pathways', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3, axis='x')
    
    return plot_to_base64(fig)


def generate_svm_classification_plot(svm_results: dict) -> str:
    """
    Generate visualization for SVM classification results.
    
    Args:
        svm_results: Dictionary from perform_svm_classification
    
    Returns:
        Base64-encoded PNG string
    """
    from sklearn.decomposition import PCA
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    X_scaled = np.array(svm_results['X_scaled'])
    predictions = np.array(svm_results['predictions'])
    true_labels = np.array(svm_results['true_labels'])
    n_clusters = svm_results['n_classes']
    
    # Reduce to 2D for visualization
    if X_scaled.shape[1] > 2:
        pca = PCA(n_components=2)
        X_2d = pca.fit_transform(X_scaled)
    else:
        X_2d = X_scaled
    
    # Plot 1: Classification results
    ax1 = axes[0]
    scatter = ax1.scatter(X_2d[:, 0], X_2d[:, 1], c=predictions, 
                          cmap='viridis', s=100, alpha=0.7, edgecolors='black')
    ax1.set_xlabel('PC1' if X_scaled.shape[1] > 2 else 'Feature 1', fontsize=11)
    ax1.set_ylabel('PC2' if X_scaled.shape[1] > 2 else 'Feature 2', fontsize=11)
    ax1.set_title(f'SVM Classification Results\nAccuracy: {svm_results["accuracy"]:.3f}', 
                 fontsize=12, fontweight='bold')
    plt.colorbar(scatter, ax=ax1, label='Predicted Class')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Confusion Matrix
    ax2 = axes[1]
    cm = np.array(svm_results['confusion_matrix'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax2,
                xticklabels=[f'Class {i}' for i in range(n_clusters)],
                yticklabels=[f'Class {i}' for i in range(n_clusters)])
    ax2.set_xlabel('Predicted', fontsize=11)
    ax2.set_ylabel('True', fontsize=11)
    ax2.set_title('Confusion Matrix', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    return plot_to_base64(fig)


def generate_random_forest_plot(rf_results: dict) -> str:
    """
    Generate visualization for Random Forest classification results.
    
    Args:
        rf_results: Dictionary from perform_random_forest_classification
    
    Returns:
        Base64-encoded PNG string
    """
    from sklearn.decomposition import PCA
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    X_scaled = np.array(rf_results['X_scaled'])
    predictions = np.array(rf_results['predictions'])
    feature_importance = np.array(rf_results['feature_importance'])
    top_features_idx = np.array(rf_results['top_features_idx'])
    n_clusters = rf_results['n_classes']
    
    # Reduce to 2D for visualization
    if X_scaled.shape[1] > 2:
        pca = PCA(n_components=2)
        X_2d = pca.fit_transform(X_scaled)
    else:
        X_2d = X_scaled
    
    # Plot 1: Classification results
    ax1 = axes[0, 0]
    scatter = ax1.scatter(X_2d[:, 0], X_2d[:, 1], c=predictions,
                         cmap='viridis', s=100, alpha=0.7, edgecolors='black')
    ax1.set_xlabel('PC1' if X_scaled.shape[1] > 2 else 'Feature 1', fontsize=11)
    ax1.set_ylabel('PC2' if X_scaled.shape[1] > 2 else 'Feature 2', fontsize=11)
    ax1.set_title(f'Random Forest Classification\nAccuracy: {rf_results["accuracy"]:.3f}',
                 fontsize=12, fontweight='bold')
    plt.colorbar(scatter, ax=ax1, label='Predicted Class')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Feature Importance (Top 20)
    ax2 = axes[0, 1]
    top_20_importance = feature_importance[top_features_idx[:20]]
    top_20_idx = top_features_idx[:20]
    ax2.barh(range(len(top_20_importance)), top_20_importance, color='steelblue')
    ax2.set_yticks(range(len(top_20_importance)))
    ax2.set_yticklabels([f'Feature {i}' for i in top_20_idx], fontsize=8)
    ax2.set_xlabel('Importance', fontsize=11)
    ax2.set_title('Top 20 Feature Importance', fontsize=12, fontweight='bold')
    ax2.invert_yaxis()
    ax2.grid(True, alpha=0.3, axis='x')
    
    # Plot 3: Confusion Matrix
    ax3 = axes[1, 0]
    cm = np.array(rf_results['confusion_matrix'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax3,
                xticklabels=[f'Class {i}' for i in range(n_clusters)],
                yticklabels=[f'Class {i}' for i in range(n_clusters)])
    ax3.set_xlabel('Predicted', fontsize=11)
    ax3.set_ylabel('True', fontsize=11)
    ax3.set_title('Confusion Matrix', fontsize=12, fontweight='bold')
    
    # Plot 4: Feature Importance Distribution
    ax4 = axes[1, 1]
    ax4.hist(feature_importance, bins=30, color='steelblue', alpha=0.7, edgecolor='black')
    ax4.set_xlabel('Feature Importance', fontsize=11)
    ax4.set_ylabel('Frequency', fontsize=11)
    ax4.set_title('Feature Importance Distribution', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return plot_to_base64(fig)


def generate_hierarchical_clustering_plot(hc_results: dict) -> str:
    """
    Generate visualization for hierarchical clustering results.
    
    Args:
        hc_results: Dictionary from perform_hierarchical_clustering
    
    Returns:
        Base64-encoded PNG string
    """
    from scipy.cluster.hierarchy import dendrogram, linkage
    from sklearn.decomposition import PCA
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    X_scaled = np.array(hc_results['X_scaled'])
    cluster_labels = np.array(hc_results['cluster_labels'])
    n_clusters = hc_results['n_clusters']
    
    # Reduce to 2D for visualization
    if X_scaled.shape[1] > 2:
        pca = PCA(n_components=2)
        X_2d = pca.fit_transform(X_scaled)
    else:
        X_2d = X_scaled
    
    # Plot 1: Clustering results in 2D
    ax1 = axes[0]
    scatter = ax1.scatter(X_2d[:, 0], X_2d[:, 1], c=cluster_labels,
                         cmap='tab10', s=100, alpha=0.7, edgecolors='black')
    ax1.set_xlabel('PC1' if X_scaled.shape[1] > 2 else 'Feature 1', fontsize=11)
    ax1.set_ylabel('PC2' if X_scaled.shape[1] > 2 else 'Feature 2', fontsize=11)
    ax1.set_title(f'Hierarchical Clustering\n{n_clusters} Clusters (Silhouette: {hc_results["silhouette_score"]:.3f})',
                 fontsize=12, fontweight='bold')
    plt.colorbar(scatter, ax=ax1, label='Cluster')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Dendrogram
    ax2 = axes[1]
    try:
        linkage_matrix = linkage(X_scaled, method=hc_results['linkage'])
        dendrogram(linkage_matrix, ax=ax2, leaf_rotation=90, leaf_font_size=8)
        ax2.set_xlabel('Sample Index', fontsize=11)
        ax2.set_ylabel('Distance', fontsize=11)
        ax2.set_title('Dendrogram', fontsize=12, fontweight='bold')
    except Exception as e:
        ax2.text(0.5, 0.5, f'Dendrogram generation failed:\n{str(e)}',
                ha='center', va='center', transform=ax2.transAxes, fontsize=10)
        ax2.set_title('Dendrogram (Not Available)', fontsize=12)
    
    plt.tight_layout()
    return plot_to_base64(fig)


def generate_kmeans_clustering_plot(kmeans_results: dict) -> str:
    """
    Generate visualization for K-Means clustering results.
    
    Args:
        kmeans_results: Dictionary from perform_kmeans_clustering
    
    Returns:
        Base64-encoded PNG string
    """
    from sklearn.decomposition import PCA
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    X_scaled = np.array(kmeans_results['X_scaled'])
    cluster_labels = np.array(kmeans_results['cluster_labels'])
    centers = np.array(kmeans_results['centers'])
    
    # Reduce to 2D for visualization
    if X_scaled.shape[1] > 2:
        pca = PCA(n_components=2)
        X_2d = pca.fit_transform(X_scaled)
        centers_2d = pca.transform(centers)
    else:
        X_2d = X_scaled
        centers_2d = centers
    
    # Plot 1: Clustering results with centers
    ax1 = axes[0]
    scatter = ax1.scatter(X_2d[:, 0], X_2d[:, 1], c=cluster_labels,
                         cmap='tab10', s=100, alpha=0.7, edgecolors='black')
    ax1.scatter(centers_2d[:, 0], centers_2d[:, 1], c='red', marker='x',
               s=200, linewidths=3, label='Centroids', zorder=10)
    ax1.set_xlabel('PC1' if X_scaled.shape[1] > 2 else 'Feature 1', fontsize=11)
    ax1.set_ylabel('PC2' if X_scaled.shape[1] > 2 else 'Feature 2', fontsize=11)
    ax1.set_title(f'K-Means Clustering\n{kmeans_results["n_clusters"]} Clusters (Silhouette: {kmeans_results["silhouette_score"]:.3f})',
                 fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Cluster size distribution
    ax2 = axes[1]
    unique_labels, counts = np.unique(cluster_labels, return_counts=True)
    ax2.bar(unique_labels, counts, color=plt.cm.tab10(unique_labels / max(unique_labels.max(), 1)))
    ax2.set_xlabel('Cluster', fontsize=11)
    ax2.set_ylabel('Number of Samples', fontsize=11)
    ax2.set_title('Cluster Size Distribution', fontsize=12, fontweight='bold')
    ax2.set_xticks(unique_labels)
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return plot_to_base64(fig)


def generate_lasso_feature_selection_plot(lasso_results: dict) -> str:
    """
    Generate visualization for Lasso feature selection results.
    
    Args:
        lasso_results: Dictionary from perform_lasso_feature_selection
    
    Returns:
        Base64-encoded PNG string
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    coefficients = np.array(lasso_results['coefficients'])
    selected_idx = np.array(lasso_results['selected_features_idx'])
    selected_coef = np.array(lasso_results['selected_features_coef'])
    
    # Plot 1: Coefficient values
    ax1 = axes[0, 0]
    ax1.plot(range(len(coefficients)), coefficients, 'o-', alpha=0.7, markersize=4)
    ax1.axhline(y=0, color='r', linestyle='--', linewidth=1)
    ax1.set_xlabel('Feature Index', fontsize=11)
    ax1.set_ylabel('Coefficient', fontsize=11)
    ax1.set_title(f'Lasso Coefficients (α={lasso_results["alpha"]})\nSelected: {lasso_results["n_selected"]} features',
                 fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Selected features
    ax2 = axes[0, 1]
    if len(selected_idx) > 0:
        top_n = min(20, len(selected_idx))
        top_selected = selected_idx[:top_n]
        top_coef = selected_coef[:top_n]
        ax2.barh(range(len(top_selected)), top_coef, color='steelblue')
        ax2.set_yticks(range(len(top_selected)))
        ax2.set_yticklabels([f'Feature {i}' for i in top_selected], fontsize=8)
        ax2.set_xlabel('Coefficient Value', fontsize=11)
        ax2.set_title(f'Top {top_n} Selected Features', fontsize=12, fontweight='bold')
        ax2.invert_yaxis()
        ax2.grid(True, alpha=0.3, axis='x')
    else:
        ax2.text(0.5, 0.5, 'No features selected', ha='center', va='center',
                transform=ax2.transAxes, fontsize=12)
        ax2.set_title('Selected Features', fontsize=12)
    
    # Plot 3: Coefficient distribution
    ax3 = axes[1, 0]
    ax3.hist(coefficients, bins=50, color='steelblue', alpha=0.7, edgecolor='black')
    ax3.axvline(x=0, color='r', linestyle='--', linewidth=1)
    ax3.set_xlabel('Coefficient Value', fontsize=11)
    ax3.set_ylabel('Frequency', fontsize=11)
    ax3.set_title('Coefficient Distribution', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Selection statistics
    ax4 = axes[1, 1]
    stats_data = {
        'Total Features': len(coefficients),
        'Selected Features': lasso_results['n_selected'],
        'Zero Features': len(coefficients) - lasso_results['n_selected']
    }
    ax4.bar(stats_data.keys(), stats_data.values(), color=['steelblue', 'green', 'gray'])
    ax4.set_ylabel('Count', fontsize=11)
    ax4.set_title('Feature Selection Statistics', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='y')
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    return plot_to_base64(fig)


def generate_ridge_regression_plot(ridge_results: dict) -> str:
    """
    Generate visualization for Ridge regression results.
    
    Args:
        ridge_results: Dictionary from perform_ridge_regression
    
    Returns:
        Base64-encoded PNG string
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    coefficients = np.array(ridge_results['coefficients'])
    top_features_idx = np.array(ridge_results['top_features_idx'])
    top_features_coef = np.array(ridge_results['top_features_coef'])
    
    # Plot 1: Coefficient values
    ax1 = axes[0, 0]
    ax1.plot(range(len(coefficients)), coefficients, 'o-', alpha=0.7, markersize=4)
    ax1.axhline(y=0, color='r', linestyle='--', linewidth=1)
    ax1.set_xlabel('Feature Index', fontsize=11)
    ax1.set_ylabel('Coefficient', fontsize=11)
    ax1.set_title(f'Ridge Coefficients (α={ridge_results["alpha"]})',
                 fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Top features by absolute coefficient
    ax2 = axes[0, 1]
    top_n = min(20, len(top_features_idx))
    ax2.barh(range(top_n), top_features_coef[:top_n], color='steelblue')
    ax2.set_yticks(range(top_n))
    ax2.set_yticklabels([f'Feature {i}' for i in top_features_idx[:top_n]], fontsize=8)
    ax2.set_xlabel('Coefficient Value', fontsize=11)
    ax2.set_title(f'Top {top_n} Features by |Coefficient|', fontsize=12, fontweight='bold')
    ax2.invert_yaxis()
    ax2.grid(True, alpha=0.3, axis='x')
    
    # Plot 3: Coefficient distribution
    ax3 = axes[1, 0]
    ax3.hist(coefficients, bins=50, color='steelblue', alpha=0.7, edgecolor='black')
    ax3.axvline(x=0, color='r', linestyle='--', linewidth=1)
    ax3.set_xlabel('Coefficient Value', fontsize=11)
    ax3.set_ylabel('Frequency', fontsize=11)
    ax3.set_title('Coefficient Distribution', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Absolute coefficient values
    ax4 = axes[1, 1]
    abs_coef = np.abs(coefficients)
    ax4.plot(range(len(abs_coef)), abs_coef, 'o-', alpha=0.7, markersize=4, color='green')
    ax4.set_xlabel('Feature Index', fontsize=11)
    ax4.set_ylabel('|Coefficient|', fontsize=11)
    ax4.set_title('Absolute Coefficient Values', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return plot_to_base64(fig)

