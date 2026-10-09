"use client";

import { useState } from "react";

/** Share or copy the link to this brief. The link rebuilds the same brief for whoever opens it. */
export function ShareBar({ title }: { title: string }) {
  const [copied, setCopied] = useState(false);

  async function share() {
    const url = window.location.href;
    if (navigator.share) {
      try {
        await navigator.share({ title, url });
        return;
      } catch {
        // User cancelled or share failed; fall back to copying.
      }
    }
    await navigator.clipboard.writeText(url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="flex gap-2 print:hidden">
      <button
        type="button"
        onClick={share}
        className="rounded-lg bg-sea-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-sea-700"
      >
        {copied ? "Link copied" : "Share brief"}
      </button>
    </div>
  );
}
