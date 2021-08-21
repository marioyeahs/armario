from django.test import TestCase
from django.urls import reverse


# Create your tests here.

from mercado.models import Cliente, Oferta_compra

class Oferta_compraModelTest(TestCase):
    def test_monto_oferta_mayor_envio(self):
        """si la oferta es mayor al costo de envío retorna True"""
        oferta = Oferta_compra(monto=200)
        self.assertIs(oferta.oferta_mayor_envio(),False)
    
