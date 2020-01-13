from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.forms import ValidationError
from django_extensions.db.fields import AutoSlugField
from model_utils.models import TimeStampedModel
from .choices import CIVILIZATION_CHOICES, COUNTRY_CHOICES


class Tournament(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField("slug", max_length=255, unique=True, populate_from=("name",))
    prize = models.CharField(max_length=255)
    web = models.URLField()
    banner = models.ImageField(upload_to="tournaments/banners", blank=True, null=True)
    icon = models.ImageField(upload_to="tournaments/icons", blank=True, null=True)
    transactions = GenericRelation("leaderboard.Transaction")

    def __str__(self):
        return self.name


class Player(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField("slug", max_length=255, unique=True, populate_from=("name",))
    country = models.CharField(max_length=60, choices=COUNTRY_CHOICES)

    def __str__(self):
        return self.name


class Team(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField("slug", max_length=255, unique=True, populate_from=("name",))
    competitive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Game(TimeStampedModel):
    tournament = models.ForeignKey(
        Tournament, on_delete=models.deletion.CASCADE, related_name="games"
    )
    phase = models.CharField(max_length=30)
    date = models.DateTimeField()
    number_of_matches = models.PositiveSmallIntegerField()
    slug = AutoSlugField(
        "slug", max_length=255, unique=True, populate_from=(["tournament", "phase"])
    )

    @property
    def winner(self):
        # TODO: calculate using self.number_of_matches and self.matches.all()
        return None

    @property
    def player_list(self):
        return " vs ".join([x.player.name for x in self.players.all()])

    def __str__(self):
        return "*{}* {} tournament".format(self.tournament, self.player_list)


class Match(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.deletion.CASCADE, related_name="matches"
    )
    winner = models.ForeignKey(
        Team, on_delete=models.deletion.CASCADE, blank=True, null=True
    )

    def clean(self):
        if self.winner is not None and self.winner not in [
            x.team for x in self.game.players.all()
        ]:
            raise ValidationError("invalid team.")

    def __str__(self):
        players = " vs ".join([x.player.name for x in self.game.players.all()])
        return "{} - {}".format(self.id, players)


class CivilizationMatch(models.Model):
    match = models.ForeignKey(
        Match, on_delete=models.deletion.CASCADE, related_name="civilizations"
    )
    game = models.ForeignKey(Game, on_delete=models.deletion.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.deletion.CASCADE)
    civilization = models.CharField(
        max_length=30, blank=True, null=True, choices=CIVILIZATION_CHOICES
    )

    def clean(self):
        if self.match.game != self.game:
            raise ValidationError("invalid game.")
        if self.player not in [x.player for x in self.game.players.all()]:
            raise ValidationError("invalid player.")

    class Meta:
        unique_together = ["match", "game", "player"]

    def __str__(self):
        return "{} using {}".format(self.player, self.civilization)


class PlayerGame(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.deletion.CASCADE, related_name="players"
    )
    player = models.ForeignKey(Player, on_delete=models.deletion.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.deletion.CASCADE)

    def __str__(self):
        return "{} in {} game".format(self.player.name, self.game.phase)
