from django.contrib import admin
from .models import *


@admin.register(Category)
class CatetgoryAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'description',
                    'created_at'
                    )



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title',)