from django.urls import path, include
from inventory.views import customer_views, equipment_views, genericproduct_views
from inventory.views import product_views
from inventory.views import order_views
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
    path('genericproducts/', include([
        path('', genericproduct_views.GenericProductListView.as_view(), name='genericproduct_list'),
        path('create', genericproduct_views.GenericProductCreateView.as_view(), name='genericproduct_create'),
        path('<int:pk>', genericproduct_views.GenericProductDetailView.as_view(), name='genericproduct_detail'),
        path('<int:pk>/delete', genericproduct_views.GenericProductDeleteView.as_view(), name='genericproduct_delete'),
        path('<int:pk>/update', genericproduct_views.GenericProductUpdateView.as_view(), name='genericproduct_update'),
    ])),
    path('equipments/', include([
        path('', equipment_views.EquipmentListView.as_view(), name='equipment_list'),
        path('create', equipment_views.EquipmentCreateView.as_view(), name='equipment_create'),
        path('<int:pk>', equipment_views.EquipmentDetailView.as_view(), name='equipment_detail'),
        path('<int:pk>/delete', equipment_views.EquipmentDeleteView.as_view(), name='equipment_delete'),
        path('<int:pk>/update', equipment_views.EquipmentUpdateView.as_view(), name='equipment_update'),
    ])),
    path('orders/', include([
        path('', order_views.OrderListView.as_view(), name='order_list'),
        path('create', order_views.OrderCreateView.as_view(), name='order_create'),
        path('<int:pk>', order_views.OrderDetailView.as_view(), name='order_detail'),
        path('<int:pk>/delete', order_views.OrderDeleteView.as_view(), name='order_delete'),
        path('<int:pk>/update', order_views.OrderUpdateView.as_view(), name='order_update'),
    ])),
    path('customers/', include([
        path('', customer_views.CustomerListView.as_view(), name='customer_list'),
        path('create', customer_views.CustomerCreateView.as_view(), name='customer_create'),
        path('<int:pk>', customer_views.CustomerDetailView.as_view(), name='customer_detail'),
        path('<int:pk>/delete', customer_views.CustomerDeleteView.as_view(), name='customer_delete'),
        path('<int:pk>/update', customer_views.CustomerUpdateView.as_view(), name='customer_update'),
    ])),
]
