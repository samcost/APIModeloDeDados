from django.urls import path
from core import views

urlpatterns = [
    path('API/', views.API),
]