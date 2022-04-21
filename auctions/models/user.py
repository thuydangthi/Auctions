from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(null=False, unique=True)
    first_name = None
    last_name = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def hidden_name(self):
        username = self.username
        username = username[:len(username)//2] + '*' * \
            (len(username) - len(username)//2)
        return username
