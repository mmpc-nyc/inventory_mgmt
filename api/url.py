from rest_framework import routers
from api.viewsets import BrandViewSet, EquipmentViewSet, MaterialViewSet, EmailViewSet, PhoneNumberViewSet, \
    ContactViewSet, CustomerViewSet, LocationViewSet, MaterialCategoryViewSet, \
    StockLocationViewSet, MaterialTypeViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'equipments', EquipmentViewSet)
router.register(r'materials', MaterialViewSet)
router.register(r'emails', EmailViewSet)
router.register(r'phone_numbers', PhoneNumberViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'categories', MaterialCategoryViewSet)
router.register(r'stock_location', StockLocationViewSet)
router.register(r'users', UserViewSet)