import re
import requests
from django.db import models
from decimal import Decimal, ROUND_HALF_UP

class Toilet(models.Model):
    name = models.CharField(max_length=255, verbose_name="Mekan Adı") 
    
    # Koordinatlar: Veritabanında 16 hane saklıyoruz (hata almamak için)
    # ama save metodunda 6 haneye yuvarlıyoruz.
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
        # 1. Google Maps Linkinden Koordinat Ayıklama (Otomasyon)
        if self.maps_url and (not self.latitude or not self.longitude):
            target_url = self.maps_url
            
            # Kısa link formatlarını (goo.gl, g.co, googleusercontent vb.) takip et
            short_domains = ["goo.gl", "g.co", "googleusercontent.com"]
            if any(domain in target_url for domain in short_domains):
                try:
                    # allow_redirects=True sayesinde asıl uzun URL'ye ulaşırız
                    response = requests.head(target_url, allow_redirects=True, timeout=5)
                    target_url = response.url
                except Exception as e:
                    # Hata durumunda loglama yapabilirsin
                    print(f"URL çözme hatası: {e}")

            # Regex: @lat,lng veya q=lat,lng gibi kalıpları yakalar
            # Negatif koordinatları da kapsar
            pattern = r"([-+]?\d{1,2}\.\d+),\s*([-+]?\d{1,3}\.\d+)"
            match = re.search(pattern, target_url)
            
            if match:
                self.latitude = Decimal(match.group(1))
                self.longitude = Decimal(match.group(2))

        # 2. Hassas Yuvarlama (6 Hane Hassasiyeti)
        # Matematiksel olarak 6 haneye quantize ediyoruz.
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