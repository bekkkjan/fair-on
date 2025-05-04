# corruptino/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin paneli uchun yo'l
    path('accounts/', include('accounts.urls')),  # Foydalanuvchi boshqaruvi uchun yo'l
    path('jobs/', include('jobs.urls')),  # Vakansiyalar uchun yo'l
    path('', include('core.urls')),  # Asosiy sahifalar uchun yo'l
]

# Media fayllar uchun URL yo'llari (faqat DEBUG rejimida)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)