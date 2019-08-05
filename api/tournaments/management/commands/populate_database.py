from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from factory import DjangoModelFactory, Faker

from api.contrib.elasticsearch import Client
from api.leaderboard.models import Prediction, Score, Transaction
from api.tournaments.models import Tournament, Player, Team, Game, PlayerGame
from api.users.models import User


es = Client()


class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")

    class Meta:
        model = User


class Command(BaseCommand):

    help = "Create and populate dummy tournaments"

    def handle(self, *args, **kwargs):
        es.indices.delete(index="player", ignore=[400, 404])
        Game.objects.all().delete()
        Player.objects.all().delete()
        Prediction.objects.all().delete()
        Score.objects.all().delete()
        Team.objects.all().delete()
        Tournament.objects.all().delete()
        Transaction.objects.all().delete()
        User.objects.filter(is_staff=False, is_superuser=False).delete()

        Tournament.objects.create(
            name="King of the desert 3",
            prize="$15,800",
            web="https://google.com/search?q=King+of+the+desert+3",
            banner="https://picsum.photos/1400/400",
            icon="https://picsum.photos/500",
        )
        Tournament.objects.create(
            name="Escape Champions League",
            prize="$60,000",
            web="https://google.com/search?q=Escape+Champions+League",
            banner="https://picsum.photos/1400/400",
            icon="https://picsum.photos/500",
        )
        Tournament.objects.create(
            name="AoE2 Hidden Cup 2",
            prize="$10,300",
            web="https://google.com/search?q=AoE2+Hidden+Cup+2",
            banner="https://picsum.photos/1400/400",
            icon="https://picsum.photos/500",
        )
        Tournament.objects.create(
            name="ECL Season 1: Southeast Asia",
            prize="$7,000",
            web="https://google.com/search?q=ECL+Season+1+Southeast+Asia",
            banner="https://picsum.photos/1400/400",
            icon="https://picsum.photos/500",
        )

        Player.objects.create(name="TheViper", country="NO")
        Player.objects.create(name="DauT", country="RS")
        Player.objects.create(name="Chris", country="CA")
        Player.objects.create(name="RiuT", country="BR")
        Player.objects.create(name="JorDan_23", country="DE")
        Player.objects.create(name="TaToH", country="ES")
        Player.objects.create(name="TheYo", country="CN")
        Player.objects.create(name="slam", country="CA")
        Player.objects.create(name="Liereyy", country="AT")

        for team in ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8"]:
            Team.objects.create(name=team, competitive=False)
        Team.objects.create(name="Secret")

        for i, tournament in enumerate(Tournament.objects.all()):
            for phase in [
                "K.O. Phase",
                "K.O. Phase",
                "K.O. Phase",
                "K.O. Phase",
                "K.O. Phase",
                "K.O. Phase",
                "Quarter-Finals",
                "Quarter-Finals",
                "Quarter-Finals",
                "Quarter-Finals",
                "Semi-Finals",
                "Semi-Finals",
                "Finals",
            ]:
                Game.objects.create(
                    tournament=tournament,
                    phase=phase,
                    date=timezone.now() + timedelta(days=i),
                    number_of_matches=7 if phase == "Finals" else 5,
                )

        players = Player.objects.all()
        for i, game in enumerate(Game.objects.all()):
            if game.phase not in ["Finals", "Semi-Finals"]:
                c = players.count()
                p1 = Team.objects.get(slug="p1")
                p2 = Team.objects.get(slug="p2")
                PlayerGame.objects.create(game=game, player=players[i % c], team=p1)
                PlayerGame.objects.create(
                    game=game, player=players[(i + 1) % c], team=p2
                )

        tournaments = Tournament.objects.all()
        c = tournaments.count()
        for i in range(100):
            user = UserFactory()
            tournament_1 = tournaments[i % c]
            tournament_2 = tournaments[(i + 1) % c]

            for game in list(tournament_1.games.all()[:4]) + list(
                tournament_2.games.all()[:4]
            ):
                playersgame = game.players.all()

                score_1 = i % game.number_of_matches
                score_2 = game.number_of_matches - score_1

                prediction = Prediction.objects.create(user=user, game=game)
                Score.objects.create(
                    prediction=prediction, player=playersgame[0].player, score=score_1
                )
                Score.objects.create(
                    prediction=prediction, player=playersgame[1].player, score=score_2
                )

            gold = [90, 90, 100, 100, 110, 110]
            for i, prediction in enumerate(Prediction.objects.filter(user=user)):
                if i % 2 == 0:
                    Transaction.objects.create(
                        user=user,
                        amount=gold[i % len(gold)],
                        description=str(game),
                        content_object=prediction.game.tournament,
                    )
