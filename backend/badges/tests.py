"""Tests for badges app — badge awarding logic."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from badges.models import Badge, UserBadge
from badges.services import check_and_award_badges
from quests.models import Quest

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username='b', email='b@t.com', password='MindQuest2026!')


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def xp_badge(db):
    return Badge.objects.create(
        name='Kolektor XP', description='500 XP', icon='gem', color='teal',
        criteria_type='TOTAL_XP', threshold=500, order=1
    )


@pytest.fixture
def level_badge(db):
    return Badge.objects.create(
        name='Naik Kelas', description='Level 5', icon='trending-up', color='blue',
        criteria_type='LEVEL', threshold=5, order=2
    )


@pytest.mark.django_db
def test_badge_awarded_when_threshold_met(user, xp_badge):
    user.profile.add_xp(500)
    new_badges = check_and_award_badges(user)
    assert len(new_badges) == 1
    assert new_badges[0]['name'] == 'Kolektor XP'
    assert UserBadge.objects.filter(user=user, badge=xp_badge).exists()


@pytest.mark.django_db
def test_badge_not_awarded_below_threshold(user, xp_badge):
    user.profile.add_xp(300)
    new_badges = check_and_award_badges(user)
    assert len(new_badges) == 0


@pytest.mark.django_db
def test_badge_not_awarded_twice(user, xp_badge):
    user.profile.add_xp(500)
    check_and_award_badges(user)
    new_badges = check_and_award_badges(user)  # Second check
    assert len(new_badges) == 0  # Already unlocked
    assert UserBadge.objects.filter(user=user).count() == 1


@pytest.mark.django_db
def test_level_badge_awarded(user, level_badge):
    user.profile.add_xp(1000)  # Level 5
    new_badges = check_and_award_badges(user)
    assert any(b['name'] == 'Naik Kelas' for b in new_badges)


@pytest.mark.django_db
def test_badge_list_endpoint(auth_client, xp_badge, level_badge):
    resp = auth_client.get('/api/badges/')
    assert resp.status_code == 200
    assert resp.data['total_count'] == 2
    assert resp.data['unlocked_count'] == 0


@pytest.mark.django_db
def test_completing_quest_awards_badge(auth_client, user):
    # Badge for 1 quest completion
    Badge.objects.create(
        name='Langkah Pertama', description='1 quest', icon='footprints',
        color='green', criteria_type='QUEST_COUNT', threshold=1, order=1
    )
    quest = Quest.objects.create(
        title='Test', description='x', category='PHYSICAL',
        difficulty='EASY', xp_reward=15
    )
    resp = auth_client.post(f'/api/quests/{quest.id}/complete/')
    assert resp.status_code == 201
    assert len(resp.data['new_badges']) == 1
    assert resp.data['new_badges'][0]['name'] == 'Langkah Pertama'
