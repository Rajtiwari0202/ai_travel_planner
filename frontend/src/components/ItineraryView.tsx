import React, { useState } from "react";
import TripMap from "./TripMap";

export default function ItineraryView({ itinerary }: { itinerary: any }) {
  const [showMap, setShowMap] = useState(false);

  const { flight, hotel, daily_plan, description, budget_breakdown } = itinerary;

  return (
    <div className="mt-6">
      <h2 className="text-xl font-semibold">Your Itinerary</h2>
      <p className="mt-2">{description}</p>

      {/* Flight + Hotel */}
      <div className="mt-4 grid grid-cols-2 gap-4">
        <div className="p-3 border rounded">
          <h4 className="font-medium">Flight</h4>
          <p>{flight.airline} — ₹{flight.price}</p>
        </div>
        <div className="p-3 border rounded">
          <h4 className="font-medium">Hotel</h4>
          <p>{hotel.name} — ₹{hotel.price_per_night}/night (Rating {hotel.rating})</p>
        </div>
      </div>

      {/* Day-by-day Plan */}
      <div className="mt-4">
        <h4 className="font-medium">Day-by-day Plan</h4>
        {daily_plan.map((d: any) => (
          <div key={d.day} className="mt-2 p-3 border rounded">
            <strong>Day {d.day}</strong>
            <ul className="mt-1 list-disc list-inside">
              {d.activities.map((a: any, idx: number) => (
                <li key={idx}>{a.name} — ₹{a.price} — {a.tags}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      {/* Budget Breakdown */}
      <div className="mt-4 p-3 border rounded">
        <h4 className="font-medium">Budget Breakdown</h4>
        <p>Flight: ₹{budget_breakdown.flight}</p>
        <p>Hotel: ₹{budget_breakdown.hotel}</p>
        <p>Activities: ₹{budget_breakdown.activities}</p>
        <p className="font-semibold text-blue-400">
          Total: ₹{budget_breakdown.total}
        </p>

        {/* Toggle Map Button */}
        <div className="text-center mt-4">
          <button
            onClick={() => setShowMap(!showMap)}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
          >
            {showMap ? "Hide Map 🗺" : "Show Map 🗺"}
          </button>
        </div>

        {/* Animated Map */}
        <div
          className={`transition-all duration-500 overflow-hidden ${
            showMap ? "max-h-[600px] mt-4" : "max-h-0"
          }`}
        >
          {showMap && <TripMap itinerary={itinerary} />}
        </div>
      </div>
    </div>
  );
}
