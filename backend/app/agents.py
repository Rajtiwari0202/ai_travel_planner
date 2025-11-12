# backend/app/agents.py
import asyncio
import os
from typing import Dict, Any
import pandas as pd
from app.scoring import score_options
from openai import OpenAI
import random
import json

# Use OpenAI client (openai python lib). If not available, fallback to mock.
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
client = None
if OPENAI_KEY:
    try:
        client = OpenAI(api_key=OPENAI_KEY)  # modern SDK style; if using openai package, adjust accordingly
    except Exception as e:
        client = None

DATA_DIR = os.path.join(os.path.dirname(__file__), "mock_data")

def read_csv(filename):
    return pd.read_csv(os.path.join(DATA_DIR, filename))

class ResearchAgent:
    """Find candidate flights, hotels, activities (mocked)."""
    async def run(self, request: Dict[str, Any]):
        # load mock data
        flights = read_csv("flights.csv")
        hotels = read_csv("hotels.csv")
        activities = read_csv("activities.csv")

        # simplistic filters
        dest = request["destination"].lower()
        budget = request["budget"]

        # filter by destination substring match
        flights_cand = flights[flights["destination"].str.contains(dest, case=False, na=False)].to_dict(orient="records")
        hotels_cand = hotels[hotels["destination"].str.contains(dest, case=False, na=False)].to_dict(orient="records")
        activities_cand = activities[activities["destination"].str.contains(dest, case=False, na=False)].to_dict(orient="records")

        # if empty, relax filters by taking top 5 from each
        if not flights_cand:
            flights_cand = flights.head(5).to_dict(orient="records")
        if not hotels_cand:
            hotels_cand = hotels.head(5).to_dict(orient="records")
        if not activities_cand:
            activities_cand = activities.head(10).to_dict(orient="records")

        # simulate stepwise progress
        await asyncio.sleep(0.5)
        return {
            "flights": flights_cand,
            "hotels": hotels_cand,
            "activities": activities_cand
        }

class OptimizerAgent:
    """Score options and create day-by-day plan. Uses scoring module."""
    async def run(self, request: Dict[str, Any], research_result: Dict[str, Any]):
        # apply scoring
        budget = request["budget"]
        travelers = request["travelers"]
        interests = request["interests"]

        # Score flights and hotels
        flights = research_result["flights"]
        hotels = research_result["hotels"]
        activities = research_result["activities"]

        scored = score_options(flights, hotels, activities, budget, interests)

        # pick best flight, hotel
        best_flight = scored["flights"][0] if scored["flights"] else flights[0]
        best_hotel = scored["hotels"][0] if scored["hotels"] else hotels[0]

        # build day-by-day: allocate 2-3 activities per day
        # compute days from dates:
        # For simplicity, assume request contains start/end and we compute days count externally; here do 3 days mock
        days = 3
        daily_plan = []
        acts = scored["activities"]
        idx = 0
        for d in range(days):
            day_acts = []
            for j in range(2):  # 2 activities a day
                if idx >= len(acts):
                    break
                day_acts.append(acts[idx])
                idx += 1
            daily_plan.append({
                "day": d+1,
                "activities": day_acts
            })

        # generate descriptions via OpenAI (optional)
        description = await generate_itinerary_text(request, best_flight, best_hotel, daily_plan)

        total_estimated = estimate_total_cost(best_flight, best_hotel, daily_plan, travelers)

        return {
            "flight": best_flight,
            "hotel": best_hotel,
            "daily_plan": daily_plan,
            "description": description,
            "budget_breakdown": total_estimated
        }

def estimate_total_cost(flight, hotel, daily_plan, travelers):
    # sum flight price + hotel price * nights + activities cost per person
    flight_cost = float(flight.get("price", 0))
    nights = max(1, len(daily_plan))
    hotel_price = float(hotel.get("price_per_night", 0))
    activities_cost = 0
    for day in daily_plan:
        for act in day["activities"]:
            activities_cost += float(act.get("price", 0))
    total = (flight_cost + hotel_price * nights + activities_cost) * travelers
    return {
        "flight": flight_cost*travelers,
        "hotel": hotel_price * nights * travelers,
        "activities": activities_cost * travelers,
        "total": total
    }

async def generate_itinerary_text(request, flight, hotel, daily_plan):
    # If API key present, call OpenAI for a short generative description. Otherwise return a simple template.
    if client:
        prompt = build_prompt(request, flight, hotel, daily_plan)
        try:
            resp = client.responses.create(
                model="gpt-4o-mini", # change to your available model
                input=prompt,
                max_output_tokens=400
            )
            return resp.output_text
        except Exception as e:
            print("OpenAI call failed:", e)
            return simple_template(request, flight, hotel, daily_plan)
    else:
        return simple_template(request, flight, hotel, daily_plan)

def build_prompt(request, flight, hotel, daily_plan):
    # Build a concise prompt for generative description
    p = f"""Create a friendly 3-paragraph itinerary summary for:
Destination: {request['destination']}
Dates: {request['start_date']} to {request['end_date']}
Budget: {request['budget']}
Travelers: {request['travelers']}

Selected Flight: {flight.get('airline')} {flight.get('price')}
Selected Hotel: {hotel.get('name')} (rating {hotel.get('rating')})
Daily plan (brief): {[(d['day'], [a['name'] for a in d['activities']]) for d in daily_plan]}

Make it personalized, highlight key experiences and keep it under 300 words.
"""
    return p

def simple_template(request, flight, hotel, daily_plan):
    lines = [f"Trip to {request['destination']} from {request['start_date']} to {request['end_date']}.",
             f"Flight: {flight.get('airline')} - ₹{flight.get('price')}.",
             f"Hotel: {hotel.get('name')} (Rating {hotel.get('rating')})"]
    for d in daily_plan:
        lines.append(f"Day {d['day']}: " + ", ".join([a.get('name') for a in d['activities']]))
    return "\n".join(lines)
