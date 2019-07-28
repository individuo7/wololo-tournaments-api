from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from api.tournaments.models import Game, Player


class Group(TimeStampedModel):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField("users.User")
    public = models.BooleanField(default=True)


class User(AbstractUser):
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    icon = models.ImageField(upload_to="icons", null=True)
    background = models.ImageField(upload_to="backgrounds", null=True)
    default_group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


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
