from django.db import models

from django.contrib.auth.models import User
from django.utils.timezone import now


class Producto(models.Model):
    CATEGORIAS = [
        ('ropa', 'Ropa'),
        ('tecnologia', 'Tecnología'),
        ('libros', 'Libros'),
        ('muebles', 'Muebles'),
    ]

    ACCIONES = [
        ('venta', 'Venta'),
        ('intercambio', 'Intercambio'),
        ('donacion', 'Donación'),
    ]

    ESTADOS = [
        ('disponible', 'Disponible'),
        ('no_disponible', 'No disponible'),
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio")
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, verbose_name="Categoría")
    accion = models.CharField(max_length=20, choices=ACCIONES, verbose_name="Acción")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible', verbose_name="Estado")
    imagen = models.ImageField(upload_to="static/media/productos/", null=True, blank=True, verbose_name="Imagen del Producto")
    fecha_publicacion = models.DateTimeField(default=now, verbose_name="Fecha de Publicación")

    def __str__(self):
        return f"{self.nombre} - {self.get_categoria_display()} - {self.get_accion_display()}"

    def es_disponible(self):
        return self.estado == 'disponible'
class Transaccion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=20, choices=[('venta', 'Venta'), ('intercambio', 'Intercambio'), ('donacion', 'Donación')])
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario} - {self.producto} - {self.accion}'



# Tabla de usuarios
class Usuario(models.Model):
    cedula = models.CharField(max_length=10, unique=True)
    nombres_y_apellidos = models.CharField(max_length=255)
    nombre_usuario = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.nombre_usuario


# Tabla para registrar intercambios
class Intercambio(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    solicitado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='intercambios_solicitados')
    ofrecido_por = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='intercambios_ofrecidos')
    status = models.CharField(max_length=50, default='pendiente')
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Intercambio: {self.producto.nombre} ({self.status})"


# Tabla para registrar ventas
class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    comprador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='compras')
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ventas')
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Venta: {self.producto.nombre} (${self.precio_final})"


# Tabla para registrar donaciones
class Donacion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    donado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='donaciones_hechas')
    recibido_por = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='donaciones_recibidas')
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Donación: {self.producto.nombre} (de {self.donado_por.nombre_usuario} a {self.recibido_por.nombre_usuario})"
