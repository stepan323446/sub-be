from django.urls import path
from .views import *

urlpatterns = [
    path('tax/labels/<int:pk>/', SingleLabelView.as_view(), name='tax-label'),
    path('tax/labels/', ListLabelView.as_view(), name='tax-label-list'),
    path('tax/labels/new/', CreateLabelView.as_view(), name='tax-label-new'),
]