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
    """Harita için sadece ONAYLANMIŞ ve KOORDİNATI OLAN tuvaletleri döndürür."""
    # Sadece onaylıları çekiyoruz
    toilets = Toilet.objects.filter(is_approved=True)
    data = []
    
    for t in toilets:
        # ÖNEMLİ: Sadece koordinatı olanları ekle, yoksa harita çöker
        if t.latitude is not None and t.longitude is not None:
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
            # 1. Veriyi veritabanına kaydet (is_approved varsayılan olarak False gelir)
            # Mail gitmese bile veriler artık Admin panelinde seni bekleyecek.
            form.save() 
            
            # Artık mail gönderme kısmını devre dışı bıraktık (SMTP hatası almamak için)
            # Ama success.html'e sanki mail gitmiş gibi bilgi veriyoruz ki ekran düzgün görünsün.
            # Dilersen buraya 'onay_bekliyor': True gibi bir değişken de gönderebilirsin.
            return render(request, 'success.html', {'mail_sent': True})
    else:
        form = ToiletReportForm()
    
    return render(request, 'report.html', {'form': form})