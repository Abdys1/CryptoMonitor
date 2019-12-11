from django.urls import path
from authenticate import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('registration/', views.UserRegistration.as_view())
]

#urlpatterns = format_suffix_patterns(urlpatterns)