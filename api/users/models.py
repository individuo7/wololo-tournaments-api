from api.contrib.elasticsearch import Client
from django.contrib.auth.models import AbstractUser
from django.db import models
from elasticsearch_dsl import Search

client = Client()


class User(AbstractUser):
    icon = models.CharField(null=True, blank=True, max_length=30)
    background = models.ImageField(upload_to="backgrounds", null=True)
    background_color = models.CharField(blank=True, max_length=30)
    default_group = models.ForeignKey(
        "leaderboard.Group", null=True, on_delete=models.SET_NULL
    )

    @property
    def gold(self):
        qs = (
            Search(using=client, index="player")
            .query("match", username=self.username)
            .execute()
        )
        return qs[0]["gold"] if len(qs) else 0

    def __str__(self):
        return self.username
