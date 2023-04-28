from django.urls import path
from . import views
from .views import PerkDetail, Perks


urlpatterns = [
    path("", views.Experiences.as_view()),
    path("<int:pk>", views.ExperienceDetail.as_view()),
    path("<int:pk>/perks", views.ExperiencePerks.as_view()),
    path("<int:pk>/photos", views.ExperiencePhotos.as_view()),
    path("<int:pk>/bookings", views.ExperienceBookings.as_view()),
    path("perks/", Perks.as_view()),
    path("perks/<int:pk>", PerkDetail.as_view()),
]
