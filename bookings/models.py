from django.db import models
from common.models import CommonModel


class Booking(CommonModel):
    "Booking model descriptions"

    class BookingKindChoices(models.TextChoices):
        WORKOUT = "workout", "Workout"
        EXPERIENCE = "experience", "Experience"

    kind = models.CharField(
        max_length=15,
        choices=BookingKindChoices.choices,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    workout = models.ForeignKey(
        "workout.Workout",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="bookings",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="bookings",
    )
    check_in = models.DateTimeField(
        null=True,
        blank=True,
    )
    check_out = models.DateTimeField(
        null=True,
        blank=True,
    )

    experience_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    participants = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.kind.title()} booking for: {self.user}"
