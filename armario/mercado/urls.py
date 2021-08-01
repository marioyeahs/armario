from django.urls import path

from . import views
from mercado.views import MercanciaListView, MarcaListView

app_name='mercado'
urlpatterns = [
    #path('',views.index, name='index'),
    path('', MercanciaListView.as_view(),name='index'),
    path('<int:producto_id>/detalles', views.detalles, name='detalles'),
    path('<int:producto_id>/compra', views.compra, name='compra'),
    path('<int:producto_id>/venta', views.venta, name='venta'),
    path('<int:producto_id>/comprado', views.comprado,name='comprado'),
    path('<int:producto_id>/vendido', views.vendido,name='vendido'),
    path('registro/', views.register,name='register'),
    path('mis_ofertas/', views.mis_ofertas,name='mis_ofertas'),
    #path('mercancia/<int:pk>', MercanciaDetailView.as_view(),name='mercancia-detail'),
    path('mercancia/<marca>', MarcaListView.as_view(), name='marca')

    #path('myurl/<int:fish>', views.my_view, {'my_template_name': 'some_path'}, name='aurl'),

]