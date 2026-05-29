"""Views for badges app."""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Badge, UserBadge
from .serializers import BadgeSerializer


class BadgeListView(APIView):
    """GET /api/badges/ — all badges with unlock status for current user."""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_badges = UserBadge.objects.filter(user=request.user)
        unlocked_ids = set(user_badges.values_list('badge_id', flat=True))
        unlocked_map = {ub.badge_id: ub.unlocked_at for ub in user_badges}

        badges = Badge.objects.all()
        serializer = BadgeSerializer(
            badges, many=True,
            context={'unlocked_ids': unlocked_ids, 'unlocked_map': unlocked_map}
        )
        return Response({
            'badges': serializer.data,
            'unlocked_count': len(unlocked_ids),
            'total_count': badges.count(),
        })
