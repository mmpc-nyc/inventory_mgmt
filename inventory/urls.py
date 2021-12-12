from django.urls import path, include
from inventory.views.storage_views import StorageList, StorageDetail

urlpatterns = [
    path('storage/', include([
        path('', StorageList.as_view(), name='storage_list'),
        path('<int:pk>', StorageDetail.as_view(), name='storage_detail')
    ])),
]