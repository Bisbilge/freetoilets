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
    # 1. LİSTE GÖRÜNÜMÜ: Artık tıklayınca doğrudan şikayet detayına gidecek
    list_display = ('id', 'toilet', 'reason', 'is_resolved', 'created_at')
    
    # 'id' ve 'toilet' sütunlarını tıklanabilir yapıyoruz (Şikayet detayını açar)
    list_display_links = ('id', 'toilet') 
    
    list_filter = ('reason', 'is_resolved', 'created_at')
    search_fields = ('description', 'toilet__name')
    actions = ['mark_as_resolved']

    # 2. DETAY SAYFASI: Sadece şikayet detayına girildiğinde görünecek özel link alanı
    readonly_fields = ('related_toilet_link', 'created_at')

    def related_toilet_link(self, obj):
        if obj.id and obj.toilet:
            # Tuvaletin düzenleme sayfasına giden URL'yi oluşturuyoruz
            url = reverse('admin:toilets_toilet_change', args=[obj.toilet.id])
            # Admin paneline yakışacak şık, mavi bir buton tasarımı
            return format_html(
                '<a href="{}" style="background-color: #1E90FF; color: white; padding: 6px 12px; '
                'border-radius: 4px; text-decoration: none; font-weight: bold; font-size: 13px;">'
                '🚀 {} Tuvaletini Düzenle'
                '</a>', 
                url, obj.toilet.name
            )
        return "-"
    
    related_toilet_link.short_description = 'Hızlı İşlem'

    @admin.action(description='Seçili şikayetleri "Çözüldü" olarak işaretle')
    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)