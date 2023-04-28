from rest_framework.serializers import ModelSerializer
from workout.serializers import WorkoutListSerializer
from .models import Wishlist


class WishlistSerializer(ModelSerializer):
    workout = WorkoutListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "workout",
        )
