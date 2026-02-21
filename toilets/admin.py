from django.contrib import admin
from django.utils.html import format_html
from .models import Toilet

@admin.register(Toilet)
class ToiletAdmin(admin.ModelAdmin):
    # Panelde neleri göreceksin
    list_display = ('name', 'is_approved', 'show_maps_url', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('name', 'description')
    
    # Maps linkini tıklanabilir buton yapalım
    def show_maps_url(self, obj):
        if obj.maps_url:
            return format_html('<a href="{0}" target="_blank">Haritada Aç</a>', obj.maps_url)
        return "Link Yok"
    show_maps_url.short_description = "Google Maps"

    # Toplu onaylama aksiyonu
    actions = ['make_approved']
    @admin.action(description='Seçili bildirimleri onayla')
    def make_approved(self, request, queryset):
        queryset.update(is_approved=True)