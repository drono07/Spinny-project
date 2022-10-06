from .models import Boxes
import django_filters

class BoxFilter(django_filters.FilterSet):
    length_gt = django_filters.NumberFilter(field_name="length", lookup_expr="gt")
    length_lt = django_filters.NumberFilter(field_name="length", lookup_expr="lt")
    heigth_gt = django_filters.NumberFilter(field_name="heigth", lookup_expr="gt")
    heigth_lt = django_filters.NumberFilter(field_name="heigth", lookup_expr="lt")
    breadth_gt = django_filters.NumberFilter(field_name="breadth", lookup_expr="gt")
    breadth_lt = django_filters.NumberFilter(field_name="breadth", lookup_expr="lt")
    area_gt = django_filters.NumberFilter(field_name="area", lookup_expr="gt")
    area_lt = django_filters.NumberFilter(field_name="area", lookup_expr="lt")
    volume_gt = django_filters.NumberFilter(field_name="volume", lookup_expr="gt")
    volume_lt = django_filters.NumberFilter(field_name="volume", lookup_expr="lt")

    class Meta:
        model=Boxes
        fields=['length','breadth', 'height', 'area','volume','length_gt','area_gt','length_lt','area_lt','heigth_gt','heigth_lt','breadth_gt','breadth_gt', 'volume_gt', 'volume_lt']