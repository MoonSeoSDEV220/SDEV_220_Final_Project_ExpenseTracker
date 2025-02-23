from django.contrib import admin
from django.urls import path, include  # Include app-level URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),  # Include app-level URLs
]
