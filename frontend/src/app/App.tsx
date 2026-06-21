import { BrowserRouter, Link, NavLink, Route, Routes } from "react-router-dom";
import { Compass, FlaskConical, History, MapPinned, ShieldCheck } from "lucide-react";
import { PlannerWorkspace } from "../features/planner/PlannerWorkspace";
import { MethodologyPage } from "../features/static/MethodologyPage";
import { SavedTripsPage } from "../features/trips/SavedTripsPage";

function Shell() {
  return (
    <div className="min-h-screen bg-paper">
      <header className="sticky top-0 z-40 border-b border-ink/10 bg-paper/92 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6">
          <Link to="/" className="flex items-center gap-2 font-semibold text-ink">
            <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-leaf text-white">
              <Compass size={20} aria-hidden="true" />
            </span>
            <span>TravelAgenticAI</span>
          </Link>
          <nav aria-label="Primary" className="flex items-center gap-1 text-sm">
            {[
              ["/", "Planner", MapPinned],
              ["/trips", "Saved", History],
              ["/methodology", "Method", FlaskConical],
            ].map(([to, label, Icon]) => (
              <NavLink
                key={to as string}
                to={to as string}
                className={({ isActive }) =>
                  `inline-flex items-center gap-2 rounded-md px-3 py-2 ${
                    isActive ? "bg-ink text-white" : "text-ink/70 hover:bg-white"
                  }`
                }
              >
                <Icon size={16} aria-hidden="true" />
                <span className="hidden sm:inline">{label as string}</span>
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <Routes>
        <Route path="/" element={<PlannerWorkspace />} />
        <Route path="/trips" element={<SavedTripsPage />} />
        <Route path="/methodology" element={<MethodologyPage />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </div>
  );
}

function NotFound() {
  return (
    <main className="mx-auto flex max-w-3xl flex-col items-start gap-4 px-4 py-16">
      <div className="rounded-lg bg-white p-3 text-clay shadow-soft">
        <ShieldCheck aria-hidden="true" />
      </div>
      <h1 className="text-3xl font-semibold text-ink">Page not found</h1>
      <p className="text-ink/70">The planner, saved trips, and methodology pages are available from the top navigation.</p>
      <Link className="rounded-md bg-leaf px-4 py-2 text-sm font-semibold text-white" to="/">
        Open planner
      </Link>
    </main>
  );
}

export function App() {
  return (
    <BrowserRouter future={{ v7_relativeSplatPath: true, v7_startTransition: true }}>
      <Shell />
    </BrowserRouter>
  );
}
