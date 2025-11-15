# BioReport Copilot API Contract

This document describes the API endpoints for the BioReport Copilot application. All endpoints are available at the base URL: `http://localhost:8000` (or your configured backend URL).

## Table of Contents

1. [Research Analysis Endpoint](#1-research-analysis-endpoint)
2. [Personal Genomics Analysis Endpoint](#2-personal-genomics-analysis-endpoint)
3. [Report Export Endpoint](#3-report-export-endpoint)
4. [Data Models](#data-models)

---

## 1. Research Analysis Endpoint

### `POST /analyze/research`

Analyzes differential gene expression (DEG) data and optional enrichment results to generate visualizations, narrative sections, and summary statistics.

#### Request

**Content-Type:** `multipart/form-data`

**Form Fields:**

| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| `deg_file` | File | Yes | CSV/TSV/XLSX file containing differential expression genes data |
| `enrichment_file` | File | No | CSV/TSV/XLSX file containing enrichment analysis results |
| `meta` | String (JSON) | Yes | JSON string containing metadata. Must be a valid JSON object with the following optional fields:<br>- `project_name` (string, optional)<br>- `species` (string, optional)<br>- `contrast_label` (string, optional) |

**Example Request (using curl):**

```bash
curl -X POST "http://localhost:8000/analyze/research" \
  -F "deg_file=@path/to/deg_data.csv" \
  -F "enrichment_file=@path/to/enrichment.csv" \
  -F 'meta={"project_name": "My Research Project", "species": "Homo sapiens", "contrast_label": "Treatment vs Control"}'
```

**Example Request (JavaScript FormData):**

```javascript
const formData = new FormData();
formData.append('deg_file', degFile);
formData.append('enrichment_file', enrichmentFile); // optional
formData.append('meta', JSON.stringify({
  project_name: 'My Research Project',
  species: 'Homo sapiens',
  contrast_label: 'Treatment vs Control'
}));
```

#### Response

**Status Code:** `200 OK`

**Content-Type:** `application/json`

**Response Body:** `ResearchAnalyzeResponse`

```json
{
  "project_name": "My Research Project",
  "plots": [
    {
      "name": "Volcano Plot",
      "type": "volcano",
      "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
      "description": "Volcano plot showing differential expression with significance thresholds"
    },
    {
      "name": "PCA Analysis",
      "type": "pca",
      "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
      "description": "Principal Component Analysis showing sample clustering"
    },
    {
      "name": "Heatmap",
      "type": "heatmap",
      "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
      "description": "Heatmap of top differentially expressed genes"
    }
  ],
  "narrative": {
    "results": {
      "title": "Results",
      "content": "Differential expression analysis identified 123 significantly differentially expressed genes (DEGs) out of 20,000 total genes analyzed (0.62% of the transcriptome).\n\nAmong the DEGs, 60 genes (48.8%) were up-regulated, while 63 genes (51.2%) were down-regulated. This indicates a substantial transcriptional response to the experimental conditions."
    },
    "discussion": {
      "title": "Discussion",
      "content": "The identification of 123 differentially expressed genes represents a significant transcriptional response. The relatively balanced distribution between up-regulated (60) and down-regulated (63) genes suggests coordinated regulatory mechanisms.\n\nThe magnitude of the response (0.62% of genes) indicates substantial biological changes under the experimental conditions."
    }
  },
  "summary_stats": {
    "num_deg": 123,
    "up": 60,
    "down": 63,
    "total_genes": 20000,
    "deg_file": "deg_data.csv",
    "enrichment_file": "enrichment.csv"
  }
}
```

**Response Fields:**

- `project_name` (string, optional): The project name provided in the request
- `plots` (array of Plot objects): List of generated visualizations
  - `name` (string): Name of the plot
  - `type` (string): Type of plot (e.g., "volcano", "pca", "heatmap", "pathway")
  - `image_base64` (string): Base64-encoded PNG image data
  - `description` (string, optional): Description of the plot
- `narrative` (object): Dictionary containing narrative sections
  - `results` (NarrativeSection): Results section with title and content
  - `discussion` (NarrativeSection): Discussion section with title and content
- `summary_stats` (object): Dictionary containing summary statistics (keys and values may vary)

**Error Responses:**

- `400 Bad Request`: Invalid metadata JSON or missing required file
- `500 Internal Server Error`: Server error during processing

---

## 2. Personal Genomics Analysis Endpoint

### `POST /analyze/personal`

Analyzes personal genomics data (SNP genotypes and lifestyle factors) to generate personalized insights, peer comparisons, and a genetic bio card.

#### Request

**Content-Type:** `application/json`

**Request Body:** `PersonalAnalyzeRequest`

```json
{
  "snps": [
    {
      "rsid": "rs762551",
      "genotype": "AA"
    },
    {
      "rsid": "rs4988235",
      "genotype": "TT"
    }
  ],
  "lifestyle": {
    "caffeine_intake": "moderate",
    "exercise_frequency": "3-4 times/week",
    "sleep_duration_hours": 7.5,
    "diet_pattern": "Mediterranean"
  }
}
```

**Request Fields:**

- `snps` (array of SNPInput, required): List of SNP genotypes to analyze
  - `rsid` (string, required): The rsID identifier (e.g., "rs762551")
  - `genotype` (string, required): The genotype (e.g., "AA", "AG", "GG")
- `lifestyle` (LifestyleInput, optional): Lifestyle factors
  - `caffeine_intake` (string, optional): e.g., "low", "moderate", "high"
  - `exercise_frequency` (string, optional): e.g., "3-4 times/week"
  - `sleep_duration_hours` (number, optional): Hours of sleep per night
  - `diet_pattern` (string, optional): e.g., "Mediterranean", "Vegetarian"

**Example Request (using curl):**

```bash
curl -X POST "http://localhost:8000/analyze/personal" \
  -H "Content-Type: application/json" \
  -d '{
    "snps": [
      {"rsid": "rs762551", "genotype": "AA"},
      {"rsid": "rs4988235", "genotype": "TT"}
    ],
    "lifestyle": {
      "caffeine_intake": "moderate",
      "exercise_frequency": "3-4 times/week"
    }
  }'
```

#### Response

**Status Code:** `200 OK`

**Content-Type:** `application/json`

**Response Body:** `PersonalAnalyzeResponse`

```json
{
  "cards": [
    {
      "domain": "Caffeine Metabolism",
      "summary": "You have a variant associated with slower caffeine metabolism. This means caffeine may stay in your system longer, potentially affecting sleep quality if consumed later in the day.",
      "score": 0.65,
      "percentile": 0.35,
      "recommendations": [
        "Consider limiting caffeine intake after 2 PM",
        "Monitor how caffeine affects your sleep patterns",
        "You may be more sensitive to caffeine's effects"
      ]
    },
    {
      "domain": "Lactose Tolerance",
      "summary": "You carry a variant associated with lactose tolerance into adulthood. You likely digest lactose well.",
      "score": 0.90,
      "percentile": 0.80,
      "recommendations": [
        "You can likely consume dairy products without issues",
        "Maintain a balanced diet including dairy if desired"
      ]
    }
  ],
  "peer_comparison": [
    {
      "metric": "caffeine_metabolism",
      "value": 0.65,
      "percentile": 0.35,
      "label": "Caffeine Metabolism Speed"
    },
    {
      "metric": "lactose_tolerance",
      "value": 0.90,
      "percentile": 0.80,
      "label": "Lactose Tolerance"
    },
    {
      "metric": "overall_genetic_profile",
      "value": 0.775,
      "percentile": 0.55,
      "label": "Overall Genetic Profile"
    }
  ],
  "genetic_card": {
    "title": "Personal Genetic Profile",
    "subtitle": "Analysis of 2 genetic variant(s)",
    "badges": [
      "Caffeine Analyzed",
      "Lactose Analyzed",
      "2 Traits Analyzed"
    ],
    "highlights": [
      "Caffeine Metabolism: You have a variant associated with slower caffeine metabolism. This means caffeine may stay in your system longer...",
      "Lactose Tolerance: You carry a variant associated with lactose tolerance into adulthood. You likely digest lactose well.",
      "Lifestyle: Caffeine: moderate, Exercise: 3-4 times/week"
    ]
  }
}
```

**Response Fields:**

- `cards` (array of PersonalInsightCard): List of personalized insight cards
  - `domain` (string): The trait or domain name (e.g., "Caffeine Metabolism")
  - `summary` (string): Summary text describing the insight
  - `score` (number): Internal score from 0 to 1
  - `percentile` (number, optional): Percentile compared to peers (0 to 1)
  - `recommendations` (array of strings): List of personalized recommendations
- `peer_comparison` (array of PeerComparison): List of peer comparison metrics
  - `metric` (string): Metric identifier
  - `value` (number): The metric value
  - `percentile` (number): Percentile compared to peers (0 to 1)
  - `label` (string): Human-readable label for the metric
- `genetic_card` (GeneticBioCard): Shareable genetic bio card
  - `title` (string): Card title
  - `subtitle` (string): Card subtitle
  - `badges` (array of strings): List of badge labels
  - `highlights` (array of strings): List of highlight text

**Error Responses:**

- `400 Bad Request`: Invalid request body or missing required fields (e.g., empty snps array)
- `500 Internal Server Error`: Server error during processing

---

## 3. Report Export Endpoint

### `POST /report/export`

Exports analysis results as a PDF or DOCX report file.

#### Request

**Content-Type:** `application/json`

**Request Body:** `ReportExportRequest`

```json
{
  "mode": "research",
  "format": "pdf",
  "payload": {
    "project_name": "My Research Project",
    "plots": [...],
    "narrative": {...},
    "summary_stats": {...}
  }
}
```

**Request Fields:**

- `mode` (string, required): Analysis mode. Must be either `"research"` or `"personal"`
- `format` (string, required): Export format. Must be either `"pdf"` or `"docx"`
- `payload` (object, required): The full JSON response from the corresponding analyze endpoint
  - For research mode: Use the complete `ResearchAnalyzeResponse` object
  - For personal mode: Use the complete `PersonalAnalyzeResponse` object

**Example Request (Research Mode):**

```json
{
  "mode": "research",
  "format": "pdf",
  "payload": {
    "project_name": "My Research Project",
    "plots": [
      {
        "name": "Volcano Plot",
        "type": "volcano",
        "image_base64": "...",
        "description": "..."
      }
    ],
    "narrative": {
      "results": {
        "title": "Results",
        "content": "..."
      },
      "discussion": {
        "title": "Discussion",
        "content": "..."
      }
    },
    "summary_stats": {
      "num_deg": 123,
      "up": 60,
      "down": 63
    }
  }
}
```

**Example Request (Personal Mode):**

```json
{
  "mode": "personal",
  "format": "pdf",
  "payload": {
    "cards": [...],
    "peer_comparison": [...],
    "genetic_card": {...}
  }
}
```

#### Response

**Status Code:** `200 OK`

**Content-Type:** `application/json`

**Response Body:** `ReportExportResponse`

```json
{
  "download_url": "/static/reports/research-1234567890.pdf"
}
```

**Response Fields:**

- `download_url` (string): URL path to the generated report file. The file can be accessed at `{base_url}{download_url}`.

**Example Response:**

```json
{
  "download_url": "/static/reports/research-1704067200.pdf"
}
```

**Note:** Currently, the backend returns a placeholder URL. In production, this URL will point to an actual generated report file.

**Error Responses:**

- `400 Bad Request`: Invalid request body, invalid mode/format, or payload structure mismatch
- `500 Internal Server Error`: Server error during report generation

---

## Data Models

### Common Models

#### Plot

```typescript
{
  name: string;
  type: string;  // e.g., "volcano", "pca", "heatmap", "pathway"
  image_base64: string;  // Base64-encoded PNG image
  description?: string | null;  // Optional description
}
```

#### NarrativeSection

```typescript
{
  title: string;
  content: string;  // Multiline text content
}
```

### Research Models

#### ResearchAnalyzeRequest (metadata)

```typescript
{
  project_name?: string | null;
  species?: string | null;
  contrast_label?: string | null;
}
```

#### ResearchAnalyzeResponse

```typescript
{
  project_name?: string | null;
  plots: Plot[];
  narrative: {
    results: NarrativeSection;
    discussion: NarrativeSection;
  };
  summary_stats: Record<string, any>;  // Flexible object with various statistics
}
```

### Personal Genomics Models

#### SNPInput

```typescript
{
  rsid: string;  // e.g., "rs762551"
  genotype: string;  // e.g., "AA", "AG", "GG"
}
```

#### LifestyleInput

```typescript
{
  caffeine_intake?: string | null;  // e.g., "low", "moderate", "high"
  exercise_frequency?: string | null;
  sleep_duration_hours?: number | null;
  diet_pattern?: string | null;
}
```

#### PersonalInsightCard

```typescript
{
  domain: string;  // e.g., "Caffeine metabolism"
  summary: string;
  score: number;  // 0 to 1
  percentile?: number | null;  // 0 to 1
  recommendations: string[];
}
```

#### PeerComparison

```typescript
{
  metric: string;
  value: number;
  percentile: number;  // 0 to 1
  label: string;
}
```

#### GeneticBioCard

```typescript
{
  title: string;
  subtitle: string;
  badges: string[];
  highlights: string[];
}
```

#### PersonalAnalyzeRequest

```typescript
{
  snps: SNPInput[];
  lifestyle?: LifestyleInput | null;
}
```

#### PersonalAnalyzeResponse

```typescript
{
  cards: PersonalInsightCard[];
  peer_comparison: PeerComparison[];
  genetic_card: GeneticBioCard;
}
```

### Report Export Models

#### ReportExportRequest

```typescript
{
  mode: "research" | "personal";
  format: "pdf" | "docx";
  payload: Record<string, any>;  // Full response from analyze endpoint
}
```

#### ReportExportResponse

```typescript
{
  download_url: string;  // URL path to the generated report
}
```

---

## Base URL and Environment

- **Development:** `http://localhost:8000`
- **Production:** Configure via environment variable `VITE_API_BASE_URL` (frontend) or set in backend configuration

## Authentication

Currently, the API does not require authentication. This may change in future versions.

## Rate Limiting

Currently, there are no rate limits. This may be implemented in future versions.

## Error Handling

All endpoints may return the following error responses:

- **400 Bad Request:** Invalid request format or missing required fields
- **500 Internal Server Error:** Server-side error during processing

Error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Support

For questions or issues, please refer to the main project README or contact the development team.

