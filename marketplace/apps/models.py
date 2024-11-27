from django.db import models

# Create your models here.


class Catalogo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    cedula = models.CharField(max_length=10, unique=True)
    nombres_y_apellidos = models.CharField(max_length=255)
    nombre_usuario = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=75)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_usuario

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.ForeignKey(Catalogo, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    url_imagen = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    comprador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='compras')
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ventas')
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class Intercambio(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    solicitado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='intercambios_solicitados')
    ofrecido_por = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='intercambios_ofrecidos')
    status = models.CharField(max_length=50, default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)
