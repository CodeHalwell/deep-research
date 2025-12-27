"use client";

import { useEffect, useState } from "react";
import { Navigation } from "./navigation";
import { ThemeProvider } from "./theme-provider";

export function RootLayoutClient({ children }: { children: React.ReactNode }) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-background">
        <Navigation />
        <main className="flex-1">{children}</main>
        <footer className="border-t border-border py-6 text-center text-sm text-muted-foreground">
          <p>
            Deep Research Workflow System © 2024 | Powered by AI Agents &
            Intelligent Orchestration
          </p>
        </footer>
      </div>
    </ThemeProvider>
  );
}
