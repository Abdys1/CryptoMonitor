from django.urls import path

from . import views

urlpatterns = [
    path("transaction/", views.TransactionDetail.as_view()),
    path("transaction/<int:pk>", views.TransactionDetail.as_view())
]