import { Document, Line, Page, Path, Rect, StyleSheet, Svg, Text, View } from "@react-pdf/renderer";

import { clockLabel, hourLabel, longDate, round } from "@/lib/format";
import type { Brief, Hour } from "@/lib/types";

// Built-in Helvetica keeps the file small and needs no font downloads.
const SEA = "#156b93";
const INK = "#0f172a";
const MUTED = "#64748b";
const RULE = "#e2e8f0";

const s = StyleSheet.create({
  page: { padding: 36, paddingBottom: 48, fontFamily: "Helvetica", fontSize: 10, color: INK },
  date: { color: SEA, fontSize: 10, fontFamily: "Helvetica-Bold" },
  title: { fontSize: 20, fontFamily: "Helvetica-Bold", marginTop: 4 },
  sub: { color: MUTED, marginTop: 3 },
  stamp: { color: MUTED, fontSize: 8, marginTop: 6 },
  tiles: { flexDirection: "row", gap: 8, marginTop: 16 },
  tile: { flex: 1, border: `1pt solid ${RULE}`, borderRadius: 6, padding: 8 },
  tileLabel: { fontSize: 7, color: MUTED, textTransform: "uppercase", letterSpacing: 0.5 },
  tileValue: { fontSize: 15, fontFamily: "Helvetica-Bold", marginTop: 3 },
  tileSub: { fontSize: 8, color: MUTED, marginTop: 2 },
  h2: { fontSize: 12, fontFamily: "Helvetica-Bold", marginTop: 18, marginBottom: 6 },
  heads: {
    backgroundColor: "#fffbeb",
    border: "1pt solid #fde68a",
    borderRadius: 6,
    padding: 7,
    marginBottom: 4,
  },
  row: { flexDirection: "row", borderBottom: `0.5pt solid ${RULE}`, paddingVertical: 4 },
  th: { fontSize: 7, color: MUTED, textTransform: "uppercase", fontFamily: "Helvetica-Bold" },
  footer: { position: "absolute", bottom: 24, left: 36, right: 36, fontSize: 7, color: MUTED },
});

const COLS = [0.9, 1, 1, 1.3, 0.8, 0.8];

function TableRow({ cells, header = false }: { cells: string[]; header?: boolean }) {
  return (
    <View style={s.row}>
      {cells.map((c, i) => (
        <Text key={i} style={[{ flex: COLS[i] }, header ? s.th : {}]}>
          {c}
        </Text>
      ))}
    </View>
  );
}

/** Wind (solid) and gusts (dashed) from 7 am to 7 pm, race window shaded. */
function Chart({ hours, heavyAirKt }: { hours: Hour[]; heavyAirKt: number }) {
  const shown = hours.filter((h) => {
    const hr = Number(h.time.slice(11, 13));
    return hr >= 7 && hr <= 19;
  });
  if (shown.length < 2) return null;
  const W = 523,
    H = 150,
    L = 28,
    B = 16,
    T = 6;
  const top =
    Math.ceil((Math.max(heavyAirKt + 4, ...shown.map((h) => h.wind_gust_kt)) + 2) / 5) * 5;
  const x = (i: number) => L + (i / (shown.length - 1)) * (W - L - 14);
  const y = (kt: number) => T + (1 - kt / top) * (H - T - B);
  const path = (key: "wind_speed_kt" | "wind_gust_kt") =>
    shown.map((h, i) => `${i ? "L" : "M"}${x(i).toFixed(1)} ${y(h[key]).toFixed(1)}`).join(" ");
  const inWin = shown.map((h, i) => (h.in_race_window ? i : -1)).filter((i) => i >= 0);
  const ticks = Array.from({ length: top / 5 + 1 }, (_, i) => i * 5);

  return (
    <View>
      <Svg width={W} height={H}>
        {inWin.length > 0 && (
          <Rect
            x={x(inWin[0])}
            y={T}
            width={x(inWin[inWin.length - 1]) - x(inWin[0])}
            height={H - T - B}
            fill="#1b84b3"
            fillOpacity={0.1}
          />
        )}
        {ticks.map((t) => (
          <Line key={t} x1={L} x2={W - 14} y1={y(t)} y2={y(t)} stroke={RULE} strokeWidth={0.5} />
        ))}
        {ticks.map((t) => (
          <Text
            key={`l${t}`}
            x={L - 4}
            y={y(t) + 2.5}
            style={{ fontSize: 7 }}
            fill={MUTED}
            textAnchor="end"
          >
            {String(t)}
          </Text>
        ))}
        {shown.map((h, i) =>
          i % 2 === 0 ? (
            <Text
              key={h.time}
              x={x(i)}
              y={H - 4}
              style={{ fontSize: 7 }}
              fill={MUTED}
              textAnchor="middle"
            >
              {hourLabel(h.time)}
            </Text>
          ) : null,
        )}
        <Path
          d={path("wind_gust_kt")}
          stroke="#94a3b8"
          strokeWidth={1}
          strokeDasharray="3 2"
          fill="none"
        />
        <Path d={path("wind_speed_kt")} stroke={SEA} strokeWidth={2} fill="none" />
      </Svg>
      <Text style={{ fontSize: 7, color: MUTED, marginTop: 2 }}>
        Knots. Solid: wind. Dashed: gusts. Shaded: race window.
      </Text>
    </View>
  );
}

