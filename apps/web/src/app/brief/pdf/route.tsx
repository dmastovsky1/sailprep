import { renderToBuffer } from "@react-pdf/renderer";

import { ApiError, getBrief } from "@/lib/api";
import { parseBriefQuery } from "@/lib/format";
import { BriefDocument } from "@/lib/pdf/BriefDocument";
import { pdfFilename } from "@/lib/pdf/filename";

export const runtime = "nodejs";

/** GET /brief/pdf?<same query as the brief page> -> the brief as a two-page PDF. */
export async function GET(request: Request) {
  const q = parseBriefQuery(Object.fromEntries(new URL(request.url).searchParams));
  if (!q) return new Response("A brief needs a venue, a boat and a date.", { status: 400 });
  try {
    const brief = await getBrief(q);
    const pdf = await renderToBuffer(<BriefDocument brief={brief} />);
    return new Response(new Uint8Array(pdf), {
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition": `inline; filename="${pdfFilename(brief)}"`,
        "Cache-Control": "private, max-age=600",
      },
    });
  } catch (e) {
    const status = e instanceof ApiError && e.status < 500 ? e.status : 502;
    const message = e instanceof Error ? e.message : "Could not build the PDF";
    return new Response(message, { status });
  }
}
