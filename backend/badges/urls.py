"""URLs for badges app."""
from django.urls import path
from .views import BadgeListView

app_name = 'badges'

urlpatterns = [
    path('', BadgeListView.as_view(), name='list'),
]