export function BriefDocument({ brief }: { brief: Brief }) {
  const c = brief.conditions;
  const issued = new Date(brief.source.fetched_at).toISOString().slice(0, 16).replace("T", " ");
  const footer = `Sailprep is a planning aid, not a coach. Check official marine forecasts and follow race committee instructions. Forecast: ${brief.source.provider}.`;
  const windowHours = brief.hours.filter((h) => h.in_race_window);

  return (
    <Document title={`Race brief: ${brief.venue.name}, ${longDate(brief.date)}`} author="Sailprep">
      <Page size="A4" style={s.page}>
        <Text style={s.date}>{longDate(brief.date)}</Text>
        <Text style={s.title}>{brief.venue.name}</Text>
        <Text style={s.sub}>
          {brief.boat.name} - racing {clockLabel(brief.start)} to {clockLabel(brief.end)}
        </Text>
        <Text style={s.stamp}>Forecast fetched {issued} UTC. Times are local to the venue.</Text>

        <View style={s.tiles}>
          <View style={s.tile}>
            <Text style={s.tileLabel}>Wind</Text>
            <Text style={s.tileValue}>{`${round(c.wind_min_kt)}–${round(c.wind_max_kt)} kt`}</Text>
            <Text style={s.tileSub}>{`mean ${round(c.wind_mean_kt)} kt`}</Text>
          </View>
          <View style={s.tile}>
            <Text style={s.tileLabel}>Gusts</Text>
            <Text style={s.tileValue}>{`${round(c.gust_max_kt)} kt`}</Text>
            <Text style={s.tileSub}>{`${c.gust_factor.toFixed(1)}× the mean`}</Text>
          </View>
          <View style={s.tile}>
            <Text style={s.tileLabel}>Direction</Text>
            <Text style={s.tileValue}>{c.direction_label}</Text>
            <Text
              style={s.tileSub}
            >{`${round(c.direction_mean_deg)}°, spread ${round(c.direction_spread_deg)}°`}</Text>
          </View>
          <View style={s.tile}>
            <Text style={s.tileLabel}>Air</Text>
            <Text style={s.tileValue}>{`${round(c.temp_min_c)}–${round(c.temp_max_c)}°C`}</Text>
            <Text style={s.tileSub}>
              {c.precipitation_mm >= 0.1 ? `${c.precipitation_mm.toFixed(1)} mm rain` : "dry"}
            </Text>
          </View>
        </View>

        <Text style={s.h2}>Heads-ups</Text>
        {brief.heads_ups.length ? (
          brief.heads_ups.map((n) => (
            <View key={n} style={s.heads}>
              <Text>{n}</Text>
            </View>
          ))
        ) : (
          <Text style={{ color: MUTED }}>Nothing unusual in the forecast for your window.</Text>
        )}

        <Text style={s.h2}>Wind through the day</Text>
        <Chart hours={brief.hours} heavyAirKt={brief.boat.heavy_air_kt} />

        <Text style={s.h2} minPresenceAhead={60}>
          Hour by hour
        </Text>
        <TableRow header cells={["Time", "Wind", "Gusts", "Direction", "Air", "Rain"]} />
        {windowHours.map((h) => (
          <TableRow
            key={h.time}
            cells={[
              hourLabel(h.time),
              `${round(h.wind_speed_kt)} kt`,
              `${round(h.wind_gust_kt)} kt`,
              `${h.direction_label} ${round(h.wind_direction_deg)}°`,
              `${round(h.temperature_c)}°C`,
              h.precipitation_mm ? `${h.precipitation_mm.toFixed(1)} mm` : "–",
            ]}
          />
        ))}
        <Text style={s.footer} fixed>
          {footer}
        </Text>
      </Page>
    </Document>
  );
}
