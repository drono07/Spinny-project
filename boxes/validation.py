import bdb
from .models import Boxes
from django.db.models import Avg
from spinny_project.settings import A1 , V1 , L1 , L2 
from datetime import timedelta,datetime
from django.utils import timezone


def check_validity(user):
        if Boxes.objects.all().count() == 0 :
            return True
        area = Boxes.objects.all().aggregate(Avg('area'))
        if area['area__avg'] > A1 :
            return False

        volume =  Boxes.objects.all().aggregate(Avg('volume'))
        if volume['volume__avg'] > V1 :
            return False     

        datetime_one_week_ago = timezone.now().date() - timedelta(days=7)

        boxes_last_week = Boxes.objects.filter(created_at__gt=datetime_one_week_ago).count()
        if boxes_last_week > L1 :
            return False
        
        boxes_last_week_by_user = Boxes.objects.filter(created_by=user,created_at__gt=datetime_one_week_ago).count()
        if boxes_last_week_by_user > L2 :
            return False
        return True 