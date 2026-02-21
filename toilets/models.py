import re
from django.db import models
from decimal import Decimal, ROUND_HALF_UP

class Toilet(models.Model):
    name = models.CharField(max_length=255, verbose_name="Mekan Adı") 
    
    latitude = models.DecimalField(
        max_digits=22, 
        decimal_places=16, 
        null=True, 
        blank=True, 
        verbose_name="Enlem (Latitude)"
    )
    longitude = models.DecimalField(
        max_digits=22, 
        decimal_places=16, 
        null=True, 
        blank=True, 
        verbose_name="Boylam (Longitude)"
    )
    
    maps_url = models.URLField(
        max_length=500, 
        null=True, 
        blank=True, 
        verbose_name="Google Maps Linki"
    )
    
    is_free = models.BooleanField(default=True, verbose_name="Ücretsiz mi?")
    price = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="Ücret (Varsa)"
    )
    code = models.CharField(
        max_length=50, 
        null=True, 
        blank=True, 
        verbose_name="Giriş Kodu (Varsa)"
    )
    description = models.TextField(blank=True, verbose_name="Açıklama/Notlar")
    is_approved = models.BooleanField(default=False, verbose_name="Onaylandı mı?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")

    def save(self, *args, **kwargs):
        # 1. Uzun Google Maps Linkinden Koordinat Ayıklama (Offline/Statik)
        if self.maps_url and (not self.latitude or not self.longitude):
            # Regex 1: Standart @41.123,28.123 veya q=41.123,28.123 yapısı
            pattern_std = r"([-+]?\d{1,2}\.\d+),\s*([-+]?\d{1,3}\.\d+)"
            # Regex 2: Google'ın iç yapı formatı (!3d41.123!4d28.123)
            pattern_long = r"!3d([-+]?\d{1,2}\.\d+)!4d([-+]?\d{1,3}\.\d+)"

            # Önce standart formatı, yoksa 'long' formatını dene
            match = re.search(pattern_std, self.maps_url) or re.search(pattern_long, self.maps_url)

            if match:
                self.latitude = Decimal(match.group(1))
                self.longitude = Decimal(match.group(2))

        # 2. Hassas Yuvarlama (6 Hane Hassasiyeti)
        # Matematiksel olarak 10^-6 mertebesinde hassasiyet yeterlidir.
        if self.latitude is not None:
            self.latitude = Decimal(str(self.latitude)).quantize(
                Decimal('0.000001'), 
                rounding=ROUND_HALF_UP
            )
        if self.longitude is not None:
            self.longitude = Decimal(str(self.longitude)).quantize(
                Decimal('0.000001'), 
                rounding=ROUND_HALF_UP
            )
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tuvalet"
        verbose_name_plural = "Tuvaletler"
        ordering = ['-created_at']