import pytest

from unittest import TestCase
from tests.factories import GameFactory, MatchFactory, PlayerFactory, TournamentFactory
from api.tournaments.serializers import (
    GameSerializer,
    MatchGameSerializer,
    PlayerSerializer,
    TournamentSerializer,
    TournamentSerializerSmall,
)


@pytest.mark.django_db
class TournamentSmallSerializerTest(TestCase):
    def test_tournament_serializers(self):
        tournament = TournamentFactory()
        expected = {"name": tournament.name, "slug": tournament.slug}
        serializer = TournamentSerializerSmall(tournament)
        assert serializer.data == expected


@pytest.mark.django_db
class TournamentSerializerTest(TestCase):
    def test_tournament_serializers(self):
        tournament = TournamentFactory()
        expected = {
            "banner": tournament.banner,
            "icon": tournament.icon,
            "name": tournament.name,
            "prize": tournament.prize,
            "slug": tournament.slug,
            "web": tournament.web,
        }
        serializer = TournamentSerializer(tournament)
        assert serializer.data == expected


@pytest.mark.django_db
class PlayerSerializerTest(TestCase):
    def test_player_serializers(self):
        player = PlayerFactory()
        expected = {"name": player.name, "slug": player.slug, "country": player.country}
        serializer = PlayerSerializer(player)
        assert serializer.data == expected


@pytest.mark.django_db
class MatchGameSerializerSerializerTest(TestCase):
    def test_match_game_serializers(self):
        match = MatchFactory()
        expected = {
            "id": match.id,
            "winner": match.winner.slug,
            "civilizations": list(match.civilizations.all()),
        }
        serializer = MatchGameSerializer(match)
        assert serializer.data == expected


@pytest.mark.django_db
class GameSerializerSerializerTest(TestCase):
    def test_Game_game_serializers(self):
        game = GameFactory()
        expected = {
            "date": game.date.isoformat() + "Z",
            "matches": list(game.matches.all()),
            "number_of_matches": game.number_of_matches,
            "players": list(game.players.all()),
            "score": "0:0",
            "slug": game.slug,
            "tournament": TournamentSerializerSmall(game.tournament).data,
            "winner": game.winner,
        }
        serializer = GameSerializer(game)
        assert serializer.data == expected
