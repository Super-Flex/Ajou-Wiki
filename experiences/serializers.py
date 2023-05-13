from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Perk, Experience


class ExperienceSerializer(ModelSerializer):
    # host = serializers.IntegerField(read_only=True)

    class Meta:
        model = Experience
        fields = "__all__"


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"
