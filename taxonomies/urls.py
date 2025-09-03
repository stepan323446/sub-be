from django.urls import path
from .views import *

urlpatterns = [
    # Labels
    path('tax/labels/<int:pk>/', SingleLabelView.as_view(), name='tax-label'),
    path('tax/labels/', ListLabelView.as_view(), name='tax-label-list'),
    path('tax/labels/new/', CreateLabelView.as_view(), name='tax-label-new'),

    # Payment types
    path('tax/payment-types/<int:pk>/', SinglePaymentMethodTypeView.as_view(), name='tax-paytype'),
    path('tax/admin/payment-types/<int:pk>/', SingleAdminPaymentMethodTypeView.as_view(), name='admin-tax-paytype'),
    path('tax/payment-types/', ListPaymentMethodTypeView.as_view(), name='tax-paytype-list'),
    path('tax/admin/payment-types/new/', CreatePaymentMethodTypeView.as_view(), name='tax-paytype-new'),

    # Payment types
    path('tax/payment-methods/<int:pk>/', SinglePaymentMethodView.as_view(), name='tax-pay'),
    path('tax/payment-methods/', ListPaymenMethodView.as_view(), name='tax-pay-list'),
    path('tax/payment-methods/new/', CreatePaymentMethodView.as_view(), name='tax-pay-new'),
]