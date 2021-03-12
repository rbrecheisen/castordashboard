from django.urls import path
from . import views


urlpatterns = [
    path('accounts/register/', views.register, name='register'),
    path('', views.dashboard, name='dashboard'),
]
