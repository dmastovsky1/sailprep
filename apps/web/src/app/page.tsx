import { PlanForm } from "@/components/PlanForm";
import { getBoatClasses } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function Home() {
  const boats = await getBoatClasses();
  return (
    <div className="mx-auto max-w-xl">
      <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">Your race-day weather brief</h1>
      <p className="mt-3 text-slate-600 dark:text-slate-400">
        Pick a venue, your boat and the race window. Sailprep pulls the forecast and flags what
        changes through the day, with heads-ups for your boat. No account needed.
      </p>
      <div className="mt-8">
        <PlanForm boats={boats} />
      </div>
    </div>
  );
}
