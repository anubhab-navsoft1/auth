from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.CreateRegistrationApiView.as_view(), name = 'register'),
    path('login/', views.LogInView.as_view(), name = 'log-in')
]
