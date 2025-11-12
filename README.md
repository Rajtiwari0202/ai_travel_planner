[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)]()
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)]()
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)]()
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)]()
[![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=for-the-badge&logo=leaflet&logoColor=white)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
# 🧭 AI Trip Planner

> An intelligent trip planning application that uses AI agents to research, optimize, and visualize your travel itinerary — complete with real-time weather, interactive maps, and smart budgeting.

---

## 🌟 Features

- 🤖 **AI-Powered Planning** — Generates day-by-day itineraries with flights, hotels, and activities.
- 💡 **Research & Optimizer Agents** — Two AI agents collaborate to plan and refine trips.
- ☁️ **Live Weather Forecasts** — Uses OpenWeather API to show daily conditions.
- 🗺️ **Interactive Maps** — Leaflet-powered maps visualize your travel path.
- 💰 **Smart Budget Breakdown** — Automatically distributes and summarizes trip expenses.
- 🎨 **Modern UI** — Built with React + TailwindCSS, dark mode, and fluid animations.
- ⚡ **FastAPI Backend** — Async Python backend for trip generation and weather integration.

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | React + TypeScript + Tailwind CSS + Vite + Leaflet |
| **Backend** | FastAPI (Python) + asyncio + OpenWeather API |
| **AI Layer** | Custom ResearchAgent & OptimizerAgent (OpenAI API ready) |
| **Map & Data** | OpenStreetMap (Nominatim API) |
| **Styling** | TailwindCSS + dark theme support |

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-trip-planner.git
cd ai-trip-planner
2️⃣ Setup Backend

cd backend
python -m venv .venv
.venv\Scripts\activate  # (Windows)
pip install -r requirements.txt
Create a .env file inside backend/:
OPENAI_API_KEY=your_openai_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
Run the FastAPI server:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

3️⃣ Setup Frontend
cd ../frontend
npm install
npm run dev

Visit → http://localhost:5173

Folder Structure:
ai-trip-planner/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── agents/
│   │   │   ├── ResearchAgent.py
│   │   │   ├── OptimizerAgent.py
│   │   └── __init__.py
│   ├── .env
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PlannerForm.tsx
│   │   │   ├── AgentProgress.tsx
│   │   │   ├── ItineraryView.tsx
│   │   │   ├── TripMap.tsx
│   │   └── App.tsx
│   ├── tailwind.config.js
│   ├── postcss.config.cjs
│   └── vite.config.ts
│
└── README.md

🧠 How It Works

User Input: Destination, dates, budget, and interests.

Research Agent: Gathers potential activities, flights, and hotels.

Optimizer Agent: Filters and builds an optimal itinerary.

Weather API: Adds 5-day forecasts for travel insights.

Frontend: Visualizes results and interactive maps.

Example Output:
Trip to Goa (Nov 20–22, 2025)
Flight: SpiceJet — ₹7500
Hotel: Budget Lodge — ₹1200/night
Day 1: Beach Relaxation + Spice Market Walk
Day 2: Fort Aguada Sunset + Old Goa Churches Tour
Day 3: Water Sports + Return

With live map markers and real-time weather popups ☀️🌧️.

🤝 Contributing

Fork the repo

Create a new branch

Commit changes

Open a pull request