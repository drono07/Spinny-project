from urllib import response
from boxes.models import Boxes ,Config
from rest_framework.response import Response

class BoxUtils:

    @classmethod
    def create_box(cls, length, breadth, height, user):
        box=Boxes.objects.create(
            length=length,
            breadth=breadth,
            height=height,
            created_by=str(user)
        )
        box.save()
        return box,"Success"

    @classmethod
    def create_config(cls , average_area ,average_volume , total_boxes , total_boxes_user):
        Config.objects.filter(active=True).update(active = False)
        config=Config.objects.create(
            average_area = average_area,
            average_volume = average_volume,
            total_boxes = total_boxes,
            total_boxes_user = total_boxes_user,
            active = True
        )
        config.save()
        return config
