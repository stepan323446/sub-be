from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .serializers import *
from project.mixins import IsAuthorOrAdminSingleMixin

# Create your views here.
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