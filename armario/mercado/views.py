from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.core.mail import send_mail, send_mass_mail
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotModified, HttpResponsePermanentRedirect
from django.http import Http404,HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mercado.forms import RegisterForm
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from datetime import datetime 
from django.utils.decorators import method_decorator

# Create your views here.
from .models import Cliente, Marca, Mercancia, Oferta_compra, Oferta_venta, Ofertas_compradas

def fam_member(type,dept):
    sizes = []
    if dept == 'CZ':
        if type == 'M':
            for i in range(23,31):
                sizes+=[f'{i} cm']
        elif type == 'W':
            for i in range (23,28):
                sizes+=[f'{i} cm']
        elif type == 'GS':
            for i in range (21,25):
                sizes+=[f'{i} cm']
        elif type == 'PS':
            for i in range (15,21):
                sizes+=[f'{i} cm']
    elif dept == 'RP':
        sizes=['XS','S','M','L','XL','XXL']

    return sizes

def add_checkout(request):
    print(request.session['monto'])
    request.session['comision'] = round(.07*request.session['monto'],2)
    request.session['total']=request.session['monto']+200+request.session['comision']  

def discount_comission(request):
    print(request.session['monto'])
    request.session['comision']=round(.07*request.session['monto'],2)
    request.session['total']=request.session['monto']-200-request.session['comision']

class IndexListView(ListView):
    model = Mercancia
    template_name = "mercado/index.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(IndexListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['marcas'] = Marca.objects.all().values_list('nombre',flat=True)
        context['deptos'] = Mercancia.DEPTO

        return context

class RegisterFormView(SuccessMessageMixin, FormView):
    template_name = 'mercado/register.html'
    form_class = RegisterForm
    initial = {'key':'value'}
    success_message = "%(email)s was created successfully"

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class(initial=self.initial)
    #     return render(request,self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            email = form.cleaned_data['email']
            passwd = form.cleaned_data['passwd']
            confirm_passwd = form.cleaned_data['confirm_passwd']
            if passwd != confirm_passwd:
                messages.error(request, "por favor verifica las contraseñas")

                return HttpResponseRedirect(reverse('mercado:register'))

            phone = form.cleaned_data['phone']
            new_user = User.objects.create_user(usuario,email,passwd)
            new_user.save()
            new_client = Cliente(user=new_user,numero=phone)
            new_client.save()
            form.send_email()
            messages.success(request, 'Usuario registrado correctamente, se ha enviado un correo de verificación a %s' %email)

            return HttpResponseRedirect(reverse('mercado:register'))
    
        return render(request,self.template_name, {'form':form})

def detalles(request,pk):
    producto = get_object_or_404(Mercancia, pk=pk)
    tallas = fam_member(producto.size_type,producto.depto)
    ofertas_compra=[]
    ofertas_venta=[]

    for talla in tallas:
        ofertas_compra+=[Oferta_compra.objects.filter(articulo=producto,talla=talla).values_list('monto',flat=True).order_by('monto').last()]

    for talla in tallas:
        ofertas_venta+=[Oferta_venta.objects.filter(articulo=producto,talla=talla).values_list('monto',flat=True).order_by('monto').first()]
    
    compras=zip(tallas,ofertas_venta,ofertas_compra)
    ventas=zip(tallas,ofertas_compra, ofertas_venta)
    
    for i in Mercancia.DEPTO:
        if producto.depto in i:
            depto=i

    return render(request,"mercado/detalles.html", {
        'producto':producto,
        'tallas':tallas,
        'ventas':ventas,
        'compras':compras,
        'depto': depto
        })  

def compra(request, producto_id):
    producto = get_object_or_404(Mercancia, pk=producto_id)

    try:
        request.session['talla']=request.POST['talla']

        if request.POST['monto']:
            request.session['monto']=request.session['comprar_ahora']=int(request.POST['monto'])
            print('**********Oferta compra************')
            add_checkout(request)
        else:
            request.session['monto']=request.session['comprar_ahora']=int(request.POST['comprar_ahora'])
            print('-----------Comprar ahora----------------')
            add_checkout(request)

            return HttpResponseRedirect(reverse('mercado:oferta_compra',args=(producto.id,)))

    except(KeyError,producto.DoesNotExist):

        return render(request, "mercado/compra.html",{
            'producto':producto,
            'error_message':"You didn´t select a Size"
            })

    else:

        return HttpResponseRedirect(reverse('mercado:compra',args=(producto.id,)))

def venta(request,producto_id):
    producto = get_object_or_404(Mercancia, pk=producto_id)
    try:
        request.session['talla']=request.POST['talla']
        if request.POST['monto']:
            request.session['monto']=request.session['vender_ahora']=int(request.POST['monto'])
            print('**********Oferta venta************')
            discount_comission(request)
        else:
            request.session['monto']=request.session['vender_ahora']=int(request.POST['vender_ahora'])
            print('-----------Vender ahora----------------')
            discount_comission(request)

            return HttpResponseRedirect(reverse('mercado:oferta_venta',args=(producto.id,)))

    except(KeyError,producto.DoesNotExist):

        return render(request, "mercado/venta.html",{
            'producto':producto,
            'error_message':"You didn´t select a Size"
            })
    else:

        return HttpResponseRedirect(reverse('mercado:venta',args=(producto.id,)))

