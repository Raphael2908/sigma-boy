"use client";

import React, { useCallback, useMemo, useRef, useState } from "react";
import Head from "next/head";
import Link from "next/link";
import Image from "next/image";
import { Upload, Loader2, ImageIcon, Wand2, Link as LinkIcon, AlertCircle } from "lucide-react";

// shadcn/ui components (ensure you've installed them)
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

// ---- Types ----
interface ApiSuccess {
  id: string; // unique ID for the report
  imageUrl: string; // URL for the generated/returned image (or base64 data URL)
  // The API also returns a huge ~500-page report text/file, but we DO NOT render it here.
}

interface ApiError {
  message: string;
}

// ---- Helper: Call the API endpoint ----
// Expects an endpoint at /api/analyze that accepts multipart/form-data with fields:
// - file: the uploaded image (File)
// - prompt: the user's text prompt (string)
// and returns JSON: { id: string, imageUrl: string, report: string | undefined }
async function callAnalyzeApi(params: { file: File; prompt: string }): Promise<ApiSuccess> {
  const form = new FormData();
  form.append("image", params.file);
  form.append("prompt", params.prompt);

  const res = await fetch("http://127.0.0.1:8000/call/buyer", {
    method: "POST",
    body: form,
  });

  if (!res.ok) {
    // Try to parse API error shape
    let message = `Request failed with status ${res.status}`;
    try {
      const payload: ApiError = await res.json();
      if (payload?.message) message = payload.message;
    } catch (exception) {console.log(exception);}
    throw new Error(message);
  }

  const data = (await res.json()) as { id: string; imageUrl?: string; report?: unknown };
  if (!data?.id) throw new Error("Malformed API response: missing id");

  // Prefer explicit URL string; if API returns a Blob or base64, ensure it's a string
  const imageUrl = typeof data.imageUrl === "string" ? data.imageUrl : "";
  return { id: data.id, imageUrl };
}

