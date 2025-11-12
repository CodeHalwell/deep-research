"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { apiClient, Workflow, WorkflowsResponse } from "@/lib/api";
import { formatDate, getStatusColor } from "@/lib/utils";
import { AlertCircle, History, RefreshCw, ArrowRight } from "lucide-react";

export default function HistoryPage() {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    loadWorkflows();
  }, []);

  const loadWorkflows = async () => {
    setIsLoading(true);
    setError("");

    try {
      const response: WorkflowsResponse = await apiClient.listWorkflows();
      setWorkflows(response.workflows);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to load workflows"
      );
      setWorkflows([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary/10">
      <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
          <div className="space-y-2">
            <h1 className="text-3xl font-bold tracking-tight">
              Workflow History
            </h1>
            <p className="text-muted-foreground">
              View all your past research workflows
            </p>
          </div>
          <Button onClick={loadWorkflows} isLoading={isLoading}>
            <RefreshCw className="mr-2 h-4 w-4" />
            Refresh
          </Button>
        </div>

        {/* Error Alert */}
        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Workflows List */}
        {workflows.length > 0 ? (
          <div className="space-y-4">
            {workflows.map((workflow) => (
              <Card
                key={workflow.workflow_id}
                className="overflow-hidden hover:shadow-lg transition-shadow"
              >
                <CardContent className="p-0">
                  <div className="flex flex-col gap-4 p-6 sm:flex-row sm:items-center sm:justify-between">
                    <div className="flex-1 space-y-2 min-w-0">
                      <div className="flex items-start justify-between gap-4">
                        <div className="min-w-0 flex-1">
                          <p className="font-mono text-xs text-muted-foreground">
                            {workflow.workflow_id}
                          </p>
                          <p className="mt-2 line-clamp-2 text-sm font-semibold">
                            {workflow.user_prompt}
                          </p>
                        </div>
                        <Badge className={getStatusColor(workflow.status)}>
                          {workflow.status.replace("_", " ")}
                        </Badge>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        Created: {formatDate(workflow.created_at)}
                      </p>
                    </div>
                    <Link href={`/monitor?workflow=${workflow.workflow_id}`}>
                      <Button variant="outline" size="sm" className="gap-2">
                        Monitor
                        <ArrowRight className="h-4 w-4" />
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : isLoading ? (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <div className="mb-4 inline-block h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent"></div>
              <p className="text-muted-foreground">Loading workflows...</p>
            </CardContent>
          </Card>
        ) : (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <History className="mb-4 h-12 w-12 text-muted-foreground/50" />
              <p className="text-center text-muted-foreground">
                No workflows found. Start by submitting a research request.
              </p>
              <Link href="/" className="mt-4">
                <Button>Submit Research</Button>
              </Link>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
