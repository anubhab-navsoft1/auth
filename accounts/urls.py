from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.CreateRegistrationApiView.as_view(), name = 'register'),
    path('login/', views.UserLoginAPIView.as_view(), name = 'log-in'),
    path('otp/', views.OTPVerifyApiView.as_view(), name = 'log-in'),
    path('delete/', views.DeleteAllUsersAPIView.as_view(), name = 'log-in')
]
