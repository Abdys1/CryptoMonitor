from django.urls import path
from RESTAuth import views

urlpatterns = [
    path("registration/", views.UserRegistration.as_view()),
    path("activate", views.ActivateRegistration.as_view(), name="activate")
]

#urlpatterns = format_suffix_patterns(urlpatterns)