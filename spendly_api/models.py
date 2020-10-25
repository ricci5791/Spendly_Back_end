from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    balance = models.PositiveIntegerField(default=0)
    currency_code = models.IntegerField(default=980)

    type = models.CharField(max_length=50)


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    time = models.IntegerField(null=False)
    description = models.CharField(max_length=100, default="")

    mcc = models.IntegerField(default=-1)
    amount = models.IntegerField(default=0)

    currency_code = models.IntegerField(default=980)
    balance = models.IntegerField(default=0)
