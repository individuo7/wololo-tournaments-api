from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db.fields import AutoSlugField

from model_utils.models import TimeStampedModel

from api.tournaments.models import Game, Player
from api.users.models import User

from .documents import PlayerDocument


class Group(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField("slug", max_length=255, unique=True, populate_from=("name",))
    members = models.ManyToManyField(User)
    public = models.BooleanField(default=True)


class Transaction(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.deletion.CASCADE, related_name="transactions"
    )
    amount = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=255)

    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.SET_NULL
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")


class Prediction(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.deletion.CASCADE)
    transactions = GenericRelation(Transaction)

    @property
    def winner(self):
        winner = None
        prev_score = 0
        for score in self.scores.all():
            if score.score > prev_score:
                winner = score.player
                prev_score = score.score
        return winner


class Score(models.Model):
    prediction = models.ForeignKey(
        Prediction, on_delete=models.deletion.CASCADE, related_name="scores"
    )
    player = models.ForeignKey(Player, on_delete=models.deletion.CASCADE)
    score = models.PositiveSmallIntegerField()


@receiver(post_save, sender=Transaction)
def update_leaderboard(sender, instance, **kwargs):
    tournament_type = ContentType.objects.get(
        app_label="tournaments", model="tournament"
    )
    user = instance.user

    if instance.content_type == tournament_type:
        transactions = instance.content_object.transactions.filter(user=user)
        title = instance.content_object.slug
    else:
        transactions = Transaction.objects.filter(user=user).exclude(
            content_type=tournament_type
        )
        title = "no-tournament"

    gold = 0
    for transaction in transactions:
        gold += transaction.amount

    player = PlayerDocument(
        meta={"id": "{}-{}".format(title, user.id)},
        tournament=title,
        username=user.username,
        gold=gold,
    )
    player.save()
