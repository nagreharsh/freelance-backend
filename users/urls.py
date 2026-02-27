from django.urls import path
from .views import register, login, profile_view, admin_list_unverified_users, admin_verify_user, admin_demand_stats
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import list_users

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('refresh/', TokenRefreshView.as_view()),
    path('profile/', profile_view),
    path('admin/unverified/', views.admin_list_unverified_users),
    path('admin/verify/<int:user_id>/', views.admin_verify_user),
    path('admin/demand/', views.admin_demand_stats),
    path("users/", list_users, name="list-users"),
]
