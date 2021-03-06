import requests
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import filters
import spendly_api.serializers as serializers
from .models import Transaction, Account
from django.http import HttpResponse
import django_filters.rest_framework
from .user_statistics import Stats

MONOBANK_URL = 'https://api.monobank.ua/personal/'


class UserInformationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.UserSerializer(user, many=False)
        return Response(serializer.data)

    def post(self, request):
        user_email = request.user.email
        user = User.objects.all().get(email=user_email)
        password = request.data['password']
        user.set_password(password)
        user.save()
        return Response(status=status.HTTP_200_OK)




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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTransactionsView(ListAPIView):
    serializer_class = serializers.TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter,
                       django_filters.rest_framework.DjangoFilterBackend]
    ordering_fields = ['time', 'amount']
    filterset_fields = ['mcc', 'account']

    def get_queryset(self):
        user = self.request.user
        transactions = Transaction.objects.all().filter(account__user=user)
        return transactions


class UserAccountsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        accounts = Account.objects.all().filter(user=user)
        serializer = serializers.AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=200)


class MonobankIntegrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        monobank_token = request.data["X-Token"]

        if self.fetch_accounts(user=user, monobank_token=monobank_token):
            self.set_monobank_webhook(monobank_token=monobank_token)
            return Response(status=200)

        return Response(status=400)

    def fetch_accounts(self, monobank_token, user):
        accounts_request_headers = {
            "X-Token": monobank_token
        }
        accounts_response = requests.get(
            MONOBANK_URL + 'client-info',
            headers=accounts_request_headers
        )

        if accounts_response.ok:
            accounts_response_json = accounts_response.json()
            accounts = accounts_response_json['accounts']
            for account in accounts:
                account.update(
                    {"user": user.email}
                )
            account_serializer = serializers.AccountSerializer(data=accounts, many=True)
            if account_serializer.is_valid():
                account_serializer.save()
            return True
        return False

    def set_monobank_webhook(self, monobank_token):
        set_webhook_request_json = {
            "webHookUrl": "https://spendly-student.herokuapp.com/api/webhook"
        }
        accounts_request_headers = {
            "X-Token": monobank_token
        }

        requests.post(
            MONOBANK_URL + 'webhook',
            json=set_webhook_request_json,
            headers=accounts_request_headers
        )


class MonobankWebhookView(APIView):
    def post(self, request):
        request_data = request.data['data']
        self.try_to_parse_transaction(request_data=request_data)
        return Response(status=200)

    def try_to_parse_transaction(self, request_data):
        try:
            account = request_data['account']
            transaction_data = request_data['statementItem']
            transaction_data.update({'account': account})
            transaction_serializer = serializers.TransactionSerializer(data=transaction_data)
            if transaction_serializer.is_valid():
                transaction_serializer.save()
        except Exception as e:
            print(e)
            pass


class CashTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        account = self.get_or_create_cash_account(user=user)

        data = request.data
        amount = request.data['amount']
        data.update({
            'account': account.id,
            'currencyCode': 980,
            'balance': account.balance + amount
        })
        serializer = serializers.TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)

        return Response(status=400)

    def delete(self, request):
        user = request.user
        time = request.headers['time'] if request.headers['time'] is not None else 0
        transactions = Transaction.objects.all().filter(account__user__email=user.email)
        transaction = transactions.filter(time=time)

        if transaction.exists():
            transaction.first().delete()
            return Response(status=200)

        return Response(status=400)

    def get_or_create_cash_account(self, user):
        user_email = user.email
        account_id = f'{user_email}-cash'
        cash_account = Account.objects.all().filter(id=account_id)
        if cash_account.exists():
            print(cash_account.first())
            return cash_account.first()
        else:
            account = Account(
                id=account_id,
                user=user,
                balance=0,
                currency_code=980,
                type='Cash'
            )
            print(account)
            account.save()
            return account


class UserStatistics(APIView):
    def get(self, request):
        user_stats = Stats(request.user)
        return Response(data=user_stats.get_total_by_mcc(), status=200)


class UserInfoApi(APIView):
    def get(self, request):
        user = request.user

        user_serializer = serializers.UserSerializer(user)

        return Response(data=user_serializer, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
