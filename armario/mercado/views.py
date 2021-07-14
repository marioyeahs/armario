from django.http.response import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Cliente, Marca, Mercancia, Oferta


def index(request):
    productos = Mercancia.objects.all()
    return render(request, 'mercado/index.html', {'productos':productos})

def detalles(request,producto_id):
    producto = get_object_or_404(Mercancia, pk=producto_id)
    return render(request,"mercado/detail.html", {'producto':producto})


def compra(request, producto_id):
    return HttpResponse('Comprar producto: %s' % producto_id)

def venta(request,producto_id):
    producto = get_object_or_404(Mercancia, pk=producto_id)
    return render(request,"mercado/venta.html", {'producto':producto})

