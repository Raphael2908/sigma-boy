import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Sigma Boi • Looksmaxxing AI Agent",
  description:
    "Generate a personalized looksmaxxing facial report. Deployed on Virtuals Protocol.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-background text-foreground antialiased">
        {children}
      </body>
    </html>
  );
}