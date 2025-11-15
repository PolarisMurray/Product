import axios, { AxiosInstance } from 'axios';
import type {
  ResearchAnalyzeResponse,
  PersonalAnalyzeRequest,
  PersonalAnalyzeResponse,
  ReportExportRequest,
  ReportExportResponse,
} from './types';

// Base URL for the FastAPI backend
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Configured axios instance for API calls.
 * Automatically handles JSON and multipart/form-data requests.
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to handle FormData (don't set Content-Type, let browser set it with boundary)
apiClient.interceptors.request.use((config) => {
  if (config.data instanceof FormData) {
    // Remove Content-Type header for FormData - browser will set it with boundary
    delete config.headers['Content-Type'];
  }
  return config;
});

export default apiClient;

/**
 * Analyze research data (DEG and optional enrichment files).
 * 
 * @param formData - FormData containing:
 *   - deg_file: File (required)
 *   - enrichment_file: File (optional)
 *   - meta: JSON string of ResearchAnalyzeRequest metadata
 * @returns Promise resolving to ResearchAnalyzeResponse
 */
export async function analyzeResearch(
  formData: FormData
): Promise<ResearchAnalyzeResponse> {
  const response = await apiClient.post<ResearchAnalyzeResponse>(
    '/analyze/research',
    formData
  );
  return response.data;
}

/**
 * Analyze personal genomics data (SNPs + lifestyle).
 * 
 * @param payload - PersonalAnalyzeRequest with SNPs and optional lifestyle data
 * @returns Promise resolving to PersonalAnalyzeResponse
 */
export async function analyzePersonal(
  payload: PersonalAnalyzeRequest
): Promise<PersonalAnalyzeResponse> {
  const response = await apiClient.post<PersonalAnalyzeResponse>(
    '/analyze/personal',
    payload
  );
  return response.data;
}

/**
 * Export analysis results as a PDF or DOCX report.
 * 
 * @param payload - ReportExportRequest with mode, format, and analysis payload
 * @returns Promise resolving to ReportExportResponse with download URL
 */
export async function exportReport(
  payload: ReportExportRequest
): Promise<ReportExportResponse> {
  const response = await apiClient.post<ReportExportResponse>(
    '/report/export',
    payload
  );
  return response.data;
}

