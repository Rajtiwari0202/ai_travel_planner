from __future__ import annotations

import asyncio
from collections import defaultdict
from collections.abc import AsyncIterator

from app.db.session import SessionLocal
from app.repositories.trips import append_event
from app.schemas.trip import AgentEvent


class EventBroker:
    def __init__(self) -> None:
        self._subscribers: dict[str, set[asyncio.Queue[AgentEvent]]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def publish(self, event: AgentEvent) -> None:
        with SessionLocal() as db:
            append_event(db, event)
        async with self._lock:
            queues = list(self._subscribers.get(event.trip_id, set()))
        for queue in queues:
            queue.put_nowait(event)

    async def subscribe(self, trip_id: str) -> AsyncIterator[AgentEvent | None]:
        queue: asyncio.Queue[AgentEvent] = asyncio.Queue()
        async with self._lock:
            self._subscribers[trip_id].add(queue)
        try:
            while True:
                try:
                    yield await asyncio.wait_for(queue.get(), timeout=15)
                except TimeoutError:
                    yield None
        finally:
            async with self._lock:
                self._subscribers[trip_id].discard(queue)


event_broker = EventBroker()
