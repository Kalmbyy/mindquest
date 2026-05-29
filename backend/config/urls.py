"""MindQuest URL configuration."""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
)


def health_check(request):
    """Simple health-check endpoint for deployment monitoring."""
    return JsonResponse({'status': 'ok', 'service': 'MindQuest API', 'version': '1.0.0'})


urlpatterns = [
    path('', health_check, name='health'),
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/auth/', include('users.urls')),
    path('api/quests/', include('quests.urls')),
    path('api/mood/', include('mood.urls')),
    path('api/badges/', include('badges.urls')),
    path('api/leaderboard/', include('users.leaderboard_urls')),

    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
