from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    is_visible = models.BooleanField()
    url = models.CharField(max_length=255, default='', unique=True)
