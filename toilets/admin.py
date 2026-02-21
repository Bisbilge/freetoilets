from django.contrib import admin
from django.utils.html import format_html
from .models import Toilet

@admin.register(Toilet)
class ToiletAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_approved', 'show_maps_url', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('name', 'description')
    
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
        Alanların okunabilirlik (kilit) durumunu dinamik olarak belirleriz.
        """
        # 1. Sistem saati herkes için her zaman kilitlidir.
        readonly = ['created_at']
        
        # 2. Eğer kullanıcı Süper Kullanıcı DEĞİLSE (yani moderatörse),
        # is_approved kutucuğunu da kilitliyoruz ki işaretlemeye çalışmasın.
        if not request.user.is_superuser:
            readonly.append('is_approved')
            
        # DİKKAT: 'latitude' ve 'longitude' bu listede YER ALMADIĞI İÇİN
        # moderatörler tarafından özgürce değiştirilebilir.
        return tuple(readonly)

    def save_model(self, request, obj, form, change):
        """
        Arka plan güvenliği (Backend Security Validation)
        """
        if not request.user.is_superuser:
            # Moderatör kaydettiği an onay kesinlikle düşer.
            obj.is_approved = False
            self.message_user(request, f"Bilgi: '{obj.name}' moderatör işlemi olduğu için onay bekliyor.")
        
        super().save_model(request, obj, form, change)