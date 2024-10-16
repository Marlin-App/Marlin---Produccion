from django.contrib import admin
from .models import UserType, StoreType, ItemTag, Store, UserProfile, Atribute

# Register your models here.

class StoreAdmin(admin.ModelAdmin):
    list_filter = ("store_type",)

admin.site.register(UserType)
admin.site.register(Store, StoreAdmin)
admin.site.register(StoreType)
admin.site.register(ItemTag)
admin.site.register(UserProfile)
admin.site.register(Atribute)