def oferta_compra(request,producto_id):
    producto = Mercancia.objects.get(id=producto_id)
    comision = request.session['comision']
    return render(request,"mercado/oferta_compra.html",{
        "producto":producto,
        "comision": round(comision,2)
        })

def oferta_venta(request,producto_id):
    producto = Mercancia.objects.get(id=producto_id)
    comision = request.session['comision']
    return render(request,"mercado/oferta_venta.html",{
        "producto":producto,
        "comision": round(comision,2)
        })

@login_required
def oferta_comprada(request,producto_id):
    """
        Cuando se acepta una oferta de venta, se crea una acepta una
        oferta de comprada
    """

    producto = get_object_or_404(Mercancia, pk=producto_id)
    monto=int(request.session['monto'])
    size=request.session['talla']
    o=Oferta_venta.objects.filter(monto=monto, talla=size, articulo=producto.id).first()

    message1=('Felicidades, has vendido {{producto}}',
    "Enhorabuena, por favor envíanos tu producto en su caja original",
    # DEFAULT_FROM_EMAIL setting.,
    'webmaster@localhost',
    [o.comprador.email])
    message2=('Se ha aceptado tu oferta!', 
    'Felicidades, tu producto llegará en los próximos días hábiles',
    # DEFAULT_FROM_EMAIL setting.,
    'webmaster@localhost',
    [request.user.email])
    send_mass_mail((message1,message2), fail_silently=False)

    comision = round(.07*monto,2)
    # Successful_offer.objects.create(oferta_comprada=None, oferta_vendida=o, ganador=request.user, comision=comision)
    Ofertas_compradas.objects.create(monto=monto,comision=comision,comprador=request.user,vendedor=o.comprador,talla=size, articulo=producto,fecha=datetime.today())
    o.delete()

    return render(request,"mercado/oferta_comprada.html",{
        'usuario':request.user.username,
        'producto':producto,
        'monto':monto,
        'talla':size,
    })

@login_required
def oferta_vendida(request,producto_id):
    producto = get_object_or_404(Mercancia, pk=producto_id)
    monto=int(request.session['monto'])
    size=request.session['talla']
    o=Oferta_compra.objects.filter(monto=monto, talla=size, articulo=producto.id).first()

    message1=('Felicidades, has vendido {{producto}}',
    "Enhorabuena, por favor envíanos tu producto en su caja original",
    'webmaster@localhost',
    [request.user.email])
    message2=('Se ha aceptado tu oferta!', 
    'Felicidades, tu producto llegará en los próximos días hábiles',
    'webmaster@localhost',
    [o.comprador.email])
    send_mass_mail((message1,message2), fail_silently=False)

    comision = round(.07*monto,2)
    # Successful_offer.objects.create(oferta_comprada=o, oferta_vendida=None, ganador=request.user, comision=comision)

    Ofertas_compradas.objects.create(monto=monto,comision=comision,comprador=o.comprador, vendedor=request.user ,talla=size, articulo=producto,fecha=datetime.today())
    o.delete()
    return render(request,"mercado/oferta_vendida.html",{
        'usuario':request.user.username,
        'producto':producto,
        'monto':monto,
        'talla':size,
    })

#buy offer sent successfully
@login_required
def oferta_compra_enviada(request,producto_id):
    usuario = User.objects.get(pk=request.user.pk)
    producto = get_object_or_404(Mercancia, pk=producto_id)
    monto=request.session['monto']
    size=request.session['talla']
    o=Oferta_compra(monto=monto,comprador=usuario,talla=size,articulo=producto,fecha=datetime.today())

    #check duplicated
    oferta_duplicada = Oferta_compra.objects.filter(comprador=usuario,talla=size,articulo=producto)
    print(oferta_duplicada)
    if oferta_duplicada:
        messages.add_message(request, messages.INFO, "Ya has creado una oferta en esta talla!!!")
        print("!!!!     Oferta de venta duplicada   !!!!")
        
        return HttpResponseRedirect(reverse('mercado:detalles', args=(producto.id,)))
    
    users=Oferta_compra.objects.filter(talla=size,articulo=producto).distinct('comprador')
    emails=[]
    for i in users:
        emails.append(i.comprador.email)
    message1=('Tu oferta de compra está activa',
    'En este momento tu oferta ha sido activada',
    'armario@armario.com',
    [request.user.email])

    oferta_mayor=Oferta_compra.objects.filter(talla=size,articulo=producto).order_by('monto').last()
    try:
        oferta_mayor=oferta_mayor.monto
    except AttributeError:
        oferta_mayor=0
        
    if(o.monto > oferta_mayor):
        print("oferta mayor")
        message2=('Una oferta mayor ha sido colocada',
                    'Alguien ha superado tu oferta, que no te lo ganen!',
                    'armario@armario.com',
                    emails
                    )
        send_mass_mail((message1,message2),fail_silently=False)
    else:
        send_mail('Tu oferta de compra está activa',
    'En este momento tu oferta ha sido activada',
    'armario@armario.com',
    [request.user.email]
    , fail_silently=False)

    o.save()
    
    return render(request,"mercado/oferta_compra_enviada.html",{
        "producto":producto,
        "talla":size,
        "monto":monto,
        })


