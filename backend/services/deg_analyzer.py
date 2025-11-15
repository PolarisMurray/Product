"""
DEG (Differential Expression Genes) data analyzer.

This module provides functions to parse and analyze DEG files.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple
import io


def parse_deg_file(file_content: bytes, filename: str) -> pd.DataFrame:
    """
    Parse DEG file (CSV, TSV, or XLSX) into a pandas DataFrame.
    
    Args:
        file_content: File content as bytes
        filename: Original filename (used to determine format)
    
    Returns:
        DataFrame with DEG data
    """
    # Determine file format
    if filename.endswith('.xlsx'):
        df = pd.read_excel(io.BytesIO(file_content))
    elif filename.endswith('.tsv'):
        df = pd.read_csv(io.BytesIO(file_content), sep='\t')
    else:
        # Default to CSV
        df = pd.read_csv(io.BytesIO(file_content))
    
    return df


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names to handle various naming conventions.
    
    Common variations:
    - log2FC, log2_FC, logFC, log_fold_change
    - pvalue, p_value, pval
    - padj, p_adj, adjusted_pvalue, FDR
    - gene_id, gene, Gene, gene_name
    """
    df = df.copy()
    df.columns = df.columns.str.lower().str.strip()
    
    # Normalize common column names
    column_mapping = {
        'log2fc': 'log2fc',
        'log2_fc': 'log2fc',
        'logfc': 'log2fc',
        'log_fold_change': 'log2fc',
        'fold_change': 'log2fc',
        'fc': 'log2fc',
        
        'pvalue': 'pvalue',
        'p_value': 'pvalue',
        'pval': 'pvalue',
        'p': 'pvalue',
        
        'padj': 'padj',
        'p_adj': 'padj',
        'adjusted_pvalue': 'padj',
        'fdr': 'padj',
        'adj_pval': 'padj',
        
        'gene_id': 'gene_id',
        'gene': 'gene_id',
        'gene_name': 'gene_id',
        'geneid': 'gene_id',
    }
    
    for old_name, new_name in column_mapping.items():
        if old_name in df.columns and new_name not in df.columns:
            df.rename(columns={old_name: new_name}, inplace=True)
    
    return df


def analyze_deg_data(df: pd.DataFrame, 
                     pvalue_threshold: float = 0.05,
                     log2fc_threshold: float = 1.0,
                     padj_threshold: Optional[float] = None) -> Dict[str, Any]:
    """
    Analyze DEG data and calculate statistics.
    
    Args:
        df: DataFrame with DEG data
        pvalue_threshold: P-value threshold for significance
        log2fc_threshold: Log2 fold change threshold
        padj_threshold: Adjusted p-value threshold (if None, uses pvalue_threshold)
    
    Returns:
        Dictionary with analysis results
    """
    if padj_threshold is None:
        padj_threshold = pvalue_threshold
    
    # Ensure required columns exist
    required_cols = ['log2fc']
    p_col = 'padj' if 'padj' in df.columns else 'pvalue'
    
    if p_col not in df.columns:
        raise ValueError(f"Required column '{p_col}' not found in data")
    if 'log2fc' not in df.columns:
        raise ValueError("Required column 'log2fc' not found in data")
    
    # Calculate total genes
    total_genes = len(df)
    
    # Filter significant DEGs
    # Use padj if available, otherwise use pvalue
    if 'padj' in df.columns:
        significant = df['padj'] < padj_threshold
    else:
        significant = df['pvalue'] < pvalue_threshold
    
    degs = df[significant & (df['log2fc'].abs() > log2fc_threshold)]
    num_deg = len(degs)
    
    # Classify up and down regulated
    up_regulated = degs[degs['log2fc'] > 0]
    down_regulated = degs[degs['log2fc'] < 0]
    
    num_up = len(up_regulated)
    num_down = len(down_regulated)
    
    # Calculate percentages
    deg_percentage = (num_deg / total_genes * 100) if total_genes > 0 else 0
    up_percentage = (num_up / num_deg * 100) if num_deg > 0 else 0
    down_percentage = (num_down / num_deg * 100) if num_deg > 0 else 0
    
    # Get top DEGs
    top_up = up_regulated.nlargest(10, 'log2fc') if len(up_regulated) > 0 else pd.DataFrame()
    top_down = down_regulated.nsmallest(10, 'log2fc') if len(down_regulated) > 0 else pd.DataFrame()
    
    # Calculate statistics
    avg_log2fc = degs['log2fc'].mean() if num_deg > 0 else 0
    median_log2fc = degs['log2fc'].median() if num_deg > 0 else 0
    
    return {
        'total_genes': total_genes,
        'num_deg': num_deg,
        'up': num_up,
        'down': num_down,
        'deg_percentage': deg_percentage,
        'up_percentage': up_percentage,
        'down_percentage': down_percentage,
        'avg_log2fc': float(avg_log2fc),
        'median_log2fc': float(median_log2fc),
        'top_up_genes': top_up.to_dict('records') if len(top_up) > 0 else [],
        'top_down_genes': top_down.to_dict('records') if len(top_down) > 0 else [],
        'degs_dataframe': degs,  # For plotting
        'full_dataframe': df,  # For plotting
    }


def parse_enrichment_file(file_content: bytes, filename: str) -> pd.DataFrame:
    """
    Parse enrichment results file.
    
    Args:
        file_content: File content as bytes
        filename: Original filename
    
    Returns:
        DataFrame with enrichment data
    """
    if filename.endswith('.xlsx'):
        df = pd.read_excel(io.BytesIO(file_content))
    elif filename.endswith('.tsv'):
        df = pd.read_csv(io.BytesIO(file_content), sep='\t')
    else:
        df = pd.read_csv(io.BytesIO(file_content))
    
    return df