// ---- Page Component ----
export default function TrySigmaBoyPage() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>("");
  const [prompt, setPrompt] = useState<string>("");
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [result, setResult] = useState<ApiSuccess | null>(null);

  const inputRef = useRef<HTMLInputElement | null>(null);

  // Derived label for the upload button
  const fileLabel = useMemo(() => (file ? file.name : "Upload a photo"), [file]);

  const openFilePicker = useCallback(() => inputRef.current?.click(), []);

  const onFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (!f) return;
    setFile(f);
    setResult(null);
    setError("");

    // preview
    const url = URL.createObjectURL(f);
    setPreviewUrl(url);
  }, []);

  const onDrop = useCallback((e: React.DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    e.stopPropagation();
    const f = e.dataTransfer.files?.[0];
    if (f) {
      setFile(f);
      setResult(null);
      setError("");
      const url = URL.createObjectURL(f);
      setPreviewUrl(url);
    }
  }, []);

  const onDragOver = useCallback((e: React.DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const onSubmit = useCallback(async () => {
    if (!file) {
      setError("Please upload a photo.");
      return;
    }
    if (!prompt.trim()) {
      setError("Please enter a prompt.");
      return;
    }

    try {
      setSubmitting(true);
      setError("");
      setResult(null);
      const data = await callAnalyzeApi({ file, prompt });
      setResult(data);
    } catch (err) {
      console.log(err);
      setError("Something went wrong.");
    } finally {
      setSubmitting(false);
    }
  }, [file, prompt]);

  return (
    <>
      <Head>
        <title>Try Sigma boy</title>
        <meta name="description" content="Modern AI chat UI that analyzes an image + prompt and returns a report." />
      </Head>

      <div className="min-h-screen bg-gradient-to-b from-background to-muted/30">
        <div className="container mx-auto max-w-5xl px-4 py-10">
          <header className="mb-8 flex flex-col gap-2">
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="rounded-2xl px-3 py-1 text-xs">experimental</Badge>
            </div>
            <h1 className="text-3xl font-semibold tracking-tight">Try Sigma boy</h1>
            <p className="text-muted-foreground">Upload a photo, enter a prompt, and get back an analyzed image plus a link to your full (~500-page) report.</p>
          </header>

          <div className="grid grid-cols-1 gap-6 lg:grid-cols-5">
            {/* Left: Composer */}
            <div className="lg:col-span-3">
              <Card className="border-l-4 border-l-primary/60">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2"><Wand2 className="h-5 w-5" /> Compose</CardTitle>
                  <CardDescription>Attach a photo and describe what you want analyzed. Then hit Generate.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Upload */}
                  <div className="space-y-2">
                    <Label htmlFor="file">Photo</Label>
                    <input ref={inputRef} id="file" type="file" accept="image/*" className="hidden" onChange={onFileChange} />
                    <Label
                      onDrop={onDrop}
                      onDragOver={onDragOver}
                      htmlFor="file"
                      className="flex h-36 cursor-pointer flex-col items-center justify-center gap-2 rounded-2xl border border-dashed bg-card/60 p-4 text-center transition hover:bg-accent/40"
                    >
                      <Upload className="h-6 w-6" />
                      <span className="text-sm text-muted-foreground">Drag & drop an image here, or click to browse</span>
                      <Button size="sm" variant="secondary" type="button" onClick={openFilePicker}>
                        {file ? "Change photo" : "Choose photo"}
                      </Button>
                      {file && <span className="text-xs text-muted-foreground">{fileLabel}</span>}
                    </Label>
                  </div>

                  {/* Prompt */}
                  <div className="space-y-2">
                    <Label htmlFor="prompt">Prompt</Label>
                    <Textarea
                      id="prompt"
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                      placeholder="Describe what Sigma boy should analyze…"
                      className="min-h-[120px] resize-y"
                    />
                  </div>
                </CardContent>
                <CardFooter className="flex items-center justify-between gap-3">
                  <div className="text-xs text-muted-foreground">We’ll generate a link to your full report after processing.</div>
                  <Button onClick={onSubmit} disabled={submitting} className="gap-2">
                    {submitting ? (<><Loader2 className="h-4 w-4 animate-spin" /> Generating…</>) : (<><Wand2 className="h-4 w-4" /> Generate</>)}
                  </Button>
                </CardFooter>
              </Card>

              {error && (
                <div className="mt-4">
                  <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertTitle>Something went wrong</AlertTitle>
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                </div>
              )}
            </div>

            {/* Right: Preview & Result */}
            <div className="lg:col-span-2 space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2"><ImageIcon className="h-5 w-5" /> Preview</CardTitle>
                  <CardDescription>Your uploaded image appears here.</CardDescription>
                </CardHeader>
                <CardContent>
                  {previewUrl ? (
                    <div className="relative aspect-[4/3] w-full overflow-hidden rounded-xl border">
                      <Image src={previewUrl} alt="Selected preview" fill className="object-cover" />
                    </div>
                  ) : (
                    <div className="flex aspect-[4/3] w-full items-center justify-center rounded-xl border text-muted-foreground">
                      No image selected
                    </div>
                  )}
                </CardContent>
              </Card>

              <Card className="border-primary/40">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2"><LinkIcon className="h-5 w-5" /> Result</CardTitle>
                  <CardDescription>Once processed, you’ll get a link to your full report.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {submitting && (
                    <div className="text-sm text-muted-foreground">Processing your request…</div>
                  )}
                  {!submitting && !result && (
                    <div className="text-sm text-muted-foreground">No result yet. Submit a photo and prompt to begin.</div>
                  )}

                  {result && (
                    <div className="space-y-3">
                      {result.imageUrl ? (
                        <div className="relative aspect-[4/3] w-full overflow-hidden rounded-xl border">
                          <Image src={result.imageUrl} alt="API returned image" fill className="object-cover" />
                        </div>
                      ) : (
                        <div className="text-sm text-muted-foreground">(No image preview returned.)</div>
                      )}

                      <Separator />
                      <div className="space-y-1">
                        <div className="text-sm">Report ID</div>
                        <code className="rounded-md bg-muted px-2 py-1 text-xs">{result.id}</code>
                        <div>
                          {/* Requirement #1: Display a link using the unique ID for the user to check out their report. */}
                          <Link href={`/report/${result.id}`} className="text-primary underline underline-offset-4">
                            View your full (~500-page) report
                          </Link>
                        </div>
                      </div>
                    </div>
                  )}
                </CardContent>
                <CardFooter className="justify-end">
                  {/* Optional secondary action: copy link */}
                  {result && (
                    <CopyLinkButton id={result.id} />
                  )}
                </CardFooter>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

function CopyLinkButton({ id }: { id: string }) {
  const [copied, setCopied] = useState(false);
  const link = useMemo(() => `${typeof window !== "undefined" ? window.location.origin : ""}/report/${id}`,[id]);

  const onCopy = async () => {
    try {
      await navigator.clipboard.writeText(link);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {}
  };

  return (
    <Button variant="outline" size="sm" onClick={onCopy}>
      {copied ? "Copied!" : "Copy report link"}
    </Button>
  );
}
