from django.contrib import admin
from .models import UserType, StoreType, ItemTag, Store, UserProfile, Atribute, Order

# Register your models here.

class StoreAdmin(admin.ModelAdmin):
    list_filter = ("status",)

admin.site.register(UserType)
admin.site.register(Store, StoreAdmin)
admin.site.register(StoreType)
admin.site.register(ItemTag)
admin.site.register(UserProfile)
admin.site.register(Atribute)
admin.site.register(Order)
