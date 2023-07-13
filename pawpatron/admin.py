from django.contrib import admin
from .models import  Alimentos, Categoria, detalle_boleta,Boleta

# Register your models here.
admin.site.register(Alimentos)
admin.site.register(Categoria)
admin.site.register(detalle_boleta)
admin.site.register(Boleta)




