from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Toilet
from .forms import ToiletReportForm # forms.py'den formu çekiyoruz

def index(request):
    return render(request, 'index.html')

def toilet_data(request):
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
    Kullanıcıdan gelen tuvalet bildirimlerini 
    form aracılığıyla alıp mail gönderen view.
    """
    if request.method == 'POST':
        form = ToiletReportForm(request.POST)
        if form.is_valid():
            # Temizlenmiş verileri al
            cd = form.cleaned_data
            
            # Mail içeriğini oluştur
            subject = f"Yeni Tuvalet Bildirimi: {cd['place_name']}"
            message = f"""
            Yeni bir tuvalet bildirimi geldi:
            
            Mekan Adı: {cd['place_name']}
            Konum/Koordinat: {cd['coordinates']}
            Ücretsiz mi: {'Evet' if cd['is_free'] else 'Hayır'}
            Ek Bilgiler: {cd['description']}
            
            Gönderim Tarihi: {settings.TIME_ZONE}
            """
            
            # Maili gönder
            # settings içindeki EMAIL_HOST_USER gönderici olarak kullanılır
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['bisbilge@gmail.com'], # Senin asıl mail adresin
                fail_silently=False,
            )
            
            # Mail sonrası kullanıcıyı bir başarı sayfasına yönlendir
            return render(request, 'success.html')
    else:
        form = ToiletReportForm()
    
    return render(request, 'report.html', {'form': form})
    
    def report_toilet(request):
    if request.method == 'POST':
        # 1. Önce veriyi veritabanına kaydet (Mail gitmese de veri kaybolmasın)
        # form.save() veya model_instance.save()
        
        try:
            # Mail göndermeyi dene
            send_mail(
                'Yeni Tuvalet Bildirimi',
                'İçerik...',
                'senin-mailin@gmail.com',
                ['hedef-mail@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, "Bildiriminiz başarıyla iletildi!")
            
        except Exception:
            # Gmail kotası dolduğunda buraya düşecek
            # Kullanıcıya hata sayfası göstermek yerine uyarı mesajı ekle
            messages.warning(request, "Günlük bildirim limitimize ulaştık. Veriniz kaydedildi ancak onay süreci biraz uzayabilir. Yarın tekrar görüşmek üzere, özür dileriz!")
        
        return render(request, 'toilets/report_success.html') # Veya ana sayfa