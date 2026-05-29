"""Serializers for badges app."""
from rest_framework import serializers
from .models import Badge, UserBadge


class BadgeSerializer(serializers.ModelSerializer):
    is_unlocked = serializers.SerializerMethodField()
    unlocked_at = serializers.SerializerMethodField()

    class Meta:
        model = Badge
        fields = (
            'id', 'name', 'description', 'icon', 'color',
            'criteria_type', 'threshold', 'is_unlocked', 'unlocked_at'
        )

    def get_is_unlocked(self, obj):
        unlocked = self.context.get('unlocked_ids', set())
        return obj.id in unlocked

    def get_unlocked_at(self, obj):
        unlocked_map = self.context.get('unlocked_map', {})
        dt = unlocked_map.get(obj.id)
        return dt.isoformat() if dt else None
