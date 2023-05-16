from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
import jwt
from django.conf import settings
from users.models import User
from . import serializers
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):  # 일반 유저 생성
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.is_active = False
            user.save()  # save해줘잉
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            message = (
                "이메일 확인 -> "
                + str(token)
                + "\n 해당 URL로 접속하여 토큰 값을 입력해 주세요.\n URL = http://127.0.0.1:8000/api/v1/users/activate"
            )
            mail_title = "계정 활성화 확인 이메일"
            mail_to = request.data.get("email")
            email = EmailMessage(mail_title, message, to=[mail_to])
            email.send()

            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):  # 예전 비번 확인
            user.set_password(new_password)
            user.save()
            return Response({"result": "OK", "status":200})
        else:
            raise ParseError


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"result": "OK", "status":200})
        else:
            return Response({"result": "Forbidden", "status":403})


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)  # reuest 필수
        return Response({"ok": "bye!"})


class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})


from rest_framework.exceptions import AuthenticationFailed


class Activate(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        token = request.data.get("Jwt")
        if not token:
            return None
        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        pk = decoded.get("pk")
        if not pk:
            raise AuthenticationFailed("Invalid Token")
        try:
            user = User.objects.get(pk=pk)
            user.is_active = True
            user.save()
            return Response({"ok": "good"})
        except User.DoesNotExist:
            raise AuthenticationFailed("User Not Found")

class is_email_available(APIView):
    def post(self, request):
        email = request.data.get("email", "None")
        if email == "None":
            return Response({"result": "Forbidden", "status":403})
        try:
            User.objects.get(email=email)
            return Response({"result": "possible email", "status":200})
        except User.DoesNotExist:
            return Response({"result": "impossible email", "status":403})
