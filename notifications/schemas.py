from pydantic import BaseModel, EmailStr

from datetime import datetime
from typing import Optional


class NotificationBase(BaseModel):
    """
    Base fields for Notification model
    """
    title: str
    description: str
    category: str
    user_id: str


class CreateNotification(NotificationBase):
    """
    Fields to create Notification
    """
    pass


class NotificationOut(NotificationBase):
    """
    Fields for the output of Notification Model.
    """
    created_at: datetime
    read: Optional[bool] = False

    class Config:
        orm_mode = True


class Message(BaseModel):
    """
    Fields for sending a message
    """
    sender_id: int
    receiver_id: int
    content: str


class Subscription(BaseModel):
    user_id: int
    expiration_date: datetime


class UserProfile(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    profile_completed: bool = False