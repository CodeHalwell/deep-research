"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Brain,
  Zap,
  Shield,
  BookOpen,
  Globe,
  Settings,
  ArrowRight,
} from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function AboutPage() {
  const features = [
    {
      icon: Brain,
      title: "AI-Powered Research",
      description:
        "Multi-agent AI system conducts comprehensive research using multiple data sources and APIs",
    },
    {
      icon: Globe,
      title: "Multiple Research Sources",
      description:
        "Access web search, academic databases (arXiv, PubMed), and knowledge bases",
    },
    {
      icon: Zap,
      title: "Intelligent Orchestration",
      description:
        "Specialized agents for planning, research, writing, review, and formatting",
    },
    {
      icon: Shield,
      title: "Quality Assurance",
      description:
        "Built-in review cycles with human-in-the-loop control points",
    },
    {
      icon: BookOpen,
      title: "Professional Output",
      description:
        "Generates polished reports with citations, formatting, and PDF/HTML export",
    },
    {
      icon: Settings,
      title: "Extensible Architecture",
      description:
        "Modular design with tool servers and configurable workflows",
    },
  ];

  const components = [
    { name: "Planning Agent", description: "Analyzes prompts and generates research plans" },
    {
      name: "Research Agent",
      description: "Gathers data from multiple sources and synthesizes information",
    },
    {
      name: "Senior Research Agent",
      description: "Validates research quality and completeness",
    },
    { name: "Write Agent", description: "Drafts comprehensive reports" },
    { name: "Review Agent", description: "Evaluates quality and flags corrections" },
    { name: "Revision Agent", description: "Implements feedback and improvements" },
    {
      name: "Formatting Agent",
      description: "Applies professional styling and document templates",
    },
    { name: "Summary Agent", description: "Generates executive summaries" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary/10">
      <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-12 space-y-4 text-center">
          <h1 className="text-4xl font-bold tracking-tight">
            About Deep Research Workflow
          </h1>
          <p className="mx-auto max-w-2xl text-lg text-muted-foreground">
            An intelligent, agent-based research automation system that conducts
            comprehensive research, generates high-quality reports, and delivers
            professionally formatted documents with human-in-the-loop quality control.
          </p>
        </div>

        {/* Features Grid */}
        <div className="mb-12">
          <h2 className="mb-6 text-2xl font-bold">Key Features</h2>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, i) => {
              const Icon = feature.icon;
              return (
                <Card key={i}>
                  <CardHeader>
                    <div className="mb-2 inline-block rounded-lg bg-primary/10 p-2">
                      <Icon className="h-5 w-5 text-primary" />
                    </div>
                    <CardTitle className="text-lg">{feature.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground">
                      {feature.description}
                    </p>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>

        {/* Architecture */}
        <div className="mb-12 space-y-6">
          <div>
            <h2 className="mb-6 text-2xl font-bold">System Architecture</h2>
            <div className="grid gap-4 lg:grid-cols-2">
              {/* Agent Components */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">AI Agents</CardTitle>
                  <CardDescription>
                    Specialized agents for different tasks
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {components.map((component, i) => (
                      <div
                        key={i}
                        className="rounded-lg border border-border p-3"
                      >
                        <p className="font-semibold text-sm">
                          {component.name}
                        </p>
                        <p className="mt-1 text-xs text-muted-foreground">
                          {component.description}
                        </p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Tech Stack */}
              <div className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Technology Stack</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <p className="mb-2 font-semibold text-sm">Backend</p>
                      <div className="flex flex-wrap gap-2">
                        <Badge variant="outline">Python 3.12+</Badge>
                        <Badge variant="outline">LlamaIndex</Badge>
                        <Badge variant="outline">FastAPI</Badge>
                        <Badge variant="outline">SQLAlchemy</Badge>
                      </div>
                    </div>
                    <div>
                      <p className="mb-2 font-semibold text-sm">Frontend</p>
                      <div className="flex flex-wrap gap-2">
                        <Badge variant="outline">React 18</Badge>
                        <Badge variant="outline">Next.js 15</Badge>
                        <Badge variant="outline">TypeScript</Badge>
                        <Badge variant="outline">Tailwind CSS</Badge>
                      </div>
                    </div>
                    <div>
                      <p className="mb-2 font-semibold text-sm">APIs & Services</p>
                      <div className="flex flex-wrap gap-2">
                        <Badge variant="outline">OpenAI GPT-4</Badge>
                        <Badge variant="outline">DuckDuckGo</Badge>
                        <Badge variant="outline">Tavily Search</Badge>
                        <Badge variant="outline">Google Scholar</Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Research Sources</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2 text-sm">
                      <li className="flex items-center gap-2">
                        <ArrowRight className="h-4 w-4 text-primary" />
                        Web Search (DuckDuckGo, Tavily)
                      </li>
                      <li className="flex items-center gap-2">
                        <ArrowRight className="h-4 w-4 text-primary" />
                        Academic Databases (arXiv, PubMed)
                      </li>
                      <li className="flex items-center gap-2">
                        <ArrowRight className="h-4 w-4 text-primary" />
                        Semantic Scholar & Google Scholar
                      </li>
                      <li className="flex items-center gap-2">
                        <ArrowRight className="h-4 w-4 text-primary" />
                        Knowledge Bases (Wikipedia, Wikidata)
                      </li>
                      <li className="flex items-center gap-2">
                        <ArrowRight className="h-4 w-4 text-primary" />
                        Web Scraping & API Integrations
                      </li>
                    </ul>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </div>

        {/* Workflow */}
        <Card className="mb-12">
          <CardHeader>
            <CardTitle>Research Workflow</CardTitle>
            <CardDescription>
              How the system processes your research request
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-start gap-4">
                <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-primary/10">
                  <span className="font-semibold text-primary">1</span>
                </div>
                <div>
                  <p className="font-semibold">Submit Request</p>
                  <p className="text-sm text-muted-foreground">
                    You submit a research topic through the web interface
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-primary/10">
                  <span className="font-semibold text-primary">2</span>
                </div>
                <div>
                  <p className="font-semibold">Plan Generation</p>
                  <p className="text-sm text-muted-foreground">
                    Planning agent analyzes your request and creates a research plan
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-primary/10">
                  <span className="font-semibold text-primary">3</span>
                </div>
                <div>
                  <p className="font-semibold">Research Execution</p>
                  <p className="text-sm text-muted-foreground">
                    Research agents gather data from multiple sources and synthesize
                    information
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-primary/10">
                  <span className="font-semibold text-primary">4</span>
                </div>
                <div>
                  <p className="font-semibold">Report Writing</p>
                  <p className="text-sm text-muted-foreground">
                    Write agent creates a comprehensive draft report
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-primary/10">
                  <span className="font-semibold text-primary">5</span>
                </div>
                <div>
                  <p className="font-semibold">Quality Review</p>
                  <p className="text-sm text-muted-foreground">
                    Review agent evaluates quality and flags necessary corrections
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-primary/10">
                  <span className="font-semibold text-primary">6</span>
                </div>
                <div>
                  <p className="font-semibold">Formatting & Export</p>
                  <p className="text-sm text-muted-foreground">
                    Final report is formatted and exported as PDF or HTML
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* CTA */}
        <Card className="bg-gradient-to-r from-primary/10 to-secondary/10">
          <CardContent className="flex flex-col items-center justify-between gap-4 p-8 sm:flex-row">
            <div>
              <h3 className="text-xl font-bold">Ready to start researching?</h3>
              <p className="mt-1 text-muted-foreground">
                Submit your first research topic and let our AI agents do the work
              </p>
            </div>
            <Link href="/">
              <Button size="lg" className="gap-2">
                Start Research
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
