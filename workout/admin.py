from django.contrib import admin
from .models import Workout, Preparation


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "address",
        "description",
        "kind",
        "total_preparation",
        "rating",
        "host",
        "avatar",
    )

    search_fields = (
        "name",
        "city",
        "host__username",
    )

    def total_preparation(self, workout):
        return workout.preparation.count()

    list_filter = (
        "name",
        "country",
        "city",
        "address",
        "pets_allowed",
        "kind",
        "host",
        "preparation",
    )


@admin.register(Preparation)
class PreparationAdmin(admin.ModelAdmin):
    pass
