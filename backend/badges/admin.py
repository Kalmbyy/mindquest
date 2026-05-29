from django.contrib import admin
from .models import Badge, UserBadge


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'criteria_type', 'threshold', 'icon', 'color', 'order')
    list_filter = ('criteria_type',)
    list_editable = ('order',)


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'unlocked_at')
    search_fields = ('user__username', 'badge__name')
