from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from simple_history.admin import SimpleHistoryAdmin

# Kendi modellerini import et. 'ToiletReport' ismini kendi model isminle değiştir.
from .models import Toilet, ToiletReport 

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


# --- YENİ EKLENEN ŞİKAYET / RAPOR SİSTEMİ ADMİNİ ---

@admin.register(ToiletReport)
class ToiletReportAdmin(admin.ModelAdmin):
    # Admin panelinde görünecek sütunlar: İlgili tuvalet linki ve şikayet nedeni eklendi
    list_display = ('id', 'toilet_link', 'reason', 'is_resolved', 'created_at')
    
    # Sağ taraftaki filtreleme menüsü
    list_filter = ('reason', 'is_resolved', 'created_at')
    
    # Arama çubuğunda neye göre arama yapılacak
    search_fields = ('description', 'toilet__name')
    
    actions = ['mark_as_resolved']

    # 1. İstediğin özellik: Tek tıkla ilgili tuvaletin düzenleme sayfasına gitme
    def toilet_link(self, obj):
        if obj.toilet:
            # ÖNEMLİ: 'toilets' kısmı uygulamanın (app) adıdır. Uygulamanın adı farklıysa burayı güncelle.
            url = reverse('admin:toilets_toilet_change', args=[obj.toilet.id])
            return format_html('<a href="{}" style="font-weight:bold; color:#1E90FF; text-decoration:underline;">{} (Düzenle)</a>', url, obj.toilet.name)
        return "-"
    toilet_link.short_description = 'İlgili Tuvalet'

    # 2. Ekstra özellik: Şikayetleri topluca "Çözüldü" olarak işaretleme aksiyonu
    @admin.action(description='Seçili şikayetleri "Çözüldü" olarak işaretle')
    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)