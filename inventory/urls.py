from django.views.generic import RedirectView
from django.urls import path, include

urlpatterns = [
    path('', RedirectView.as_view(url='customers'), name='home'),
]