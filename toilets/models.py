import re
import requests
from django.db import models
from decimal import Decimal, ROUND_HALF_UP

class Toilet(models.Model):
    name = models.CharField(max_length=255, verbose_name="Mekan Adı") 
    
    # Koordinatlar: Veritabanında 16 hane saklıyoruz
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
        # 1. Google Maps Linkinden Koordinat Ayıklama
        if self.maps_url and (not self.latitude or not self.longitude):
            target_url = self.maps_url
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

            try:
                # stream=False yapıyoruz çünkü bazen sayfa içeriğini okumamız gerekecek
                response = requests.get(target_url, allow_redirects=True, timeout=10, headers=headers)
                final_url = response.url
                html_content = response.text # Sayfa içeriğini aldık

                # Regex 1: Standart @lat,lng veya q=lat,lng
                pattern_std = r"([-+]?\d{1,2}\.\d+),\s*([-+]?\d{1,3}\.\d+)"
                # Regex 2: Google'ın 'long' formatı (!3d41.123!4d28.123)
                pattern_long = r"!3d([-+]?\d{1,2}\.\d+)!4d([-+]?\d{1,3}\.\d+)"

                # Önce URL içinde ara
                match = re.search(pattern_std, final_url) or re.search(pattern_long, final_url)
                
                # Eğer URL'de bulamazsan HTML içeriği (meta tagler) içinde ara
                if not match:
                    match = re.search(pattern_std, html_content) or re.search(pattern_long, html_content)

                if match:
                    self.latitude = Decimal(match.group(1))
                    self.longitude = Decimal(match.group(2))
                    print(f"DEBUG: Başarıyla yakalandı -> {self.latitude}, {self.longitude}")
                else:
                    print(f"DEBUG: Hiçbir yerde koordinat bulunamadı: {final_url}")

            except Exception as e:
                print(f"URL çözme hatası: {e}")

        # 2. Hassas Yuvarlama (6 Hane - Matematikçi Hassasiyeti)
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