from rest_framework import routers
from api.viewsets import BrandViewSet, EquipmentViewSet, ProductViewSet, EmailViewSet, PhoneNumberViewSet, \
    ContactViewSet, CustomerViewSet, GenericProductViewSet, LocationViewSet, CategoryViewSet, OrderViewSet, \
    WarehouseViewSet, ProductTypeViewSet, UserViewSet

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
router.register(r'warehouse', WarehouseViewSet)
router.register(r'users', UserViewSet)