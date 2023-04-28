from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")
        OTHER = ("other", "Other")

    class LanguageChoices(models.TextChoices):
        EN = ("en", "English")
        KR = ("kr", "Korean")

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )

    avatar = models.URLField(blank=True)

    name = models.CharField(
        max_length=150,
        default="",
    )
    is_host = models.BooleanField(
        default=False,
    )

    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        null=True,
    )

    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
        null=True,
    )
