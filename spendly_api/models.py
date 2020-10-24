from django.db import models
from django.contrib.auth.models import User as DUser


class User(DUser):
    pass


class Account(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    balance = models.PositiveIntegerField(default=0)
    creditLimit = models.PositiveIntegerField(default=0)
    currency_code = models.IntegerField(default=980)
    cashbackType = models.CharField(max_length=10, default=0)
    user = models.ForeignKey('User', on_delete=models.CASCADE)


class Transaction(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    time = models.IntegerField(null=False)
    description = models.CharField(max_length=100, default="")
    mcc = models.IntegerField(default=-1)
    hold = models.BooleanField(default=True)
    amount = models.IntegerField(default=0)
    operationAmount = models.IntegerField(default=0)
    currency_code = models.IntegerField(default=980)
    commissionRate = models.IntegerField(default=0)
    cashbackAmount = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    account = models.ForeignKey('spendly_api.Account', on_delete=models.CASCADE)
