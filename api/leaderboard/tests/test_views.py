import json
import pytest

from unittest import TestCase
from rest_framework.test import APIClient
from ..models import Group, Prediction


@pytest.mark.django_db
class PredictionViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_prediction_list(self):
        response = self.client.get("/api/predictions/")
        assert response.status_code == 200
        response_json = json.loads(response.content)
        assert len(response_json) == Prediction.objects.count()


@pytest.mark.django_db
class GroupViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_prediction_list(self):
        response = self.client.get("/api/groups/")
        assert response.status_code == 200
        response_json = json.loads(response.content)
        assert len(response_json) == Group.objects.count()
