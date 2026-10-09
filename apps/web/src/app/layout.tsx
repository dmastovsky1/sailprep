import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import Link from "next/link";

import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: { default: "Sailprep", template: "%s · Sailprep" },
  description: "Race-day weather briefs for sailors. A forecaster, not a coach.",
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#f8fafc" },
    { media: "(prefers-color-scheme: dark)", color: "#020617" },
  ],
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="min-h-dvh font-sans">
        <header className="border-b border-slate-200 bg-white/80 backdrop-blur dark:border-slate-800 dark:bg-slate-900/80 print:hidden">
          <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-3">
            <Link href="/" className="flex items-center gap-2 font-semibold tracking-tight">
              <span aria-hidden className="text-sea-500">
                <svg viewBox="0 0 24 24" className="h-6 w-6" fill="currentColor">
                  <path d="M11 2 4 16h7V2Zm2 3v11h6L13 5ZM3 18h18l-2 3H5l-2-3Z" />
                </svg>
              </span>
              Sailprep
            </Link>
            <span className="text-sm text-slate-500 dark:text-slate-400">
              Race-day weather briefs
            </span>
          </div>
        </header>
        <main className="mx-auto max-w-4xl px-4 py-6 sm:py-10">{children}</main>
        <footer className="mx-auto max-w-4xl px-4 pb-10 text-xs text-slate-500 dark:text-slate-400 print:hidden">
          Sailprep is a planning aid. Always check official marine forecasts and follow race
          committee instructions. Forecast data from{" "}
          <a className="underline" href="https://open-meteo.com">
            Open-Meteo
          </a>
          .
        </footer>
      </body>
    </html>
  );
}
