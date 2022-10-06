from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Boxes(models.Model):
    length=models.IntegerField()
    breadth=models.IntegerField()
    height=models.IntegerField()
    area=models.IntegerField()
    volume=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by=models.CharField(max_length=10)

