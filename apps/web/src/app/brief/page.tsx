import type { Metadata } from "next";
import Link from "next/link";

import { BriefView } from "@/components/BriefView";
import { ApiError, getBrief } from "@/lib/api";
import { longDate, parseBriefQuery } from "@/lib/format";

type SearchParams = Promise<Record<string, string | string[] | undefined>>;

export async function generateMetadata({
  searchParams,
}: {
  searchParams: SearchParams;
}): Promise<Metadata> {
  const q = parseBriefQuery(await searchParams);
  return { title: q ? `${q.venue}, ${longDate(q.date)}` : "Race brief" };
}

function Problem({ title, detail }: { title: string; detail: string }) {
  return (
    <div className="mx-auto max-w-xl rounded-2xl border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900">
      <h1 className="text-xl font-semibold">{title}</h1>
      <p className="mt-2 text-slate-600 dark:text-slate-400">{detail}</p>
      <Link href="/" className="mt-4 inline-block font-medium text-sea-600 underline">
        Plan another brief
      </Link>
    </div>
  );
}

export default async function BriefPage({ searchParams }: { searchParams: SearchParams }) {
  const q = parseBriefQuery(await searchParams);
  if (!q) {
    return (
      <Problem
        title="That link is missing something"
        detail="A brief needs a venue, a boat and a date."
      />
    );
  }
  try {
    const brief = await getBrief(q);
    return <BriefView brief={brief} />;
  } catch (e) {
    if (e instanceof ApiError && e.status < 500) {
      return <Problem title="We couldn't build that brief" detail={e.message} />;
    }
    return (
      <Problem
        title="The forecast is unavailable right now"
        detail="The forecast provider didn't respond. Try again in a minute."
      />
    );
  }
}
