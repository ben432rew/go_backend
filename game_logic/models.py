from django.db import models
from django.conf import settings


class Game(models.Model):
    player_w = models.ForeignKey(settings.AUTH_USER_MODEL)
    player_b = models.ForeignKey(settings.AUTH_USER_MODEL)
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    sgf_file = models.TextField()
