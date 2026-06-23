from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

from app.schemas.trip import (
    AccommodationOption,
    BudgetBreakdown,
    CandidateActivity,
    TransportOption,
    TripRequest,
)

MONEY_QUANTUM = Decimal("0.01")
ROUNDING = ROUND_HALF_UP
LOCAL_TRANSPORT_PER_TRAVELER_DAY = Decimal("350.00")
FOOD_PER_TRAVELER_DAY = Decimal("800.00")
ACCOMMODATION_TAX_RATE = Decimal("0.08")
CONTINGENCY_RATE = Decimal("0.05")
ROUND_TRIP_MULTIPLIER = Decimal("2")


def money(value: float | int | str | Decimal) -> Decimal:
    return Decimal(str(value)).quantize(MONEY_QUANTUM, rounding=ROUNDING)


def _as_float(value: Decimal) -> float:
    return float(value.quantize(MONEY_QUANTUM, rounding=ROUNDING))


def calculate_budget(
    request: TripRequest,
    transport: TransportOption,
    accommodation: AccommodationOption,
    activities: list[CandidateActivity],
) -> BudgetBreakdown:
    travelers = Decimal(request.traveler_count)
    days = Decimal(request.day_count)
    nights = Decimal(request.night_count)
    rooms = Decimal(request.assumed_rooms)

    transport_total = money(transport.estimated_cost_per_person) * travelers * ROUND_TRIP_MULTIPLIER
    accommodation_total = money(accommodation.nightly_price_per_room) * rooms * nights
    activities_total = sum((money(activity.estimated_cost) for activity in activities), Decimal("0.00")) * travelers
    local_transport = LOCAL_TRANSPORT_PER_TRAVELER_DAY * travelers * days
    food = FOOD_PER_TRAVELER_DAY * travelers * days
    taxes_and_fees = accommodation_total * ACCOMMODATION_TAX_RATE
    subtotal = transport_total + accommodation_total + activities_total + local_transport + food + taxes_and_fees
    contingency = subtotal * CONTINGENCY_RATE
    total = subtotal + contingency
    requested_budget = money(request.total_budget)

    return BudgetBreakdown(
        currency=request.currency,
        transport=_as_float(transport_total),
        accommodation=_as_float(accommodation_total),
        activities=_as_float(activities_total),
        local_transport=_as_float(local_transport),
        food=_as_float(food),
        contingency=_as_float(contingency),
        taxes_and_fees=_as_float(taxes_and_fees),
        total=_as_float(total),
        remaining=_as_float(requested_budget - money(total)),
        room_count=request.assumed_rooms,
        nights=request.night_count,
        assumptions=[
            "Transport estimate is modeled as outbound plus return cost per traveler.",
            "Accommodation is calculated per room per night using explicit occupancy and room-count assumptions.",
            f"Accommodation fees use an estimated {ACCOMMODATION_TAX_RATE * 100:.0f}% tax/fee rate.",
            f"Contingency is estimated at {CONTINGENCY_RATE * 100:.0f}% of modeled trip costs.",
        ],
    )


def budget_reconciles(budget: BudgetBreakdown) -> bool:
    pieces = (
        money(budget.transport)
        + money(budget.accommodation)
        + money(budget.activities)
        + money(budget.local_transport)
        + money(budget.food)
        + money(budget.taxes_and_fees)
        + money(budget.contingency)
    )
    return money(budget.total) == money(pieces)
