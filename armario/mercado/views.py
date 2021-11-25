from datetime import datetime
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
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth.backends import BaseBackend
from mercado.forms import RegisterForm
from .models import Client, Brand, Product, BuyOffer, SellOffer, SuccessfulOffer

def fam_member(type: str,dept: str):
    sizes = []
    if dept == 'SH':
        if type == 'M':
            for i in range(25,32):
                sizes+=[f'{i} cm']
        elif type == 'W':
            for i in range (23,27):
                sizes+=[f'{i} cm']
        elif type == 'GS':
            for i in range (21,25):
                sizes+=[f'{i} cm']
        elif type == 'PS':
            for i in range (15,21):
                sizes+=[f'{i} cm']
    elif dept == 'CL':
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
    model = Product
    template_name = "mercado/index.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(IndexListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['marcas'] = Brand.objects.all().values_list('name',flat=True)
        context['deptos'] = Product.DEPT

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
            username = form.cleaned_data['usuario']
            email = form.cleaned_data['email']
            passwd = form.cleaned_data['passwd']
            confirm_passwd = form.cleaned_data['confirm_passwd']
            if passwd != confirm_passwd:
                messages.error(request, "por favor verifica las contraseñas")

                return HttpResponseRedirect(reverse('mercado:register'))

            phone = form.cleaned_data['phone']
            new_user = User.objects.create_user(username,email,passwd)
            new_user.save()
            new_client = Client(user=new_user,number=phone, slug=username)
            new_client.save()
            form.send_email()
            messages.success(request, 'Usuario registrado correctamente, se ha enviado un correo de verificación a %s' %email)

            return HttpResponseRedirect(reverse('mercado:register'))
    
        return render(request,self.template_name, {'form':form})

# class MyBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None):
#         # Check the username/password and return a user.
#         if username.password in User.objects.all():
#             print("ok")
#             return username
#     def get_user(user):
#         return User.objects.filter()

def detalles(request,pk):
    product = get_object_or_404(Product, pk=pk)
    sizes = fam_member(product.size_type,product.dept)
    buy_bids=[]
    sell_offers=[]

    for size in sizes:
        buy_bids+=[BuyOffer.objects.filter(product=product,size=size).values_list('offer',flat=True).order_by('offer').last()]

    for size in sizes:
        sell_offers+=[SellOffer.objects.filter(product=product,size=size).values_list('offer',flat=True).order_by('offer').first()]
    
    to_buy=zip(sizes,sell_offers,buy_bids)
    to_sell=zip(sizes,buy_bids, sell_offers)
    
    for i in Product.DEPT:
        if product.dept in i:
            dept=i

    return render(request, "mercado/detalles.html", {
        'producto':product,
        'tallas':sizes,
        'ventas':to_sell,
        'compras':to_buy,
        'depto': dept
        })  

def compra(request, producto_id):
    product = get_object_or_404(Product, pk=producto_id)

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

            return HttpResponseRedirect(reverse('mercado:oferta_compra',args=(product.id,)))

    except(KeyError,product.DoesNotExist):

        return render(request, "mercado/compra.html",{
            'producto':product,
            'error_message':"You didn´t select a Size"
            })

    else:

        return HttpResponseRedirect(reverse('mercado:compra',args=(product.id,)))

def venta(request,producto_id):
    product = get_object_or_404(Product, pk=producto_id)
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

            return HttpResponseRedirect(reverse('mercado:oferta_venta',args=(product.id,)))

    except(KeyError,product.DoesNotExist):

        return render(request, "mercado/venta.html",{
            'producto':product,
            'error_message':"You didn´t select a Size"
            })
    else:

        return HttpResponseRedirect(reverse('mercado:venta',args=(product.id,)))

def oferta_compra(request,producto_id):
    product = Product.objects.get(id=producto_id)
    comision = request.session['comision']
    return render(request,"mercado/oferta_compra.html",{
        "producto":product,
        "comision": round(comision,2)
        })

def oferta_venta(request,producto_id):
    product = Product.objects.get(id=producto_id)
    comision = request.session['comision']
    return render(request,"mercado/oferta_venta.html",{
        "producto":product,
        "comision": round(comision,2)
        })

