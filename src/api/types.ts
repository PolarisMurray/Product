// TypeScript interfaces matching backend Pydantic models
// These types mirror the schemas defined in backend/models/schemas.py

// ============================================================================
// Common Models
// ============================================================================

export interface Plot {
  name: string;
  type: string; // e.g. "volcano", "pca", "heatmap", "pathway"
  image_base64: string; // base64-encoded PNG
  description?: string | null;
}

export interface NarrativeSection {
  title: string;
  content: string;
}

// ============================================================================
// Research Mode Models
// ============================================================================

export interface ResearchAnalyzeRequest {
  project_name?: string | null;
  species?: string | null;
  contrast_label?: string | null;
}

export interface ResearchAnalyzeResponse {
  project_name?: string | null;
  plots: Plot[];
  narrative: Record<string, NarrativeSection>; // keys like "results", "discussion"
  summary_stats: Record<string, any>; // e.g. {"num_deg": 123, "up": 60, "down": 63}
}

// ============================================================================
// Personal Genomics Models
// ============================================================================

export interface SNPInput {
  rsid: string;
  genotype: string; // e.g. "AA", "AG", "GG"
}

export interface LifestyleInput {
  caffeine_intake?: string | null; // e.g. "low", "moderate", "high"
  exercise_frequency?: string | null;
  sleep_duration_hours?: number | null;
  diet_pattern?: string | null;
}

export interface PersonalInsightCard {
  domain: string; // e.g. "Caffeine metabolism"
  summary: string;
  score: number; // 0–1 for internal scoring
  percentile?: number | null; // 0–1 percentile compared to peers
  recommendations: string[];
}

export interface PeerComparison {
  metric: string;
  value: number;
  percentile: number;
  label: string;
}

export interface GeneticBioCard {
  title: string;
  subtitle: string;
  badges: string[];
  highlights: string[];
}

export interface PersonalAnalyzeRequest {
  snps: SNPInput[];
  lifestyle?: LifestyleInput | null;
}

export interface PersonalAnalyzeResponse {
  cards: PersonalInsightCard[];
  peer_comparison: PeerComparison[];
  genetic_card: GeneticBioCard;
}

// ============================================================================
// Report Export Models
// ============================================================================

export interface ReportExportRequest {
  mode: "research" | "personal";
  format: "pdf" | "docx";
  payload: Record<string, any>; // the full JSON returned by the corresponding analyze endpoint
}

export interface ReportExportResponse {
  download_url: string; // URL for the generated report file
}

