from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Perk, Experience
from users.serializers import TinyUserSerializer
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceDetailSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    perks = PerkSerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(read_only=True)

    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Experience
        fields = "__all__"


class ExperienceListSerializer(ModelSerializer):
    is_host = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Experience
        fields = (
            "pk",
            "country",
            "city",
            "is_host",
            "photos",
        )

    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user
