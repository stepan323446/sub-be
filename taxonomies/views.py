from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from .serializers import *
from project.mixins import IsAuthorOrAdminSingleMixin

# Label model
@extend_schema(tags=["Taxonomies"], 
               description="Retrieve, update or delete the label for subscriptions (admin or author)")
class SingleLabelView(IsAuthorOrAdminSingleMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = LabelSerializer
    queryset = Label.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

@extend_schema(tags=["Taxonomies"], 
               description="Retrieve a paginated list of labels.")
class ListLabelView(ListAPIView):
    serializer_class = LabelSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    search_fields = ['name']
    filter_backends = [SearchFilter]

    def get_queryset(self):
        return Label.objects.filter(user=self.request.user)
    

@extend_schema(tags=["Taxonomies"], 
               description="Create new label by user")
class CreateLabelView(CreateAPIView):
    serializer_class = LabelSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Payment Method Type model
@extend_schema(tags=["Taxonomies"], 
               description="Retrieve the payment type for subscriptions")
class SinglePaymentMethodTypeView(RetrieveAPIView):
    serializer_class = PaymentMethodTypeSerializer
    queryset = PaymentMethodType.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

@extend_schema(tags=["Taxonomies"], 
               description="Retrieve, update or delete the payment type for subscriptions (only admin)")
class SingleAdminPaymentMethodTypeView(RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentMethodTypeSerializer
    queryset = PaymentMethodType.objects.all()
    permission_classes = (permissions.IsAdminUser, )

@extend_schema(tags=["Taxonomies"], 
               description="Retrieve a paginated list of payment types.")
class ListPaymentMethodTypeView(ListAPIView):
    serializer_class = PaymentMethodTypeSerializer
    queryset = PaymentMethodType.objects.all()
    search_fields = ['type']
    filter_backends = [SearchFilter]
    permission_classes = (permissions.IsAuthenticated,)

@extend_schema(tags=["Taxonomies"], 
               description="Create new payment type (only admin)")
class CreatePaymentMethodTypeView(CreateAPIView):
    serializer_class = PaymentMethodTypeSerializer
    permission_classes = (permissions.IsAdminUser,)


# Payment Method for subscriptions
@extend_schema(tags=["Taxonomies"], 
               description="Retrieve, update or delete the payment method for subscriptions (admin or author)")
class SinglePaymentMethodView(IsAuthorOrAdminSingleMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

@extend_schema(tags=["Taxonomies"], 
               description="Retrieve a paginated list of payment methods.")
class ListPaymenMethodView(ListAPIView):
    serializer_class = PaymentMethodSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    search_fields = ['name', 'type__type']
    filter_backends = [SearchFilter]

    def get_queryset(self):
        return PaymentMethod.objects.filter(user=self.request.user)
    
@extend_schema(tags=["Taxonomies"], 
            description="Create new label by user")
class CreatePaymentMethodView(CreateAPIView):
    serializer_class = PaymentMethodSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)