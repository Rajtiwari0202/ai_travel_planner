import React, { useEffect, useRef, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import iconUrl from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";

const DefaultIcon = L.icon({
  iconUrl,
  shadowUrl: iconShadow,
  iconAnchor: [12, 41],
});
L.Marker.prototype.options.icon = DefaultIcon;

interface TripMapProps {
  itinerary: any;
}

export default function TripMap({ itinerary }: TripMapProps) {
  const [coords, setCoords] = useState<[number, number][]>([]);
  const [weather, setWeather] = useState<any[]>([]); // 🌤 weather data
  const mapRef = useRef<L.Map>(null);

  // Fetch coordinates for destinations
  useEffect(() => {
    async function fetchCoords() {
      if (!itinerary) return;
      const days = itinerary.daily_plan || itinerary.days;
      if (!days?.length) return;

      const locations = days.map(
        (d: any) => d.location || itinerary.destination || ""
      );

      const all: [number, number][] = [];
      for (const loc of locations) {
        if (!loc) continue;
        try {
          await new Promise((res) => setTimeout(res, 300));
          const res = await fetch(
            `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(loc)}`
          );
          const data = await res.json();
          if (data.length)
            all.push([parseFloat(data[0].lat), parseFloat(data[0].lon)]);
        } catch (err) {
          console.warn("❌ Failed to geocode", loc, err);
        }
      }

      setCoords(all);
    }

    fetchCoords();
  }, [itinerary]);

  // 🌤 Fetch weather data from backend
  useEffect(() => {
    async function fetchWeather() {
      if (!itinerary?.destination) return;
      try {
        const res = await fetch("http://localhost:8000/weather", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            city: itinerary.destination,
            start_date: itinerary.start_date,
            end_date: itinerary.end_date,
          }),
        });
        const data = await res.json();
        if (data.forecast) setWeather(data.forecast);
      } catch (err) {
        console.warn("⚠️ Failed to fetch weather", err);
      }
    }

    fetchWeather();
  }, [itinerary]);

  useEffect(() => {
    if (coords.length > 1 && mapRef.current) {
      const bounds = L.latLngBounds(coords);
      mapRef.current.fitBounds(bounds, { padding: [30, 30] });
    }
  }, [coords]);

  if (!coords.length)
    return <div className="text-slate-400 text-center mt-3">Loading map...</div>;

  return (
    <div className="mt-6 rounded-xl overflow-hidden border border-slate-700 shadow">
      <MapContainer
        ref={mapRef}
        center={coords[0]}
        zoom={6}
        scrollWheelZoom={false}
        style={{ height: "400px", width: "100%" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {coords.map((c, i) => (
          <Marker key={i} position={c}>
            <Popup>
              <strong>Day {i + 1}</strong>
              <br />
              {itinerary.daily_plan?.[i]?.title || itinerary.destination}
              <br />
              {/* 🌤 Weather info for that day */}
              {weather[i] && (
                <>
                  <hr className="my-1" />
                  <div>
                    <span>🌡 {weather[i].temp}°C</span> — {weather[i].condition}
                  </div>
                </>
              )}
            </Popup>
          </Marker>
        ))}

        <Polyline positions={coords} color="dodgerblue" />
      </MapContainer>
    </div>
  );
}
