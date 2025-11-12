import React, { useState } from "react";
import PlannerForm from "./components/PlannerForm";
import AgentProgress from "./components/AgentProgress";
import ItineraryView from "./components/ItineraryView";
import LoadingOverlay from "./components/LoadingOverlay";

export default function App() {
  const [progress, setProgress] = useState<string[]>([]);
  const [itinerary, setItinerary] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function handlePlan(data: any) {
    setLoading(true);
    setProgress(["Research Agent: Starting..."]);
    setItinerary(null);
    try {
      const res = await fetch("http://localhost:8000/plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      setProgress((p) => [...p, "Optimizer Agent: Running..."]);
      if (!res.ok) throw new Error(await res.text());
      const j = await res.json();
      setItinerary(j.itinerary);
      setProgress((p) => [...p, "Done!"]);
    } catch (err: any) {
      setProgress((p) => [...p, `Error: ${err.message}`]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen p-6 relative">
      {/* loading overlay shown on top */}
      <LoadingOverlay visible={loading} />

      {/* main content card */}
      <div className="max-w-4xl mx-auto bg-white dark:bg-slate-800 rounded-xl p-6 shadow relative z-10">
        <h1 className="text-2xl font-semibold mb-4">AI Trip Planner</h1>
        <PlannerForm onSubmit={handlePlan} loading={loading} />
        <AgentProgress steps={progress} />
        {itinerary && <ItineraryView itinerary={itinerary} />}
      </div>
    </div>
  );
}
