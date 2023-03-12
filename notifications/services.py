import json

from typing import Dict
from fastapi import WebSocket

from notifications.utils import generate_notification_live_message


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, websocket: WebSocket, user_id: int):
        del self.active_connections[user_id]

    async def send_personal_message(self, message: str, notification_id: int, websocket: WebSocket):
        data = {"message": message, "notificationId": notification_id}
        await websocket.send_text(json.dumps(data))

    async def send_user_live_message(self, notification: dict):
        user_id = notification.user_id
        if user_id in self.active_connections:
            message = generate_notification_live_message(notification)
            await self.send_personal_message(message, notification.id, self.active_connections[user_id])