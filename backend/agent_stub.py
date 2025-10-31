# agent_stub.py
# Simple stub that returns a fake plan for testing without calling any external API.

def generate_plan_stub(goal: str):
    """
    Returns a mock plan (list of steps) for a given goal.
    This simulates the agent planning stage without using Gemini 1.5 Flash yet.
    """
    return {
        "goal": goal,
        "plan": [
            "Step 1: Clarify scope and break down tasks",
            "Step 2: Gather resources and references",
            "Step 3: Draft the deliverables (code, README, slides)",
            "Step 4: Implement core features and test",
            "Step 5: Polish UI and prepare demo"
        ]
    }
