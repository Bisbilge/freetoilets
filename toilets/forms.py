from django import forms
from .models import Toilet, ToiletReport  # YENİ: ToiletReport modelini import ettik
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

# 1. YENİ TUVALET EKLEME FORMU (Senin mevcut formun)
class ToiletReportForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = Toilet
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

# 2. YENİ EKLENEN: HARİTADAKİ MEVCUT TUVALETİ ŞİKAYET ETME FORMU
class ToiletIssueForm(forms.ModelForm):
    # Şikayet formunu da botlardan korumak için captcha ekliyoruz
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = ToiletReport
        # Kullanıcıdan sadece şikayet nedenini ve açıklamasını istiyoruz. 
        # Hangi tuvalet olduğu URL'den (id) gelecek, view içinde biz ekleyeceğiz.
        fields = ['reason', 'description']
        
        widgets = {
            'reason': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required',
                'style': 'width: 100%; padding: 12px; border-radius: 8px; border: 2px solid #CED6E0; font-size: 16px;'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Lütfen sorunu detaylıca açıklayın... (Örn: Şifre artık 1234 değil, 4567 olmuş veya bu tuvalet artık tamamen kapatılmış.)',
                'style': 'width: 100%; padding: 12px; border-radius: 8px; border: 2px solid #CED6E0; font-size: 16px; margin-top: 10px;'
            }),
        }