from django.db import models

class Toilet(models.Model):
    name = models.CharField(max_length=255) 
    # Koordinatlar ilk başta boş gelebilir (sen dolduracaksın)
    latitude = models.DecimalField(max_digits=13, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=13, decimal_places=10, null=True, blank=True)
    
    # Kullanıcının gönderdiği link burada duracak (Haritada gözükmeyecek)
    maps_url = models.URLField(max_length=500, null=True, blank=True, verbose_name="Google Maps Linki")
    
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True)
    
    # Admin Onayı
    is_approved = models.BooleanField(default=False, verbose_name="Onaylandı mı?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name