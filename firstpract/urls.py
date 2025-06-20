from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('firstpractooos.urls', namespace='firstpractooos')),
    path('accounts/', include([
        path('', include('django.contrib.auth.urls')),
        path('', include('users.urls')), 
    ])),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('api/', include('api_firstpract.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)