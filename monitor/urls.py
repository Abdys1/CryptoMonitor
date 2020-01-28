from django.urls import path

from . import views

urlpatterns = [
    path("transaction/", views.TransactionDetail.as_view()),
    path("exchangeRate", views.exchange_rate)
]