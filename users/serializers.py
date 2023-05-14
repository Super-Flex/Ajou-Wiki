from rest_framework.serializers import ModelSerializer
from .models import User
from rest_framework import serializers


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):
        check = "@ajou.ac.kr"
        if data["email"][-len(check) :] != check:
            raise serializers.ValidationError("아주대 이메일을 사용하여 주세요.")
        return data
