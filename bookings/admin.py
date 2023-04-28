from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class Booking(admin.ModelAdmin):
    list_display = (
        "kind",
        "user",
        "workout",
        "experience",
        "check_in",
        "check_out",
        "experience_time",
        "participants",
    )

    list_filter = ("kind",)
