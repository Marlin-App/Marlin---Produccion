from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DeliveryOrderSerializer, DeliveryProfileSerializer, OrderSerializer, StoreSerializer, UserSerializer, StoreItemSerializer, StoreTypeSerializer, StoreItemTagSerializer, UserProfileSerializer, AtributeValueSerializer, StoreWithItemsSerializer
from . models import DeliveryOrder, DeliveryProfile, Order, Store, StoreItem, StoreType, ItemTag, UserProfile, AtributeValue
from .permissions import IsAuthenticatedOrOwner
from django_filters.rest_framework import DjangoFilterBackend

class StoreViewSet(viewsets.ModelViewSet):
    # permission_classes =  [IsAuthenticatedOrOwner]
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store_type', 'user_id']

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

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store_id', 'user_id']

class StoreWithItemsViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreWithItemsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store_type', 'user_id']

class DeliveryProfileViewSet(viewsets.ModelViewSet):
    queryset = DeliveryProfile.objects.all()
    serializer_class = DeliveryProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id']

class DeliveryOrderViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveryOrderSerializer  # Asegúrate de tener un serializer asignado
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'deliveryprofile'):
            return DeliveryOrder.objects.filter(status='Pendiente', delivery_id=user.deliveryprofile.id)
        else:
            return DeliveryOrder.objects.none()
        
