import type { Brief } from "@/lib/types";

/** "Newport, Rhode Island, United States" + date -> "sailprep-newport-2026-07-18.pdf" */
export function pdfFilename(brief: Brief): string {
  const place = brief.venue.name
    .split(",")[0]
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
  return `sailprep-${place || "brief"}-${brief.date}.pdf`;
}
