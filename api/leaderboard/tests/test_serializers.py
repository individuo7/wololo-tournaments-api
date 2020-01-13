import pytest
import random

from unittest import TestCase
from tests.factories import (
    GameFactory,
    GroupFactory,
    PlayerFactory,
    PredictionFactory,
    ScoreFactory,
    UserFactory,
)
from api.leaderboard.serializers import (
    GroupSerializer,
    PredictionSerializer,
    ScoreSerializer,
)


@pytest.mark.django_db
class GroupSerializerTest(TestCase):
    def test_group_serializers(self):
        group = GroupFactory()
        expected = {
            "members": list(group.members.all()),
            "name": group.name,
            "public": group.public,
            "slug": group.slug,
        }
        serializer = GroupSerializer(group)
        assert serializer.data == expected


@pytest.mark.django_db
class ScoreSerializerTest(TestCase):
    def test_score_serializers(self):
        player = PlayerFactory()
        score = random.randint(1, 10)
        scoreRecord = ScoreFactory(player=player, score=score)
        expected = {"player": player.slug, "score": score}
        serializer = ScoreSerializer(scoreRecord)
        assert serializer.data == expected


@pytest.mark.django_db
class PredictionSerializerTest(TestCase):
    def test_prediction_serializers(self):
        user = UserFactory()
        game = GameFactory()
        prediction = PredictionFactory(user=user, game=game)
        expected = {
            "game": game.id,
            "id": prediction.id,
            "scores": list(prediction.scores.all()),
            "user": user.id,
        }
        serializer = PredictionSerializer(prediction)
        assert serializer.data == expected
