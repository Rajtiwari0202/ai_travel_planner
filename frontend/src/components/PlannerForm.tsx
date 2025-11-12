import React, { useState } from "react";

interface Props {
  onSubmit: (data: any) => void;
  loading: boolean;
}

export default function PlannerForm({ onSubmit, loading }: Props) {
  const [destination, setDestination] = useState("Goa");
  const [start_date, setStart] = useState("2025-11-20");
  const [end_date, setEnd] = useState("2025-11-22");
  const [budget, setBudget] = useState(30000);
  const [travelers, setTravelers] = useState(2);
  const [interests, setInterests] = useState("beach,food");

  function submit(e: React.FormEvent) {
    e.preventDefault();
    onSubmit({
      destination,
      start_date,
      end_date,
      budget: Number(budget),
      travelers: Number(travelers),
      interests: interests.split(",").map((s) => s.trim()),
    });
  }

  return (
    <form onSubmit={submit} className="grid grid-cols-1 gap-3 mb-4">
      <div className="flex gap-2">
        <input value={destination} onChange={(e) => setDestination(e.target.value)} placeholder="Destination" className="flex-1 p-2 rounded border" />
        <input type="date" value={start_date} onChange={(e) => setStart(e.target.value)} className="p-2 rounded border" />
        <input type="date" value={end_date} onChange={(e) => setEnd(e.target.value)} className="p-2 rounded border" />
      </div>

      <div className="flex gap-2">
        <input type="number" value={budget} onChange={(e) => setBudget(Number(e.target.value))} className="p-2 rounded border" placeholder="Budget" />
        <input type="number" value={travelers} onChange={(e) => setTravelers(Number(e.target.value))} className="p-2 rounded border" placeholder="Travelers" />
        <input value={interests} onChange={(e) => setInterests(e.target.value)} className="p-2 rounded border" placeholder="Interests" />
      </div>

      <button type="submit" disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50">
        {loading ? "Planning..." : "Plan Trip"}
      </button>
    </form>
  );
}
