from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext as _

# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.IntegerField()
    slug =models.SlugField(max_length=255, null=True, unique=True)
    def __str__(self):
        return f"{self.user.username} - Celular:{self.number}"
    def get_absolute_url(self):
        return reverse('mercado:my_profile', kwargs={'slug':self.slug})
        #save function creates slug based on the username to give us a better SEO
        #what it does is before save it, the username get through slugify function
        #and save it on the slug field, after that we store it on our bbdd
    def save(self,*args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Client, self).save(*args, **kwargs)

class Brand(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('mercado:marca', kwargs={'name':self.name})

class Product(models.Model):
    model = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    SIZE_TYPE = (
        ('M','Men'), 
        ('W','Women'),
        ('GS','Grade School'),
        ('PS','Preschool'),
        ('IF','Infant'),
        ('TD','Toddler'),
        ('NA','NotApply')
    )
    DEPT =(
        ('SH','Calzado'),
        ('WR','Ropa'),
        ('WT','Reloj'),
        ('CL','Coleccionable')
    )
    size_type = models.CharField(verbose_name="Miembro",max_length=2, choices=SIZE_TYPE)
    dept = models.CharField(verbose_name="Departamento",max_length=2, choices=DEPT)
    def __str__(self):
        return f"{self.brand} {self.model}."

    def get_absolute_url(self):
        return reverse('mercado:detalles', kwargs={'pk':self.pk})

class BuyOffer(models.Model):
    offer = models.IntegerField()
    buyer = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client')
    size = models.CharField(max_length=5, null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, related_name="product")
    date = models.DateTimeField()
    def __str__(self):
        return f"Puja en {self.product.model} {self.size} - ${self.offer}.00 mxn | {self.buyer}"
    
    def oferta_mayor_envio(self):
        """verify if the offer is greater than the deilvery cost"""
        return self.offer > 200

class SellOffer(models.Model):
    offer = models.IntegerField()
    seller = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='owner')
    size = models.CharField(max_length=5, null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    date = models.DateTimeField()
    def __str__(self):
        return f"Oferta en {self.product.model} {self.size} - ${self.offer}.00 mxn | {self.seller}"

# class Successful_offer(models.Model):
#     oferta_comprada = models.OneToOneField(Oferta_compra, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='comprada')
#     oferta_vendida = models.OneToOneField(Oferta_venta, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='vendida')
#     #ganador, aquel que acepta la oferta de compra o venta
#     ganador = models.ForeignKey(User, on_delete=models.CASCADE)
#     comision = models.FloatField()

#     # def select_offer(self):
#     #     if self.oferta_vendida != None:
#     #         return "Oferta vendida"
#     #     else:
#     #         return "Oferta_comprada"

#     def __str__(self):
#         return f"Comprada:{self.oferta_vendida} - Vendida:{self.oferta_comprada} | Ganador:{self.ganador}"

class SuccessfulOffer(models.Model):
    offer = models.IntegerField()
    comision= models.FloatField()
    buyer = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='comprador')
    seller = models.ForeignKey(Client, on_delete=models.CASCADE)
    size = models.CharField(max_length=5, null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField()
    def __str__(cls):
        return f"${cls.offer}.00 mxn en {cls.product.model} - De:{cls.seller} Para:{cls.buyer} | Comisión:${cls.comision} - Día: {cls.date}"


# class CustomAccountManager(BaseUserManager):
    
#     def create_superuser(self,email,user_name,first_name,password, **other_fields):
#         other_fields.setdefault('is_staff',True)
#         other_fields.setdefault('is_superuser',True)
#         other_fields.setdefault('is_active',True)

#         if other_fields.get('is_staff') is not True:
#             raise ValueError("Superuser must be set to is_staff=True")

#         return self.create_user(email,user_name,first_name,password,**other_fields)

#     def create_user(self,email,user_name,first_name,password, **other_fields):
        
#         if not email:
#             raise ValueError(_("Por favor intorduce un email válido"))

#         user = self.model(email=email,user_name=user_name,first_name=first_name,**other_fields)
#         user.set_password(password)
#         user.save()
#         return user
        

# class NewUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(_('email address'), unique=True)
#     user_name = models.CharField(max_length=150, unique=True)
#     first_name = models.CharField(max_length=150, blank=True)
#     start_date = models.DateField(default=timezone.now)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)

#     objects = CustomAccountManager()
    
#     USER_NAME = 'email'
#     REQUIRED_FIELDS = ['user_name']

#     def __str__(self):
#         return self.username