# Sailprep web

Next.js app for planning a race and reading the brief. It talks only to the Sailprep API: server components call it directly, and the browser reaches it through the `/api/v1/*` rewrite in `next.config.ts`.

## Run it

Start the API first (see [apps/api](../api/README.md)), then:

```bash
cd apps/web
npm install
SAILPREP_API_URL=http://localhost:8000 npm run dev
```

Open http://localhost:3000. Or run the whole stack with `docker compose up --build` from the repo root.

## Pages

| Path                                                     | What it shows                                                                                                                        |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `/`                                                      | Venue search, boat, race day and window                                                                                              |
| `/brief?venue=…&boat=…&date=…&start=…&end=…&lat=…&lon=…` | The brief: conditions at a glance, timed heads-ups, wind chart with the race window shaded, hour by hour. The URL is the share link. |

## Checks

```bash
npm run lint && npm run typecheck && npm run format:check && npm test && npm run build
```
