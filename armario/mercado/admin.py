from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.

from mercado.models import Oferta_compra, Mercancia, Marca, Cliente, Oferta_venta, Ofertas_compradas

admin.site.register(Oferta_compra)
admin.site.register(Oferta_venta)
admin.site.register(Marca)
# admin.site.register(Cliente)
admin.site.register(Mercancia)
admin.site.register(Ofertas_compradas)

class ClienteInLine(admin.StackedInline):
    model = Cliente
    can_delete = False
    verbose_name_plural = 'clientes'

class UserAdmin(BaseUserAdmin):
    inlines = (ClienteInLine,)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)