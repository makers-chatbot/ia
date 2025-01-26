from fastapi import WebSocket
from chat_engine import ChatEngine
import uuid


class WebSocketManager:
    def __init__(self):
        self.chat_engine = ChatEngine()
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket) -> str:
        await websocket.accept()
        session_id = str(uuid.uuid4())
        self.active_connections[session_id] = websocket
        return session_id

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def process_message(
        self, websocket: WebSocket, message: str, session_id: str
    ):
        response = await self.chat_engine.process_message(message, session_id)
        await websocket.send_json({"message": response})
