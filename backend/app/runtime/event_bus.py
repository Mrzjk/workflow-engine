import asyncio
from .events import RuntimeEvent
class EventBus:
    def __init__(self): self.events=[]; self._waiters=[]
    async def publish(self,event: RuntimeEvent):
        self.events.append(event)
        for q in self._waiters: await q.put(event)
    async def subscribe(self):
        q=asyncio.Queue(); self._waiters.append(q)
        try:
            for e in self.events: yield e
            while True: yield await q.get()
        finally: self._waiters.remove(q)
