from django.urls import path, include
from inventory.views import customer_views
from inventory.views import item_views
from inventory.views import job_views
from inventory.views import storage_views
from inventory.views.dashboard_views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('storage/', include([
        path('', storage_views.StorageListView.as_view(), name='storage_list'),
        path('create', storage_views.StorageCreateView.as_view(), name='storage_create'),
        path('<int:pk>', storage_views.StorageDetailView.as_view(), name='storage_detail'),
        path('<int:pk>/delete', storage_views.StorageDeleteView.as_view(), name='storage_delete'),
        path('<int:pk>/update', storage_views.StorageUpdateView.as_view(), name='storage_update'),
    ])),
    path('items/', include([
        path('', item_views.ItemListView.as_view(), name='item_list'),
        path('create', item_views.ItemCreateView.as_view(), name='item_create'),
        path('<int:pk>', item_views.ItemDetailView.as_view(), name='item_detail'),
        path('<int:pk>/delete', item_views.ItemDeleteView.as_view(), name='item_delete'),
        path('<int:pk>/update', item_views.ItemUpdateView.as_view(), name='item_update'),
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
