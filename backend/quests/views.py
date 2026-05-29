"""Views for quests app."""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404
from .models import Quest, UserQuestLog
from .serializers import QuestSerializer, UserQuestLogSerializer
from badges.services import check_and_award_badges


class TodayQuestListView(generics.ListAPIView):
    """GET /api/quests/today/ — list active quests with completion status."""
    serializer_class = QuestSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return Quest.objects.filter(is_active=True)


class CompleteQuestView(APIView):
    """POST /api/quests/{id}/complete/ — mark quest done, award XP, update streak."""
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request, quest_id):
        quest = get_object_or_404(Quest, id=quest_id, is_active=True)
        today = timezone.localdate()

        try:
            log = UserQuestLog.objects.create(
                user=request.user,
                quest=quest,
                completed_date=today,
                xp_earned=quest.xp_reward,
            )
        except IntegrityError:
            return Response(
                {'detail': 'Quest sudah diselesaikan hari ini.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        profile = request.user.profile
        leveled_up = profile.add_xp(quest.xp_reward)
        profile.update_streak()
        profile.refresh_from_db()

        # Check for newly unlocked badges
        new_badges = check_and_award_badges(request.user)

        return Response({
            'message': f'Quest "{quest.title}" selesai! +{quest.xp_reward} XP',
            'leveled_up': leveled_up,
            'new_level': profile.current_level if leveled_up else None,
            'new_badges': new_badges,
            'profile': {
                'total_xp': profile.total_xp,
                'current_level': profile.current_level,
                'current_streak': profile.current_streak,
                'best_streak': profile.best_streak,
                'xp_progress': profile.xp_progress_to_next_level(),
            },
            'log': UserQuestLogSerializer(log).data,
        }, status=status.HTTP_201_CREATED)


class QuestHistoryView(generics.ListAPIView):
    """GET /api/quests/history/ — paginated list of completed quests."""
    serializer_class = UserQuestLogSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserQuestLog.objects.filter(
            user=self.request.user
        ).select_related('quest')


class TodayCompletionStatsView(APIView):
    """GET /api/quests/today-stats/ — summary of today's progress."""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        today = timezone.localdate()
        total_active = Quest.objects.filter(is_active=True).count()
        logs_today = UserQuestLog.objects.filter(
            user=request.user, completed_date=today
        )
        completed_today = logs_today.count()
        xp_today = sum(logs_today.values_list('xp_earned', flat=True))

        return Response({
            'date': today,
            'total_active_quests': total_active,
            'completed_today': completed_today,
            'completion_percent': round(
                (completed_today / total_active * 100), 1
            ) if total_active > 0 else 0,
            'xp_earned_today': xp_today,
        })
