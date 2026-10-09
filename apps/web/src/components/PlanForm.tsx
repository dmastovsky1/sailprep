"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { briefSearch } from "@/lib/format";
import type { BoatClass, BoatType, Venue } from "@/lib/types";

import { VenuePicker } from "./VenuePicker";

const TYPE_LABELS: Record<BoatType, string> = {
  dinghy: "Dinghies",
  foiler: "Foilers",
  keelboat: "Keelboats",
};

const field =
  "w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 shadow-sm outline-none focus:border-sea-500 focus:ring-2 focus:ring-sea-500/30 dark:border-slate-700 dark:bg-slate-900";

function today(): string {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

export function PlanForm({ boats }: { boats: BoatClass[] }) {
  const router = useRouter();
  const [venue, setVenue] = useState<Venue | null>(null);
  const [boat, setBoat] = useState("");
  const [date, setDate] = useState(today);
  const [start, setStart] = useState("11:00");
  const [end, setEnd] = useState("16:00");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const groups = (Object.keys(TYPE_LABELS) as BoatType[]).map((t) => ({
    type: t,
    boats: boats.filter((b) => b.type === t),
  }));

  function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!venue) return setError("Pick a venue from the list.");
    if (!boat) return setError("Choose your boat.");
    if (end <= start) return setError("The race window must end after it starts.");
    setError(null);
    setBusy(true);
    router.push(
      `/brief?${briefSearch({
        venue: venue.name,
        lat: venue.latitude.toFixed(4),
        lon: venue.longitude.toFixed(4),
        boat,
        date,
        start,
        end,
      })}`,
    );
  }

  return (
    <form
      onSubmit={submit}
      className="space-y-5 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6 dark:border-slate-800 dark:bg-slate-900"
    >
      <div>
        <label htmlFor="venue" className="mb-1.5 block text-sm font-medium">
          Venue
        </label>
        <VenuePicker onSelect={setVenue} />
      </div>

      <div>
        <label htmlFor="boat" className="mb-1.5 block text-sm font-medium">
          Boat
        </label>
        <select id="boat" value={boat} onChange={(e) => setBoat(e.target.value)} className={field}>
          <option value="" disabled>
            Choose your class
          </option>
          {groups.map((g) => (
            <optgroup key={g.type} label={TYPE_LABELS[g.type]}>
              {g.boats.map((b) => (
                <option key={b.key} value={b.key}>
                  {b.name}
                </option>
              ))}
            </optgroup>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div>
          <label htmlFor="date" className="mb-1.5 block text-sm font-medium">
            Race day
          </label>
          <input
            id="date"
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className={field}
            required
          />
        </div>
        <div>
          <label htmlFor="start" className="mb-1.5 block text-sm font-medium">
            First warning
          </label>
          <input
            id="start"
            type="time"
            step={900}
            value={start}
            onChange={(e) => setStart(e.target.value)}
            className={field}
            required
          />
        </div>
        <div>
          <label htmlFor="end" className="mb-1.5 block text-sm font-medium">
            Last finish
          </label>
          <input
            id="end"
            type="time"
            step={900}
            value={end}
            onChange={(e) => setEnd(e.target.value)}
            className={field}
            required
          />
        </div>
      </div>

      {error && (
        <p role="alert" className="text-sm text-red-600">
          {error}
        </p>
      )}

      <button
        type="submit"
        disabled={busy}
        className="w-full rounded-lg bg-sea-600 px-4 py-3 font-semibold text-white shadow-sm transition hover:bg-sea-700 disabled:opacity-60"
      >
        {busy ? "Building your brief…" : "Get the brief"}
      </button>
    </form>
  );
}
