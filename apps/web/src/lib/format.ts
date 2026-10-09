import type { BriefQuery } from "./types";

const BRIEF_KEYS = ["venue", "boat", "date", "start", "end", "lat", "lon"] as const;

/** Query string shared by the brief page URL and the API call, so a link is the brief. */
export function briefSearch(q: BriefQuery): string {
  const params = new URLSearchParams();
  for (const key of BRIEF_KEYS) {
    const value = q[key];
    if (value) params.set(key, value);
  }
  return params.toString();
}

/** Read a brief query from page search params; null if anything required is missing. */
export function parseBriefQuery(
  sp: Record<string, string | string[] | undefined>,
): BriefQuery | null {
  const get = (k: string) => {
    const v = sp[k];
    return Array.isArray(v) ? v[0] : v;
  };
  const venue = get("venue");
  const boat = get("boat");
  const date = get("date");
  if (!venue || !boat || !date || !/^\d{4}-\d{2}-\d{2}$/.test(date)) return null;
  return {
    venue,
    boat,
    date,
    start: get("start") ?? "11:00",
    end: get("end") ?? "16:00",
    lat: get("lat"),
    lon: get("lon"),
  };
}

/** "2026-07-18T14:00:00" -> "2 pm". Times are already venue-local from the API. */
export function hourLabel(iso: string): string {
  const h = Number(iso.slice(11, 13));
  if (h === 0) return "12 am";
  if (h === 12) return "noon";
  return h < 12 ? `${h} am` : `${h - 12} pm`;
}

/** "14:00:00" or "14:00" -> "2 pm"; keeps minutes when they matter ("2:30 pm"). */
export function clockLabel(t: string): string {
  const [h, m] = t.split(":").map(Number);
  const base = hourLabel(`0000-00-00T${String(h).padStart(2, "0")}`);
  if (!m) return base;
  const [num, suffix] = base === "noon" ? ["12", "pm"] : base.split(" ");
  return `${num}:${String(m).padStart(2, "0")} ${suffix}`;
}

const WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const MONTHS = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

/** "2026-07-18" -> "Saturday 18 July 2026", identical on server and browser in any timezone. */
export function longDate(d: string): string {
  const [y, m, day] = d.split("-").map(Number);
  const weekday = WEEKDAYS[new Date(Date.UTC(y, m - 1, day)).getUTCDay()];
  return `${weekday} ${day} ${MONTHS[m - 1]} ${y}`;
}

export const round = (n: number) => Math.round(n);
