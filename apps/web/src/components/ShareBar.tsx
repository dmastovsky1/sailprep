"use client";

import { useState } from "react";

type State = "idle" | "working" | "copied" | "error";

/**
 * Share the brief as a PDF (straight into WhatsApp or any app via the phone's share sheet),
 * download it, or copy the link. The link rebuilds the same brief for whoever opens it.
 */
export function ShareBar({ title, filename }: { title: string; filename: string }) {
  const [state, setState] = useState<State>("idle");

  const pdfUrl = () => `/brief/pdf${window.location.search}`;

  async function fetchPdf(): Promise<File> {
    const res = await fetch(pdfUrl());
    if (!res.ok) throw new Error(await res.text());
    return new File([await res.blob()], filename, { type: "application/pdf" });
  }

  async function sharePdf() {
    setState("working");
    try {
      const file = await fetchPdf();
      if (navigator.canShare?.({ files: [file] })) {
        await navigator.share({ files: [file], title });
      } else {
        download(file);
      }
      setState("idle");
    } catch (e) {
      // AbortError means the person closed the share sheet; that's not a failure.
      setState(e instanceof DOMException && e.name === "AbortError" ? "idle" : "error");
    }
  }

  function download(file: File) {
    const url = URL.createObjectURL(file);
    const a = Object.assign(document.createElement("a"), { href: url, download: file.name });
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  async function downloadPdf() {
    setState("working");
    try {
      download(await fetchPdf());
      setState("idle");
    } catch {
      setState("error");
    }
  }

  async function copyLink() {
    await navigator.clipboard.writeText(window.location.href);
    setState("copied");
    setTimeout(() => setState("idle"), 2000);
  }

  const secondary =
    "rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:hover:bg-slate-800";

  return (
    <div className="flex flex-col items-start gap-1 sm:items-end print:hidden">
      <div className="flex flex-wrap gap-2">
        <button
          type="button"
          onClick={sharePdf}
          disabled={state === "working"}
          className="rounded-lg bg-sea-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-sea-700 disabled:opacity-60"
        >
          {state === "working" ? "Making PDF…" : "Share PDF"}
        </button>
        <button
          type="button"
          onClick={downloadPdf}
          disabled={state === "working"}
          className={secondary}
        >
          Download
        </button>
        <button type="button" onClick={copyLink} className={secondary}>
          {state === "copied" ? "Link copied" : "Copy link"}
        </button>
      </div>
      {state === "error" && (
        <p role="alert" className="text-sm text-red-600">
          Couldn&apos;t make the PDF. Try again in a minute.
        </p>
      )}
    </div>
  );
}
