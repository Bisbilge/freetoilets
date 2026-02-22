from django import forms
from .models import Toilet

class ToiletReportForm(forms.ModelForm):
    class Meta:
        model = Toilet
        # 'price' ve 'code' alanlarını listeye dahil ettik
        fields = ['name', 'maps_url', 'is_free', 'price', 'code', 'description']
        
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
                'placeholder': 'Ücretliyse fiyat (Örn: 10.00)',
                'step': '0.50',
                'min': '0'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Varsa kapı şifresi (Örn: 1234#)',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Temizlik durumu veya tam yer tarifi...'
            }),
        }