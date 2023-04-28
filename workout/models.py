from django.db import models
from common.models import CommonModel


class Workout(CommonModel):
    class WorkoutKindChoices(models.TextChoices):
        FOOTBALL = ("football", "Football")
        RUNNING = ("running", "Running")
        YOGA = ("yoga", "Yoga")

    name = models.CharField(max_length=150, default="")
    country = models.CharField(
        max_length=50,
        default="United Kingdom",
    )
    city = models.CharField(
        max_length=80,
        default="Leeds",
    )
    address = models.CharField(
        max_length=250,
    )
    description = models.TextField()
    pets_allowed = models.BooleanField(default=False)
    kind = models.CharField(
        max_length=20,
        choices=WorkoutKindChoices.choices,
    )

    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="workout",
    )
    avatar = models.URLField(blank=True)

    preparation = models.ManyToManyField(
        "workout.Preparation",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="workout",
    )

    def __str__(self) -> str:
        return self.name

    def rating(self):
        count = self.reviews.count()
        if count == 0:
            return 0
        else:
            total_rating = 0
            print(self.reviews.all().values("rating"))
            for review in self.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2)


class Preparation(CommonModel):
    """Preparation for workouts"""

    name = models.CharField(max_length=150)
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Preparations"
