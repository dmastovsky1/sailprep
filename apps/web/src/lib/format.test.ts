import { describe, expect, it } from "vitest";

import { briefSearch, clockLabel, hourLabel, longDate, parseBriefQuery } from "./format";

describe("briefSearch / parseBriefQuery", () => {
  it("round-trips a brief query, dropping empty coordinates", () => {
    const q = { venue: "Newport", boat: "j70", date: "2026-07-18", start: "11:00", end: "16:00" };
    const s = briefSearch(q);
    expect(s).toBe("venue=Newport&boat=j70&date=2026-07-18&start=11%3A00&end=16%3A00");
    const back = parseBriefQuery(Object.fromEntries(new URLSearchParams(s)));
    expect(back).toEqual({ ...q, lat: undefined, lon: undefined });
  });

  it("rejects a missing or malformed date", () => {
    expect(parseBriefQuery({ venue: "X", boat: "j70" })).toBeNull();
    expect(parseBriefQuery({ venue: "X", boat: "j70", date: "18/07/2026" })).toBeNull();
  });

  it("defaults the race window", () => {
    expect(parseBriefQuery({ venue: "X", boat: "j70", date: "2026-07-18" })).toMatchObject({
      start: "11:00",
      end: "16:00",
    });
  });
});

describe("time labels", () => {
  it.each([
    ["2026-07-18T00:00", "12 am"],
    ["2026-07-18T09:00", "9 am"],
    ["2026-07-18T12:00", "noon"],
    ["2026-07-18T14:00", "2 pm"],
  ])("hourLabel(%s) = %s", (iso, label) => expect(hourLabel(iso)).toBe(label));

  it("clockLabel keeps minutes only when present", () => {
    expect(clockLabel("14:00:00")).toBe("2 pm");
    expect(clockLabel("14:30")).toBe("2:30 pm");
    expect(clockLabel("12:15")).toBe("12:15 pm");
  });

  it("longDate does not drift across timezones", () => {
    expect(longDate("2026-07-18")).toBe("Saturday 18 July 2026");
  });
});

describe("pdfFilename", async () => {
  const { pdfFilename } = await import("./pdf/filename");
  it("slugs the first part of the venue name", () => {
    const brief = { venue: { name: "Newport, Rhode Island, United States" }, date: "2026-07-18" };
    expect(pdfFilename(brief as never)).toBe("sailprep-newport-2026-07-18.pdf");
  });
  it("falls back when the name has no usable characters", () => {
    expect(pdfFilename({ venue: { name: "???" }, date: "2026-07-18" } as never)).toBe(
      "sailprep-brief-2026-07-18.pdf",
    );
  });
});