#sell offer sent successfully
@login_required
def oferta_venta_enviada(request,producto_id):
    usuario = User.objects.get(pk=request.user.pk)
    producto = get_object_or_404(Mercancia, pk=producto_id)
    monto=int(request.session['monto'])
    size=request.session['talla']
    o=Oferta_venta(monto=monto,comprador=usuario,talla=size,articulo=producto,fecha=datetime.today())    

    #check duplicated offer
    oferta_duplicada = Oferta_compra.objects.filter(comprador=usuario,talla=size,articulo=producto)
    print(oferta_duplicada)
    if oferta_duplicada:
        messages.add_message(request, messages.INFO, "Ya has creado una oferta en esta talla!!!")
        print("!!!!     Oferta de venta duplicada   !!!!")
        
        return HttpResponseRedirect(reverse('mercado:detalles', args=(producto.id,)))
    
    users=Oferta_venta.objects.filter(talla=size,articulo=producto).distinct('comprador')
    emails=[]
    for i in users:
        emails.append(i.comprador.email)
    message1=('Tu oferta de venta está activa',
    'En este momento tu oferta ha sido activada',
    'armario@armario.com',
    [request.user.email])
    oferta_mayor=Oferta_venta.objects.filter(talla=size,articulo=producto).order_by('monto').first()
    try:
        oferta_mayor=oferta_mayor.monto
    except AttributeError:
        oferta_mayor=0
    if(o.monto < oferta_mayor):
        message2=('Una oferta menor ha sido colocada',
                    'Alguien ha superado tu oferta, que no te lo ganen!',
                    'armario@armario.com',
                    emails
                    )
        send_mass_mail((message1,message2),fail_silently=False)
    else:
        send_mail('Tu oferta de venta está activa',
    'En este momento tu oferta ha sido activada',
    'armario@armario.com',
    [request.user.email]
    , fail_silently=False)

    o.save()

    return render(request,"mercado/oferta_venta_enviada.html",{
        "producto":producto,
        "talla":size,
        "monto":monto,
        })

@login_required
def eliminar_compra(request,oferta_id):
    oferta = get_object_or_404(Oferta_compra, pk=oferta_id)
    oferta.delete()

    return HttpResponseRedirect(reverse('mercado:mis_ofertas'))

@login_required
def eliminar_venta(request,oferta_id):
    oferta = get_object_or_404(Oferta_venta, pk=oferta_id)
    oferta.delete()

    return HttpResponseRedirect(reverse('mercado:mis_ofertas'))

class ByBrandListView(ListView):
    context_object_name = 'productos'
    template_name = 'mercado/products_by_type.html'
    def get_queryset(self):
        self.marca = get_object_or_404(Marca, nombre=self.kwargs['marca'])
        return Mercancia.objects.filter(marca=self.marca)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type']=self.marca
        context['brands']=Marca.objects.exclude(pk=self.marca.pk)
        return context

class ByDepartmentListView(ListView):
    context_object_name = 'productos'
    template_name = 'mercado/products_by_type.html'

    def get_queryset(self):
        return Mercancia.objects.filter(depto=self.kwargs['department'])

    def get_context_data(self, **kwargs):
        context = super(ByDepartmentListView,self).get_context_data(**kwargs)
        context['all']=[]
        for depto in Mercancia.DEPTO:
            context['all'].append(depto[1])
            if self.kwargs['department'] in depto:
                context['type'] = depto[1]
        # context['departments'].remove(context['type'])
        return context

@method_decorator(login_required, name='dispatch')
class MyOffersListView(ListView):
    context_object_name = 'successfull_offers'
    template_name='mercado/mis_ofertas.html'
    def get_queryset(self):
        return Ofertas_compradas.objects.filter(comprador=self.request.user).union(Ofertas_compradas.objects.filter(vendedor=self.request.user))

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['buy_offers'] = Oferta_compra.objects.filter(comprador=self.request.user)
        context['sell_offers'] = Oferta_venta.objects.filter(comprador=self.request.user)
        return context

class ProfileDetailView(DetailView):
    def get_object(self):
        return get_object_or_404(Cliente, pk=self.request.user.pk)

