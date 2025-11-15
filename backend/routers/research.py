from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from typing import Optional
import json

from models.schemas import (
    ResearchAnalyzeRequest,
    ResearchAnalyzeResponse,
    Plot,
    NarrativeSection,
)

from services.deg_analyzer import (
    parse_deg_file,
    normalize_column_names,
    analyze_deg_data,
    parse_enrichment_file,
)

from services.plot_generator import (
    generate_volcano_plot,
    generate_pca_plot,
    generate_heatmap,
    generate_pathway_enrichment_plot,
    generate_svm_classification_plot,
    generate_random_forest_plot,
    generate_hierarchical_clustering_plot,
    generate_kmeans_clustering_plot,
    generate_lasso_feature_selection_plot,
    generate_ridge_regression_plot,
)

from services.ml_analyzer import (
    perform_svm_classification,
    perform_random_forest_classification,
    perform_hierarchical_clustering,
    perform_kmeans_clustering,
    perform_lasso_feature_selection,
    perform_ridge_regression,
)

from services.research_service import generate_scientific_narrative

router = APIRouter(prefix="/analyze", tags=["research"])




def parse_metadata(meta: str = Form(..., description="JSON string of ResearchAnalyzeRequest metadata")) -> ResearchAnalyzeRequest:
    """Dependency function to parse and validate metadata from form data."""
    try:
        meta_dict = json.loads(meta)
        return ResearchAnalyzeRequest(**meta_dict)
    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=f"Invalid metadata JSON: {str(e)}")


