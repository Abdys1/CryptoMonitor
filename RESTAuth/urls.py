from django.urls import path
from RESTAuth import views

urlpatterns = [
    path('registration/', views.UserRegistration.as_view())
]

#urlpatterns = format_suffix_patterns(urlpatterns)