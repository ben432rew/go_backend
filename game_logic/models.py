from django.db import models
from django.conf import settings


class Game(models.Model):
    player_w = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='%(class)s_w_requests_created')
    player_b = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='%(class)s_b_requests_created')
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    sgf_file = models.TextField()
