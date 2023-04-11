from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Boxes(models.Model):
    length=models.IntegerField()
    breadth=models.IntegerField()
    height=models.IntegerField()
    area=models.IntegerField(null=True,blank=True)
    volume=models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by=models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        self.area, self.volume = self.calculate_area_volume()
        super().save(*args, **kwargs)

    def calculate_area_volume(self):
        l = int(self.length)
        b = int(self.breadth)
        h = int(self.height)

        area = 2 * (l * b + b * h + l * h)
        volume =  l* b * h
    
        return area, volume

class Config(models.Model):
    average_area = models.IntegerField(default=100)
    average_volume = models.IntegerField(default=1000)
    total_boxes = models.IntegerField(default=100)
    total_boxes_user = models.IntegerField(default=50)
    active = models.BooleanField(default= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     self.objects.filter(active = True).update(active =False)
    #     super().save(*args, **kwargs)




