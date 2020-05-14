from django.urls import path
from . import views

urlpatterns = [
    path("registration/", views.UserRegistration.as_view()),
    path("account", views.AccountInformation.as_view())
]