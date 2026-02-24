import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Toilet, ToiletReport # ToiletReport modelini import ettik
from .forms import ToiletReportForm, ToiletIssueForm # Yeni formumuzu import ettik

# Hataları loglamak için
logger = logging.getLogger(__name__)

def index(request):
    """Ana sayfa."""
    return render(request, 'index.html')

def toilet_data(request):
    """Harita için sadece ONAYLANMIŞ ve KOORDİNATI OLAN tuvaletleri JSON olarak döndürür."""
    toilets = Toilet.objects.filter(is_approved=True)
    data = []

    for t in toilets:
        if t.latitude is not None and t.longitude is not None:
            data.append({
                'id': t.id, # KRİTİK DÜZELTME: Haritadaki Hata Bildir butonu için ID şart!
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
        # Honeypot ve Spam Filtresi (Botları ve istenmeyen kelimeleri sessizce başarı sayfasına yolla)
        honeypot = request.POST.get('website_url')
        name_input = request.POST.get('name', '').upper()
        spam_keywords = ['CEYDA', 'AFFET', 'PİŞMANIM']

        if honeypot or any(word in name_input for word in spam_keywords):
            return render(request, 'success.html')

        form = ToiletReportForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')
    else:
        form = ToiletReportForm()

    return render(request, 'report.html', {'form': form})


# --- YENİ: MEVCUT TUVALET İÇİN HATA/ŞİKAYET BİLDİRME SİSTEMİ ---
def report_issue(request):
    """Haritadaki mevcut bir tuvalet için hata bildirme sayfası."""
    # URL'den gelen ?id=5 değerini alıyoruz
    toilet_id = request.GET.get('id')
    
    # Eğer adam URL ile oynayıp id girmezse veya harf girerse ana sayfaya şutla
    if not toilet_id or not toilet_id.isdigit():
        return redirect('index')

    # Veritabanında bu ID'ye sahip tuvalet var mı bak, yoksa 404 hatası ver
    target_toilet = get_object_or_404(Toilet, id=toilet_id)

    if request.method == 'POST':
        # Botlara karşı aynı Honeypot tuzağını buraya da koyabiliriz
        if request.POST.get('website_url'):
            return render(request, 'success.html', {'mail_sent': True})

        form = ToiletIssueForm(request.POST)
        
        if form.is_valid():
            # Formu kaydetmeden önce durduruyoruz (commit=False)
            # Çünkü bu şikayetin HANGİ tuvalete ait olduğunu form bilmiyor, biz ekleyeceğiz
            issue = form.save(commit=False)
            issue.toilet = target_toilet # URL'den bulduğumuz tuvaleti şikayete bağladık
            issue.save() # Şimdi güvenle veritabanına yazabiliriz
            
            return render(request, 'success.html', {'mail_sent': True})
    else:
        form = ToiletIssueForm()

    # Formu ve hangi tuvalet olduğunu HTML sayfasına gönderiyoruz
    return render(request, 'toilet_report.html', {
        'form': form,
        'toilet': target_toilet
    })