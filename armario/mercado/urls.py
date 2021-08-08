from django.urls import path
from django.views.generic import TemplateView

from . import views
from mercado.views import IndexListView, MarcaListView, RegisterFormView, MasVendidosListView

app_name='mercado'
urlpatterns = [
    #path('',views.index, name='index'),
    path('', IndexListView.as_view(),name='index'),
    path('<int:producto_id>/detalles', views.detalles, name='detalles'),
    path('<int:producto_id>/compra', views.compra, name='compra'),
    path('<int:producto_id>/venta', views.venta, name='venta'),
    path('<int:producto_id>/comprado', views.comprado,name='comprado'),
    path('<int:producto_id>/vendido', views.vendido,name='vendido'),
    path('registro/', RegisterFormView.as_view(),name='register'),
    path('mis_ofertas/', views.mis_ofertas,name='mis_ofertas'),
    #path('mercancia/<int:pk>', MercanciaDetailView.as_view(),name='mercancia-detail'),
    path('mercancia/<marca>', MarcaListView.as_view(), name='marca'),
    path('mis_ofertas/<int:oferta_id>/eliminar_venta', views.eliminar_venta, name='eliminar_venta'),
    path('mis_ofertas/<int:oferta_id>/eliminar_compra', views.eliminar_compra, name='eliminar_compra'),
    #path('myurl/<int:fish>', views.my_view, {'my_template_name': 'some_path'}, name='aurl'),
    path('mas_vendidos/',MasVendidosListView.as_view(), name='mas_vendidos')

]