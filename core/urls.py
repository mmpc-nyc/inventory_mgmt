from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.viewsets import BrandViewSet, EquipmentViewSet, ProductViewSet, EmailViewSet, PhoneNumberViewSet, \
    ContactViewSet, CustomerViewSet, GenericProductViewSet, LocationViewSet, CategoryViewSet, OrderViewSet, \
    StockViewSet, ProductTypeViewSet, UserViewSet
from core import settings
from users.views import LoginView, LogoutView

router = routers.DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'equipments', EquipmentViewSet)
router.register(r'products', ProductViewSet)
router.register(r'emails', EmailViewSet)
router.register(r'phone_numbers', PhoneNumberViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'generic_products', GenericProductViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'stock', StockViewSet)
router.register(r'product_types', ProductTypeViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
               path('api/', include(router.urls)),
               path('accounts/', include('allauth.urls'), name='socialaccount_signup'), path('admin/', admin.site.urls),
               path('main/', include(('main.urls', 'main'), namespace='main')),
               path('', include(('inventory.urls', 'inventory'), namespace='inventory')),
               path('users/', include(('users.urls', 'users'), namespace='users')),
               path('login/', LoginView.as_view(), name='login'),
               path('logout/', LogoutView.as_view(), name='logout'), ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
