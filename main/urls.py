from django.urls import path

from main.views import success

urlpatterns = [
    path('success', success, name='success'),
]