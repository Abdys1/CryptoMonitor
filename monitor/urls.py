from django.urls import path

from monitor import views

urlpatterns = [
    path("transaction/", views.TransactionDetail.as_view())
]