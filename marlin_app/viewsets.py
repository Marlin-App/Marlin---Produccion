from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StoreSerializer, UserSerializer, StoreItemSerializer, StoreTypeSerializer, StoreItemTagSerializer, UserProfileSerializer
from . models import Store, StoreItem, StoreType, ItemTag, UserProfile
from .permissions import IsAuthenticatedOrOwner
from django_filters.rest_framework import DjangoFilterBackend

class StoreViewSet(viewsets.ModelViewSet):
    # permission_classes =  [IsAuthenticatedOrOwner]
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store_type']

class StoreItemViewSet(viewsets.ModelViewSet):
    # permission_classes =  [IsAuthenticatedOrOwner]
    queryset = StoreItem.objects.all()
    serializer_class = StoreItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store_id']

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
