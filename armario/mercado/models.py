from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

# Create your models here.

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numero = models.IntegerField()
    def __str__(self):
        return f"{self.user.username} - Celular:{self.numero}"

class Marca(models.Model):
    nombre = models.CharField(max_length=255)
    def __str__(self):
        return self.nombre
    

class Mercancia(models.Model):
    modelo = models.CharField(max_length=255)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="brand")
    SIZE_TYPE = (
        ('M','Men'), 
        ('W','Women'),
        ('GS','Grade School'),
        ('PS','Preschool'),
        ('IF','Infant'),
        ('TD','Toddler')
    )
    DEPTO =(
        ('CZ','Calzado'),
        ('RP','Ropa'),
        ('RJ','Reloj'),
        ('CL','Coleccionable')
    )
    size_type = models.CharField(verbose_name="Miembro",max_length=2, choices=SIZE_TYPE)
    depto = models.CharField(verbose_name="Departamento",max_length=2, choices=DEPTO)
    def __str__(self):
        return f"{self.marca} {self.modelo}."

    def get_absolute_url(self):
        return reverse('mercado:detalles', kwargs={'pk':self.pk})
        

class Oferta_compra(models.Model):
    monto = models.IntegerField()
    comprador = models.ForeignKey(User, on_delete=models.CASCADE)
    talla = models.CharField(max_length=5, null=True,blank=True)
    articulo = models.ForeignKey(Mercancia, on_delete=models.RESTRICT)
    fecha = models.DateTimeField()
    def __str__(self):
        return f"${self.monto}.00 mxn en {self.articulo.modelo} - {self.talla} | {self.comprador}"
    
    def oferta_mayor_envio(self):
        """verify if the offer is greater than the deilvery cost"""
        return self.monto > 200

class Oferta_venta(models.Model):
    monto = models.IntegerField()
    comprador = models.ForeignKey(User, on_delete=models.CASCADE)
    talla = models.CharField(max_length=5, null=True,blank=True)
    articulo = models.ForeignKey(Mercancia, on_delete=models.RESTRICT)
    fecha = models.DateTimeField()
    def __str__(self):
        return f"${self.monto}.00 mxn en {self.articulo.modelo} - {self.talla} | {self.comprador}"

class Successful_offer(models.Model):
    oferta_comprada = models.OneToOneField(Oferta_compra, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='comprada')
    oferta_vendida = models.OneToOneField(Oferta_venta, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='vendida')
    #ganador, aquel que acepta la oferta de compra o venta
    ganador = models.ForeignKey(User, on_delete=models.CASCADE)
    comision = models.FloatField()

    # def select_offer(self):
    #     if self.oferta_vendida != None:
    #         return "Oferta vendida"
    #     else:
    #         return "Oferta_comprada"

    def __str__(self):
        return f"Comprada:{self.oferta_vendida} - Vendida:{self.oferta_comprada} | Ganador:{self.ganador}"

class Ofertas_compradas(models.Model):
    monto = models.IntegerField()
    comision= models.FloatField()
    comprador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comprador')
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    talla = models.CharField(max_length=5, null=True,blank=True)
    articulo = models.ForeignKey(Mercancia, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    def __str__(self):
        return f"${self.monto}.00 mxn en {self.articulo.modelo} - De:{self.vendedor} | Para:{self.comprador} | Comisión:${self.comision}"


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