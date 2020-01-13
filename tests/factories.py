import random

from api.leaderboard.models import Group, Prediction, Score
from api.tournaments.models import Game, Team, Player, Tournament, Match
from api.users.models import User
from datetime import datetime
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = Faker("email")
    username = Faker("user_name")
    password = Faker("password")
    is_active = True


class TournamentFactory(DjangoModelFactory):
    class Meta:
        model = Tournament

    name = Faker("name")
    slug = Faker("slug")
    prize = Faker("sentence")
    web = Faker("url")


class PlayerFactory(DjangoModelFactory):
    class Meta:
        model = Player

    name = Faker("name")
    slug = Faker("slug")
    country = Faker("name")


class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game

    tournament = SubFactory(TournamentFactory)
    phase = Faker("name")
    date = datetime(2020, 1, 1)
    number_of_matches = random.randint(1, 10)
    slug = Faker("slug")


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    name = Faker("name")
    slug = Faker("slug")


class PredictionFactory(DjangoModelFactory):
    class Meta:
        model = Prediction

    user = SubFactory(UserFactory)
    game = SubFactory(GameFactory)


class ScoreFactory(DjangoModelFactory):
    class Meta:
        model = Score

    prediction = SubFactory(PredictionFactory)
    player = SubFactory(PlayerFactory)
    score = random.randint(1, 10)


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    name = Faker("name")
    slug = Faker("slug")
    competitive = True


class MatchFactory(DjangoModelFactory):
    class Meta:
        model = Match

    game = SubFactory(GameFactory)
    winner = SubFactory(TeamFactory)
