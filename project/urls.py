from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/', include([
        path('', include('users.urls')),
        path('', include('taxonomies.urls')),
    ])),
]
