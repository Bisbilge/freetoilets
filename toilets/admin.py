from django.contrib import admin
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin
from .models import Toilet

@admin.register(Toilet)
class ToiletAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'is_approved', 'show_maps_url', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('name', 'description')
    
    # Geçmiş kayıtları tablosunda ekstra hangi sütunlar görünsün
    history_list_display = ["is_approved"]
    
    def show_maps_url(self, obj):
        if obj.maps_url:
            return format_html('<a href="{0}" target="_blank" style="color: #2b7de9; font-weight: bold;">Haritada Aç</a>', obj.maps_url)
        return "Link Yok"
    show_maps_url.short_description = "Google Maps"

    actions = ['make_approved']
    
    @admin.action(description='Seçili bildirimleri onayla')
    def make_approved(self, request, queryset):
        queryset.update(is_approved=True)

    def get_readonly_fields(self, request, obj=None):
        """
        Sadece sistemin oluşturduğu eklenme tarihi kilitlidir.
        Moderatörler onay kutusu dahil her alanı değiştirebilir.
        """
        return ('created_at',)