from django.db import models

from submit.models import Game, Developer
from django.contrib.auth.models import User

# Create your models here.

class Letter(models.Model):
    name = 'bob'

    def __init__(self):
        return self.name
