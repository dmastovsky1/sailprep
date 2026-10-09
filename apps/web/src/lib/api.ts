import { briefSearch } from "./format";
import type { BoatClass, Brief, BriefQuery } from "./types";

// Server-side calls go straight to the API; the browser uses the /api/v1 rewrite instead.
const API_URL = process.env.SAILPREP_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

async function get<T>(path: string, revalidate: number): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, { next: { revalidate } });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const detail = typeof body.detail === "string" ? body.detail : res.statusText;
    throw new ApiError(res.status, detail);
  }
  return res.json() as Promise<T>;
}

export function getBoatClasses(): Promise<BoatClass[]> {
  return get("/api/v1/boat-classes", 3600);
}

/** Forecasts refresh hourly at most, so a brief is cached for 10 minutes. */
export function getBrief(q: BriefQuery): Promise<Brief> {
  return get(`/api/v1/brief?${briefSearch(q)}`, 600);
}
