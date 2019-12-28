from django.urls import path

from monitor import views

urlpatterns = [
    path("create-transaction/", views.TransactionDetail.as_view())
]