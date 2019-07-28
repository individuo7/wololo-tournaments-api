from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_extensions.db.fields import AutoSlugField

from model_utils.models import TimeStampedModel
from api.tournaments.models import Game, Player
from api.users.models import User


class Group(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField("slug", max_length=255, unique=True, populate_from=("name",))
    members = models.ManyToManyField(User)
    public = models.BooleanField(default=True)


class Transaction(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
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
    winner = models.ForeignKey(Player, on_delete=models.deletion.CASCADE)
    votes = GenericRelation(Transaction)
