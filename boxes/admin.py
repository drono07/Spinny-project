from django.contrib import admin
from .models import Boxes

# Register your models here.



class BoxesAdmin(admin.ModelAdmin):
    list_display = ['length', 'breadth','height','created_by','area']
    search_fields =['length', 'breadth','height','created_by','area']


admin.site.register(Boxes, BoxesAdmin)
