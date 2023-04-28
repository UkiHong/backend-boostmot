from django.db import models
from common.models import CommonModel


class Wishlist(CommonModel):
    """wishlist model description"""

    name = models.CharField(
        max_length=150,
    )
    workout = models.ManyToManyField(
        "workout.Workout",
    )
    experiences = models.ManyToManyField(
        "experiences.Experience",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="wishlists",
    )

    def __str__(self) -> str:
        return self.name
