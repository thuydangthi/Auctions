from django.db import models


class CategoryRelationship(models.Model):
    child = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='category_parent')
    parent = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='category_child')
