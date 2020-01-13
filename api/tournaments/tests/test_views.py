import json
import pytest

from unittest import TestCase
from rest_framework.test import APIClient
from ..models import Tournament


@pytest.mark.django_db
class TournamentViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_prediction_list(self):
        response = self.client.get("/api/tournaments/")
        assert response.status_code == 200
        response_json = json.loads(response.content)
        assert len(response_json) == Tournament.objects.count()
