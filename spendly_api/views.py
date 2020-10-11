from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def main_view(request):
    return HttpResponse("<html><body>It is now </body></html>")
