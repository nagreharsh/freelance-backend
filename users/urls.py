from django.urls import path
from .views import register, login
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('refresh/', TokenRefreshView.as_view()),
]
