from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Proyecto_1.views import saludo
from Proyecto_1.views import show_gif
from Proyecto_1.views import current_datetime
from .views import show_image
from .views import combined_view
from Proyecto_1.views import custom_handler404
from Proyecto_1.views import view_presentacion
from .views import show_gif_presentacion
from .views import agregar_cliente
from .views import tienda
from Proyecto_1.views import realizar_compra
from Proyecto_1.views import carrito
from .views import about_view
from Proyecto_1.views import blog_list_view
from Proyecto_1.views import page_detail_view
from Proyecto_1.views import no_pages_view
from Proyecto_1.views import create_page_view
from Proyecto_1.views import edit_page_view
from Proyecto_1.views import delete_page_view
from Proyecto_1.views import profile_view
from Proyecto_1.views import update_profile_view
from Proyecto_1.views import signup_view
from Proyecto_1.views import login_view
from Proyecto_1.views import logout_view
from Proyecto_1.views import messages_view
from Proyecto_1.views import add_artwork


urlpatterns = [
    path('combined/', combined_view, name='combined'),
    path('about/', about_view, name='about'),
    path('pages/', blog_list_view, name='blog_list'),
    path('pages/<pageId>/', page_detail_view, name='page_detail'),
    path('pages/no-pages/', no_pages_view, name='no_pages'),
    path('pages/create/', create_page_view, name='create_page'),
    path('pages/<pageId>/edit/', edit_page_view, name='edit_page'),
    path('pages/<pageId>/delete/', delete_page_view, name='delete_page'),
    path('accounts/', include('Proyecto_11.urls')),
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/profile/', profile_view, name='profile'),
    path('add_artwork/', add_artwork, name='add_artwork'),
    path('accounts/profile/update/', update_profile_view, name='update_profile'),
    path('accounts/logout/', logout_view, name='logout'),
    path('messages/', messages_view, name='messages'),
    path("agregar_cliente/", agregar_cliente, name="agregar_cliente"),
    path("show_gif_presentacion/", show_gif_presentacion, name="show_gif_presentacion"),
    path('tienda/', tienda, name='tienda'),
    path('realizar_compra/', realizar_compra, name='realizar_compra'),
    path('carrito/', carrito, name='carrito'),
    path("view_presentacion/", view_presentacion, name="view_presentacion"),
    path("show_gif/", show_gif, name="show_gif"),
    path("current_datetime/", current_datetime, name="current_datetime"),
    path("show_image/", show_image, name="show_image"),
    path("admin/", admin.site.urls),
    path("saludo/", saludo),
    path("custom_handler404/", custom_handler404, name="custom_handler404")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
