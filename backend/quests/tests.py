"""Tests for quests app — quest listing, completion, XP award, stats."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from quests.models import Quest, UserQuestLog

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='player', email='p@test.com', password='MindQuest2026!'
    )


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def quest(db):
    return Quest.objects.create(
        title='Minum air', description='8 gelas',
        category='NUTRITION', difficulty='EASY', xp_reward=15, icon='glass-water'
    )


@pytest.mark.django_db
def test_today_quests_requires_auth():
    client = APIClient()
    resp = client.get('/api/quests/today/')
    assert resp.status_code == 401


@pytest.mark.django_db
def test_today_quests_lists_active(auth_client, quest):
    Quest.objects.create(
        title='Inactive', description='x', category='MENTAL',
        difficulty='EASY', xp_reward=10, is_active=False
    )
    resp = auth_client.get('/api/quests/today/')
    assert resp.status_code == 200
    assert len(resp.data) == 1  # Only active quest
    assert resp.data[0]['title'] == 'Minum air'
    assert resp.data[0]['is_completed_today'] is False


@pytest.mark.django_db
def test_complete_quest_awards_xp(auth_client, user, quest):
    resp = auth_client.post(f'/api/quests/{quest.id}/complete/')
    assert resp.status_code == 201
    assert resp.data['profile']['total_xp'] == 15
    assert resp.data['profile']['current_streak'] == 1

    user.profile.refresh_from_db()
    assert user.profile.total_xp == 15
    assert UserQuestLog.objects.filter(user=user, quest=quest).exists()


@pytest.mark.django_db
def test_complete_quest_twice_same_day_fails(auth_client, quest):
    auth_client.post(f'/api/quests/{quest.id}/complete/')
    resp = auth_client.post(f'/api/quests/{quest.id}/complete/')
    assert resp.status_code == 400
    assert 'sudah diselesaikan' in resp.data['detail'].lower()


@pytest.mark.django_db
def test_complete_marks_is_completed_today(auth_client, quest):
    auth_client.post(f'/api/quests/{quest.id}/complete/')
    resp = auth_client.get('/api/quests/today/')
    assert resp.data[0]['is_completed_today'] is True


@pytest.mark.django_db
def test_levelup_in_complete_response(auth_client, db):
    # Quest worth 100 XP → instant level up to 2
    big_quest = Quest.objects.create(
        title='Big', description='x', category='PHYSICAL',
        difficulty='HARD', xp_reward=100
    )
    resp = auth_client.post(f'/api/quests/{big_quest.id}/complete/')
    assert resp.data['leveled_up'] is True
    assert resp.data['new_level'] == 2


@pytest.mark.django_db
def test_today_stats(auth_client, quest):
    auth_client.post(f'/api/quests/{quest.id}/complete/')
    resp = auth_client.get('/api/quests/today-stats/')
    assert resp.status_code == 200
    assert resp.data['completed_today'] == 1
    assert resp.data['xp_earned_today'] == 15


@pytest.mark.django_db
def test_quest_history(auth_client, quest):
    auth_client.post(f'/api/quests/{quest.id}/complete/')
    resp = auth_client.get('/api/quests/history/')
    assert resp.status_code == 200
    assert resp.data['count'] == 1
    assert resp.data['results'][0]['quest_title'] == 'Minum air'
