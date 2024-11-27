from django.db import models

# Create your models here.
# marketplace/models.py
from django.db import models

class Catalogo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

class Usuario(models.Model):
    cedula = models.CharField(max_length=10, unique=True)
    nombres_y_apellidos = models.CharField(max_length=255)
    nombre_usuario = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.ForeignKey(Catalogo, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    url_imagen = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Intercambio(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    solicitado_por = models.ForeignKey(Usuario, related_name='solicitado_por', on_delete=models.CASCADE)
    ofrecido_por = models.ForeignKey(Usuario, related_name='ofrecido_por', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    comprador = models.ForeignKey(Usuario, related_name='comprador', on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Usuario, related_name='vendedor', on_delete=models.CASCADE)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
