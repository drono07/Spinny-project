from rest_framework import serializers
from .models import Boxes
from spinny_project.settings import A1 
from datetime import timedelta,datetime
from django.utils import timezone
from django.db.models import Avg


class AdminBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boxes
        fields = ['id','length','breadth','height','area','volume','created_by','created_at','updated_at']


class BoxesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Boxes
        fields='__all__'