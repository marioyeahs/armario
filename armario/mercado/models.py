from django.db import models

# Create your models here.

class Cliente(models.Model):
    numero = models.IntegerField()
    def __str__(self):
        return self.numero

class Marca(models.Model):
    nombre = models.CharField(max_length=255)
    def __str__(self):
        return self.nombre

class Mercancia(models.Model):
    modelo = models.CharField(max_length=255)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="brand")
    def __str__(self):
        return f"{self.modelo} de {self.marca}"


class Oferta(models.Model):
    monto = models.IntegerField()
    comprador = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Mercancia, on_delete=models.CASCADE)
    def __str__(self):
        return f"${self.monto}.00 mxn en {self.articulo}"