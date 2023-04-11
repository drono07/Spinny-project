from urllib import response
from boxes.models import Boxes
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

