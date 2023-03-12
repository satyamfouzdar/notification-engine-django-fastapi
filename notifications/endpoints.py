from typing import Any, List, Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends
from fastapi.templating import Jinja2Templates
from notifications.schemas import NotificationOut, Message, Subscription, UserProfile
from notifications.models import Notification
from notifications.services import ConnectionManager
from notifications.utils import generate_notification_live_message

import json
import asyncio

from datetime import datetime, timedelta, timezone

router = APIRouter()
templates = Jinja2Templates(directory="templates")

manager = ConnectionManager()


@router.post("/send_message/")
async def send_message(message: Message) -> Any:
    """
    Endpoint to send a message to a user id.
    """
    content = message.content
    notification = Notification.objects.create(
        title="New Message Received",
        description=content,
        category="MESSAGE",
        user_id=message.receiver_id,
        created_at=datetime.utcnow(),
        read=False
    )

    await manager.send_user_live_message(notification)

    return {"message": "Message sent and notification fired sucessfully."}


@router.post("/subscriptions/check/")
async def check_subscription_status(subscription: Subscription) -> Any:
    """
    Endpoint to check if a subcription is about to expire.
    If the subscription is about the expire in next 7 days, then send a notification to the user.
    """
    expiration_date_utc = subscription.expiration_date.astimezone(timezone.utc)

    # Calculate the time until the subscription expires
    time_until_expiry = expiration_date_utc - datetime.utcnow().replace(tzinfo=timezone.utc)

    if time_until_expiry <= timedelta(days=7):
        # Fire Notification
        notification = Notification.objects.create(
            title="Subscription Expiring Soon",
            description=f"Your subscription expires on {subscription.expiration_date}.",
            category="SUBSCRIPTION_EXPIRY",
            user_id=subscription.user_id,
            created_at=datetime.utcnow(),
            read=False
        )

    await manager.send_user_live_message(notification)

    return {"message": "Subscription status checked sucessfully."}


@router.post("/profile/setup")
async def complete_profile(user_profile: UserProfile) -> Any:
    """
    Endpoint to complete a user profile (Mocking the functionality).
    Create a notification if the UserProfile is completed.
    """
    if user_profile.profile_completed:
        notification = Notification.objects.create(
            title="Profile Setup Complete",
            description="Congratulations! Your profile setup is complete.",
            category="PROFILE_SETUP",
            user_id=user_profile.user_id,
            created_at=datetime.utcnow(),
            read=False)

        await manager.send_user_live_message(notification)

    return {"message": "Profile setup complete"}


@router.put("/read_notification/{notification_id}")
def mark_notification_as_read(notification_id: int) -> Any:
    """
    Endpoint to mark a notification as read.
    """

    notification = Notification.objects.filter(id=notification_id)

    if notification.exists():
        notification = notification.first()
        notification.read = True
        notification.save()
        message = f"Marked Notification with id {notification_id} as read sucessfully."
    else:
        message = f"Notification with id {notification_id} does not exists."

    return {"message": message}


@router.get("/live/{user_id}/")
def live_notifications(request: Request, user_id: int):
    notifications_messages = {}
    notifications = Notification.objects.filter(user_id=user_id).exclude(read=True)

    # This is a bad use, we can use something else for this purpose.
    for notification in notifications:
        message = generate_notification_live_message(notification)
        notifications_messages[notification.id] = message

    return templates.TemplateResponse("live_notifications.html", {"request": request, "notifications": notifications_messages, "user_id": user_id})


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)