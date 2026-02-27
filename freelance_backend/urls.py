from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/projects/', include('projects.urls')),
    path('api/proposals/', include('proposals.urls')),
    path('api/', include('users.urls')),
    path("api/contracts/", include("contracts.urls")),
    path("api/messages/", include("messaging.urls")),
    path("api/notifications/", include("notifications.urls")),
    path("api/reviews/", include("reviews.urls")),
    path("api/admin/contracts/", include("contracts.admin_urls")),
    path("api/admin/reviews/", include("reviews.admin_urls")),
]