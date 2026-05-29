"""MoodLog model — daily mood and energy check-in."""
from django.db import models
from django.conf import settings
from django.utils import timezone


class MoodLog(models.Model):
    """Daily mood + energy check-in (1-5 scale)."""
    SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mood_logs'
    )
    mood_score = models.PositiveSmallIntegerField(
        choices=SCORE_CHOICES, help_text="1=sangat buruk, 5=sangat baik"
    )
    energy_score = models.PositiveSmallIntegerField(
        choices=SCORE_CHOICES, help_text="1=sangat lelah, 5=sangat bertenaga"
    )
    note = models.TextField(blank=True, max_length=500)
    log_date = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-log_date', '-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'log_date'],
                name='unique_user_mood_per_day'
            )
        ]

    def __str__(self):
        return f"{self.user.username} — {self.log_date} (M:{self.mood_score} E:{self.energy_score})"
