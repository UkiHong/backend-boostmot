from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Perk, Experience
from categories.models import Category
from .serializers import (
    PerkSerializer,
    ExperienceListSerializer,
    ExperienceDetailSerializer,
)
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import (
    PublicBookingSerializer,
    CreateExperienceBookingSerializer,
)

# Create your views here.


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(
                PerkSerializer(updated_perk).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Experiences(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = ExperienceListSerializer(
            all_experiences,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            experience = serializer.save(host=request.user)
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("Category kind should be 'experience'")
            except Category.DoesNotExist:
                raise ParseError("Category not found")
            try:
                with transaction.atomic():
                    experience = serializer.save(
                        host=request.user,
                        category=category,
                    )
                    perks = request.data.get("perks")
                    if perks:
                        perk_objects = []
                        for perk_pk in perks:
                            try:
                                perk = Perk.objects.get(pk=perk_pk)
                                perk_objects.append(perk)
                            except Perk.DoesNotExist:
                                pass
                            experience.perks.set(perk_objects)
                    serializer = ExperienceDetailSerializer(
                        experience, context={"request": request}
                    )
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Perk not found")
        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceDetailSerializer(
            experience,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        serializer = ExperienceDetailSerializer(
            experience,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperiencePerks(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        experience = self.get_object(pk)
        serializer = PerkSerializer(
            experience.perks.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class ExperiencePhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        experience = self.get_object(pk)
        if request.user != experience.host:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(experience=experience)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            check_in__gt=now,
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
