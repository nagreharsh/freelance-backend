from django.urls import path
from .views import (
    register,
    login,
    profile_view,
    UnverifiedUsersView,
    ApproveUserView,
    RejectUserView,
    HighDemandClientsView,
    LowDemandClientsView,
)

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('refresh/', TokenRefreshView.as_view()),
    path('profile/', profile_view),

    # Admin endpoints
    path("admin/unverified-users/", UnverifiedUsersView.as_view()),
    path("admin/approve-user/<int:user_id>/", ApproveUserView.as_view()),
    path("admin/reject-user/<int:user_id>/", RejectUserView.as_view()),

    path("admin/high-demand-clients/", HighDemandClientsView.as_view()),
    path("admin/low-demand-clients/", LowDemandClientsView.as_view()),

]
