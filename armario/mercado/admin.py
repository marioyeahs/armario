from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.

from mercado.models import BuyOffer, Product, Brand, Client, SellOffer, SuccessfulOffer
admin.site.register(BuyOffer)
admin.site.register(SellOffer)
admin.site.register(Brand)
# admin.site.register(Cliente)
admin.site.register(Product)
admin.site.register(SuccessfulOffer)

class ClienteInLine(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = 'clientes'

class UserAdmin(BaseUserAdmin):
    inlines = (ClienteInLine,)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)