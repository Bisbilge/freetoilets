from django import forms

class ToiletReportForm(forms.Form):
    place_name = forms.CharField(label='Mekan Adı', max_length=100)
    coordinates = forms.CharField(label='Koordinatlar (veya Konum Linki)', max_length=200)
    is_free = forms.BooleanField(label='Ücretsiz mi?', required=False)
    description = forms.CharField(label='Ek Notlar (Şifre vb.)', widget=forms.Textarea)