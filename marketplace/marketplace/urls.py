"""
URL configuration for marketplace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.views import index, login_view, register_view, logout_view, page_view,  subir_producto, aceptar_venta, listar_productos, detalle_producto, realizar_accion, aceptar_donacion, aceptar_intercambio
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),  
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('page/', page_view, name='page'), 
    path('subir-producto/',subir_producto, name='subir_producto'),
    path('listar_productos/', listar_productos, name='listar_productos'),
    path('aceptar_donacion/<int:producto_id>/', aceptar_donacion, name='aceptar_donacion'),
    path('aceptar_intercambio/<int:producto_id>/',aceptar_intercambio, name='aceptar_intercambio'),
    path('listar_productos/', listar_productos, name='listar_productos'),
    path('realizar_accion/<int:producto_id>/<str:accion>/', realizar_accion, name='realizar_accion'),
    path('producto/<int:producto_id>/', detalle_producto, name='detalle_producto'),
    path('aceptar_venta/<int:producto_id>/', aceptar_venta, name='aceptar_venta'),


    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

