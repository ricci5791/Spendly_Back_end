import requests
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import spendly_api.serializers as serializers
from .models import Transaction, Account, User
from django.http import HttpResponse

MONOBANK_URL = 'https://api.monobank.ua/personal/'


class UserInformationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.UserSerializer(user, many=False)
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
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            User.objects.create(request.data['username'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionInfoView(APIView):
    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = serializers.TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        data = request.data
        serializer = serializers.TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class AccountInfoView(APIView):
    def get(self, request, user_id=None):
        if id is not None:
            accounts = Account.objects.filter(user_id=user_id)
        else:
            accounts = Account.objects.all()
        serializer = serializers.AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        data = request.data
        serializer = serializers.AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class MonobankWebhookView(APIView):
    def post(self, request):
        data = request.data['data']
        trans_info = data['statementItem']
        trans_info.update({"account": data['account']})
        serializer = serializers.TransactionSerializer(data=trans_info)
        print(trans_info)

        if serializer.is_valid():
            serializer.save()
            print("saved")
        print(serializer.errors)
        return Response(status=200)


def monobank_set_hook(request):
    response = requests.post(MONOBANK_URL + "webhook",
                             json={"webhook": "https://spendly-student.herokuapp.com/api/webhook"},
                             headers={"X-Token": request.headers["X-Token"]})

    if response.ok:
        return HttpResponse(status=response.status_code)

    return HttpResponse(response.json(), status=response.status_code)
