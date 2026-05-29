"""Views for users app — register, profile, leaderboard."""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from .serializers import (
    RegisterSerializer, UserProfileSerializer, UserSerializer,
    LeaderboardEntrySerializer,
)


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ — create new user, return JWT tokens."""
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Registrasi berhasil!',
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveAPIView):
    """GET /api/auth/profile/ — return current user's profile + stats."""
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile


class CurrentUserView(generics.RetrieveAPIView):
    """GET /api/auth/me/ — return basic info of authenticated user."""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class LeaderboardView(APIView):
    """GET /api/leaderboard/ — top 50 users by XP + current user's rank."""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        profiles = list(
            UserProfile.objects.select_related('user').order_by('-total_xp', 'user__username')
        )

        # Build ranked entries
        entries = []
        my_rank = None
        for idx, profile in enumerate(profiles, start=1):
            profile.rank = idx
            if profile.user_id == request.user.id:
                my_rank = idx
            if idx <= 50:
                entries.append(profile)

        serializer = LeaderboardEntrySerializer(entries, many=True)
        return Response({
            'leaderboard': serializer.data,
            'my_rank': my_rank,
            'total_players': len(profiles),
        })
