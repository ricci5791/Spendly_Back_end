import requests as http
import json
from spendly_api import models as m
from django.http import HttpResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from spendly_api.serializers import UserSerializer, TransactionSerializer, AccountSerializer
from .models import Transaction, Account

MONOBANK_URL = 'https://api.monobank.ua/personal/'


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


class TransactionInfoView(APIView):
    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        data = JSONParser.parse(request)
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class AccountInfoView(APIView):
    def get(self, request):
        accounts = Account.objects.filter(user_id=request.GET.get('email'))
        print(request.data)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        data = JSONParser.parse(request)
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


def init_request(request):
    user_token = request.GET.get('token')
    email = request.GET.get("email")
    password = request.GET.get("password")
    # TODO: add model logics to check user credentials

    url = 'https://spendly-student.herokuapp.com/hook'

    https.post(mono_url, json={"webHookUrl": url}, headers={"X-Token": user_token})

    return HttpResponse()


def monobank_webhook_response(request):
    # TODO:
    return None
