# Generated by Django 5.1.3 on 2024-12-02 02:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_remove_producto_imagen_url_producto_imagen'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='producto',
            options={'verbose_name': 'Producto', 'verbose_name_plural': 'Productos'},
        ),
        migrations.AddField(
            model_name='producto',
            name='fecha_publicacion',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de Publicación'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='accion',
            field=models.CharField(choices=[('venta', 'Venta'), ('intercambio', 'Intercambio'), ('donacion', 'Donación')], max_length=20, verbose_name='Acción'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='categoria',
            field=models.CharField(choices=[('ropa', 'Ropa'), ('tecnologia', 'Tecnología'), ('libros', 'Libros'), ('muebles', 'Muebles')], max_length=20, verbose_name='Categoría'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.TextField(verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='productos/', verbose_name='Imagen del Producto'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(max_length=100, verbose_name='Nombre del Producto'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precio'),
        ),
    ]
