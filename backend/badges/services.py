"""
Badge awarding logic — checks criteria and unlocks badges for a user.
Called after quest completion.
"""
from django.db import IntegrityError
from .models import Badge, UserBadge


def check_and_award_badges(user) -> list:
    """
    Check all badge criteria against user's current stats.
    Award any newly-earned badges. Returns list of newly unlocked badge dicts.
    """
    profile = user.profile
    quest_count = user.quest_logs.count()

    # Map criteria type to the user's current value
    current_values = {
        Badge.Criteria.TOTAL_XP: profile.total_xp,
        Badge.Criteria.LEVEL: profile.current_level,
        Badge.Criteria.STREAK: profile.best_streak,
        Badge.Criteria.QUEST_COUNT: quest_count,
    }

    already_unlocked_ids = set(
        UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
    )

    newly_unlocked = []
    eligible_badges = Badge.objects.exclude(id__in=already_unlocked_ids)

    for badge in eligible_badges:
        current = current_values.get(badge.criteria_type, 0)
        if current >= badge.threshold:
            try:
                UserBadge.objects.create(user=user, badge=badge)
                newly_unlocked.append({
                    'name': badge.name,
                    'description': badge.description,
                    'icon': badge.icon,
                    'color': badge.color,
                })
            except IntegrityError:
                pass  # Race condition — already unlocked

    return newly_unlocked
