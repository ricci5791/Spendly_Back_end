from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

import spendly_api.views as views

urlpatterns = [
    path('login', obtain_auth_token),
    path('register/', views.UserRegistrationView.as_view()),


    path('webhook', views.MonobankWebhookView.as_view()),
    path('webhook/set', views.MonobankIntegrationView.as_view()),

    path('user/info/', views.UserInformationView.as_view()),
    path('user/transactions/', views.UserTransactionsView.as_view()),
    path('user/accounts/', views.UserAccountsView.as_view()),
]
