from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import ProductoForm
from .models import Producto, Intercambio, Venta, Donacion, Transaccion, Usuario
from django.db.models import Q
from django.utils.timezone import now



def index(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        nombres_y_apellidos = request.POST.get('nombres_y_apellidos')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Verificar contraseñas
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'register.html')

        # Generar nombre de usuario automáticamente desde el correo
        nombre_usuario = email.split('@')[0]

        # Verificar que el nombre de usuario no exista
        original_username = nombre_usuario  # Guardar el nombre inicial para modificaciones
        counter = 1  # Contador para sufijos en caso de duplicados
        while Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
            nombre_usuario = f"{original_username}{counter}"
            counter += 1

        # Crear el nuevo usuario
        usuario = Usuario(
            cedula=cedula,
            nombres_y_apellidos=nombres_y_apellidos,
            nombre_usuario=nombre_usuario,
            email=email,
            contrasena=make_password(password),
        )
        usuario.save()

        # Mostrar mensaje de éxito
        messages.success(request, "Usuario registrado exitosamente. Ahora puedes iniciar sesión.")
        return redirect('login')  # Redirigir al login después de registrarse

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre_usuario = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Buscar el usuario en la base de datos
            usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)

            # Verificar la contraseña
            if check_password(password, usuario.contrasena):
                # Guardar datos en la sesión
                request.session['usuario_id'] = usuario.id
                request.session['nombre_usuario'] = usuario.nombre_usuario

                # Redirigir a la nueva página (page.html)
                return redirect('page')  # Cambiar a la URL de 'page'
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")

    return render(request, 'login.html')


def page_view(request):
    # Asegúrate de que el usuario esté autenticado
    if 'usuario_id' not in request.session:
        return redirect('login')  # Redirigir al login si no está autenticado

    # Obtener información del usuario si es necesario
    usuario_id = request.session['usuario_id']
    nombre_usuario = request.session['nombre_usuario']

    context = {
        'nombre_usuario': nombre_usuario,
    }
    return render(request, 'page.html', context)


def logout_view(request):
    # Eliminar los datos de la sesión
    request.session.flush()
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')




# Vista para subir un producto

def subir_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        categoria = request.POST.get('categoria')
        accion = request.POST.get('accion')
        precio = request.POST.get('precio')  # Solo se requiere para 'venta'
        imagen = request.FILES.get('imagen')

        # Validar que si la acción es 'venta', se proporcione un precio
        if accion == 'venta' and not precio:
            messages.error(request, "Debes ingresar un precio si seleccionas 'Venta'.")
            return redirect('subir_producto')

        # Crear el producto sin necesidad de categoria_intercambio
        producto = Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            categoria=categoria,
            accion=accion,
            precio=precio if accion == 'venta' else None,
            imagen=imagen,
            fecha_publicacion=now()
        )

        messages.success(request, "Producto subido exitosamente.")
        return redirect('subir_producto')

    return render(request, 'productos.html')



def listar_productos(request):
    accion = request.GET.get('accion', '')  # Filtrar por acción si se selecciona
    productos = Producto.objects.filter(estado='disponible')  # Solo productos disponibles

    if accion:
        productos = productos.filter(accion=accion)

    return render(request, 'listar_productos.html', {'productos': productos, 'accion': accion})

def realizar_accion(request, producto_id, accion):
    producto = get_object_or_404(Producto, id=producto_id)

    # Verificamos si el producto está disponible
    if producto.estado == "disponible":
        if accion == "donacion":
            producto.estado = "no_disponible"
            messages.success(request, f"Donación aceptada para '{producto.nombre}'.")
        elif accion == "intercambio":
            producto.estado = "no_disponible"
            messages.success(request, f"Intercambio aceptado para '{producto.nombre}'.")
        elif accion == "venta":
            producto.estado = "no_disponible"
            messages.success(request, f"Venta aceptada para '{producto.nombre}'.")
        else:
            messages.error(request, "Acción no válida.")
        
        producto.save()  # Guardamos los cambios en la base de datos
    else:
        messages.error(request, f"El producto '{producto.nombre}' ya no está disponible.")

    return redirect('listar_productos')




def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)  # Esto buscará el producto por su ID
    return render(request, 'detalle_producto.html', {'producto': producto})



def aceptar_donacion(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if producto.estado == "disponible":
        producto.estado = "no_disponible"
        producto.save()
        messages.success(request, f"Has aceptado la donación del producto '{producto.nombre}'.")
    else:
        messages.error(request, f"El producto '{producto.nombre}' ya no está disponible.")
    return redirect('listar_productos')


def aceptar_venta(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if producto.estado == "disponible":
        producto.estado = "no_disponible"
        producto.save()
        messages.success(request, f"Has aceptado la venta del producto '{producto.nombre}'.")
    else:
        messages.error(request, f"El producto '{producto.nombre}' ya no está disponible.")
    return redirect('listar_productos')

def aceptar_intercambio(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if producto.estado == "disponible":
        producto.estado = "no_disponible"
        producto.save()
        messages.success(request, f"Has aceptado el intercambio del producto '{producto.nombre}'.")
    else:
        messages.error(request, f"El producto '{producto.nombre}' ya no está disponible.")
    return redirect('listar_productos')