from django.urls import path, include
from inventory.views import customer_views
from inventory.views import inventoryitem_views
from inventory.views import job_views
from inventory.views import inventory_views
from inventory.views.dashboard_views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('inventory/', include([
        path('', inventory_views.InventoryListView.as_view(), name='inventory_list'),
        path('create', inventory_views.InventoryCreateView.as_view(), name='inventory_create'),
        path('<int:pk>', inventory_views.InventoryDetailView.as_view(), name='inventory_detail'),
        path('<int:pk>/delete', inventory_views.InventoryDeleteView.as_view(), name='inventory_delete'),
        path('<int:pk>/update', inventory_views.InventoryUpdateView.as_view(), name='inventory_update'),
    ])),
    path('inventoryitems/', include([
        path('', inventoryitem_views.InventoryItemListView.as_view(), name='inventoryitem_list'),
        path('create', inventoryitem_views.InventoryItemCreateView.as_view(), name='inventoryitem_create'),
        path('<int:pk>', inventoryitem_views.InventoryItemDetailView.as_view(), name='inventoryitem_detail'),
        path('<int:pk>/delete', inventoryitem_views.InventoryItemDeleteView.as_view(), name='inventoryitem_delete'),
        path('<int:pk>/update', inventoryitem_views.InventoryItemUpdateView.as_view(), name='inventoryitem_update'),
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
