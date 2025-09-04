from django.urls import path
from .views import *

urlpatterns = [
    # Labels
    path('services/<int:pk>/', SingleServiceView.as_view(), name='service'),
    path('services/', ListServiceView.as_view(), name='service-list'),
    path('services/new/', CreateServiceView.as_view(), name='service-new'),
]