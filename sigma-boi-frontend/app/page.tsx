"use client";

import Link from "next/link";
import { Camera, ShieldCheck, Sparkles, Wand2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

// Custom X logo (SVG) so we don't rely on external icon packs for the X brand mark
const XIcon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
    <path
      d="M18.9 2H22l-9.6 11.01L22.5 22h-7.2l-5.6-6.53L3.3 22H.2l10.3-11.8L.1 2h7.3l5 5.86L18.9 2zM17.7 20.1h2.0L6.4 3.9H4.3l13.4 16.2z"
      fill="currentColor"
    />
  </svg>
);

export default function Page() {
  return (
    <div className="relative">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b bg-background/70 backdrop-blur supports-[backdrop-filter]:bg-background/50">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <Link href="#" className="flex items-center gap-3">
            <div className="grid h-9 w-9 place-items-center rounded-2xl bg-primary/10 text-xl font-bold">Σ</div>
            <span className="text-sm font-semibold tracking-tight">Sigma Boy • Looksmaxxing AI</span>
          </Link>

          <nav className="hidden items-center gap-6 text-sm md:flex">
            <Link href="#about" className="text-muted-foreground hover:text-foreground">
              About
            </Link>
            <Link href="#how" className="text-muted-foreground hover:text-foreground">
              How it works
            </Link>
            <Link href="#features" className="text-muted-foreground hover:text-foreground">
              Features
            </Link>
          </nav>

          <div className="flex items-center gap-2">
            <Button asChild variant="outline">
              <a
                href="https://x.com/sigma_boi_ai"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2"
              >
                <XIcon className="h-4 w-4" />
                <span className="hidden sm:inline">Follow on X</span>
              </a>
            </Button>
            <Button asChild>
              <a
                href="https://app.virtuals.io/acp"
                target="_blank"
                rel="noopener noreferrer"
              >
                Try on Virtuals
              </a>
            </Button>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="pointer-events-none absolute inset-0 -z-10 opacity-40">
          <div className="absolute left-1/2 top-[-12rem] h-[42rem] w-[42rem] -translate-x-1/2 rounded-full bg-primary/40 blur-[140px]" />
        </div>

        <div className="container mx-auto grid gap-10 px-4 pb-20 pt-16 lg:grid-cols-2 lg:items-center">
          <div className="space-y-6">
            <h1 className="text-4xl font-extrabold leading-tight tracking-tight md:text-6xl">
              Looksmaxxing, powered by an
              <span className="text-primary"> on‑chain AI Agent</span>
            </h1>
            <p className="max-w-prose text-lg text-muted-foreground">
              Upload a selfie on the Virtuals Protocol dApp and receive a structured Looksmaxxing report: facial cues, grooming & skincare tips, hairstyle recommendations, and actionable lifestyle tweaks—personalized to you.
            </p>
            <div className="flex flex-wrap gap-2">
              <Button asChild size="lg">
                <Link href="/try" target="_blank" rel="noopener noreferrer">
                  Try the Agent
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg">
                <a
                  href="https://x.com/sigma_boi_ai"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2"
                >
                  <XIcon className="h-5 w-5" /> Visit X Profile
                </a>
              </Button>
            </div>
            <div className="flex items-center gap-4 pt-2 text-sm text-muted-foreground">
              <div className="-space-x-2 flex">
                {[...Array(5)].map((_, i) => (
                  <div
                    key={i}
                    className="h-6 w-6 rounded-full border bg-muted shadow-sm"
                    aria-hidden
                  />
                ))}
              </div>
              <span>Trusted by early adopters on Virtuals Protocol</span>
            </div>
          </div>

          <Card className="border-primary/20 bg-primary/5">
            <CardHeader>
              <CardTitle className="text-base text-muted-foreground">Sample Report Snapshot</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm">
              <div>• Symmetry score: <span className="font-semibold">7.8/10</span></div>
              <div>• Skin analysis: “Mild T‑zone oiliness; consider niacinamide 4–5%.”</div>
              <div>• Hairstyle fit: "Textured crop, medium fade"</div>
              <div>• Grooming: "Tidy brows; light stubble suits your jawline"</div>
              <div>• Lifestyle: “+Protein 20–30g breakfast; 7–8h sleep target.”</div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* About */}
      <section id="about" className="container mx-auto px-4 py-16">
        <div className="grid items-start gap-10 lg:grid-cols-5">
          <div className="lg:col-span-2">
            <h2 className="text-3xl font-bold tracking-tight md:text-4xl">About Sigma Boy</h2>
            <p className="mt-4 text-muted-foreground">
              Sigma Boy is an autonomous AI Agent that lives on the <span className="font-semibold text-primary">Virtuals Protocol</span>. It blends computer‑vision signals and aesthetics heuristics to produce a concise Looksmaxxing report that’s practical and respectful.
            </p>
            <p className="mt-4 text-muted-foreground">
              You’re always in control: connect wallet, upload on the dApp, review, and keep what resonates. No gimmicks—habit and style choices that compound over time.
            </p>
            <div className="mt-6 flex flex-wrap gap-2">
              <Button asChild>
                <Link href="/try" target="_blank" rel="noopener noreferrer">
                  Try the Agent
                </Link>
              </Button>
              <Button asChild variant="outline">
                <a
                  href="https://x.com/sigma_boi_ai"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2"
                >
                  <XIcon className="h-5 w-5" /> Follow on X
                </a>
              </Button>
            </div>
          </div>
          <div className="grid gap-4 lg:col-span-3">
            <FeatureCard
              icon={<ShieldCheck className="h-5 w-5" />}
              title="Private by design"
              body="Images are processed for analysis; long‑term storage/history is opt‑in at the dApp level."
            />
            <FeatureCard
              icon={<Sparkles className="h-5 w-5" />}
              title="Action‑first output"
              body="Clear, ranked suggestions you can apply today—grooming, skincare, hair, and lifestyle."
            />
            <FeatureCard
              icon={<Wand2 className="h-5 w-5" />}
              title="On‑chain agent"
              body="Deployed on the Virtuals Protocol network for transparent coordination and verifiable actions."
            />
          </div>
        </div>
      </section>

      {/* How it works */}
      <section id="how" className="container mx-auto px-4 py-16">
        <h2 className="mb-8 text-3xl font-bold tracking-tight md:text-4xl">How it works</h2>
        <div className="grid gap-6 md:grid-cols-3">
          <StepCard
            icon={<Camera className="h-5 w-5" />}
            step={1}
            title="Open the dApp"
            body="Go to the Virtuals Protocol Agent Control Panel and select Sigma Boy."
          />
          <StepCard
            icon={<Sparkles className="h-5 w-5" />}
            step={2}
            title="Upload a selfie"
            body="Use even lighting and a neutral expression for best results."
          />
          <StepCard
            icon={<Wand2 className="h-5 w-5" />}
            step={3}
            title="Get your report"
            body="Receive a prioritized Looksmaxxing report with next steps."
          />
        </div>
      </section>

      {/* Features (optional extra) */}
      <section id="features" className="container mx-auto px-4 pb-20">
        <h2 className="mb-8 text-3xl font-bold tracking-tight md:text-4xl">What’s inside the report</h2>
        <div className="grid gap-6 lg:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle>Facial cues</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground space-y-2">
              <div>• Symmetry hints</div>
              <div>• Proportions & angles</div>
              <div>• Feature highlights</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Grooming & skincare</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground space-y-2">
              <div>• Brow & beard tips</div>
              <div>• Routine suggestions</div>
              <div>• Product‑type guidance</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Style & lifestyle</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground space-y-2">
              <div>• Haircuts that fit</div>
              <div>• Glasses & accessories</div>
              <div>• Sleep & nutrition nudges</div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-10">
        <div className="container mx-auto flex flex-col items-center justify-between gap-4 px-4 text-sm text-muted-foreground md:flex-row">
          <div className="flex items-center gap-2">
            <div className="grid h-7 w-7 place-items-center rounded-xl bg-foreground/10 text-sm font-bold">Σ</div>
            <span>Sigma Boy • Looksmaxxing AI Agent</span>
          </div>
          <div className="flex items-center gap-4">
            <a href="https://app.virtuals.io/acp" target="_blank" rel="noopener noreferrer" className="hover:text-foreground">
              Virtuals Protocol dApp
            </a>
            <a href="https://x.com/sigma_boi_ai" target="_blank" rel="noopener noreferrer" className="hover:text-foreground">
              X Profile
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  body,
}: {
  icon: React.ReactNode;
  title: string;
  body: string;
}) {
  return (
    <Card className="border-muted-foreground/10">
      <CardHeader className="flex flex-row items-center gap-3 space-y-0">
        <div className="grid h-9 w-9 place-items-center rounded-lg bg-muted text-foreground/70">
          {icon}
        </div>
        <CardTitle className="text-base">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground">{body}</p>
      </CardContent>
    </Card>
  );
}

function StepCard({
  icon,
  step,
  title,
  body,
}: {
  icon: React.ReactNode;
  step: number;
  title: string;
  body: string;
}) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center gap-3 space-y-0">
        <div className="grid h-8 w-8 place-items-center rounded-lg bg-primary text-primary-foreground">
          {step}
        </div>
        <CardTitle className="text-base flex items-center gap-2">
          {icon} {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground">{body}</p>
      </CardContent>
    </Card>
  );
}