@login_required
def oferta_comprada(request,producto_id):
    """
        aceptar una oferta de venta; el usuario compra la oferta de venta mas baja
    """
    product = get_object_or_404(Product, pk=producto_id)
    offer=int(request.session['monto'])
    size=request.session['talla']
    successful_offer=SellOffer.objects.filter(offer=offer, size=size, product=product.id).first()

    message1=('Felicidades, has vendido {{product}}',
    "Enhorabuena, por favor envíanos tu producto en su caja original",
    # DEFAULT_FROM_EMAIL setting.,
    'webmaster@localhost',
    [successful_offer.seller.user.email])
    message2=('Se ha aceptado tu oferta!', 
    'Felicidades, tu producto llegará en los próximos días hábiles',
    # DEFAULT_FROM_EMAIL setting.,
    'webmaster@localhost',
    [request.user.email])
    send_mass_mail((message1,message2), fail_silently=False)

    comision = round(.07*offer,2)
    # Successful_offer.objects.create(oferta_comprada=None, oferta_vendida=o, ganador=request.user, comision=comision)
    SuccessfulOffer.objects.create(offer=offer,comision=comision,buyer=request.user.client,seller=successful_offer.seller,size=size, product=product,date=datetime.today())
    successful_offer.delete()

    return render(request,"mercado/oferta_comprada.html",{
        'usuario':request.user.username,
        'producto':product,
        'monto':offer,
        'talla':size,
    })

@login_required
def oferta_vendida(request,producto_id):
    product = get_object_or_404(Product, pk=producto_id)
    offer=int(request.session['monto'])
    size=request.session['talla']
    successful_offer=BuyOffer.objects.filter(offer=offer, size=size, product=product.id).first()

    message1=('Felicidades, has vendido {{producto}}',
    "Enhorabuena, por favor envíanos tu producto en su caja original",
    'webmaster@localhost',
    [request.user.email])
    message2=('Se ha aceptado tu oferta!', 
    'Felicidades, {{producto}} llegará en los próximos 5 días hábiles',
    'webmaster@localhost',
    [successful_offer.buyer.user.email])
    send_mass_mail((message1,message2), fail_silently=False)

    comision = round(.07*offer,2)
    # Successful_offer.objects.create(oferta_comprada=o, oferta_vendida=None, ganador=request.user, comision=comision)

    SuccessfulOffer.objects.create(offer=offer,comision=comision,buyer=successful_offer.buyer.user.client, seller=request.user.client ,size=size, product=product,date=datetime.today())
    successful_offer.delete()
    return render(request,"mercado/oferta_vendida.html",{
        'usuario':request.user.username,
        'producto':product,
        'monto':offer,
        'talla':size,
    })

def check_duplicated(request,duplicated_offer,product):
    if duplicated_offer:
        print('oferta duplicada')
        print(duplicated_offer)
        messages.add_message(request, messages.INFO, "Ya has creado una oferta en esta talla!!!")
        print("!!!!     Oferta de venta duplicada   !!!!")

        return HttpResponseRedirect(reverse('mercado:detalles', args=(product.id,)))

#buy offer sent successfully
@login_required
def oferta_compra_enviada(request,producto_id):
    user = Client.objects.get(pk=request.user.pk)
    product = get_object_or_404(Product, pk=producto_id)
    offer=request.session['monto']
    size=request.session['talla']
    bid_sent=BuyOffer(offer=offer,buyer=user,size=size,product=product,date=datetime.today())

    duplicated_offer = BuyOffer.objects.filter(buyer=user,size=size,product=product)

    #check duplicated
    check_duplicated(request,duplicated_offer,product)
    
    users=BuyOffer.objects.filter(size=size,product=product).distinct('buyer')
    emails=[]
    for i in users:
        emails.append(i.buyer.user.email)
    message1=('Tu oferta de compra está activa',
    'En este momento tu oferta ha sido activada',
    'armario@armario.com',
    [request.user.email])

    oferta_mayor=BuyOffer.objects.filter(size=size,product=product).order_by('offer').last()
    try:
        oferta_mayor=oferta_mayor.offer
    except AttributeError:
        oferta_mayor=0
        
    if(bid_sent.offer > oferta_mayor):
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

    bid_sent.save()
    
    return render(request,"mercado/oferta_compra_enviada.html",{
        "producto":product,
        "talla":size,
        "monto":offer,
        })

#sell offer sent successfully
@login_required
def oferta_venta_enviada(request,producto_id):
    user = Client.objects.get(pk=request.user.pk)
    product = get_object_or_404(Product, pk=producto_id)
    offer=int(request.session['monto'])
    size=request.session['talla']
    offer_sent=SellOffer(offer=offer,seller=user,size=size,product=product,date=datetime.today())    

    #check duplicated offer
    oferta_duplicada = BuyOffer.objects.filter(buyer=user,size=size,product=product)
    print(oferta_duplicada)
    if oferta_duplicada:
        messages.add_message(request, messages.INFO, "Ya has creado una oferta en esta talla!!!")
        print("!!!!     Oferta de venta duplicada   !!!!")
        
        return HttpResponseRedirect(reverse('mercado:detalles', args=(product.id,)))
    
    users=SellOffer.objects.filter(size=size,product=product).distinct('seller')
    emails=[]
    for i in users:
        emails.append(i.seller.user.email)
    message1=('Tu oferta de venta está activa',
    'En este momento tu oferta ha sido activada',
    'armario@armario.com',
    [request.user.email])
    oferta_mayor=SellOffer.objects.filter(size=size,product=product).order_by('offer').first()
    try:
        oferta_mayor=oferta_mayor.offer
    except AttributeError:
        oferta_mayor=0
    if(offer_sent.offer < oferta_mayor):
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

    offer_sent.save()

    return render(request,"mercado/oferta_venta_enviada.html",{
        "producto":product,
        "talla":size,
        "monto":offer,
        })

