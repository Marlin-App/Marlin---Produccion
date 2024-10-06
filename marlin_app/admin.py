from django.contrib import admin
from .models import UserType, StoreType, ItemTag, Store, UserProfile

# Register your models here.

admin.site.register(UserType)
admin.site.register(Store)
admin.site.register(StoreType)
admin.site.register(ItemTag)
admin.site.register(UserProfile)

