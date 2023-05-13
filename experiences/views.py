from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Perk
from .serializers import PerkSerializer
from experiences.models import Experience, Perk
from experiences.serializers import ExperienceSerializer
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bookings.serializers import PublicBookingSerializer

# Create your views here.


class Perks(APIView):
    def get(self, request):
        return Response(
            PerkSerializer(
                Perk.objects.all(),
                many=True,
            ).data,
        )
        # all_perks = Perk.objects.all()
        # serializer = PerkSerializer(all_perks, many=True)
        # return Response(serializer.data)

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
            return Response(PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)


""" 

[x] # path("", Experiences.as_view()),  POST
[x] # path("<int:pk>", ExperienceDetail.as_view()), GET PUT DELETE
[x] # path("<int:pk>/perks", PerksOfExperience.as_view()), GET
[ ] # path("<int:pk>/bookings", BookingsOfExperience.as_view()), GET POST
[ ] # path("<int:pk>/bookings/<int:book_pk>", BookingOfExperience.as_view()), GET PUT DELETE
"""


class Experiences(APIView):
    def get(self, requset):
        all_experiences = Experience.objects.all()
        serializer = ExperienceSerializer(all_experiences, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ExperienceDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, requset, pk):
        experience = self.get_object(pk)
        serializer = ExperienceSerializer(experience)
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        if request.user != experience.host:
            raise PermissionDenied
        serializer = ExperienceSerializer(
            experience,
            data=request.data,
            partial=True,
        )
        serializer.fields["host"].read_only = True

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience: Experience = self.get_object(pk)
        if request.user != experience.host:
            raise PermissionDenied
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class PerksOfExperience(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk=pk)
        return Response(
            PerkSerializer(
                experience.perks,
                many=True,
            ).data
        )


class BookingsOfExperience(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk=pk)
        return Response(
            PublicBookingSerializer(
                experience.bookings,
                many=True,
            ).data
        )

    # def post():
