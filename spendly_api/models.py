from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=50, primary_key=True)
    password = models.CharField(max_length=30)


class Account(models.Model):
    acc_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('spendly_api.User', on_delete=models.CASCADE)
    currency_code = models.IntegerField()
    acc_type = models.CharField(max_length=10)


class Transaction(models.Model):
    account = models.ForeignKey('spendly_api.Account', on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=30, unique=True)
    time_since_epoch = models.IntegerField()
    desc = models.CharField(max_length=100)
    balance = models.IntegerField()
    amount = models.IntegerField()
    merchant_category_code = models.IntegerField()
    currency_code = models.IntegerField()
