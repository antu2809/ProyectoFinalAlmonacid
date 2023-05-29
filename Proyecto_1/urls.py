"""
URL configuration for Proyecto_1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from Proyecto_1.views import saludo
from Proyecto_1.views import show_gif
from Proyecto_1.views import current_datetime
from Proyecto_1.views import show_image
from .views import combined_view
from django.conf import settings
from django.conf.urls.static import static
from Proyecto_1.views import custom_handler404
from django.urls import path
from Proyecto_1.views import view_presentacion
from .views import show_gif_presentacion
from .views import agregar_cliente
from .views import tienda
from Proyecto_1.views import realizar_compra
from Proyecto_1.views import carrito

# Para acceder a la vista hay que importar el modulo y el método
urlpatterns = [
    path("agregar_cliente/", agregar_cliente, name="agregar_cliente"),
    path("show_gif_presentacion/", show_gif_presentacion, name="show_gif_presentacion"),
    path('tienda/', tienda, name='tienda'),
    path('realizar_compra/', realizar_compra, name='realizar_compra'),
    path('carrito/', carrito, name='carrito'),
    path("view_presentacion/", view_presentacion, name="view_presentacion"),
    path("show_gif/", show_gif, name="show_gif"),
    path("current_datetime/", current_datetime, name="current_datetime"),
    path("show_image/", show_image, name="show_image"),
    path("combined/", combined_view, name="combined"),
    path("admin/", admin.site.urls),
    path("saludo/", saludo),
    path("custom_handler404/", custom_handler404, name="custom_handler404")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler404 = custom_handler404
