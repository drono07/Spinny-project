from django.contrib import admin
from .models import Boxes , Config

# Register your models here.



class BoxesAdmin(admin.ModelAdmin):
    list_display = ['length', 'breadth','height','created_by']
    search_fields =['length', 'breadth','height','created_by']

class ConfigAdmin(admin.ModelAdmin):
    list_display = ['average_area','average_volume','total_boxes','total_boxes_user','active']
    search_fields = ['average_area','average_volume','total_boxes']

admin.site.register(Boxes, BoxesAdmin)
admin.site.register(Config , ConfigAdmin)

