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
            cd = form.cleaned_data
            subject = f"Yeni Tuvalet Bildirimi: {cd['place_name']}"
            message = f"Mekan: {cd['place_name']}\nKoordinat: {cd['coordinates']}\nBilgi: {cd['description']}"
            
            mail_sent = False # Mail durumunu takip etmek için
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    ['bisbilge@gmail.com'],
                    fail_silently=False,
                )
                mail_sent = True
                messages.success(request, "Bildiriminiz başarıyla iletildi!")
            except Exception as e:
                logger.error(f"Gmail Kotası Hatası: {e}")
                # Hata durumunda success mesajı göndermiyoruz
                mail_sent = False
            
            # success.html'e mailin gidip gitmediği bilgisini gönderiyoruz
            return render(request, 'success.html', {'mail_sent': mail_sent})
    else:
        form = ToiletReportForm()
    
    return render(request, 'report.html', {'form': form})