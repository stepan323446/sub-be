from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from drf_spectacular.utils import extend_schema

from .models import Currency
from .serializers import CurrencySerializer
from .utils import update_currencies, get_cached_currencies

# Create your views here.
@extend_schema(tags=["Currency"], 
               description="Refresh currencies by external service ExchangeRate-api (only admin)",
               responses=CurrencySerializer(many=True))
class RefreshCurrencyView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request: Request, format=None):
        currencies = update_currencies()
        serializer = CurrencySerializer(currencies, many=True)

        return Response(serializer.data)

@extend_schema(tags=["Currency"], 
               description="List of all currencies with rate by USD",
               responses=CurrencySerializer(many=True))
class ListCurrencyView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request: Request, format=None):
        currencies = get_cached_currencies()
        serializer = CurrencySerializer(currencies, many=True)

        return Response(serializer.data)

@extend_schema(tags=["Currency"], 
               description="Retrieve, update or delete the label for subscriptions (only admin)")
class SingleCurrency(RetrieveUpdateDestroyAPIView):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    permission_classes = (permissions.IsAdminUser,)