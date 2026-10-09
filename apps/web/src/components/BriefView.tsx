import { clockLabel, hourLabel, longDate, round } from "@/lib/format";
import type { Brief } from "@/lib/types";

import { pdfFilename } from "@/lib/pdf/filename";

import { ShareBar } from "./ShareBar";
import { WindArrow } from "./WindArrow";
import { WindChart } from "./WindChart";

function Tile({ label, value, sub }: { label: string; value: React.ReactNode; sub?: string }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900">
      <div className="text-xs font-medium tracking-wide text-slate-500 uppercase dark:text-slate-400">
        {label}
      </div>
      <div className="mt-1 text-2xl font-semibold tabular-nums">{value}</div>
      {sub && <div className="mt-0.5 text-sm text-slate-500 dark:text-slate-400">{sub}</div>}
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mt-8">
      <h2 className="mb-3 text-lg font-semibold">{title}</h2>
      {children}
    </section>
  );
}

export function BriefView({ brief }: { brief: Brief }) {
  const c = brief.conditions;
  const windowHours = brief.hours.filter((h) => h.in_race_window);
  const issued = new Date(brief.source.fetched_at).toLocaleString("en-GB", {
    dateStyle: "medium",
    timeStyle: "short",
  });

  return (
    <article>
      <header className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-sm font-medium text-sea-600 dark:text-sea-100">
            {longDate(brief.date)}
          </p>
          <h1 className="mt-1 text-2xl font-bold tracking-tight sm:text-3xl">{brief.venue.name}</h1>
          <p className="mt-1 text-slate-600 dark:text-slate-400">
            {brief.boat.name} · racing {clockLabel(brief.start)} to {clockLabel(brief.end)}
          </p>
        </div>
        <ShareBar
          title={`Race brief: ${brief.venue.name}, ${longDate(brief.date)}`}
          filename={pdfFilename(brief)}
        />
      </header>

      <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <Tile
          label="Wind"
          value={`${round(c.wind_min_kt)}–${round(c.wind_max_kt)} kt`}
          sub={`mean ${round(c.wind_mean_kt)} kt`}
        />
        <Tile
          label="Gusts"
          value={`${round(c.gust_max_kt)} kt`}
          sub={`${c.gust_factor.toFixed(1)}× the mean`}
        />
        <Tile
          label="Direction"
          value={
            <span className="flex items-center gap-2">
              <WindArrow deg={c.direction_mean_deg} className="h-5 w-5 text-sea-500" />
              {c.direction_label}
            </span>
          }
          sub={`${round(c.direction_mean_deg)}°, spread ${round(c.direction_spread_deg)}°`}
        />
        <Tile
          label="Air"
          value={`${round(c.temp_min_c)}–${round(c.temp_max_c)}°C`}
          sub={c.precipitation_mm >= 0.1 ? `${c.precipitation_mm.toFixed(1)} mm rain` : "dry"}
        />
      </div>

      <Section title="Heads-ups">
        {brief.heads_ups.length ? (
          <ul className="space-y-2">
            {brief.heads_ups.map((n) => (
              <li
                key={n}
                className="flex gap-3 rounded-xl border border-amber-200 bg-amber-50 p-3 text-sm leading-relaxed dark:border-amber-900/60 dark:bg-amber-950/40"
              >
                <span aria-hidden className="mt-0.5 text-amber-600">
                  ●
                </span>
                {n}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Nothing unusual in the forecast for your window.
          </p>
        )}
      </Section>

      <Section title="Wind through the day">
        <div className="rounded-xl border border-slate-200 bg-white p-4 text-slate-500 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-400">
          <WindChart hours={brief.hours} heavyAirKt={brief.boat.heavy_air_kt} />
        </div>
      </Section>

      <Section title="Hour by hour">
        <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
          <table className="w-full text-sm whitespace-nowrap tabular-nums">
            <thead className="bg-slate-50 text-left text-xs text-slate-500 uppercase dark:bg-slate-800/60 dark:text-slate-400">
              <tr>
                <th className="px-3 py-2 font-medium">Time</th>
                <th className="px-3 py-2 font-medium">Wind</th>
                <th className="px-3 py-2 font-medium">Gusts</th>
                <th className="px-3 py-2 font-medium">Direction</th>
                <th className="px-3 py-2 font-medium">Air</th>
                <th className="px-3 py-2 font-medium">Rain</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {windowHours.map((h) => (
                <tr key={h.time}>
                  <td className="px-3 py-2 font-medium">{hourLabel(h.time)}</td>
                  <td className="px-3 py-2">{round(h.wind_speed_kt)} kt</td>
                  <td className="px-3 py-2">{round(h.wind_gust_kt)} kt</td>
                  <td className="px-3 py-2">
                    <span className="flex items-center gap-1.5">
                      <WindArrow deg={h.wind_direction_deg} className="h-4 w-4 text-sea-500" />
                      {h.direction_label} {round(h.wind_direction_deg)}°
                    </span>
                  </td>
                  <td className="px-3 py-2">{round(h.temperature_c)}°C</td>
                  <td className="px-3 py-2">
                    {h.precipitation_mm ? `${h.precipitation_mm.toFixed(1)} mm` : "–"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>

      <p className="mt-6 text-xs text-slate-500 dark:text-slate-400">
        Forecast from {brief.source.provider}, fetched {issued}. Times are local to the venue.
        Sailprep is a forecaster, not a coach: heads-ups describe the weather, not how to sail it.
      </p>
    </article>
  );
}
