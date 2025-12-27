"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { apiClient } from "@/lib/api";
import { CheckCircle, AlertCircle, Zap } from "lucide-react";

const EXAMPLE_TOPICS = [
  "Quantum computing and its applications in cryptography",
  "Recent advances in artificial intelligence and machine learning",
  "Climate change mitigation strategies and renewable energy",
  "The future of space exploration and colonization",
  "Cybersecurity threats and defense mechanisms",
];

export default function Home() {
  const [topic, setTopic] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [apiUrl, setApiUrl] = useState("http://localhost:8000");
  const [isConnected, setIsConnected] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [workflowId, setWorkflowId] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    checkApiConnection();
    // Load saved API URL
    const saved = localStorage.getItem("apiUrl");
    if (saved) {
      setApiUrl(saved);
      apiClient.setBaseURL(saved);
    }
  }, []);

  useEffect(() => {
    checkApiConnection();
  }, [apiUrl]);

  const checkApiConnection = async () => {
    try {
      const isHealthy = await apiClient.checkHealth();
      setIsConnected(isHealthy);
      setError("");
    } catch {
      setIsConnected(false);
    }
  };

  const handleApiUrlChange = (newUrl: string) => {
    setApiUrl(newUrl);
    localStorage.setItem("apiUrl", newUrl);
    apiClient.setBaseURL(newUrl);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!topic.trim()) {
      setError("Please enter a research topic");
      return;
    }

    if (!isConnected) {
      setError("API server is not connected. Please check the connection.");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const response = await apiClient.submitWorkflow(topic);
      setWorkflowId(response.workflow_id);
      setSubmitted(true);
      setTopic("");

      // Copy to clipboard
      navigator.clipboard.writeText(response.workflow_id);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to submit workflow"
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleExampleClick = (example: string) => {
    setTopic(example);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary/10">
      <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8 space-y-4 text-center">
          <h1 className="text-4xl font-bold tracking-tight">
            Deep Research Workflow
          </h1>
          <p className="text-lg text-muted-foreground">
            Submit your research topic and let our AI agents conduct comprehensive
            research and generate professional reports
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-3">
          {/* Main Form */}
          <div className="lg:col-span-2 space-y-6">
            {/* API Configuration */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">API Configuration</CardTitle>
                <CardDescription>
                  Configure the API server connection
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="api-url">API Server URL</Label>
                  <div className="flex gap-2">
                    <Input
                      id="api-url"
                      value={apiUrl}
                      onChange={(e) => handleApiUrlChange(e.target.value)}
                      placeholder="http://localhost:8000"
                      className="flex-1"
                    />
                    <Button
                      variant="outline"
                      onClick={checkApiConnection}
                      size="sm"
                    >
                      Test
                    </Button>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <div
                    className={`h-2 w-2 rounded-full ${
                      isConnected ? "bg-green-500" : "bg-red-500"
                    }`}
                  />
                  <span className="text-sm">
                    {isConnected
                      ? "Connected to API server"
                      : "Cannot connect to API server"}
                  </span>
                </div>
              </CardContent>
            </Card>

            {/* Submit Form */}
            <Card>
              <CardHeader>
                <CardTitle>Submit Research Request</CardTitle>
                <CardDescription>
                  Enter your research topic to start the workflow
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  {/* Success Message */}
                  {submitted && (
                    <Alert variant="success">
                      <CheckCircle className="h-4 w-4" />
                      <div className="ml-3">
                        <h3 className="font-semibold">Workflow Submitted</h3>
                        <div className="mt-2 space-y-2">
                          <p className="text-sm">
                            Your research workflow has been submitted successfully.
                          </p>
                          <div className="bg-background/50 rounded px-3 py-2">
                            <p className="break-all font-mono text-xs">
                              ID: {workflowId}
                            </p>
                            <p className="mt-1 text-xs text-muted-foreground">
                              (Copied to clipboard)
                            </p>
                          </div>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => {
                              setSubmitted(false);
                              setWorkflowId("");
                            }}
                            type="button"
                          >
                            Submit Another Research
                          </Button>
                        </div>
                      </div>
                    </Alert>
                  )}

                  {/* Error Message */}
                  {error && (
                    <Alert variant="destructive">
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>{error}</AlertDescription>
                    </Alert>
                  )}

                  {/* Topic Input */}
                  <div className="space-y-2">
                    <Label htmlFor="topic">Research Topic</Label>
                    <Textarea
                      id="topic"
                      placeholder="Enter your research topic... (e.g., 'Recent advances in quantum computing')"
                      value={topic}
                      onChange={(e) => setTopic(e.target.value)}
                      disabled={isLoading || !isConnected}
                      rows={5}
                    />
                    <p className="text-xs text-muted-foreground">
                      Be specific for better results. Include key terms and concepts.
                    </p>
                  </div>

                  {/* Submit Button */}
                  <Button
                    type="submit"
                    size="lg"
                    isLoading={isLoading}
                    disabled={!isConnected || isLoading || !topic.trim()}
                    className="w-full"
                  >
                    <Zap className="mr-2 h-4 w-4" />
                    Submit Research
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Examples */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Example Topics</CardTitle>
                <CardDescription>
                  Click to quickly populate the research topic field
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                {EXAMPLE_TOPICS.map((example, i) => (
                  <button
                    key={i}
                    onClick={() => handleExampleClick(example)}
                    className="w-full rounded-lg bg-secondary/10 p-3 text-left text-sm transition-colors hover:bg-secondary/20 disabled:opacity-50"
                    disabled={isLoading || !isConnected}
                  >
                    {example}
                  </button>
                ))}
              </CardContent>
            </Card>

            {/* Quick Stats */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">How It Works</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4 text-sm">
                <div className="space-y-3">
                  <div className="flex gap-3">
                    <Badge variant="outline" className="flex-shrink-0">
                      1
                    </Badge>
                    <div>
                      <p className="font-semibold">Submit Topic</p>
                      <p className="text-xs text-muted-foreground">
                        Enter your research question
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <Badge variant="outline" className="flex-shrink-0">
                      2
                    </Badge>
                    <div>
                      <p className="font-semibold">AI Research</p>
                      <p className="text-xs text-muted-foreground">
                        Agents gather data from multiple sources
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <Badge variant="outline" className="flex-shrink-0">
                      3
                    </Badge>
                    <div>
                      <p className="font-semibold">Report Generation</p>
                      <p className="text-xs text-muted-foreground">
                        Professional document is created
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <Badge variant="outline" className="flex-shrink-0">
                      4
                    </Badge>
                    <div>
                      <p className="font-semibold">Download</p>
                      <p className="text-xs text-muted-foreground">
                        Get your completed report in multiple formats
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
