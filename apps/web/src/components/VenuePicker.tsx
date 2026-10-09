"use client";

import { useEffect, useId, useRef, useState } from "react";

import type { Venue } from "@/lib/types";

interface Props {
  onSelect: (venue: Venue | null) => void;
}

/** Type a place name, pick from up to five matches. */
export function VenuePicker({ onSelect }: Props) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Venue[]>([]);
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);
  const [status, setStatus] = useState<"idle" | "loading" | "error">("idle");
  const chosen = useRef<string | null>(null);
  const listId = useId();

  useEffect(() => {
    const q = query.trim();
    if (q.length < 2 || q === chosen.current) {
      setResults([]);
      return;
    }
    const ctrl = new AbortController();
    const timer = setTimeout(async () => {
      setStatus("loading");
      try {
        const res = await fetch(`/api/v1/venues/search?q=${encodeURIComponent(q)}`, {
          signal: ctrl.signal,
        });
        if (!res.ok) throw new Error(String(res.status));
        setResults(await res.json());
        setActive(0);
        setOpen(true);
        setStatus("idle");
      } catch {
        if (!ctrl.signal.aborted) setStatus("error");
      }
    }, 250);
    return () => {
      clearTimeout(timer);
      ctrl.abort();
    };
  }, [query]);

  function choose(v: Venue) {
    chosen.current = v.name;
    setQuery(v.name);
    setOpen(false);
    onSelect(v);
  }

  return (
    <div className="relative">
      <input
        id="venue"
        type="text"
        role="combobox"
        aria-expanded={open && results.length > 0}
        aria-controls={listId}
        aria-autocomplete="list"
        autoComplete="off"
        placeholder="e.g. Newport, Cowes, Lake Garda"
        value={query}
        onChange={(e) => {
          chosen.current = null;
          setQuery(e.target.value);
          onSelect(null);
        }}
        onFocus={() => results.length && setOpen(true)}
        onBlur={() => setTimeout(() => setOpen(false), 120)}
        onKeyDown={(e) => {
          if (!open || !results.length) return;
          if (e.key === "ArrowDown") {
            e.preventDefault();
            setActive((a) => Math.min(a + 1, results.length - 1));
          } else if (e.key === "ArrowUp") {
            e.preventDefault();
            setActive((a) => Math.max(a - 1, 0));
          } else if (e.key === "Enter") {
            e.preventDefault();
            choose(results[active]);
          } else if (e.key === "Escape") {
            setOpen(false);
          }
        }}
        className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 shadow-sm outline-none focus:border-sea-500 focus:ring-2 focus:ring-sea-500/30 dark:border-slate-700 dark:bg-slate-900"
      />
      {status === "loading" && (
        <span className="absolute top-3 right-3 text-xs text-slate-400">Searching…</span>
      )}
      {status === "error" && (
        <p className="mt-1 text-sm text-red-600">Place search is unavailable. Try again shortly.</p>
      )}
      {open && results.length > 0 && (
        <ul
          id={listId}
          role="listbox"
          className="absolute z-10 mt-1 w-full overflow-hidden rounded-lg border border-slate-200 bg-white shadow-lg dark:border-slate-700 dark:bg-slate-900"
        >
          {results.map((v, i) => (
            <li
              key={`${v.latitude},${v.longitude}`}
              role="option"
              aria-selected={i === active}
              onMouseDown={() => choose(v)}
              onMouseEnter={() => setActive(i)}
              className={`cursor-pointer px-3 py-2 text-sm ${
                i === active ? "bg-sea-50 dark:bg-sea-900" : ""
              }`}
            >
              {v.name}
              <span className="ml-2 text-xs text-slate-400">
                {v.latitude.toFixed(2)}, {v.longitude.toFixed(2)}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
