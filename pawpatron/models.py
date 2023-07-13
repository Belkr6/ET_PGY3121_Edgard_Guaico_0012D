import datetime
from distutils.command.upload import upload
from django.db import models
from tabnanny import verbose
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.

            
class Categoria(models.Model):
    idCategoria = models.IntegerField(primary_key=True, verbose_name="Id de categoria")
    nombreCategoria = models.CharField(max_length=50, blank=True, verbose_name="Nombre de Categoria")

    def __str__(self) :
        return self.nombreCategoria
    
    
class Alimentos(models.Model):
    itemid = models.IntegerField(primary_key=True, verbose_name="Id")
    marca = models.CharField(max_length=50, blank=True, verbose_name="Marca")
    tipodeal = models.CharField(max_length=50, blank=True, verbose_name="Tipo de alimento")
    tmascot = models.CharField(max_length=50, blank=True, verbose_name="Para:")
    imagen = models.ImageField(upload_to="imagenes", null=True, verbose_name="Imagen")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoría")
    precio = models.IntegerField(default=0, verbose_name="Precio")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    cantidad_disponible = models.PositiveIntegerField(default=40)

    def __str__(self):
        return str(self.itemid)

class Boleta(models.Model):
    id_boleta=models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total=models.BigIntegerField()
    fechaCompra=models.DateTimeField(blank=False, null=False, default = datetime.datetime.now)
    
    def __str__(self):
        return str(self.id_boleta)

class detalle_boleta(models.Model):
    id_boleta = models.ForeignKey('Boleta', blank=True, on_delete=models.CASCADE)
    id_detalle_boleta = models.AutoField(primary_key=True)
    itemid = models.ForeignKey('Alimentos', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.BigIntegerField()

    def __str__(self):
        return str(self.id_detalle_boleta)
    

    
        
    


    