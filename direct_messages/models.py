from django.db import models
from common.models import CommonModel


class ChattingRoom(CommonModel):
    """Workout Model description"""

    users = models.ManyToManyField(
        "users.user",
    )

    def __str__(self) -> str:
        return "Chatting Room"


class Message(CommonModel):
    """Message Model Description"""

    text = models.TextField()
    user = models.ForeignKey(
        "users.user",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="messages",
    )

    workout = models.ForeignKey(
        "direct_messages.chattingroom",
        on_delete=models.CASCADE,
        related_name="messages",
    )

    def __str__(self) -> str:
        return f"{self.user} says: {self.text}"
