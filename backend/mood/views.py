"""Views for mood app."""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from django.db import IntegrityError
from .models import MoodLog
from .serializers import MoodLogSerializer


class MoodCreateView(generics.CreateAPIView):
    """POST /api/mood/ — log today's mood & energy."""
    serializer_class = MoodLogSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except IntegrityError:
            return Response(
                {'detail': 'Mood untuk hari ini sudah dicatat.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MoodHistoryView(generics.ListAPIView):
    """GET /api/mood/history/ — last 7 days of mood logs."""
    serializer_class = MoodLogSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        seven_days_ago = timezone.localdate() - timedelta(days=7)
        return MoodLog.objects.filter(
            user=self.request.user, log_date__gte=seven_days_ago
        )
