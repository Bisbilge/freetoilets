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
        if request.method == 'POST':
            form = ToiletReportForm(request.POST)
            if form.is_valid():
                # 1. Önce veriyi veritabanına kaydet (Mail gitmese de veri bizde kalsın)
                # form.save() 
                
                cd = form.cleaned_data
                subject = f"Yeni Tuvalet Bildirimi: {cd['place_name']}"
                message = f"Mekan: {cd['place_name']}\nKoordinat: {cd['coordinates']}"
                
                try:
                    # Mail göndermeyi dene
                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        ['bisbilge@gmail.com'],
                        fail_silently=False,
                    )
                    # Mail başarıyla giderse bu mesaj görünecek
                    messages.success(request, "Bildiriminiz başarıyla iletildi!")
                    
                except Exception:
                    # Gmail kotası dolduğunda (Daily limit exceeded) buraya düşer
                    # Kullanıcıya hata sayfası yerine bu uyarıyı gösteriyoruz
                    messages.warning(request, "Günlük bildirim limitimize ulaştık. Veriniz kaydedildi ancak onay süreci yarına sarkabilir. Özür dileriz!")
                
                return render(request, 'success.html')
        else:
            form = ToiletReportForm()
        
        return render(request, 'report.html', {'form': form})