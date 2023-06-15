from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Proyecto_1.views import saludo, show_gif, current_datetime, show_image
from Proyecto_1.views import view_presentacion, show_gif_presentacion , combined_view
from Proyecto_1.views import custom_handler404
from .views import tienda, carrito
from .views import about_view, no_pages_view
from Proyecto_1.views import signup_view, create_profile, profile_view, update_profile_view, login_view, logout_view, delete_account_view
from Proyecto_1.views import messages_view, artwork_upload, artwork_detail
from Proyecto_1.views import share_facebook, share_instagram, share_tiktok, copy_link, save_artwork, send_message
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", view_presentacion, name="view_presentacion"),
    path('combined/', combined_view, name='combined'),
    path('about/', about_view, name='about'),
    path('pages/no-pages/', no_pages_view, name='no_pages'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login_view'),
    path('create_profile/', create_profile, name='create_profile'),
    path('profile/', profile_view, name='profile_view'),
    path('delete_account/', delete_account_view, name='delete_account'),
    path('artwork_upload/', artwork_upload, name='artwork_upload'),
    path('artwork/<int:pk>/', artwork_detail, name='artwork_detail'),
    path('artwork/<int:pk>/send-message/', send_message, name='send_message'),
    path('save_artwork/<int:pk>/', save_artwork, name='save_artwork'),
    path('share_facebook/<int:id>/',share_facebook , name='share_facebook'),
    path('share_instagram/<int:id>/', share_instagram, name='share_instagram'),
    path('share_tiktok/<int:id>/', share_tiktok, name='share_tiktok'),
    path('copy_link/<int:id>/', copy_link, name='copy_link'),
    path('profile/update/', update_profile_view, name='update_profile'),
    path('logout/', logout_view, name='logout'),
    path('messages/', messages_view, name='messages'),
    path("show_gif_presentacion/", show_gif_presentacion, name="show_gif_presentacion"),
    path('tienda/', tienda, name='tienda'),
    path('carrito/', carrito, name='carrito'),
    path("show_gif/", show_gif, name="show_gif"),
    path("current_datetime/", current_datetime, name="current_datetime"),
    path("show_image/", show_image, name="show_image"),
    path("saludo/", saludo),
    path("custom_handler404/", custom_handler404, name="custom_handler404")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
