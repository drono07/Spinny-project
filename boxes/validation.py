import bdb
from .models import Boxes, Config
from django.db.models import Avg
from datetime import timedelta,datetime
from django.utils import timezone
from spinny_project.settings import A1, V1, L1 , L2


def check_validity(user):
        try:
            config = Config.objects.get(active = True)
            A1 = config.average_area
            V1 = config.average_volume
            L1 = config.total_boxes
            L2 = config.total_boxes_user

        except Config.DoesNotExist:
            pass 
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