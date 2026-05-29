"""Tests for mood app."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from mood.models import MoodLog

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username='m', email='m@t.com', password='MindQuest2026!')


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_create_mood(auth_client):
    resp = auth_client.post('/api/mood/', {
        'mood_score': 4, 'energy_score': 3, 'note': 'Lumayan'
    }, format='json')
    assert resp.status_code == 201
    assert resp.data['mood_score'] == 4


@pytest.mark.django_db
def test_mood_invalid_score(auth_client):
    resp = auth_client.post('/api/mood/', {
        'mood_score': 9, 'energy_score': 3
    }, format='json')
    assert resp.status_code == 400


@pytest.mark.django_db
def test_mood_duplicate_same_day(auth_client):
    auth_client.post('/api/mood/', {'mood_score': 4, 'energy_score': 3}, format='json')
    resp = auth_client.post('/api/mood/', {'mood_score': 2, 'energy_score': 2}, format='json')
    assert resp.status_code == 400


@pytest.mark.django_db
def test_mood_history(auth_client):
    auth_client.post('/api/mood/', {'mood_score': 4, 'energy_score': 3}, format='json')
    resp = auth_client.get('/api/mood/history/')
    assert resp.status_code == 200
    assert len(resp.data) == 1
