from rest_framework.serializers import ModelSerializer
from .models import User


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "name"


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "name"
