from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import *

admin.site.register(Category, DraggableMPTTAdmin)
admin.site.register(Product, DraggableMPTTAdmin)
