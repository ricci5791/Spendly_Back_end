from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

import spendly_api.views as views

urlpatterns = [
    path('setwebhook/', views.monobank_set_hook),
    path('webhook/', views.MonobankWebhookView.as_view()),
    path('login/', obtain_auth_token),
    path('register/', views.UserRegistrationView.as_view()),
    path('usersinfo/', views.UserInformationView.as_view()),
    path('transactionsinfo/', views.TransactionInfoView.as_view()),
    path('accountinfo/<str:user_id>', views.AccountInfoView.as_view()),
    path('accountinfo/', views.AccountInfoView.as_view()),
]
