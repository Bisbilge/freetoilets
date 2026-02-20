from django.shortcuts import render
from django.http import JsonResponse
from .models import Toilet

def index(request):
    # 'toilets/index.html' yerine sadece 'index.html' yazıyoruz
    # Çünkü settings içindeki DIRS bizi zaten klasörün içine soktu.
    return render(request, 'index.html')

def toilet_data(request):
    # Veritabanındaki tüm tuvaletleri çekiyoruz
    toilets = Toilet.objects.all()
    data = []
    
    for t in toilets:
        data.append({
            'name': t.name,
            'lat': float(t.latitude),
            'lng': float(t.longitude),
            'is_free': t.is_free,
            # Decimal değerleri JSON'a basarken string'e çevirmek hata almanı önler
            'price': str(t.price) if t.price else "0",
            'code': t.code if t.code else "Gerekmiyor",
            'desc': t.description
        })
    
    # safe=False diyoruz çünkü bir liste döndürüyoruz, dict değil.
    return JsonResponse(data, safe=False)