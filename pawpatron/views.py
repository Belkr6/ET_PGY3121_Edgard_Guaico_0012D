from django.shortcuts import render, redirect
from .models import Alimentos, Boleta, detalle_boleta
from .forms import ItemForm
from .forms import RegistroUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.db.models import Max
from pawpatron.compra import Carrito
from django.core.paginator import Paginator,  PageNotAnInteger, EmptyPage
import io
from django.http import HttpResponse
from django.template.loader import render_to_string



# Create your views here.
def index(request):
    return render(request,'index.html')

def knowus(request):
    return render(request,'knowus.html')

def apires(request):
    return render(request,'apires.html')

def store(request):
    MAX_ITEMS = 6  # Número máximo de elementos a mostrar por página
    page = request.GET.get('page', 1)  # Obtener el número de página actual de la consulta GET

    alimentos = Alimentos.objects.all()  # Obtener todos los elementos

    paginator = Paginator(alimentos, MAX_ITEMS)  # Crear un objeto Paginator con los elementos
    try:
        alimentos = paginator.page(page)  # Obtener la página actual
    except PageNotAnInteger:
        alimentos = paginator.page(1)  # Si el número de página no es un entero, mostrar la primera página
    except EmptyPage:
        alimentos = paginator.page(paginator.num_pages)  # Si la página está vacía, mostrar la última página

    carrito_compra = Carrito(request)
    total_con_envio, impuesto = carrito_compra.calcular_total_general()  # Calcular el total general
    
    return render(request, 'store.html', {'total_con_envio': total_con_envio,'alimentos': alimentos, 'impuesto': impuesto})




@login_required
def crear(request):
    if request.method == "POST":
        itemform = ItemForm(request.POST, request.FILES)  # Asegúrate de incluir request.FILES para manejar la imagen
        if itemform.is_valid():
            item = itemform.save(commit=False)  # Guarda el formulario sin commit para realizar modificaciones adicionales
            item.categoria_id = request.POST['categoria']  # Asigna la categoría seleccionada desde el formulario
            item.save()  # Guarda el objeto 'item' en la base de datos
            return redirect('store')  # Redirige a la página 'store' después de guardar los datos
    else:
        itemform = ItemForm()
    return render(request, 'crear.html', {'itemform': itemform})


@login_required
def eliminar(request, id):
    itemEliminado=Alimentos.objects.get(itemid=id) #buscamos un vehiculo por la patentes
    itemEliminado.delete()
    return redirect('store')






def registrar(request):
    data={
        'form':RegistroUserForm()
    }
    if request.method=="POST":
        formulario=RegistroUserForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user=authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request,user)
            return redirect ('index')
        data["form"]=formulario   
    return render(request,'registrar.html', data)

def mostrar(request):
    items=Alimentos.objects.all()
    datos={
        'items':items
    }
    return render(request,'store.html', datos)

def buscar_alimentos(request):
    if 'q' in request.GET:
        termino_busqueda = request.GET['q']
        alimentos = Alimentos.objects.filter(marca__icontains=termino_busqueda)
    else:
        alimentos = Alimentos.objects.all()

    context = {'alimentos': alimentos}
    return render(request, 'store.html', context)

@login_required
def modificar(request, item_id):
    itemMod = get_object_or_404(Alimentos, itemid=item_id)

    if request.method == "POST":
        formulario = ItemForm(data=request.POST, files=request.FILES, instance=itemMod)

        if formulario.is_valid():
            formulario.save()
            return redirect('store')

    else:
        formulario = ItemForm(instance=itemMod)

    datos = {
        'form': formulario,
        'itemMod': itemMod
    }

    return render(request, 'modificar.html', datos)


def agregar_producto(request,id):
    carrito_compra= Carrito(request)
    alimento =Alimentos.objects.get(itemid=id)
    carrito_compra.agregar(Alimentos=alimento)
    return redirect('store')

def eliminar_producto(request, id):
    carrito_compra= Carrito(request)
    alimento =Alimentos.objects.get(itemid=id)
    carrito_compra.eliminar(Alimentos=alimento)
    return redirect('store')



def restar_producto(request, id):
    carrito_compra= Carrito(request)
    alimento =Alimentos.objects.get(itemid=id)
    carrito_compra.restar(Alimentos=alimento)
    return redirect('store')

def limpiar_carrito(request):
    carrito_compra= Carrito(request)
    carrito_compra.limpiar()
    return redirect('store')    

@login_required
def generarBoleta(request):
    precio_total = 0
    for key, value in request.session['carrito'].items():
        precio_total += int(value['precio']) * int(value['cantidad'])
    
    # Calcular el monto de impuestos (por ejemplo, 10%)
    impuestos = precio_total * 0.1
    
    # Calcular el total incluyendo los impuestos
    total_con_impuestos = int(precio_total + impuestos + 1200)
    
    boleta = Boleta(total=total_con_impuestos)
    boleta.save()
    
    productos = []
    for key, value in request.session['carrito'].items():
        producto = Alimentos.objects.get(itemid=value['Alimentos_id'])
        cant = value['cantidad']
        subtotal = cant * int(value['precio'])
        detalle = detalle_boleta(id_boleta=boleta, itemid=producto, cantidad=cant, subtotal=subtotal)
        detalle.save()
        productos.append(detalle)
        
        producto.cantidad_disponible -= cant
        producto.save()
    
    datos = {
        'productos': productos,
        'boleta': boleta,
        'fecha': boleta.fechaCompra,
        'total': boleta.total
    }
    
    request.session['boleta'] = boleta.id_boleta
    carrito = Carrito(request)
    carrito.limpiar()

    # Renderizar la plantilla 'detallecarrito.html' con los datos de la boleta
    return render(request, 'detallecarrito.html', datos)

def descargarBoleta(request, boleta_id):
    # Obtener los datos de la boleta
    boleta = Boleta.objects.get(id_boleta=boleta_id)
    productos = detalle_boleta.objects.filter(id_boleta=boleta)

    # Generar los datos para la plantilla
    datos = {
        'boleta': boleta,
        'productos': productos,
        'fecha': boleta.fechaCompra,
        'total': boleta.total
    }

    # Generar contenido del archivo TXT utilizando una plantilla
    contenido = render_to_string('boleta.txt', datos)

    # Crear el objeto de respuesta HTTP con el archivo adjunto
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="boleta.txt"'

    # Escribir el contenido en la respuesta HTTP
    response.write(contenido)

    # Devolver la respuesta HTTP de descarga de la boleta
    return response


