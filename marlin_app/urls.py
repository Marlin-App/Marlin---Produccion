from django.urls import path, include
from rest_framework import routers
from . import viewsets
from .views import RegisterUserAPIView, PasswordResetRequestView, PasswordResetView, redirect_view, DeleteAccount, AcceptOrder, AcceptDeliveryOrder

# Url para las apis
router = routers.DefaultRouter()
router.register(r'stores', viewsets.StoreViewSet)
router.register(r'storeItems',viewsets.StoreItemViewSet)
router.register(r'storeTypes',viewsets.StoreTypeViewSet)
router.register(r'itemTags',viewsets.StoreItemTagViewSet)
router.register(r'userProfile', viewsets.UserProfileViewSet)
router.register(r'orders', viewsets.OrderViewSet)
router.register(r'storesWithItems', viewsets.StoreWithItemsViewSet, basename='fullstore')
router.register(r'delivery-profiles', viewsets.DeliveryProfileViewSet)
router.register(r'delivery-orders', viewsets.DeliveryOrderViewSet, basename='delivery_orders')


urlpatterns = [
    path('', include(router.urls)),
    path('redirect/<uidb64>/<token>/', redirect_view),
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('reset-password/<uidb64>/<token>/', PasswordResetView.as_view(), name='password_reset_confirm'),
    path('delete-account/', DeleteAccount.as_view(), name='delete_account'),
    path('accept-order/', AcceptOrder.as_view(), name='accept_order'),
    path('accept-delivery/', AcceptDeliveryOrder.as_view(), name='accept_delivery'),
]