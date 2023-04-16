from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("monitor.urls")),
    path("admin/", admin.site.urls),
    path("monitor/", include('monitor.urls')),
]
