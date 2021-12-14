from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from inventory_mgmt import settings

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('accounts/', include('allauth.urls'), name='socialaccount_signup'),
    path('admin/', admin.site.urls),
    path('main/', include(('main.urls', 'main'), namespace='main')),
    path('', include(('inventory.urls', 'inventory'), namespace='inventory')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)