from django.db import models
from datetime import datetime


class Notification(models.Model):
    """
    Model for Notifications
    """

    title: str = models.CharField(max_length=155)
    description: str = models.CharField(max_length=255)
    category: str = models.CharField(max_length=155, blank=True, null=True)
    user_id: int = models.PositiveIntegerField()
    created_at: datetime = models.DateTimeField(auto_created=True)
    read: bool = models.BooleanField(default=False)

    class Meta:
        verbose_name: str = "notification"
        verbose_name_plural: str = "notifications"
        ordering: list = ["-created_at"]

    def __repr__(self) -> str:
        return "<Post %r>" % self.title

    def __str__(self) -> str:
        return f"{self.title}"