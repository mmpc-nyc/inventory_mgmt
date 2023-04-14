from django.urls import path, include
from inventory.views import customer_views, equipment_views
from inventory.views import material_views
from inventory.views import storage_location_views
from inventory.views.dashboard_views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('stock_location/', include([
        path('', storage_location_views.StorageLocationListView.as_view(), name='stock_location_list'),
        path('create', storage_location_views.StorageLocationCreateView.as_view(), name='stock_location_create'),
        path('<int:pk>', storage_location_views.StorageLocationDetailView.as_view(), name='stock_location_detail'),
        path('<int:pk>/delete', storage_location_views.StorageLocationDeleteView.as_view(), name='stock_location_delete'),
        path('<int:pk>/update', storage_location_views.StorageLocationUpdateView.as_view(), name='stock_location_update'),
    ])),
    path('materials/', include([
        path('', material_views.MaterialListView.as_view(), name='material_list'),
        path('create', material_views.MaterialCreateView.as_view(), name='material_create'),
        path('<int:pk>', material_views.MaterialDetailView.as_view(), name='material_detail'),
        path('<int:pk>/delete', material_views.MaterialDeleteView.as_view(), name='material_delete'),
        path('<int:pk>/update', material_views.MaterialUpdateView.as_view(), name='material_update'),
    ])),
    path('equipments/', include([
        path('', equipment_views.EquipmentListView.as_view(), name='equipment_list'),
        path('create', equipment_views.EquipmentCreateView.as_view(), name='equipment_create'),
        path('<int:pk>', equipment_views.EquipmentDetailView.as_view(), name='equipment_detail'),
        path('<int:pk>/delete', equipment_views.EquipmentDeleteView.as_view(), name='equipment_delete'),
        path('<int:pk>/update', equipment_views.EquipmentUpdateView.as_view(), name='equipment_update'),
    ])),
    path('customers/', include([
        path('', customer_views.CustomerListView.as_view(), name='customer_list'),
        path('create', customer_views.CustomerCreateView.as_view(), name='customer_create'),
        path('<int:pk>', customer_views.CustomerDetailView.as_view(), name='customer_detail'),
        path('<int:pk>/delete', customer_views.CustomerDeleteView.as_view(), name='customer_delete'),
        path('<int:pk>/update', customer_views.CustomerUpdateView.as_view(), name='customer_update'),
    ])),
]
