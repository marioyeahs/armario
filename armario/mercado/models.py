from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numero = models.IntegerField()
    def __str__(self):
        return f"Cliente {self.numero}"

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
        ('JG','Juguete'),
        ('CL','Coleccionable')
    )
    size_type = models.CharField(verbose_name="Miembro",max_length=2, choices=SIZE_TYPE)
    depto = models.CharField(verbose_name="Departamento",max_length=2, choices=DEPTO)
    def __str__(self):
        return f"{self.marca} {self.modelo}, {self.size_type}."


class Oferta_compra(models.Model):
    monto = models.IntegerField()
    comprador = models.ForeignKey(User, on_delete=models.CASCADE)
    talla = models.CharField(max_length=5, null=True,blank=True)
    articulo = models.ForeignKey(Mercancia, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    def __str__(self):
        return f"Compra: ${self.monto}.00 mxn en {self.articulo}: {self.comprador}"

class Oferta_venta(models.Model):
    monto = models.IntegerField()
    comprador = models.ForeignKey(User, on_delete=models.CASCADE)
    talla = models.CharField(max_length=5, null=True,blank=True)
    articulo = models.ForeignKey(Mercancia, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    def __str__(self):
        return f"Venta: ${self.monto}.00 mxn en {self.articulo}: {self.comprador}"