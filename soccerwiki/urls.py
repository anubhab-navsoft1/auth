from django.urls import path
from . import views
urlpatterns = [
    path('add/', views.AddAllInformationsApiView.as_view(), name= "Adding Informations")
]
