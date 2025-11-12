# backend/app/scoring.py
import pandas as pd
from typing import List, Dict, Any

def score_options(flights: List[Dict], hotels: List[Dict], activities: List[Dict], budget: float, interests: List[str]):
    """
    Simple scoring:
    - normalize price (lower is better)
    - rating higher better
    - distance lower better (if present)
    Combine into a score = w_price*norm_price + w_rating*(1-norm_rating) + w_distance*norm_distance
    For activities, boost items matching interests.
    """
    def normalize(values):
        smin = min(values)
        smax = max(values)
        if smax == smin:
            return [0.5 for _ in values]
        return [(v - smin) / (smax - smin) for v in values]

    # Flights
    flight_prices = [float(f.get("price", 0)) for f in flights]
    np_f = normalize(flight_prices)
    for i,f in enumerate(flights):
        f['_score'] = (1 - np_f[i])  # lower price -> higher score

    flights_sorted = sorted(flights, key=lambda x: -x['_score'])

    # Hotels
    hotel_prices = [float(h.get("price_per_night", 0)) for h in hotels]
    hotel_ratings = [float(h.get("rating", 3)) for h in hotels]
    np_hp = normalize(hotel_prices)
    np_hr = normalize(hotel_ratings)
    for i,h in enumerate(hotels):
        # combine price (0.6) and rating (0.4)
        h['_score'] = 0.6*(1-np_hp[i]) + 0.4*np_hr[i]
    hotels_sorted = sorted(hotels, key=lambda x: -x['_score'])

    # Activities - boost by interest match
    for a in activities:
        base = 0
        price = float(a.get('price', 0))
        rating = float(a.get('rating', 3)) if 'rating' in a else 3
        # interest match
        match = any(k.lower() in a.get('tags','').lower() for k in interests)
        a['_score'] = rating + (1 if match else 0) - (price/1000.0)
    activities_sorted = sorted(activities, key=lambda x: -x['_score'])

    return {
        "flights": flights_sorted,
        "hotels": hotels_sorted,
        "activities": activities_sorted
    }
