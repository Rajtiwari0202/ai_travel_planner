import os
import asyncio
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables (.env)
load_dotenv()

# Import AI Agents (make sure you have app/agents.py)
from app.agents import ResearchAgent, OptimizerAgent

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not OPENAI_API_KEY:
    print("⚠️  Warning: OPENAI_API_KEY not set. Mock generation will be used.")
if not OPENWEATHER_API_KEY:
    print("⚠️  Warning: OPENWEATHER_API_KEY not set. Weather features may not work.")

# Initialize FastAPI app
app = FastAPI(title="AI Trip Planner - Backend")

# Enable CORS for frontend (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Request Models
# -------------------------
class PlanRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    budget: float
    travelers: int
    interests: list[str]


class WeatherRequest(BaseModel):
    city: str
    start_date: str
    end_date: str


# -------------------------
# Endpoints
# -------------------------

@app.post("/plan")
async def plan_trip(req: PlanRequest):
    """
    Generate a full travel itinerary using AI Agents.
    """
    try:
        research = ResearchAgent()
        optimizer = OptimizerAgent()

        # Run both agents asynchronously
        research_task = asyncio.create_task(research.run(req.dict()))
        research_result = await research_task

        optimize_task = asyncio.create_task(optimizer.run(req.dict(), research_result))
        itinerary = await optimize_task

        return {"status": "ok", "itinerary": itinerary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/weather")
def get_weather(req: WeatherRequest):
    """
    Get 5-day weather forecast for a city using OpenWeather.
    Returns daily average temperature and conditions.
    """
    if not OPENWEATHER_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OpenWeather API key not set. Please configure OPENWEATHER_API_KEY in .env",
        )

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={req.city}&appid={OPENWEATHER_API_KEY}&units=metric"
    res = requests.get(url)
    if res.status_code != 200:
        raise HTTPException(status_code=400, detail=res.text)

    data = res.json()
    forecast = {}

    for item in data["list"]:
        date = item["dt_txt"].split(" ")[0]
        temp = item["main"]["temp"]
        condition = item["weather"][0]["description"]
        if date not in forecast:
            forecast[date] = {"temps": [], "conditions": []}
        forecast[date]["temps"].append(temp)
        forecast[date]["conditions"].append(condition)

    # Summarize daily averages
    daily_weather = []
    for date, info in forecast.items():
        avg_temp = sum(info["temps"]) / len(info["temps"])
        main_condition = max(set(info["conditions"]), key=info["conditions"].count)
        daily_weather.append(
            {"date": date, "temp": round(avg_temp, 1), "condition": main_condition}
        )

    return {"city": req.city, "forecast": daily_weather}


@app.get("/")
def root():
    return {"message": "AI Trip Planner Backend is running 🚀"}
