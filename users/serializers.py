from rest_framework.serializers import ModelSerializer
from .models import User
from wiki.models import Wiki
from wiki.serializers import WikiSerializer
from rest_framework import serializers


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PrivateUserSerializer(ModelSerializer):
    wiki = WikiSerializer(many=True, read_only=True)  # 역으로 접근한거 related_name
    class Meta:
        model = User
        fields = ("name", "department", "sex", "email","student_id", "wiki")
        

    def validate(self, data):
        check = "@ajou.ac.kr"
        if data["email"][-len(check) :] != check:
            raise serializers.ValidationError("아주대 이메일을 사용하여 주세요.")
        return data
