# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from agent_stub import generate_plan_stub
from notion_helper_stub import add_task_to_notion_stub

app = FastAPI(title="TaskPilot - Backend (Step1)")

class GoalRequest(BaseModel):
    goal: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/plan")
def plan_goal(req: GoalRequest):
    """
    Generate a mock plan for the provided goal (stub).
    Later we'll replace with real OpenAI agent calls.
    """
    result = generate_plan_stub(req.goal)
    return result

@app.post("/notion/add")
def notion_add(req: GoalRequest):
    """
    Simulate adding a task to Notion (stub).
    """
    result = add_task_to_notion_stub(req.goal)
    return result
