from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('session_security/', include('session_security.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
