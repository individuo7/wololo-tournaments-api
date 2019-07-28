from django.contrib.auth.models import AbstractUser
from django.db import models

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    icon = models.ImageField(upload_to="icons", null=True)
    background = models.ImageField(upload_to="backgrounds", null=True)
    default_group = models.ForeignKey(
        "leaderboard.Group", null=True, on_delete=models.SET_NULL
    )

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
