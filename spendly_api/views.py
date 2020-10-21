from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseForbidden
import requests as http
import json
from spendly_api import models as m

MONOBANK_URL = 'https://api.monobank.ua/personal/'


def main_view(request):
    return HttpResponse(
        "<html><body>Hello motherfakers. If you see this text i haven't wasted 3 hours of reading</body></html>")


def registration(request):
    user_token = request.GET.get('token')
    req_email = request.GET.get("email")
    req_password = request.GET.get("password")

    user = m.User.objects.filter(email__exact=req_email)

    if user.first() is None or user.first().password != req_password:
        return HttpResponseForbidden("doesn't exist such email or not correct password")

    url = 'https://spendly-student.herokuapp.com/hook'

    mono_post_response = http.post(MONOBANK_URL + 'webhook', json={"webHookUrl": url}, headers={"X-Token": user_token})

    if mono_post_response.ok:
        return HttpResponse()
    else:
        return HttpResponseForbidden(mono_post_response.status_code)


def monobank_webhook_response(request):
    try:
        response = json.loads(request.body)
    except AttributeError:
        response = request

    trans = response['data']['statementItem']

    m.Transaction.objects.create(transaction_id=trans['id'], time_since_epoch=trans['time'], desc=trans['description'],
                                 balance=trans['balance'], amount=trans['amount'], merchant_category_code=trans['mcc'],
                                 currency_code=trans['currencyCode'], account_id=response['data']['account'])

    return HttpResponse()


def get_discharge(request):
    mono_discharge_response = http.post(MONOBANK_URL + f'statement/0/{request.GET.get("from")}/',
                                        headers={'X-Token': request.headers.get('X-Token')})

    print(mono_discharge_response)
    print(mono_discharge_response.status_code)

    for trans in mono_discharge_response:
        monobank_webhook_response(trans)

    return HttpResponse(mono_discharge_response)
