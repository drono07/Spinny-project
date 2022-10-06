from urllib import response
from boxes.models import Boxes
from rest_framework.response import Response

class BoxUtils:

    @classmethod
    def calculate_area_volume(cls, length, breadth, height):
        area = 2 * (length * breadth + breadth * height + length * height)
        volume = length * breadth * height
        return area, volume

    @classmethod
    def create_box(cls, length, breadth, height, user):
        area, volume = cls.calculate_area_volume(length=length, breadth=breadth, height=height)
        box=Boxes.objects.create(
            length=length,
            breadth=breadth,
            height=height,
            area=area,
            volume=volume,
            created_by=user,
        )
        return box,"Success"

