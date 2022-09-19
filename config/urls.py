
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('djadmin/', admin.site.urls),
    path('', include("apps.user.urls")),
    path('', include("apps.startups.urls")),
]