"""Signals to auto-create UserProfile when User is created."""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile

logger = logging.getLogger(__name__)
User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create profile for new users."""
    if created:
        try:
            UserProfile.objects.create(user=instance)
        except Exception as e:
            logger.error(f"Failed to create UserProfile for user {instance.id}: {e}")
