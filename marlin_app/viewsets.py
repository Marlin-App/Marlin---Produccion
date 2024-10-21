from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrderSerializer, StoreSerializer, UserSerializer, StoreItemSerializer, StoreTypeSerializer, StoreItemTagSerializer, UserProfileSerializer, AtributeValueSerializer, TinyStoreItemSerializer
from . models import Order, Store, StoreItem, StoreType, ItemTag, UserProfile, AtributeValue
from .permissions import IsAuthenticatedOrOwner
from django_filters.rest_framework import DjangoFilterBackend

class StoreViewSet(viewsets.ModelViewSet):
    # permission_classes =  [IsAuthenticatedOrOwner]
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store_type', 'user_id']

class StoreItemViewSet(viewsets.ModelViewSet):
    queryset = StoreItem.objects.all()
    serializer_class = StoreItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store_id']

class TinyStoreItemViewSet(viewsets.ModelViewSet):
    queryset = StoreItem.objects.all()[:10]
    serializer_class = StoreItemSerializer

class StoreTypeViewSet(viewsets.ModelViewSet):
    queryset = StoreType.objects.all()
    serializer_class = StoreTypeSerializer

class StoreItemTagViewSet(viewsets.ModelViewSet):
    queryset = ItemTag.objects.all()
    serializer_class = StoreItemTagSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filterset_fields = ['user__id']

class AttributeValueViewSet(viewsets.ModelViewSet):
    queryset = AtributeValue.objects.all()
    serializer_class = AtributeValueSerializer
    filterset_fields = ['storeItem']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


