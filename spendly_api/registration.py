from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.validators import UniqueValidator

from .models import User


class RegisterView(APIView):

    def post(self, request):
        data = request.data
        login = data['login']
        password = data['password']
        name = data['name']
        last_name = data['lastName']

        validation_res = UniqueValidator(data)

        if validation_res.message != "ok":
            return Response(validation_res.message, status=400)

        new_user = User(username=login, password=password, first_name=name, last_name=last_name)

        new_user.save()
        return Response("ok", status=200)


class LoginView(APIView):

    def get(self, request):
        data = request.data
        token = data['token']

        user = User.objects.get(token=token)
        if user is None:
            return Response("Wrong token was provided", status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"token": token}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        login = data['login']
        password = data['password']

        try:
            user = User.objects.get(username=login, password=password)
            return Response(data={"token": user.token}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response("Wrong credentials were provided", status=status.HTTP_400_BAD_REQUEST)
