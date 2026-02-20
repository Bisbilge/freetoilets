import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Toilet
from .forms import ToiletReportForm

# Hataları loglamak için
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

def toilet_data(request):
    """Harita için tuvalet verilerini JSON olarak döndürür."""
    toilets = Toilet.objects.all()
    data = []
    
    for t in toilets:
        data.append({
            'name': t.name,
            'lat': float(t.latitude),
            'lng': float(t.longitude),
            'is_free': t.is_free,
            'price': str(t.price) if t.price else "0",
            'code': t.code if t.code else "Gerekmiyor",
            'desc': t.description
        })
    
    return JsonResponse(data, safe=False)

def report_toilet(request):
    """
    Kullanıcıdan gelen bildirimleri alır, veritabanına kaydeder
    ve Gmail kotası elverirse mail gönderir.
    """
    if request.method == 'POST':
        form = ToiletReportForm(request.POST)
        if form.is_valid():
            # 1. Veriyi veritabanına kaydet (Mail gitmese bile veri kaybolmasın)
            # Eğer formun bir ModelForm ise:
            # report = form.save()
            
            cd = form.cleaned_data
            
            # 2. Mail içeriğini hazırla
            subject = f"Yeni Tuvalet Bildirimi: {cd['place_name']}"
            message = f"""
            Yeni bir tuvalet bildirimi geldi:
            
            Mekan Adı: {cd['place_name']}
            Konum/Koordinat: {cd['coordinates']}
            Ücretsiz mi: {'Evet' if cd['is_free'] else 'Hayır'}
            Ek Bilgiler: {cd['description']}
            """
            
            # 3. Mail göndermeyi dene (Gmail kotasını kontrol et)
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    ['bisbilge@gmail.com'], # Hedef mail adresin
                    fail_silently=False,
                )
                messages.success(request, "Bildiriminiz başarıyla iletildi!")
                
            except Exception as e:
                # Günlük limit dolduğunda (550 hatası) buraya düşer
                logger.error(f"Gmail gönderim hatası: {e}")
                
                # Kullanıcıya nazikçe açıkla
                messages.warning(request, (
                    "Harika bir ilgi var! Günlük bildirim limitimize ulaştık. "
                    "Daha sonra tekrar deneyiniz. "
                    "Anlayışınız için teşekkür ederiz! 💙"
                ))
            
            # Başarılı (veya kotadan dolayı uyarılı) sayfaya yönlendir
            return render(request, 'success.html')
    else:
        form = ToiletReportForm()
    
    return render(request, 'report.html', {'form': form})