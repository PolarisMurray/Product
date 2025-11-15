from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel


# ============================================================================
# Common Models
# ============================================================================

class Plot(BaseModel):
    """Represents a generated plot visualization."""
    name: str
    type: str  # e.g. "volcano", "pca", "heatmap", "pathway"
    image_base64: str  # base64-encoded PNG
    description: Optional[str] = None


class NarrativeSection(BaseModel):
    """Represents a section of narrative text (e.g., Results, Discussion)."""
    title: str
    content: str


# ============================================================================
# Research Mode Models
# ============================================================================

class ResearchAnalyzeRequest(BaseModel):
    """Request model for research mode analysis.
    
    Note: Actual DEG/enrichment data will be uploaded as files,
    not included in this JSON model.
    """
    project_name: Optional[str] = None
    species: Optional[str] = None
    contrast_label: Optional[str] = None


class ResearchAnalyzeResponse(BaseModel):
    """Response model for research mode analysis."""
    project_name: Optional[str] = None
    plots: List[Plot]
    narrative: Dict[str, NarrativeSection]  # keys like "results", "discussion"
    summary_stats: Dict[str, Any]  # e.g. {"num_deg": 123, "up": 60, "down": 63}


# ============================================================================
# Personal Genomics Models
# ============================================================================

class SNPInput(BaseModel):
    """Input model for a single SNP genotype."""
    rsid: str
    genotype: str  # e.g. "AA", "AG", "GG"


class LifestyleInput(BaseModel):
    """Input model for lifestyle factors."""
    caffeine_intake: Optional[str] = None  # e.g. "low", "moderate", "high"
    exercise_frequency: Optional[str] = None
    sleep_duration_hours: Optional[float] = None
    diet_pattern: Optional[str] = None


class PersonalInsightCard(BaseModel):
    """Represents a personalized insight card for a specific domain."""
    domain: str  # e.g. "Caffeine metabolism"
    summary: str
    score: float  # 0–1 for internal scoring
    percentile: Optional[float] = None  # 0–1 percentile compared to peers
    recommendations: List[str]


class PeerComparison(BaseModel):
    """Represents a single metric comparison to peers."""
    metric: str
    value: float
    percentile: float
    label: str


class GeneticBioCard(BaseModel):
    """Represents a shareable genetic bio card."""
    title: str
    subtitle: str
    badges: List[str]
    highlights: List[str]


class PersonalAnalyzeRequest(BaseModel):
    """Request model for personal genomics analysis."""
    snps: List[SNPInput]
    lifestyle: Optional[LifestyleInput] = None


class PersonalAnalyzeResponse(BaseModel):
    """Response model for personal genomics analysis."""
    cards: List[PersonalInsightCard]
    peer_comparison: List[PeerComparison]
    genetic_card: GeneticBioCard


# ============================================================================
# Report Export Models
# ============================================================================

class ReportExportRequest(BaseModel):
    """Request model for report export."""
    mode: Literal["research", "personal"]
    format: Literal["pdf", "docx"]
    payload: Dict[str, Any]  # the full JSON returned by the corresponding analyze endpoint


class ReportExportResponse(BaseModel):
    """Response model for report export."""
    download_url: str  # URL for the generated report file

