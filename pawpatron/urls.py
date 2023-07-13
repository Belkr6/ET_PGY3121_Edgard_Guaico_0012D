from django.urls import path
from .views import index, apires, knowus, store, crear, eliminar, modificar, registrar, login, buscar_alimentos, generarBoleta,agregar_producto,eliminar_producto,restar_producto,limpiar_carrito, descargarBoleta


urlpatterns=[
    path('', index, name="index"),
    path('knowus/', knowus, name="knowus"),
    path('apires/', apires, name="apires"),
    path('store/', store, name="store"),
    path('crear/', crear, name="crear"),
    path('eliminar/<id>', eliminar, name="eliminar"),
    path('registrar/',registrar,name="registrar"),
    path('login/',login,name="login"),
    path('buscar_alimentos/', buscar_alimentos, name='buscar_alimentos'),
    path('modificar/<int:item_id>/', modificar, name='modificar'),
    path('generarBoleta/', generarBoleta,name="generarBoleta"),
    path('agregar/<id>', agregar_producto, name="agregar"),
    path('eliminar/<id>', eliminar_producto, name="eliminar"),
    path('restar/<id>', restar_producto, name="restar"),
    path('limpiar/', limpiar_carrito, name="limpiar"),
    path('descargar-boleta/<int:boleta_id>', descargarBoleta, name='descargarBoleta'),
   
    
    
    
]