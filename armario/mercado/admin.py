from django.contrib import admin

# Register your models here.

from .models import Oferta_compra, Mercancia, Marca, Cliente

admin.site.register(Oferta_compra)
admin.site.register(Marca)
admin.site.register(Cliente)
admin.site.register(Mercancia)