from django.urls import path, include
from inventory.views.storage_views import StorageList

urlpatterns = [
    path('storage', include([
        path('', StorageList.as_view(), name='storage_list'),
    ])),
]