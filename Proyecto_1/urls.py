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
from Proyecto_1.views import no_pages_view
from Proyecto_1.views import profile_view
from Proyecto_1.views import update_profile_view
from Proyecto_1.views import signup_view
from Proyecto_1.views import login_view
from Proyecto_1.views import logout_view
from Proyecto_1.views import messages_view
from Proyecto_1.views import artwork_upload
from Proyecto_1.views import share_facebook
from Proyecto_1.views import share_instagram
from Proyecto_1.views import share_tiktok
from Proyecto_1.views import copy_link
from Proyecto_1.views import delete_account_view


urlpatterns = [
    path("view_presentacion/", view_presentacion, name="view_presentacion"),
    path('combined/', combined_view, name='combined'),
    path('about/', about_view, name='about'),
    path('pages/', blog_list_view, name='blog_list'),
    path('pages/no-pages/', no_pages_view, name='no_pages'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login_view'),
    path('profile/', profile_view, name='profile_view'),
    path('delete_account/', delete_account_view, name='delete_account'),
    path('artwork_upload/', artwork_upload, name='artwork_upload'),
    path('share/facebook/<int:id>/',share_facebook , name='share-facebook'),
    path('share/instagram/<int:id>/', share_instagram, name='share-instagram'),
    path('share/tiktok/<int:id>/', share_tiktok, name='share-tiktok'),
    path('copy-link/<int:id>/', copy_link, name='copy-link'),
    path('profile/update/', update_profile_view, name='update_profile'),
    path('logout/', logout_view, name='logout'),
    path('messages/', messages_view, name='messages'),
    path("agregar_cliente/", agregar_cliente, name="agregar_cliente"),
    path("show_gif_presentacion/", show_gif_presentacion, name="show_gif_presentacion"),
    path('tienda/', tienda, name='tienda'),
    path('realizar_compra/', realizar_compra, name='realizar_compra'),
    path('carrito/', carrito, name='carrito'),
    path("show_gif/", show_gif, name="show_gif"),
    path("current_datetime/", current_datetime, name="current_datetime"),
    path("show_image/", show_image, name="show_image"),
    path("admin/", admin.site.urls),
    path("saludo/", saludo),
    path("custom_handler404/", custom_handler404, name="custom_handler404")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
