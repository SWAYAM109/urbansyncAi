import asyncio
from typing import Callable, Awaitable, Dict, List
from models.events import AgentMessage

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[AgentMessage], Awaitable[None]]]] = {}
        self._queue = None
        self._task = None

    def subscribe(self, topic: str, callback: Callable[[AgentMessage], Awaitable[None]]):
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(callback)

    async def publish(self, message: AgentMessage):
        if self._queue is None:
            self._queue = asyncio.Queue()
        await self._queue.put(message)

    async def _process_events(self):
        while True:
            try:
                message: AgentMessage = await self._queue.get()
                topic = message.receiver_or_topic
                
                # Find matching callbacks
                callbacks = self._subscribers.get(topic, [])
                
                if callbacks:
                    # Execute all callbacks for this topic concurrently
                    tasks = [callback(message) for callback in callbacks]
                    await asyncio.gather(*tasks, return_exceptions=True)
                
                self._queue.task_done()
            except Exception as e:
                pass

    def start(self):
        """Starts the event loop processor in the background"""
        if self._queue is None:
            self._queue = asyncio.Queue()
        if self._task is None:
            self._task = asyncio.create_task(self._process_events())

    async def stop(self):
        """Stops the event bus"""
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
