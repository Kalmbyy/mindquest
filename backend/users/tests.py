"""Tests for users app — auth, profile, XP/leveling/streak logic."""
import pytest
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from users.models import UserProfile

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='abiyyu', email='abiyyu@test.com', password='MindQuest2026!'
    )


@pytest.fixture
def auth_client(client, user):
    client.force_authenticate(user=user)
    return client


# ── Profile auto-creation ─────────────────────────────────────────────
@pytest.mark.django_db
def test_profile_auto_created_on_user_creation(user):
    assert hasattr(user, 'profile')
    assert user.profile.total_xp == 0
    assert user.profile.current_level == 1
    assert user.profile.current_streak == 0


# ── XP & Leveling ─────────────────────────────────────────────────────
@pytest.mark.django_db
def test_xp_threshold_formula():
    assert UserProfile.xp_threshold_for_level(1) == 0
    assert UserProfile.xp_threshold_for_level(2) == 100
    assert UserProfile.xp_threshold_for_level(3) == 300
    assert UserProfile.xp_threshold_for_level(4) == 600
    assert UserProfile.xp_threshold_for_level(5) == 1000


@pytest.mark.django_db
def test_add_xp_no_levelup(user):
    leveled = user.profile.add_xp(50)
    assert user.profile.total_xp == 50
    assert user.profile.current_level == 1
    assert leveled is False


@pytest.mark.django_db
def test_add_xp_triggers_levelup(user):
    leveled = user.profile.add_xp(100)
    assert user.profile.total_xp == 100
    assert user.profile.current_level == 2
    assert leveled is True


@pytest.mark.django_db
def test_add_xp_multiple_levels_at_once(user):
    leveled = user.profile.add_xp(300)
    assert user.profile.current_level == 3
    assert leveled is True


@pytest.mark.django_db
def test_xp_progress_calculation(user):
    user.profile.add_xp(150)  # Level 2 (needs 100), 50 into level 2
    progress = user.profile.xp_progress_to_next_level()
    assert progress['current'] == 50   # 150 - 100
    assert progress['needed'] == 200   # 300 - 100
    assert progress['percent'] == pytest.approx(25.0, abs=0.1)


# ── Streak logic ──────────────────────────────────────────────────────
@pytest.mark.django_db
def test_streak_first_activity(user):
    user.profile.update_streak()
    assert user.profile.current_streak == 1
    assert user.profile.best_streak == 1


@pytest.mark.django_db
def test_streak_same_day_no_change(user):
    user.profile.update_streak()
    user.profile.update_streak()  # Same day again
    assert user.profile.current_streak == 1


@pytest.mark.django_db
def test_streak_consecutive_day(user):
    yesterday = timezone.localdate() - timedelta(days=1)
    user.profile.last_activity_date = yesterday
    user.profile.current_streak = 3
    user.profile.save()

    user.profile.update_streak()
    assert user.profile.current_streak == 4


@pytest.mark.django_db
def test_streak_resets_after_gap(user):
    three_days_ago = timezone.localdate() - timedelta(days=3)
    user.profile.last_activity_date = three_days_ago
    user.profile.current_streak = 5
    user.profile.best_streak = 5
    user.profile.save()

    user.profile.update_streak()
    assert user.profile.current_streak == 1  # Reset
    assert user.profile.best_streak == 5     # Best preserved


# ── Auth endpoints ────────────────────────────────────────────────────
@pytest.mark.django_db
def test_register_success(client):
    resp = client.post('/api/auth/register/', {
        'username': 'newuser', 'email': 'new@test.com',
        'password': 'StrongPass123!', 'password_confirm': 'StrongPass123!'
    }, format='json')
    assert resp.status_code == 201
    assert 'tokens' in resp.data
    assert resp.data['tokens']['access']
    assert User.objects.filter(username='newuser').exists()


@pytest.mark.django_db
def test_register_password_mismatch(client):
    resp = client.post('/api/auth/register/', {
        'username': 'newuser', 'email': 'new@test.com',
        'password': 'StrongPass123!', 'password_confirm': 'Different123!'
    }, format='json')
    assert resp.status_code == 400


@pytest.mark.django_db
def test_login_returns_tokens(client, user):
    resp = client.post('/api/auth/login/', {
        'username': 'abiyyu', 'password': 'MindQuest2026!'
    }, format='json')
    assert resp.status_code == 200
    assert 'access' in resp.data
    assert 'refresh' in resp.data


@pytest.mark.django_db
def test_profile_requires_auth(client):
    resp = client.get('/api/auth/profile/')
    assert resp.status_code == 401


@pytest.mark.django_db
def test_profile_returns_stats(auth_client):
    resp = auth_client.get('/api/auth/profile/')
    assert resp.status_code == 200
    assert resp.data['current_level'] == 1
    assert 'xp_progress' in resp.data


# ── Leaderboard ───────────────────────────────────────────────────────
@pytest.mark.django_db
def test_leaderboard_ranks_by_xp(auth_client, user):
    other = User.objects.create_user(username='other', email='o@t.com', password='Pass12345!')
    other.profile.add_xp(500)
    user.profile.add_xp(100)

    resp = auth_client.get('/api/leaderboard/')
    assert resp.status_code == 200
    board = resp.data['leaderboard']
    assert board[0]['username'] == 'other'  # Higher XP first
    assert board[0]['rank'] == 1
