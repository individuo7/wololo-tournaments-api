from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from .models import CivilizationMatch, Game, Match, Player, PlayerGame, Tournament


class TournamentSerializer(ModelSerializer):
    class Meta:
        model = Tournament
        fields = ["slug", "name", "prize", "web", "banner", "icon"]


class TournamentSerializerSmall(ModelSerializer):
    class Meta:
        model = Tournament
        fields = ["slug", "name"]


class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = ["name", "slug", "country"]


class PlayerGameSerializer(ModelSerializer):
    player = PlayerSerializer()
    team = CharField(source="team.slug")

    class Meta:
        model = PlayerGame
        fields = ["player", "team"]


class CivilizationMatchSerializer(ModelSerializer):
    player = CharField(source="player.slug")

    class Meta:
        model = CivilizationMatch
        fields = ["player", "civilization"]


class MatchGameSerializer(ModelSerializer):
    civilizations = CivilizationMatchSerializer(many=True)
    winner = SerializerMethodField()

    class Meta:
        model = Match
        fields = ["id", "winner", "civilizations"]

    def get_winner(self, obj):
        return obj.winner.slug if obj.winner else None


class GameSerializer(ModelSerializer):
    players = PlayerGameSerializer(many=True)
    matches = MatchGameSerializer(many=True)
    tournament = TournamentSerializerSmall()
    score = SerializerMethodField()

    def get_score(self, obj):
        return "0:0"

    class Meta:
        model = Game
        fields = [
            "date",
            "matches",
            "number_of_matches",
            "players",
            "score",
            "slug",
            "tournament",
            "winner",
        ]
