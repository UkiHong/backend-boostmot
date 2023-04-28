from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Preparation, Workout
from users.serializers import TinyUserSerializer
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class PreparationSerializer(ModelSerializer):
    class Meta:
        model = Preparation
        fields = (
            "pk",
            "name",
            "description",
        )


class WorkoutDetailSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    preparations = PreparationSerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(read_only=True)

    rating = serializers.SerializerMethodField()
    is_host = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = "__all__"

    def get_rating(self, workout):
        return workout.rating()

    def get_is_host(self, workout):
        request = self.context.get("request")
        if request:
            return workout.host == request.user
        return False

    def get_is_liked(self, workout):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return Wishlist.objects.filter(
                    user=request.user,
                    workout__pk=workout.pk,
                ).exists()
        return False


class WorkoutListSerializer(ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_host = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "rating",
            "is_host",
            "photos",
        )

    def get_rating(self, workout):
        return workout.rating()

    def get_is_host(self, workout):
        request = self.context["request"]
        return workout.host == request.user
