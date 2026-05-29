"""Models for users app — Custom User and UserProfile (gamification stats)."""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Custom User model — extend Django default to allow future fields."""
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """Gamification stats per user. Auto-created via signal."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    total_xp = models.PositiveIntegerField(default=0)
    current_level = models.PositiveIntegerField(default=1)
    current_streak = models.PositiveIntegerField(default=0)
    best_streak = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-total_xp']

    def __str__(self):
        return f"{self.user.username} — Level {self.current_level}"

    # ── XP & LEVELING LOGIC ────────────────────────────────────────────
    @staticmethod
    def xp_threshold_for_level(level: int) -> int:
        """
        XP needed to reach a given level.
        Level 1 = 0, Level 2 = 100, Level 3 = 250, Level 4 = 450, ...
        Formula: 50 * level * (level - 1)
        """
        return 50 * level * (level - 1)

    def calculate_level(self) -> int:
        """Calculate current level based on total_xp."""
        level = 1
        while self.xp_threshold_for_level(level + 1) <= self.total_xp:
            level += 1
        return level

    def xp_progress_to_next_level(self) -> dict:
        """Return dict with current/needed XP for next level."""
        current_threshold = self.xp_threshold_for_level(self.current_level)
        next_threshold = self.xp_threshold_for_level(self.current_level + 1)
        xp_in_level = self.total_xp - current_threshold
        xp_needed = next_threshold - current_threshold
        return {
            'current': xp_in_level,
            'needed': xp_needed,
            'percent': round((xp_in_level / xp_needed) * 100, 1) if xp_needed > 0 else 100,
        }

    def add_xp(self, amount: int) -> bool:
        """Add XP and recalculate level. Returns True if leveled up."""
        old_level = self.current_level
        self.total_xp += amount
        self.current_level = self.calculate_level()
        self.save(update_fields=['total_xp', 'current_level', 'updated_at'])
        return self.current_level > old_level

    # ── STREAK LOGIC ───────────────────────────────────────────────────
    def update_streak(self):
        """Update streak based on activity. Called on quest completion."""
        today = timezone.localdate()

        if self.last_activity_date is None:
            self.current_streak = 1
        elif self.last_activity_date == today:
            return  # Already counted today
        elif (today - self.last_activity_date).days == 1:
            self.current_streak += 1  # Consecutive day
        else:
            self.current_streak = 1  # Streak broken

        if self.current_streak > self.best_streak:
            self.best_streak = self.current_streak

        self.last_activity_date = today
        self.save(update_fields=[
            'current_streak', 'best_streak',
            'last_activity_date', 'updated_at'
        ])