@login_required
def eliminar_compra(request,oferta_id):
    offer = get_object_or_404(BuyOffer, pk=oferta_id)
    offer.delete()

    return HttpResponseRedirect(reverse('mercado:mis_ofertas'))

@login_required
def eliminar_venta(request,oferta_id):
    offer = get_object_or_404(SellOffer, pk=oferta_id)
    offer.delete()

    return HttpResponseRedirect(reverse('mercado:mis_ofertas'))

class ByBrandListView(ListView):
    context_object_name = 'list' #list of brands
    template_name = 'mercado/products_by_type.html'

    def get_queryset(self):
        self.marca = get_object_or_404(Brand, name=self.kwargs['marca'])
        return Product.objects.filter(brand=self.marca)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type']=self.marca
        context['brands']=Brand.objects.exclude(pk=self.marca.pk)
        return context

class ByDepartmentListView(ListView):
    context_object_name = 'list' #list of departments
    template_name = 'mercado/products_by_type.html'

    def get_queryset(self):
        return Product.objects.filter(dept=self.kwargs['department'])

    def get_context_data(self, **kwargs):
        context = super(ByDepartmentListView,self).get_context_data(**kwargs)
        for depto in Product.DEPT:
            if self.kwargs['department'] in depto:
                context['type'] = depto[1]
        # context['departments'].remove(context['type'])
        return context

# @method_decorator(login_required, name='dispatch')
# class MyOffersListView(ListView):
#     context_object_name = 'successfull_offers'
#     template_name='mercado/mis_ofertas.html'
#     def get_queryset(self):
#         return SuccessfulOffer.objects.filter(buyer=self.request.user.client).union(SuccessfulOffer.objects.filter(seller=self.request.user.client))

#     def get_context_data(self,**kwargs):
#         context = super().get_context_data(**kwargs)
#         client =  get_object_or_404(Client, pk=self.request.user.pk)
#         context['buy_offers'] = BuyOffer.objects.filter(buyer=client)
#         context['sell_offers'] = SellOffer.objects.filter(seller=client)
#         context['offers'] = zip(context['buy_offers'],context['sell_offers'])
#         return context

@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView):
    model= Client
    context_object_name = 'profile'
    template_name = "mercado/my_profile.html"

@method_decorator(login_required, name='dispatch')
class EditProfileFormView (FormView):
    template_name = "mercado/edit_profile.html"
    form_class = RegisterForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            client = get_object_or_404(Client, pk=self.request.user.pk)
            user_client = get_object_or_404(User,pk=self.request.user.pk)
            user_client.first_name = form.cleaned_data['first_name']
            user_client.last_name = form.cleaned_data['last_name']
            user_client.username = form.cleaned_data['usuario']
            client.number = form.cleaned_data['phone']
            if form.cleaned_data['passwd'] != form.cleaned_data['confirm_passwd']:
                    messages.error(request, "por favor verifica las contraseñas")

                    return HttpResponseRedirect(reverse('mercado:edit_profile'))
            client.save()
            user_client.save()
            messages.success(request, "Se editó su perfil correctamente")

            return HttpResponseRedirect(reverse('mercado:my_profile'))

        return render(request,self.template_name, {'form':form})

class AskBidListView(ListView):
    template_name = 'mercado/ask_n_bid.html'

    def get_queryset(self):
        return Client.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        client =  get_object_or_404(Client, pk=self.request.user.pk)
        context = super().get_context_data(**kwargs)
        if (self.kwargs['info'] == 'BuyOffer'):
            context['type']="Pujas"
            context['offers'] = BuyOffer.objects.filter(buyer=client)
        elif (self.kwargs['info'] == 'SellOffer'):
            context['type']="Ofertas"
            context['offers'] = SellOffer.objects.filter(seller=client)
        elif (self.kwargs['info'] == 'SuccessfulOffer'):
            context['type']="Concluidas"
            context['offers'] = SuccessfulOffer.objects.filter(seller=client).union(SuccessfulOffer.objects.filter(buyer=client))
        return context

class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class AskListView(ListView):
    model = BuyOffer

    def get_queryset(self):
        buyer = get_object_or_404(Client, pk=self.request.user.pk)
        return BuyOffer.objects.filter(buyer=buyer)
