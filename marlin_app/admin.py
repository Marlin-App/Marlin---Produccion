from django.contrib import admin
from .models import UserType, StoreType, ItemTag, Store

# Register your models here.

admin.site.register(UserType)
admin.site.register(Store)
admin.site.register(StoreType)
admin.site.register(ItemTag)

