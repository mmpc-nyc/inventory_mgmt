from django.urls import path, include
from inventory.views import customer_views, equipment_views, interchangeableproduct_views
from inventory.views import product_views
from inventory.views import warehouse_views
from inventory.views.dashboard_views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('warehouse/', include([
        path('', warehouse_views.WarehouseListView.as_view(), name='warehouse_list'),
        path('create', warehouse_views.WarehouseCreateView.as_view(), name='warehouse_create'),
        path('<int:pk>', warehouse_views.WarehouseDetailView.as_view(), name='warehouse_detail'),
        path('<int:pk>/delete', warehouse_views.WarehouseDeleteView.as_view(), name='warehouse_delete'),
        path('<int:pk>/update', warehouse_views.WarehouseUpdateView.as_view(), name='warehouse_update'),
    ])),
    path('products/', include([
        path('', product_views.ProductListView.as_view(), name='product_list'),
        path('create', product_views.ProductCreateView.as_view(), name='product_create'),
        path('<int:pk>', product_views.ProductDetailView.as_view(), name='product_detail'),
        path('<int:pk>/delete', product_views.ProductDeleteView.as_view(), name='product_delete'),
        path('<int:pk>/update', product_views.ProductUpdateView.as_view(), name='product_update'),
    ])),
    path('interchangeableproducts/', include([
        path('', interchangeableproduct_views.InterchangeableProductListView.as_view(), name='interchangeableproduct_list'),
        path('create', interchangeableproduct_views.InterchangeableProductCreateView.as_view(), name='interchangeableproduct_create'),
        path('<int:pk>', interchangeableproduct_views.InterchangeableProductDetailView.as_view(), name='interchangeableproduct_detail'),
        path('<int:pk>/delete', interchangeableproduct_views.InterchangeableProductDeleteView.as_view(), name='interchangeableproduct_delete'),
        path('<int:pk>/update', interchangeableproduct_views.InterchangeableProductUpdateView.as_view(), name='interchangeableproduct_update'),
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
