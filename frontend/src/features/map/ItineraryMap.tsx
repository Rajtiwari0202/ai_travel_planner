import { MapContainer, Marker, Polyline, Popup, TileLayer, useMap } from "react-leaflet";
import L, { LatLngBoundsExpression } from "leaflet";
import type { GeoPoint, TripPlan } from "../../types/api";

delete (L.Icon.Default.prototype as unknown as { _getIconUrl?: unknown })._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

export function ItineraryMap({ plan }: { plan: TripPlan }) {
  const activityPoints = plan.days.flatMap((day) => day.activities.map((activity) => activity.location));
  const points = [plan.accommodation.location, ...activityPoints];
  const center = plan.destination.center;
  const path = points.map(toLatLng);

  return (
    <section className="rounded-lg border border-ink/10 bg-white p-4 shadow-soft" aria-label="Itinerary map">
      <div className="mb-3">
        <h2 className="font-semibold text-ink">Map and activity route</h2>
        <p className="text-sm text-ink/65">All coordinates come from the backend response. The browser does not geocode.</p>
      </div>
      <div className="h-[420px] overflow-hidden rounded-lg border border-ink/10">
        <MapContainer center={[center.latitude, center.longitude]} zoom={12} scrollWheelZoom={false}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <FitBounds points={points} />
          <Marker position={toLatLng(plan.accommodation.location)}>
            <Popup>
              <strong>{plan.accommodation.name}</strong>
              <br />
              Recommended stay
            </Popup>
          </Marker>
          {plan.days.map((day) =>
            day.activities.map((activity, index) => (
              <Marker key={activity.activity_id} position={toLatLng(activity.location)}>
                <Popup>
                  <strong>
                    Day {plan.days.indexOf(day) + 1}.{index + 1} {activity.title}
                  </strong>
                  <br />
                  {activity.category} · {activity.data_kind.replace("_", " ")}
                </Popup>
              </Marker>
            )),
          )}
          {path.length > 1 && <Polyline positions={path} color="#1f7a8c" weight={4} opacity={0.7} />}
        </MapContainer>
      </div>
    </section>
  );
}

function FitBounds({ points }: { points: GeoPoint[] }) {
  const map = useMap();
  if (points.length > 1) {
    const bounds = points.map(toLatLng) as LatLngBoundsExpression;
    window.setTimeout(() => map.fitBounds(bounds, { padding: [28, 28] }), 0);
  }
  return null;
}

function toLatLng(point: GeoPoint): [number, number] {
  return [point.latitude, point.longitude];
}
