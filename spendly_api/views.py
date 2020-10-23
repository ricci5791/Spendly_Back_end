from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseForbidden
import requests as http
import json
from spendly_api import models as m

MONOBANK_URL = 'https://api.monobank.ua/personal/'


def main_view(request):
    return HttpResponse(
        "<html><body>Test</body></html>")


def init_request(request):
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
    except json.JSONDecodeError:
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


def register(request):
    data = json.loads(request.body)

    x_token = request.headers['X-Token']

    mono_get_client_info = http.get(MONOBANK_URL + "client-info",
                                    headers={"X-Token": x_token})  # data['mono-response']

    if not mono_get_client_info.ok:
        return HttpResponse(status=mono_get_client_info.status_code)

    user = m.User(email=data['email'], password=data['password'])

    accounts_list = []

    for account_data in mono_get_client_info.json()['accounts']:
        account = m.Account(acc_id=account_data['id'], currency_code=account_data['currencyCode'],
                            balance=account_data['balance'], user_id=user.email)
        accounts_list.append(account)

    user.save()
    for item in accounts_list:
        item.save()

    return HttpResponse(status=mono_get_client_info.status_code)
