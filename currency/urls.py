from django.urls import path
from .views import *

urlpatterns = [
    path('currencies/', ListCurrencyView.as_view(), name='currency-list'),
    path('admin/currencies/refresh', RefreshCurrencyView.as_view(), name='currency-refresh'),
    path('admin/currencies/<int:pk>/', SingleCurrency.as_view(), name='currency'),
]