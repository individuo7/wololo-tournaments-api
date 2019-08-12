from rest_framework.serializers import ModelSerializer, CharField
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
    winner = CharField(source="winner.slug")

    class Meta:
        model = Match
        fields = ["id", "winner", "civilizations"]


class GameSerializer(ModelSerializer):
    players = PlayerGameSerializer(many=True)
    matches = MatchGameSerializer(many=True)
    tournament = TournamentSerializerSmall()

    class Meta:
        model = Game
        fields = [
            "slug",
            "tournament",
            "date",
            "winner",
            "players",
            "number_of_matches",
            "matches",
        ]
