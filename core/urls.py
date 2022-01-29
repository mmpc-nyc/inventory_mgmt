from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from api.url import router
from core import settings
from users.views import LoginView, LogoutView

urlpatterns = [
    path('', include(('inventory.urls', 'inventory'), namespace='inventory')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/', include(router.urls)),
    path('main/', include(('main.urls', 'main'), namespace='main')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'), ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)