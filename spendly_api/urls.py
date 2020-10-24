from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from spendly_api.views import UserInformationView, UserRegistrationView, TransactionInfoView, AccountInfoView

urlpatterns = [
    path('login/', obtain_auth_token),
    path('register/', UserRegistrationView.as_view()),
    path('userinfo/', UserInformationView.as_view()),
    path('transactionsinfo/', TransactionInfoView.as_view()),
    path('accountinfo/', AccountInfoView.as_view()),
]
