# Generated by Django 5.1.3 on 2024-11-27 05:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=10, unique=True)),
                ('nombres_y_apellidos', models.CharField(max_length=255)),
                ('nombre_usuario', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('contrasena', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.catalogo')),
            ],
        ),
        migrations.CreateModel(
            name='ImagenProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_imagen', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='apps.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Intercambio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='pendiente', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.producto')),
                ('ofrecido_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intercambios_ofrecidos', to='apps.usuario')),
                ('solicitado_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intercambios_solicitados', to='apps.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio_final', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comprador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compras', to='apps.usuario')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.producto')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ventas', to='apps.usuario')),
            ],
        ),
    ]
