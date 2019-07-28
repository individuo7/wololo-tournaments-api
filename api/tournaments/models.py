from django.db import models
from django.forms import ValidationError
from django_extensions.db.fields import AutoSlugField
from model_utils.models import TimeStampedModel


class Tournament(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField("slug", max_length=255, unique=True, populate_from=("name",))
    prize = models.CharField(max_length=255)
    web = models.URLField()
    banner = models.ImageField(upload_to="tournaments/banners", blank=True, null=True)
    icon = models.ImageField(upload_to="tournaments/icons", blank=True, null=True)

    def __str__(self):
        return self.name


class Player(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField("slug", max_length=255, unique=True, populate_from=("name",))
    # TODO: add country choices
    country = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Team(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField("slug", max_length=255, unique=True, populate_from=("name",))
    competitive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Game(TimeStampedModel):
    tournament = models.ForeignKey(Tournament, on_delete=models.deletion.CASCADE)
    phase = models.CharField(max_length=30)
    date = models.DateTimeField()
    number_of_matches = models.PositiveSmallIntegerField()

    @property
    def winner(self):
        # TODO: calculate using self.number_of_matches and self.matches.all()
        return None

    def __str__(self):
        return "{} - {} game of '{}' tournament".format(
            self.id, self.phase, self.tournament
        )


class Match(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.deletion.CASCADE, related_name="matches"
    )
    winner = models.ForeignKey(Team, on_delete=models.deletion.CASCADE)

    def clean(self):
        if self.winner not in [x.team for x in self.game.players.all()]:
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
    # TODO: add civilization choices
    civilization = models.CharField(max_length=30, blank=True, null=True)

    def clean(self):
        if self.match.game != self.game:
            raise ValidationError("invalid game.")
        if self.player not in [x.player for x in self.game.players.all()]:
            raise ValidationError("invalid player.")

    class Meta:
        unique_together = ["match", "game", "player"]


class PlayerGame(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.deletion.CASCADE, related_name="players"
    )
    player = models.ForeignKey(Player, on_delete=models.deletion.CASCADE)
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "{} in {} game".format(self.player.name, self.game.phase)
