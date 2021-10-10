from django.urls import path
from django.views.generic import TemplateView

from . import views
from mercado.views import IndexListView, ProfileDetailView, RegisterFormView, ByBrandListView, ByDepartmentListView, MyOffersListView

app_name='mercado'
urlpatterns = [
    path('', IndexListView.as_view(),name='index'),
    path('<int:pk>/detalles/', views.detalles, name='detalles'),
    path('<int:producto_id>/compra/', views.compra, name='compra'),
    path('<int:producto_id>/venta/', views.venta, name='venta'),
    path('<int:producto_id>/oferta_compra_enviada/', views.oferta_compra_enviada, name='oferta_compra_enviada'),
    path('<int:producto_id>/oferta_venta_enviada/', views.oferta_venta_enviada,name='oferta_venta_enviada'),
    path('registro/', RegisterFormView.as_view(),name='register'),
    path('mis_ofertas/', MyOffersListView.as_view(), name='mis_ofertas'),
    path('productos/<marca>/', ByBrandListView.as_view(), name='marca'),
    path('departamento/<department>/', ByDepartmentListView.as_view(), name='department'),
    path('mis_ofertas/<int:oferta_id>/eliminar_venta/', views.eliminar_venta, name='eliminar_venta'),
    path('mis_ofertas/<int:oferta_id>/eliminar_compra/', views.eliminar_compra, name='eliminar_compra'),
    #path('myurl/<int:fish>', views.my_view, {'my_template_name': 'some_path'}, name='aurl'),
    path('<int:producto_id>/oferta_venta/', views.oferta_venta, name='oferta_venta'),
    path('<int:producto_id>/oferta_vendida/', views.oferta_vendida, name='oferta_vendida'),
    path('<int:producto_id>/oferta_compra/', views.oferta_compra, name='oferta_compra'),
    path('<int:producto_id>/oferta_comprada/', views.oferta_comprada, name='oferta_comprada'),
    path('mi_perfil/', ProfileDetailView.as_view(), name='my_profile'),
    ]