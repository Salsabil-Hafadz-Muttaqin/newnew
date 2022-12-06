from django.contrib import admin
from .models import *

# Register your models here.
from django.contrib.auth.admin import UserAdmin

# class CustomUserAdmin(UserAdmin):
#     pass
class CustomUserAdmin(UserAdmin):
     list_display = ('username', 'role', 'address', 'phone')
     fieldsets = (
          (None, {"fields": ('username','password', 'role')}),
          ('Informasi Pribadi', {"fields": ('name','address', 'phone', 'telegram')}),
    )
    


admin.site.register(Account, CustomUserAdmin)

admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Category)
# admin.site.register(Account)
admin.site.register(Supplier)
admin.site.register(Bengkel)
admin.site.register(Stock)
admin.site.register(Order)
admin.site.register(OrderItem)
