from django import forms
from .models import Toilet

class ToiletReportForm(forms.ModelForm):
    class Meta:
        model = Toilet
        # Kullanıcıya sadece bunları gösteriyoruz
        fields = ['name', 'maps_url', 'is_free', 'description']
        widgets = {
            'maps_url': forms.URLInput(attrs={
                'placeholder': 'https://www.google.com/maps/...',
                'required': 'required',
                'class': 'form-control'
            }),
        }