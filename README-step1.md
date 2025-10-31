# 🧠 TaskPilot - Step 1

## 🎯 Goal
Set up the backend skeleton for TaskPilot and verify that the FastAPI server runs correctly.

---

## ✅ What’s done in Step 1
- Created a Python virtual environment
- Installed free dependencies (`fastapi`, `uvicorn`, `requests`, `python-dotenv`)
- Built folder structure  
taskpilot/
├─ backend/
│ ├─ main.py
│ ├─ agent_stub.py
│ ├─ notion_helper_stub.py
│ ├─ requirements.txt
│ └─ .env.example

- Implemented 3 routes  
- `/health` → returns `{"status": "ok"}`
- `/plan` → returns mock plan (from `agent_stub.py`)
- `/notion/add` → simulates Notion entry

---

## ⚙️ How to run
```bash
# Inside backend/
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

Test endpoints:
Health
curl http://127.0.0.1:8000/health
→ {"status":"ok"}
Plan (PowerShell safe)
Invoke-RestMethod -Uri "http://127.0.0.1:8000/plan" -Method Post -Body (@{goal="Prepare hackathon project"} | ConvertTo-Json) -ContentType "application/json"
→ Returns goal + plan list

🌱 Next Step

Replace stub agent with real reasoning using Gemini API (free tier)
and start storing generated plans in Notion database.