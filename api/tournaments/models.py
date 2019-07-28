from django.db import models
from model_utils.models import TimeStampedModel


class Tournament(TimeStampedModel):
    name = models.CharField(max_length=255)
    prize = models.CharField(max_length=255)
    web = models.URLField()


class Player(TimeStampedModel):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=60)


class Team(TimeStampedModel):
    name = models.CharField(max_length=255)


class Game(TimeStampedModel):
    tournament = models.ForeignKey(Tournament, on_delete=models.deletion.CASCADE)
    date = models.DateTimeField()
    winner = models.ForeignKey(Player, null=True, on_delete=models.deletion.CASCADE)


class PlayerGame(models.Model):
    game = models.ForeignKey(Game, on_delete=models.deletion.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.deletion.CASCADE)
    civilization = models.CharField(max_length=30, blank=True, null=True)
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    team_number = models.PositiveSmallIntegerField(null=True)
