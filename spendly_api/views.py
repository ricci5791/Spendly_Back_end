from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def main_view(request):
    return HttpResponse(
        "<html><body>Hello motherfakers. If you see this text i haven't wasted 3 hours of reading</body></html>")
