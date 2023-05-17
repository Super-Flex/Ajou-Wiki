from rest_framework.serializers import ModelSerializer
from .models import Wiki
# from wiki.models import Wiki
from rest_framework import serializers




class WikiSerializer(ModelSerializer):
    class Meta:
        model = Wiki
        fields = "__all__"
