from django.contrib import admin

# Register your models here.

from .models import Oferta, Mercancia, Marca, Cliente

admin.site.register(Oferta)
admin.site.register(Marca)
admin.site.register(Cliente)
admin.site.register(Mercancia)