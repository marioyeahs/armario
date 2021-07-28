from django.urls import path

from . import views

app_name='mercado'
urlpatterns = [
    path('',views.index, name='index'),
    path('<int:producto_id>/detalles/', views.detalles, name='detalles'),
    path('<int:producto_id>/compra/', views.compra, name='compra'),
    path('<int:producto_id>/venta/', views.venta, name='venta'),
    path('<int:producto_id>/comprado/', views.comprado,name='comprado'),
    path('<int:producto_id>/vendido/', views.vendido,name='vendido'),
    path('registro/', views.register,name='register')

]