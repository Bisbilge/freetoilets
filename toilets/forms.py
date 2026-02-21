from django import forms
from .models import Toilet

class ToiletReportForm(forms.ModelForm):
    class Meta:
        model = Toilet
        # 'price' alanını listeye dahil ettik
        fields = ['name', 'maps_url', 'is_free', 'price', 'description']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mekan Adı (Örn: Beşiktaş Meydan Tuvaleti)',
            }),
            'maps_url': forms.URLInput(attrs={
                'placeholder': 'https://maps.google.com/...',
                'required': 'required',
                'class': 'form-control'
            }),
            'is_free': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ücretliyse fiyat (Örn: 5.00 veya 10)',
                'step': '0.50',  # 5.50 gibi küsüratlı girişlere izin verir
                'min': '0'       # Negatif fiyat girilmesini engeller
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Varsa eklemek istedikleriniz (Temizlik durumu, kapı şifresi vb.)'
            }),
        }