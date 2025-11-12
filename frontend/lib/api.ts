import axios, { AxiosInstance } from "axios";

export interface Workflow {
  workflow_id: string;
  status: "submitted" | "in_progress" | "completed" | "failed";
  user_prompt: string;
  created_at: string;
  completed_at?: string | null;
  output_path?: string;
  error_message?: string | null;
}

export interface WorkflowResult {
  workflow_id: string;
  user_prompt: string;
  research_plan: string;
  draft_report: string;
  final_report: string;
  summary: string;
  output_path: string;
  status: string;
}

export interface WorkflowStatistics {
  workflow_id: string;
  iterations: number;
  research_notes: number;
  searches: number;
  approvals: number;
}

export interface WorkflowsResponse {
  count: number;
  workflows: Workflow[];
}

class APIClient {
  private client: AxiosInstance;
  private baseURL: string;

  constructor(baseURL: string = "http://localhost:8000") {
    this.baseURL = baseURL;
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
    });
  }

  setBaseURL(url: string): void {
    this.baseURL = url;
    this.client = axios.create({
      baseURL: url,
      timeout: 30000,
    });
  }

  async checkHealth(): Promise<boolean> {
    try {
      const response = await this.client.get("/health");
      return response.status === 200;
    } catch {
      return false;
    }
  }

  async submitWorkflow(topic: string): Promise<Workflow> {
    const response = await this.client.post<Workflow>("/workflows", {
      topic,
      config_path: ".config/config.yaml",
    });
    return response.data;
  }

  async getWorkflow(workflowId: string): Promise<Workflow> {
    const response = await this.client.get<Workflow>(
      `/workflows/${workflowId}`
    );
    return response.data;
  }

  async getWorkflowResult(workflowId: string): Promise<WorkflowResult> {
    const response = await this.client.get<WorkflowResult>(
      `/workflows/${workflowId}/result`
    );
    return response.data;
  }

  async getWorkflowStatistics(
    workflowId: string
  ): Promise<WorkflowStatistics> {
    const response = await this.client.get<WorkflowStatistics>(
      `/workflows/${workflowId}/statistics`
    );
    return response.data;
  }

  async downloadReport(
    workflowId: string,
    format: "html" | "pdf" = "html"
  ): Promise<Blob> {
    const response = await this.client.get<Blob>(
      `/workflows/${workflowId}/report`,
      {
        responseType: "blob",
        params: { format },
      }
    );
    return response.data;
  }

  async listWorkflows(): Promise<WorkflowsResponse> {
    const response = await this.client.get<WorkflowsResponse>("/workflows");
    return response.data;
  }

  getBaseURL(): string {
    return this.baseURL;
  }
}

export const apiClient = new APIClient();
