from django.http.response import HttpResponse
from django.http import Http404,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mercado.forms import registerForm

# Create your views here.
from .models import Cliente, Marca, Mercancia, Oferta

def fam_member(type,dept):
    sizes = []
    if dept == 'CZ':
        if type == 'M':
            for i in range(23,31):
                sizes+=[f'{i} cm']
        elif type == 'W':
            for i in range (23,28):
                sizes+=[f'{i} cm W']
        elif type == 'GS':
            for i in range (21,25):
                sizes+=[f'{i} cm ']
        elif type == 'PS':
            for i in range (15,21):
                sizes+=[f'{i} cm ']
    elif dept == 'RP':
        sizes=['XS','S','M','L','XL','XXL']

    return sizes

def index(request):
    productos = Mercancia.objects.all()

    return render(request, 'mercado/index.html', {'productos':productos})

def register(request):
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            email = form.cleaned_data['email']
            passwd = form.cleaned_data['passwd']
            new_user = User.objects.create_user(usuario,email,passwd)
            new_user.save()

            return HttpResponseRedirect(reverse('mercado:index'))
    else:
        form = registerForm()

    return render(request, 'mercado/register.html',{'form':form})


def detalles(request,producto_id):
    producto = get_object_or_404(Mercancia, pk=producto_id)
    tallas = fam_member(producto.size_type,producto.depto)
    #ofertas = Oferta.objects.filter(articulo=producto_id)
    ofertas=[]
    for i in tallas:
        ofertas+=[Oferta.objects.filter(articulo=producto,talla=i).last()]
    ventas=zip(tallas,ofertas)
    return render(request,"mercado/detalles.html", {
        'producto':producto,
        'tallas':tallas,
        'ofertas':ofertas,
        'ventas':ventas,
        })

def compra(request, producto_id):
    producto = get_object_or_404(Mercancia, pk=producto_id)
    try:
        talla=request.POST['talla']
        #comprador
        monto=int(request.POST['monto'])
        total=monto+200
    except(KeyError,producto.DoesNotExist):

        return render(request, "mercado/compra.html",{
            'producto':producto,
            'error_message':"You didn´t select a Size"
            })
    else:

        return render(request,"mercado/compra.html", {
            'producto':producto,
            'total':total,
            'talla':talla,
            'monto':monto,
            })

def venta(request,producto_id):
    producto = get_object_or_404(Mercancia, pk=producto_id)

    return render(request,"mercado/venta.html", {'producto':producto})

@login_required
def comprado(request,producto_id,talla,total):
    p = Cliente.objects.get(pk=request.user.pk)
    producto = get_object_or_404(Mercancia, pk=producto_id)
    # talla = request.POST['talla']
    # total = request.POST['total']
    o=Oferta(monto=total, comprador=p,talla=talla,articulo=producto)
    o.save()
    
    return render(request,"mercado/comprado.html",{
        "producto":producto,
        "talla":talla,
        "total":total,
        })


