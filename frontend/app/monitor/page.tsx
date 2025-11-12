"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { apiClient, Workflow, WorkflowStatistics, WorkflowResult } from "@/lib/api";
import { formatDate, getStatusColor, downloadFile } from "@/lib/utils";
import {
  RefreshCw,
  Download,
  AlertCircle,
  CheckCircle,
  Clock,
  BarChart3,
} from "lucide-react";

export default function MonitorPage() {
  const [workflowId, setWorkflowId] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [workflow, setWorkflow] = useState<Workflow | null>(null);
  const [statistics, setStatistics] = useState<WorkflowStatistics | null>(null);
  const [result, setResult] = useState<WorkflowResult | null>(null);
  const [error, setError] = useState("");
  const [autoRefresh, setAutoRefresh] = useState(false);

  useEffect(() => {
    if (autoRefresh && workflow && workflow.status !== "completed") {
      const interval = setInterval(
        () => {
          if (workflowId) {
            checkWorkflow(workflowId);
          }
        },
        5000
      ); // Refresh every 5 seconds
      return () => clearInterval(interval);
    }
  }, [autoRefresh, workflow, workflowId]);

  const checkWorkflow = async (id: string) => {
    if (!id.trim()) {
      setError("Please enter a workflow ID");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const [workflowData, statsData] = await Promise.all([
        apiClient.getWorkflow(id),
        apiClient.getWorkflowStatistics(id),
      ]);

      setWorkflow(workflowData);
      setStatistics(statsData);

      // Fetch result if completed
      if (workflowData.status === "completed") {
        const resultData = await apiClient.getWorkflowResult(id);
        setResult(resultData);
      }

      // Save to recent workflows
      saveRecentWorkflow(id);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to fetch workflow"
      );
      setWorkflow(null);
      setStatistics(null);
    } finally {
      setIsLoading(false);
    }
  };

  const saveRecentWorkflow = (id: string) => {
    const recent = JSON.parse(
      localStorage.getItem("recentWorkflows") || "[]"
    ) as string[];
    if (!recent.includes(id)) {
      recent.unshift(id);
      if (recent.length > 5) {
        recent.pop();
      }
      localStorage.setItem("recentWorkflows", JSON.stringify(recent));
    }
  };

  const handleDownload = async (format: "html" | "pdf" = "html") => {
    try {
      const blob = await apiClient.downloadReport(workflowId, format);
      const filename = `research-report-${workflowId.slice(0, 8)}.${
        format === "pdf" ? "pdf" : "html"
      }`;
      downloadFile(blob, filename);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to download report"
      );
    }
  };

  const getProgressPercentage = () => {
    if (!workflow) return 0;
    switch (workflow.status) {
      case "submitted":
        return 25;
      case "in_progress":
        return 75;
      case "completed":
        return 100;
      case "failed":
        return 100;
      default:
        return 0;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case "in_progress":
        return <RefreshCw className="h-5 w-5 animate-spin text-blue-500" />;
      case "failed":
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      case "submitted":
        return <Clock className="h-5 w-5 text-yellow-500" />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary/10">
      <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8 space-y-4">
          <h1 className="text-3xl font-bold tracking-tight">
            Monitor Workflow
          </h1>
          <p className="text-muted-foreground">
            Track the progress of your research workflow in real-time
          </p>
        </div>

        {/* Search Section */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Search Workflow</CardTitle>
            <CardDescription>
              Enter a workflow ID to monitor its progress
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="workflow-id">Workflow ID</Label>
                <div className="flex flex-col gap-2 sm:flex-row">
                  <Input
                    id="workflow-id"
                    placeholder="Enter workflow ID..."
                    value={workflowId}
                    onChange={(e) => setWorkflowId(e.target.value)}
                    disabled={isLoading}
                  />
                  <Button
                    onClick={() => checkWorkflow(workflowId)}
                    isLoading={isLoading}
                    className="sm:w-auto"
                  >
                    <RefreshCw className="mr-2 h-4 w-4" />
                    Check Status
                  </Button>
                </div>
              </div>

              {/* Auto Refresh Toggle */}
              {workflow && (
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="auto-refresh"
                    checked={autoRefresh}
                    onChange={(e) => setAutoRefresh(e.target.checked)}
                    disabled={workflow.status === "completed"}
                  />
                  <Label
                    htmlFor="auto-refresh"
                    className="cursor-pointer text-sm"
                  >
                    Auto-refresh every 5 seconds
                  </Label>
                </div>
              )}

              {/* Error Display */}
              {error && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Workflow Details */}
        {workflow && (
          <div className="space-y-6">
            {/* Status Card */}
            <Card>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="space-y-2">
                    <CardTitle className="flex items-center gap-2">
                      {getStatusIcon(workflow.status)}
                      Workflow Status
                    </CardTitle>
                    <CardDescription>
                      ID: {workflow.workflow_id}
                    </CardDescription>
                  </div>
                  <Badge className={getStatusColor(workflow.status)}>
                    {workflow.status.replace("_", " ").toUpperCase()}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Progress Bar */}
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="font-semibold">Overall Progress</span>
                    <span className="text-muted-foreground">
                      {getProgressPercentage()}%
                    </span>
                  </div>
                  <Progress value={getProgressPercentage()} max={100} />
                </div>

                {/* Timeline Info */}
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="rounded-lg bg-secondary/10 p-4">
                    <p className="text-xs font-semibold text-muted-foreground">
                      Created
                    </p>
                    <p className="mt-1 font-mono text-sm">
                      {formatDate(workflow.created_at)}
                    </p>
                  </div>
                  {workflow.completed_at && (
                    <div className="rounded-lg bg-secondary/10 p-4">
                      <p className="text-xs font-semibold text-muted-foreground">
                        Completed
                      </p>
                      <p className="mt-1 font-mono text-sm">
                        {formatDate(workflow.completed_at)}
                      </p>
                    </div>
                  )}
                </div>

                {/* Research Topic */}
                <div className="rounded-lg bg-secondary/10 p-4">
                  <p className="text-xs font-semibold text-muted-foreground">
                    Research Topic
                  </p>
                  <p className="mt-1 text-sm">{workflow.user_prompt}</p>
                </div>
              </CardContent>
            </Card>

            {/* Statistics */}
            {statistics && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="h-5 w-5" />
                    Statistics
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                    <div className="rounded-lg border border-border p-4">
                      <p className="text-xs font-semibold text-muted-foreground">
                        Iterations
                      </p>
                      <p className="mt-2 text-2xl font-bold">
                        {statistics.iterations}
                      </p>
                    </div>
                    <div className="rounded-lg border border-border p-4">
                      <p className="text-xs font-semibold text-muted-foreground">
                        Research Notes
                      </p>
                      <p className="mt-2 text-2xl font-bold">
                        {statistics.research_notes}
                      </p>
                    </div>
                    <div className="rounded-lg border border-border p-4">
                      <p className="text-xs font-semibold text-muted-foreground">
                        Searches Performed
                      </p>
                      <p className="mt-2 text-2xl font-bold">
                        {statistics.searches}
                      </p>
                    </div>
                    <div className="rounded-lg border border-border p-4">
                      <p className="text-xs font-semibold text-muted-foreground">
                        Approvals
                      </p>
                      <p className="mt-2 text-2xl font-bold">
                        {statistics.approvals}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Results - Show when completed */}
            {workflow.status === "completed" && result && (
              <div className="space-y-6">
                {/* Executive Summary */}
                <Card>
                  <CardHeader>
                    <CardTitle>Executive Summary</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="prose prose-sm dark:prose-invert max-w-none">
                      <p className="whitespace-pre-wrap text-sm leading-relaxed">
                        {result.summary.slice(0, 500)}
                        {result.summary.length > 500 ? "..." : ""}
                      </p>
                    </div>
                  </CardContent>
                </Card>

                {/* Download Options */}
                <Card>
                  <CardHeader>
                    <CardTitle>Download Report</CardTitle>
                    <CardDescription>
                      Download your completed research report
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="flex flex-wrap gap-2">
                    <Button
                      onClick={() => handleDownload("html")}
                      variant="outline"
                      className="gap-2"
                    >
                      <Download className="h-4 w-4" />
                      Download HTML
                    </Button>
                    <Button
                      onClick={() => handleDownload("pdf")}
                      variant="outline"
                      className="gap-2"
                    >
                      <Download className="h-4 w-4" />
                      Download PDF
                    </Button>
                  </CardContent>
                </Card>
              </div>
            )}

            {/* Error State */}
            {workflow.status === "failed" && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  {workflow.error_message ||
                    "The workflow failed. Please try again."}
                </AlertDescription>
              </Alert>
            )}
          </div>
        )}

        {/* Empty State */}
        {!workflow && !error && (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <BarChart3 className="mb-4 h-12 w-12 text-muted-foreground/50" />
              <p className="text-center text-muted-foreground">
                Enter a workflow ID above to start monitoring
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
