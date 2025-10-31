# 🚀 TaskPilot — Your Agentic AI Task Executor

> **Theme:** Agentic AI SaaS Application  
> **Built for:** HackWithUttarPradesh 2025  
> **Team:** Raj Tiwari  
> **Duration:** 30 hours  

---

## 🧩 Overview

**TaskPilot** is an **Agentic AI assistant** that not only plans but *executes* your goals automatically.

You simply tell it:  
> “Plan and start my hackathon prep.”

And it will:
1. **Understand** your goal (via Gemini API)
2. **Break it into actionable subtasks**
3. **Store them** in a structured database (or Notion API)
4. **Track progress** — and execute small steps automatically

Think of it as your *personal autonomous project manager.*

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-------------|
| Frontend | React + TailwindCSS |
| Backend | FastAPI (Python) |
| AI | Gemini API (Free tier) |
| Database | SQLite / Notion API |
| Hosting (future) | Render / Railway |
| Version Control | Git + GitHub |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Rajtiwari0202/Task-Pilot.git
cd Task-Pilot
2️⃣ Create a virtual environment
python -m venv venv
venv\Scripts\activate   # for Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add your environment variables
Create a file named .env in the root:
GEMINI_API_KEY=your_free_api_key_here
🎯 Future Scope

✅ Autonomous Task Execution (multi-agent chaining)

✅ Notion integration for real-time task tracking

✅ Browser automation for task completion

✅ Voice interface for commands

✅ SaaS dashboard with analytics

👨‍💻 Developer

Raj Tiwari
📍 India
💡 Passionate about AI, Automation & Agentic Intelligence
🌐 GitHub: Rajtiwari0202

“TaskPilot — Don’t just plan. Let AI do it for you.”