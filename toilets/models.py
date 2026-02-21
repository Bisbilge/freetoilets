from django.db import models
from decimal import Decimal, ROUND_HALF_UP

class Toilet(models.Model):
    name = models.CharField(max_length=255, verbose_name="Mekan Adı") 
    
    # Koordinatlar: max_digits=13 ve decimal_places=10 Google'dan gelen uzun veriyi 
    # hata vermeden kabul eder, ancak biz save metodunda bunu 6 haneye indireceğiz.
    latitude = models.DecimalField(
        max_digits=20, 
        decimal_places=6, 
        null=True, 
        blank=True, 
        verbose_name="Enlem (Latitude)"
    )
    longitude = models.DecimalField(
        max_digits=20, 
        decimal_places=6, 
        null=True, 
        blank=True, 
        verbose_name="Boylam (Longitude)"
    )
    
    # Kullanıcının formdan gönderdiği Google Maps linki
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
    
    # Admin Onay Mekanizması
    is_approved = models.BooleanField(default=False, verbose_name="Onaylandı mı?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")

    def save(self, *args, **kwargs):
        """
        Google Maps'ten kopyalanan 41.034943016249244 gibi çok uzun koordinatları
        veritabanına kaydetmeden önce 6 haneye (hassasiyet kaybı olmadan) yuvarlar.
        """
        if self.latitude is not None:
            # Decimal kullanarak hassas yuvarlama yapıyoruz
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