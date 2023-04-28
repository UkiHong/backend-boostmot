from django.urls import path
from .views import Wishlists, WishlistDetail, WishlistToggle

urlpatterns = [
    path("", Wishlists.as_view()),
    path("<int:pk>", WishlistDetail.as_view()),
    path("<int:pk>/workout/<int:workout_pk>", WishlistToggle.as_view()),
]
