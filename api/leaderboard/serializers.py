from django.db import transaction
from rest_framework.serializers import CharField, ModelSerializer
from .models import Group, Prediction, Score
from api.tournaments.models import Player


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ["slug", "name", "members", "public"]


class ScoreSerializer(ModelSerializer):
    player = CharField(source="player.slug")

    class Meta:
        model = Score
        fields = ["player", "score"]


class PredictionSerializer(ModelSerializer):
    scores = ScoreSerializer(many=True)

    class Meta:
        model = Prediction
        fields = ["id", "user", "game", "scores"]

    @transaction.atomic()
    def create(self, validated_data):
        scores = validated_data.pop("scores")
        prediction = Prediction.objects.create(**validated_data)
        for score in scores:
            Score.objects.create(
                prediction=prediction,
                player=Player.objects.get(**score.pop("player")),
                **score
            )
        return prediction
