from django.db import models

class Toilet(models.Model):
    # max_digits yerine max_length kullanıyoruz
    name = models.CharField(max_length=255) 
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name