@router.post("/research", response_model=ResearchAnalyzeResponse)
async def analyze_research(
    deg_file: UploadFile = File(..., description="DEG (Differential Expression Genes) data file"),
    enrichment_file: Optional[UploadFile] = File(None, description="Optional enrichment results file"),
    request_meta: ResearchAnalyzeRequest = Depends(parse_metadata),
):
    """
    Analyze research data (DEG and optional enrichment files).
    
    This endpoint accepts:
    - DEG file (required): CSV/TSV file with differential expression data
    - Enrichment file (optional): CSV/TSV file with enrichment results
    - Metadata: JSON string containing project_name, species, contrast_label
    
    Returns analysis results with plots, narrative, and summary statistics.
    """
    
    # Read files in memory
    deg_content = await deg_file.read()
    deg_filename = deg_file.filename
    
    enrichment_content = None
    enrichment_filename = None
    enrichment_df = None
    if enrichment_file:
        enrichment_content = await enrichment_file.read()
        enrichment_filename = enrichment_file.filename
    
    try:
        # Parse and analyze DEG file
        deg_df = parse_deg_file(deg_content, deg_filename)
        deg_df = normalize_column_names(deg_df)
        
        # Analyze DEG data
        analysis_results = analyze_deg_data(deg_df)
        
        # Parse enrichment file if provided
        if enrichment_file and enrichment_content:
            try:
                enrichment_df = parse_enrichment_file(enrichment_content, enrichment_filename)
            except Exception as e:
                # If enrichment parsing fails, continue without it
                print(f"Warning: Failed to parse enrichment file: {e}")
                enrichment_df = None
        
        # Generate plots using real data
        plots = []
        
        # Volcano plot
        try:
            volcano_img = generate_volcano_plot(
                analysis_results['full_dataframe'],
                pvalue_col='padj' if 'padj' in analysis_results['full_dataframe'].columns else 'pvalue',
                log2fc_col='log2fc'
            )
            plots.append(Plot(
                name="Volcano Plot",
                type="volcano",
                image_base64=volcano_img,
                description="Volcano plot showing differential expression with significance thresholds"
            ))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate volcano plot: {str(e)}")
        
        # PCA plot (keep existing PCA as dimensionality reduction method)
        try:
            pca_img = generate_pca_plot(analysis_results['full_dataframe'])
            plots.append(Plot(
                name="PCA Analysis",
                type="pca",
                image_base64=pca_img,
                description="Principal Component Analysis for dimensionality reduction"
            ))
        except Exception as e:
            # PCA might fail if no expression matrix, create placeholder
            print(f"Warning: PCA plot generation failed: {e}")
        
        # Heatmap
        try:
            heatmap_img = generate_heatmap(
                analysis_results['full_dataframe'],
                top_n=50
            )
            plots.append(Plot(
                name="Heatmap",
                type="heatmap",
                image_base64=heatmap_img,
                description="Heatmap of top differentially expressed genes"
            ))
        except Exception as e:
            print(f"Warning: Heatmap generation failed: {e}")
        
        # Pathway enrichment plot (if enrichment file provided)
        if enrichment_df is not None:
            try:
                pathway_img = generate_pathway_enrichment_plot(enrichment_df, top_n=20)
                plots.append(Plot(
                    name="Pathway Enrichment",
                    type="pathway",
                    image_base64=pathway_img,
                    description="Enrichment analysis of significant pathways"
                ))
            except Exception as e:
                print(f"Warning: Pathway enrichment plot generation failed: {e}")
        
        # Machine Learning Analysis - Sample Classification
        try:
            # SVM Classification
            svm_results = perform_svm_classification(analysis_results['full_dataframe'], n_classes=2)
            svm_img = generate_svm_classification_plot(svm_results)
            plots.append(Plot(
                name="SVM Classification",
                type="svm_classification",
                image_base64=svm_img,
                description=f"SVM classification results (Accuracy: {svm_results['accuracy']:.3f})"
            ))
        except Exception as e:
            print(f"Warning: SVM classification failed: {e}")
        
        try:
            # Random Forest Classification
            rf_results = perform_random_forest_classification(analysis_results['full_dataframe'], n_classes=2)
            rf_img = generate_random_forest_plot(rf_results)
            plots.append(Plot(
                name="Random Forest Classification",
                type="random_forest",
                image_base64=rf_img,
                description=f"Random Forest classification results (Accuracy: {rf_results['accuracy']:.3f})"
            ))
        except Exception as e:
            print(f"Warning: Random Forest classification failed: {e}")
        
        # Clustering Analysis
        try:
            # Hierarchical Clustering
            hc_results = perform_hierarchical_clustering(analysis_results['full_dataframe'], n_clusters=3)
            hc_img = generate_hierarchical_clustering_plot(hc_results)
            plots.append(Plot(
                name="Hierarchical Clustering",
                type="hierarchical_clustering",
                image_base64=hc_img,
                description=f"Hierarchical clustering results ({hc_results['n_clusters']} clusters, Silhouette: {hc_results['silhouette_score']:.3f})"
            ))
        except Exception as e:
            print(f"Warning: Hierarchical clustering failed: {e}")
        
        try:
            # K-Means Clustering
            kmeans_results = perform_kmeans_clustering(analysis_results['full_dataframe'], n_clusters=3)
            kmeans_img = generate_kmeans_clustering_plot(kmeans_results)
            plots.append(Plot(
                name="K-Means Clustering",
                type="kmeans_clustering",
                image_base64=kmeans_img,
                description=f"K-Means clustering results ({kmeans_results['n_clusters']} clusters, Silhouette: {kmeans_results['silhouette_score']:.3f})"
            ))
        except Exception as e:
            print(f"Warning: K-Means clustering failed: {e}")
        
        # Feature Selection / Dimensionality Reduction
        try:
            # Lasso Feature Selection
            lasso_results = perform_lasso_feature_selection(analysis_results['full_dataframe'], alpha=0.1)
            lasso_img = generate_lasso_feature_selection_plot(lasso_results)
            plots.append(Plot(
                name="Lasso Feature Selection",
                type="lasso",
                image_base64=lasso_img,
                description=f"Lasso regression for feature selection (Selected: {lasso_results['n_selected']} features)"
            ))
        except Exception as e:
            print(f"Warning: Lasso feature selection failed: {e}")
        
        try:
            # Ridge Regression
            ridge_results = perform_ridge_regression(analysis_results['full_dataframe'], alpha=1.0)
            ridge_img = generate_ridge_regression_plot(ridge_results)
            plots.append(Plot(
                name="Ridge Regression",
                type="ridge",
                image_base64=ridge_img,
                description="Ridge regression for feature selection and regularization"
            ))
        except Exception as e:
            print(f"Warning: Ridge regression failed: {e}")
        
        # Generate narrative using analysis results
        summary_stats = {
            "num_deg": analysis_results['num_deg'],
            "up": analysis_results['up'],
            "down": analysis_results['down'],
            "total_genes": analysis_results['total_genes'],
            "deg_percentage": round(analysis_results['deg_percentage'], 2),
            "up_percentage": round(analysis_results['up_percentage'], 2),
            "down_percentage": round(analysis_results['down_percentage'], 2),
            "avg_log2fc": round(analysis_results['avg_log2fc'], 3),
            "median_log2fc": round(analysis_results['median_log2fc'], 3),
            "deg_file": deg_filename,
            "enrichment_file": enrichment_filename if enrichment_file else None,
        }
        
        # Generate AI narrative
        narrative = await generate_scientific_narrative(summary_stats)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Data parsing error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")
    
    return ResearchAnalyzeResponse(
        project_name=request_meta.project_name,
        plots=plots,
        narrative=narrative,
        summary_stats=summary_stats
    )

