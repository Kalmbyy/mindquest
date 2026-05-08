"""Serializers for users app."""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Handle new user registration."""
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password": "Password tidak cocok."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Profile with full gamification stats."""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    xp_progress = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'username', 'email',
            'total_xp', 'current_level',
            'current_streak', 'best_streak',
            'last_activity_date', 'xp_progress',
        )
        read_only_fields = fields

    def get_xp_progress(self, obj):
        return obj.xp_progress_to_next_level()


class UserSerializer(serializers.ModelSerializer):
    """Basic user info (used in nested responses)."""
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile')

    def get_profile(self, obj):
        try:
            return UserProfileSerializer(obj.profile).data
        except Exception:
            return None
