from django.urls import path
from RESTAuth import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("registration/", views.UserRegistration.as_view()),
    path("activate", views.ActivateRegistration.as_view(), name="activate")
]
