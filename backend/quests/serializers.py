"""Serializers for quests app."""
from rest_framework import serializers
from django.utils import timezone
from .models import Quest, UserQuestLog


class QuestSerializer(serializers.ModelSerializer):
    """Quest with completed-today flag for the current user."""
    is_completed_today = serializers.SerializerMethodField()
    category_display = serializers.CharField(
        source='get_category_display', read_only=True
    )
    difficulty_display = serializers.CharField(
        source='get_difficulty_display', read_only=True
    )

    class Meta:
        model = Quest
        fields = (
            'id', 'title', 'description',
            'category', 'category_display',
            'difficulty', 'difficulty_display',
            'xp_reward', 'icon', 'is_active',
            'is_completed_today',
        )

    def get_is_completed_today(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        today = timezone.localdate()
        return UserQuestLog.objects.filter(
            user=request.user, quest=obj, completed_date=today
        ).exists()


class UserQuestLogSerializer(serializers.ModelSerializer):
    """Read-only serializer for quest history."""
    quest_title = serializers.CharField(source='quest.title', read_only=True)
    quest_icon = serializers.CharField(source='quest.icon', read_only=True)
    quest_category = serializers.CharField(
        source='quest.get_category_display', read_only=True
    )

    class Meta:
        model = UserQuestLog
        fields = (
            'id', 'quest', 'quest_title', 'quest_icon', 'quest_category',
            'completed_date', 'xp_earned', 'created_at'
        )
        read_only_fields = fields
