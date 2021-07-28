from django.contrib import admin

# Register your models here.

from .models import Oferta_compra, Mercancia, Marca, Cliente, Oferta_venta

admin.site.register(Oferta_compra)
admin.site.register(Oferta_venta)
admin.site.register(Marca)
admin.site.register(Cliente)
admin.site.register(Mercancia)