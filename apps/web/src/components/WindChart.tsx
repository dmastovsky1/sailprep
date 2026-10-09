"use client";

import {
  Area,
  CartesianGrid,
  ComposedChart,
  Line,
  ReferenceArea,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { hourLabel } from "@/lib/format";
import type { Hour } from "@/lib/types";

interface Props {
  hours: Hour[];
  heavyAirKt: number;
}

/** Wind and gusts across the day, with the race window shaded. */
export function WindChart({ hours, heavyAirKt }: Props) {
  // Show 7 am to 7 pm: enough context around a typical race day without crowding phones.
  const shown = hours.filter((h) => {
    const hr = Number(h.time.slice(11, 13));
    return hr >= 7 && hr <= 19;
  });
  const data = shown.map((h) => ({
    label: hourLabel(h.time),
    wind: Math.round(h.wind_speed_kt),
    gust: Math.round(h.wind_gust_kt),
    dir: h.direction_label,
  }));
  const inWindow = shown.filter((h) => h.in_race_window);
  const first = inWindow.length ? hourLabel(inWindow[0].time) : null;
  const last = inWindow.length ? hourLabel(inWindow[inWindow.length - 1].time) : null;
  const top = Math.ceil((Math.max(heavyAirKt + 4, ...data.map((d) => d.gust)) + 2) / 5) * 5;
  const ticks = Array.from({ length: top / 5 + 1 }, (_, i) => i * 5);

  return (
    <figure>
      <div className="h-64 w-full sm:h-72">
        <ResponsiveContainer>
          <ComposedChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="currentColor"
              strokeOpacity={0.12}
              vertical={false}
            />
            {first && last && (
              <ReferenceArea
                x1={first}
                x2={last}
                fill="#1b84b3"
                fillOpacity={0.08}
                ifOverflow="visible"
              />
            )}
            <XAxis
              dataKey="label"
              tick={{ fontSize: 12, fill: "currentColor" }}
              tickLine={false}
              axisLine={false}
              interval="preserveStartEnd"
            />
            <YAxis
              domain={[0, top]}
              ticks={ticks}
              tick={{ fontSize: 12, fill: "currentColor" }}
              tickLine={false}
              axisLine={false}
              unit=" kt"
              width={56}
            />
            <Tooltip
              contentStyle={{ borderRadius: 8, fontSize: 13 }}
              formatter={(v: number, name: string) => [
                `${v} kt`,
                name === "wind" ? "Wind" : "Gusts",
              ]}
              labelFormatter={(l, p) => `${l}${p?.[0] ? ` · ${p[0].payload.dir}` : ""}`}
            />
            <Area
              type="monotone"
              dataKey="gust"
              stroke="#94a3b8"
              strokeDasharray="4 3"
              fill="#94a3b8"
              fillOpacity={0.12}
              isAnimationActive={false}
            />
            <Line
              type="monotone"
              dataKey="wind"
              stroke="#1b84b3"
              strokeWidth={2.5}
              dot={false}
              isAnimationActive={false}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      <figcaption className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-500 dark:text-slate-400">
        <span className="flex items-center gap-1.5">
          <span className="inline-block h-0.5 w-4 bg-sea-500" /> Wind
        </span>
        <span className="flex items-center gap-1.5">
          <span className="inline-block h-0.5 w-4 border-t-2 border-dashed border-slate-400" />{" "}
          Gusts
        </span>
        <span className="flex items-center gap-1.5">
          <span className="inline-block h-3 w-4 rounded-sm bg-sea-500/15" /> Race window
        </span>
      </figcaption>
    </figure>
  );
}
