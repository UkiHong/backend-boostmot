from django.urls import path
from . import views

urlpatterns = [
    path("", views.Workouts.as_view()),
    path("<int:pk>", views.WorkoutDetail.as_view()),
    path("<int:pk>/reviews", views.WorkoutReviews.as_view()),
    path("<int:pk>/preparations", views.WorkoutPreparations.as_view()),
    path("<int:pk>/photos", views.WorkoutPhotos.as_view()),
    path("<int:pk>/bookings", views.WorkoutBookings.as_view()),
    path("<int:pk>/bookings/check", views.WorkoutBookingCheck.as_view()),
    path("preparations", views.Preparations.as_view()),
    path("preparations/<int:pk>", views.PreparationDetail.as_view()),
    path("make-error", views.make_error),
]
