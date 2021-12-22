from django.urls import path, include
from inventory.views import customer_views
from inventory.views import product_views
from inventory.views import job_views
from inventory.views import stock_views
from inventory.views.dashboard_views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('stock/', include([
        path('', stock_views.InventoryListView.as_view(), name='stock_list'),
        path('create', stock_views.InventoryCreateView.as_view(), name='stock_create'),
        path('<int:pk>', stock_views.InventoryDetailView.as_view(), name='stock_detail'),
        path('<int:pk>/delete', stock_views.InventoryDeleteView.as_view(), name='stock_delete'),
        path('<int:pk>/update', stock_views.InventoryUpdateView.as_view(), name='stock_update'),
    ])),
    path('products/', include([
        path('', product_views.ProductListView.as_view(), name='product_list'),
        path('create', product_views.ProductCreateView.as_view(), name='product_create'),
        path('<int:pk>', product_views.ProductDetailView.as_view(), name='product_detail'),
        path('<int:pk>/delete', product_views.ProductDeleteView.as_view(), name='product_delete'),
        path('<int:pk>/update', product_views.ProductUpdateView.as_view(), name='product_update'),
    ])),
    path('jobs/', include([
        path('', job_views.JobListView.as_view(), name='job_list'),
        path('create', job_views.JobCreateView.as_view(), name='job_create'),
        path('<int:pk>', job_views.JobDetailView.as_view(), name='job_detail'),
        path('<int:pk>/delete', job_views.JobDeleteView.as_view(), name='job_delete'),
        path('<int:pk>/update', job_views.JobUpdateView.as_view(), name='job_update'),
    ])),
    path('customers/', include([
        path('', customer_views.CustomerListView.as_view(), name='customer_list'),
        path('create', customer_views.CustomerCreateView.as_view(), name='customer_create'),
        path('<int:pk>', customer_views.CustomerDetailView.as_view(), name='customer_detail'),
        path('<int:pk>/delete', customer_views.CustomerDeleteView.as_view(), name='customer_delete'),
        path('<int:pk>/update', customer_views.CustomerUpdateView.as_view(), name='customer_update'),
    ])),
]
