from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, Account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',
                  'username',
                  'password']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(raw_password=validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    credential = serializers.CharField()
    password = serializers.CharField(min_length=6)


class AccountSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(),
                                        slug_field='email',
                                        many=False)

    # To deal with camel case in responses
    currencyCode = serializers.IntegerField(source='currency_code')

    class Meta:
        model = Account
        fields = ['user',
                  'id',
                  'balance',
                  'currencyCode',
                  'type']


class TransactionSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), many=False)

    # To deal with camel case in responses
    currencyCode = serializers.IntegerField(source='currency_code')

    class Meta:
        model = Transaction
        fields = ['account',
                  'time',
                  'description',
                  'mcc',
                  'amount',
                  'currencyCode',
                  'balance']


class CashTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'time',
            'description',
            'mcc',
            'amount',
        ]


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
