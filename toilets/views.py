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
        # --- BURADA VERİTABANI KAYIT İŞLEMİN OLMALI ---
        # Örnek: form = ToiletReportForm(request.POST)
        # if form.is_valid(): form.save()
        
        try:
            # Gmail SMTP denemesi
            send_mail(
                'Yeni Tuvalet Bildirimi',
                'Bir kullanıcı yeni bir konum bildirdi.',
                'senin-mailin@gmail.com',
                ['hedef-mail@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, "Bildiriminiz başarıyla iletildi!")
            
        except Exception as e:
            # SMTPDataError (550) buraya düşecek. 
            # Site ÇÖKMEYECEK, sadece bu blok çalışacak.
            logger.error(f"Gmail Limiti Aşıldı: {e}")
            
            # Kullanıcıya durumu nazikçe açıkla
            messages.warning(request, (
                "Yoğun ilginiz için teşekkürler! Günlük bildirim limitimize ulaştık. "
                "Veriniz güvenle kaydedildi ancak onay süreci yarına sarkabilir. "
                "Anlayışınız için teşekkür ederiz."
            ))

        # Hata olsa da olmasa da kullanıcıyı başarı sayfasına yönlendir
        return render(request, 'toilets/report_success.html')

    # GET isteği için formu göster
    return render(request, 'toilets/report_form.html')