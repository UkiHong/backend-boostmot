from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Preparation, Workout
from categories.models import Category
from .serializers import (
    PreparationSerializer,
    WorkoutListSerializer,
    WorkoutDetailSerializer,
)
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateWorkoutBookingSerializer


class Preparations(APIView):
    def get(self, request):
        all_preparations = Preparation.objects.all()
        serializer = PreparationSerializer(all_preparations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PreparationSerializer(data=request.data)
        if serializer.is_valid():
            preparation = serializer.save()
            return Response(PreparationSerializer(preparation).data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class PreparationDetail(APIView):
    def get_object(self, pk):
        try:
            return Preparation.objects.get(pk=pk)
        except Preparation.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        preparation = self.get_object(pk)
        serializer = PreparationSerializer(preparation)
        return Response(serializer.data)

    def put(self, request, pk):
        preparation = self.get_object(pk)
        serializer = PreparationSerializer(
            preparation,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_preparation = serializer.save()
            return Response(
                PreparationSerializer(updated_preparation).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        preparation = self.get_object(pk)
        preparation.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Workouts(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_workout = Workout.objects.all()
        serializer = WorkoutListSerializer(
            all_workout,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkoutDetailSerializer(data=request.data)
        if serializer.is_valid():
            workout = serializer.save(host=request.user)
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("Category kind should be 'workout'")
            except Category.DoesNotExist:
                raise ParseError("Category not found")
            try:
                with transaction.atomic():
                    workout = serializer.save(
                        host=request.user,
                        category=category,
                    )
                    preparations = request.data.get("preparations")
                    if preparations:
                        preparation_objects = []
                        for preparation_pk in preparation:
                            try:
                                preparation = Preparation.objects.get(pk=preparation_pk)
                                preparation_objects.append(preparation)
                            except Preparation.DoesNotExist:
                                pass
                    serializer = WorkoutDetailSerializer(
                        workout, context={"request": request}
                    )
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Preparation not found")
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class WorkoutDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Workout.objects.get(pk=pk)
        except Workout.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        workout = self.get_object(pk)
        serializer = WorkoutDetailSerializer(
            workout,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        workout = self.get_object(pk)
        if workout.host != request.user:
            raise PermissionDenied

    def delete(self, request, pk):
        workout = self.get_object(pk)
        if workout.host != request.user:
            raise PermissionDenied
        workout.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class WorkoutReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Workout.objects.get(pk=pk)
        except Workout.DoesNotExist:
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
        workout = self.get_object(pk)
        serializer = ReviewSerializer(
            workout.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                workout=self.get_object(pk),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class WorkoutPreparations(APIView):
    def get_object(self, pk):
        try:
            return Workout.objects.get(pk=pk)
        except Workout.DoesNotExist:
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
        workout = self.get_object(pk)
        serializer = PreparationSerializer(
            workout.preparation.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class WorkoutPhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Workout.objects.get(pk=pk)
        except Workout.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        workout = self.get_object(pk)
        if request.user != workout.host:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(workout=workout)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WorkoutBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Workout.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        workout = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            workout=workout,
            kind=Booking.BookingKindChoices.WORKOUT,
            check_in__gt=now,
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        workout = self.get_object(pk)
        serializer = CreateWorkoutBookingSerializer(
            data=request.data,
            context={"workout": workout},
        )
        if serializer.is_valid():
            booking = serializer.save(
                workout=workout,
                user=request.user,
                kind=Booking.BookingKindChoices.WORKOUT,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WorkoutBookingCheck(APIView):
    def get_object(self, pk):
        try:
            return Workout.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        workout = self.get_object(pk)
        check_out = request.query_params.get("check_out")
        check_in = request.query_params.get("check_in")
        exists = Booking.objects.filter(
            workout=workout,
            check_in__lte=check_out,
            check_out__gte=check_in,
        ).exists()
        if exists:
            return Response({"ok": False})
        return Response({"ok": True})
