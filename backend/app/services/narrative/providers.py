from __future__ import annotations

from typing import Protocol

from app.schemas.trip import TripPlan


class LLMProvider(Protocol):
    async def generate_text(self, plan: TripPlan) -> str:
        ...


class TemplateLLMProvider:
    async def generate_text(self, plan: TripPlan) -> str:
        day_count = len(plan.days)
        interest_text = ", ".join(plan.request.preferences.interests) or "balanced discovery"
        return (
            f"{plan.request.destination} is planned as a {day_count}-day itinerary for "
            f"{plan.request.traveler_count} traveler(s), focused on {interest_text}. "
            f"The plan uses {plan.transport.mode} transport, stays at {plan.accommodation.name}, "
            f"and keeps the reconciled estimate at {plan.budget.currency} {plan.budget.total:,.0f}."
        )
