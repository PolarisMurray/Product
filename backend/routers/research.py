from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from typing import Optional
import json

from models.schemas import (
    ResearchAnalyzeRequest,
    ResearchAnalyzeResponse,
    Plot,
    NarrativeSection,
)

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
    
    # Read files in memory (stub - just verify they're uploaded)
    deg_content = await deg_file.read()
    deg_filename = deg_file.filename
    
    enrichment_content = None
    enrichment_filename = None
    if enrichment_file:
        enrichment_content = await enrichment_file.read()
        enrichment_filename = enrichment_file.filename
    
    # TODO: Implement actual analysis logic
    # For now, return stub data
    
    # Create dummy plots
    plots = [
        Plot(
            name="Volcano Plot",
            type="volcano",
            image_base64="TODO_BASE64_IMAGE",
            description="Volcano plot showing differential expression with significance thresholds"
        ),
        Plot(
            name="PCA Analysis",
            type="pca",
            image_base64="TODO_BASE64_IMAGE",
            description="Principal Component Analysis showing sample clustering"
        ),
        Plot(
            name="Heatmap",
            type="heatmap",
            image_base64="TODO_BASE64_IMAGE",
            description="Heatmap of top differentially expressed genes"
        ),
    ]
    
    # Add pathway plot if enrichment file was provided
    if enrichment_file:
        plots.append(
            Plot(
                name="Pathway Enrichment",
                type="pathway",
                image_base64="TODO_BASE64_IMAGE",
                description="Enrichment analysis of significant pathways"
            )
        )
    
    # Create narrative sections
    narrative = {
        "results": NarrativeSection(
            title="Results",
            content="This is a stub results section. In the full implementation, this will contain AI-generated analysis of the differential expression data, including key findings, significant genes, and biological insights."
        ),
        "discussion": NarrativeSection(
            title="Discussion",
            content="This is a stub discussion section. In the full implementation, this will contain AI-generated interpretation of the results, biological context, implications, and potential follow-up experiments."
        )
    }
    
    # Create summary statistics
    summary_stats = {
        "num_deg": 123,
        "up": 60,
        "down": 63,
        "total_genes": 20000,
        "deg_file": deg_filename,
        "enrichment_file": enrichment_filename if enrichment_file else None,
    }
    
    return ResearchAnalyzeResponse(
        project_name=request_meta.project_name,
        plots=plots,
        narrative=narrative,
        summary_stats=summary_stats
    )

