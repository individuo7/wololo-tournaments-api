from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db.fields import AutoSlugField

from model_utils.models import TimeStampedModel

from api.tournaments.models import Game, Player
from api.users.documents import UserDocument
from api.users.models import User


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
    user = (
        User.objects.filter(id=instance.user.id)
        .annotate(total_gold=Sum("transactions__amount"))
        .first()
    )
    user = UserDocument(
        meta={"id": instance.user.id}, title=user.username, gold=user.total_gold
    )
    user.save()
