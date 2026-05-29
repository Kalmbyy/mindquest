"""Models for badges app — Achievement badges and user unlocks."""
from django.db import models
from django.conf import settings


class Badge(models.Model):
    """An achievement badge users can unlock."""

    class Criteria(models.TextChoices):
        TOTAL_XP = 'TOTAL_XP', 'Total XP'
        LEVEL = 'LEVEL', 'Level tertentu'
        STREAK = 'STREAK', 'Streak tertentu'
        QUEST_COUNT = 'QUEST_COUNT', 'Jumlah quest selesai'

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=50, default='award',
                            help_text="Lucide icon name")
    color = models.CharField(max_length=20, default='amber',
                             help_text="Tailwind color name")
    criteria_type = models.CharField(max_length=20, choices=Criteria.choices)
    threshold = models.PositiveIntegerField(
        help_text="Value needed to unlock (e.g. 1000 XP, 7 day streak)"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'threshold']

    def __str__(self):
        return f"{self.name} ({self.get_criteria_type_display()} ≥ {self.threshold})"


class UserBadge(models.Model):
    """Records a badge unlocked by a user."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='badges'
    )
    badge = models.ForeignKey(
        Badge, on_delete=models.CASCADE, related_name='unlocked_by'
    )
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-unlocked_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'badge'],
                name='unique_user_badge'
            )
        ]

    def __str__(self):
        return f"{self.user.username} unlocked {self.badge.name}"
