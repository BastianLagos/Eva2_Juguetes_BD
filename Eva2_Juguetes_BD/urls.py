"""Eva2_Juguetes_BD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from juguetes import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.mostrarIndex),
    path('index',views.mostrarIndex),
    path('login', views.iniciarSesion),
    path('logout', views.cerrarSesion),

    path('menu_admin',views.mostrarMenuAdmin),
    path('form_origen',views.mostrarFormOrigen),
    path('registrar_origen',views.registrarOrigen),
    path('form_actualizar_origen/<int:id>', views.mostrarFormActualizarOrigen),
    path('actualizar_origen/<int:id>', views.actualizarOrigen),
    path('eliminar_origen/<int:id>', views.eliminarOrigen),

    path('form_tipo',views.mostrarFormTipo),
    path('registrar_tipo',views.registrarTipo),
    path('form_actualizar_tipo/<int:id>', views.mostrarFormActualizarTipo),
    path('actualizar_tipo/<int:id>', views.actualizarTipo),
    path('eliminar_tipo/<int:id>', views.eliminarTipo),

    path('listar_historial', views.mostrarListarHistorial),

    path('menu_operador',views.mostrarMenuOperador),
    path('form_registrar',views.mostrarFormularioRegistro),
    path('listado',views.mostrarListado),
    path('insertar',views.insertarJuguete),
    path('eliminar/<int:id>',views.eliminarJuguete),
    path('form_actualizar/<int:id>',views.mostrarFormularioActualizar),
    path('actualizar/<int:id>',views.actualizarJuguete),
]
