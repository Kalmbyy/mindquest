"""Models for quests app — Quest definitions and user completion logs."""
from django.db import models
from django.conf import settings
from django.utils import timezone


class Quest(models.Model):
    """A daily mission that users can complete to earn XP."""

    class Category(models.TextChoices):
        PHYSICAL = 'PHYSICAL', 'Fisik'
        MENTAL = 'MENTAL', 'Mental'
        SLEEP = 'SLEEP', 'Tidur'
        NUTRITION = 'NUTRITION', 'Nutrisi'
        MINDFULNESS = 'MINDFULNESS', 'Mindfulness'
        DIGITAL = 'DIGITAL', 'Digital Detox'

    class Difficulty(models.TextChoices):
        EASY = 'EASY', 'Mudah'
        MEDIUM = 'MEDIUM', 'Sedang'
        HARD = 'HARD', 'Sulit'

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=Category.choices)
    difficulty = models.CharField(
        max_length=10, choices=Difficulty.choices, default=Difficulty.EASY
    )
    xp_reward = models.PositiveIntegerField(default=10)
    icon = models.CharField(max_length=50, default='star',
                            help_text="Lucide icon name")
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'xp_reward']

    def __str__(self):
        return f"{self.title} ({self.xp_reward} XP)"


class UserQuestLog(models.Model):
    """Records each time a user completes a quest."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quest_logs'
    )
    quest = models.ForeignKey(
        Quest, on_delete=models.CASCADE, related_name='logs'
    )
    completed_date = models.DateField(default=timezone.localdate)
    xp_earned = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'quest', 'completed_date'],
                name='unique_user_quest_per_day'
            )
        ]

    def __str__(self):
        return f"{self.user.username} → {self.quest.title} ({self.completed_date})"
