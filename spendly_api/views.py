from django.shortcuts import render
from django.http import HttpResponse
import requests as https
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from spendly_api.serializers import UserSerializer


class UserInformationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


class UserRegistrationView(APIView):
    def get(self, request):
        example_data = {
            "information": "This is an example template. Use POST method.",
            "email": "your_email",
            "username": "your_username",
            "password": "your_password"
        }
        return Response(data=example_data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def init_response(request):
    user_token = request.GET.get('token')
    email = request.GET.get("email")
    password = request.GET.get("password")
    # TODO: add model logics to check user credentials

    url = 'https://spendly-student.herokuapp.com/hook'
    mono_url = 'https://api.monobank.ua/personal/webhook'

    https.post(mono_url, json={"webHookUrl": url}, headers={"X-Token": user_token})

    return HttpResponse()


def monobank_webhook_response(request):
    # TODO:
    return None
