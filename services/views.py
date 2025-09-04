from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema

from .models import Service
from .serializers import *
from project.mixins import IsAuthorOrAdminSingleMixin

# Create your views here.
# Label model
@extend_schema(tags=["Services"], 
               description="Retrieve, update or delete the service for subscriptions (admin or author)")
class SingleServiceView(IsAuthorOrAdminSingleMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

@extend_schema(tags=["Services"], 
               description="Retrieve a paginated list of services.")
class ListServiceView(ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    search_fields = ['name']
    filter_backends = [SearchFilter]

    def get_queryset(self):
        return Service.objects.filter(user=self.request.user)
    

@extend_schema(tags=["Services"], 
               description="Create new service by user")
class CreateServiceView(CreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)