import logging
from django.shortcuts import render
from django.http import JsonResponse
from .models import Toilet
from .forms import ToiletReportForm

# Hataları loglamak için
logger = logging.getLogger(__name__)

def index(request):
    """Ana sayfa."""
    return render(request, 'index.html')

def toilet_data(request):
    """Harita için sadece ONAYLANMIŞ ve KOORDİNATI OLAN tuvaletleri JSON olarak döndürür."""
    # Sadece admin onayı almış kayıtları çekiyoruz
    toilets = Toilet.objects.filter(is_approved=True)
    data = []

    for t in toilets:
        # Koordinatı olmayan (henüz admin tarafından işlenmemiş) verileri haritaya gönderme
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
    """Bot korumalı (Honeypot + Filtre) bildirim formu."""
    if request.method == 'POST':
        # --- 1. SAVUNMA HATTI: HONEYPOT (BAL KÜPÜ) ---
        # Eğer gizli 'website_url' alanı doluysa bu bir bottur.
        if request.POST.get('website_url'):
            # Botu engelle ama başarı sayfasına gönder ki bot pes etmesin
            return render(request, 'success.html', {'mail_sent': True})

        form = ToiletReportForm(request.POST)
        
        if form.is_valid():
            # --- 2. SAVUNMA HATTI: SPAM KELİME FİLTRESİ ---
            name = form.cleaned_data.get('name', '').upper()
            spam_keywords = ['CEYDA', 'AFFET', 'PİŞMANIM']
            
            if any(word in name for word in spam_keywords):
                # Spam ise kaydetmeden başarı sayfasına yönlendir
                return render(request, 'success.html', {'mail_sent': True})

            # Eğer her şey temizse veritabanına onaysız (False) olarak kaydet
            form.save() 
            return render(request, 'success.html', {'mail_sent': True})
    else:
        form = ToiletReportForm()

    return render(request, 'report.html', {'form': form})
