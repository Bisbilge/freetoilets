from django.contrib import admin
from .models import Toilet

@admin.register(Toilet)
class ToiletAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_free', 'price', 'code', 'created_at')
    list_filter = ('is_free',)
    search_fields = ('name', 'description')