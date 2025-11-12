import type { Metadata } from "next";
import "./globals.css";
import { RootLayoutClient } from "@/components/root-layout-client";

export const metadata: Metadata = {
  title: "Deep Research Workflow",
  description: "Intelligent research automation system with AI agents",
  viewport: "width=device-width, initial-scale=1",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <RootLayoutClient>{children}</RootLayoutClient>
      </body>
    </html>
  );
}
