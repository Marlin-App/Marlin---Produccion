from django.urls import path, include
from rest_framework import routers
from . import viewsets
from .views import RegisterUserAPIView

# Url para las apis
router = routers.DefaultRouter()
router.register(r'stores', viewsets.StoreViewSet)
router.register(r'storeItems',viewsets.StoreItemViewSet)
router.register(r'storeTypes',viewsets.StoreTypeViewSet)
router.register(r'itemTags',viewsets.StoreItemTagViewSet)
router.register(r'userProfile', viewsets.UserProfileViewSet)
router.register(r'attributes', viewsets.AttributeValueViewSet)
router.register(r'store-items', viewsets.ItemViewSet, basename='item')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterUserAPIView.as_view(), name='register'),
]