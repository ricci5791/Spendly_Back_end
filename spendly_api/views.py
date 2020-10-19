from django.shortcuts import render
from django.http import HttpResponse
import requests as https


# Create your views here.
def main_view(request):
    return HttpResponse(
        "<html><body>Hello motherfakers. If you see this text i haven't wasted 3 hours of reading</body></html>")


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
