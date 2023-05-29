from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings
from io import BytesIO
import base64
from django.db.models import Q
from Proyecto_1.models import Artwork
from django.http import HttpResponseNotFound
from django.urls import reverse
from django.shortcuts import redirect


def search_images(request):
    search = request.GET.get("search")
    if search:
        images = Image.objects.filter(title__icontains=search)
    else:
        images = Image.objects.all()
    return render(request, "search_images.html", {"images": images})


def custom_handler404(request, exception):
    return redirect(reverse("search_images"))


handler404 = custom_handler404


def view_presentacion(request):
    return render(
        request,
        "presentacion.html",
        {
            "gif_name": "iniciogifkai",
            "boton_font": "Orbitron-VariableFont_wght",
            "boton_url": "http://127.0.0.1:8000/combined/",
        },
    )


def show_image(request):
    image_path = settings.STATICFILES_DIRS[0] + "/images/my_image.jpg"
    try:
        # Abre la imagen
        image = Image.open(image_path)
        # Crea un objeto ImageDraw para dibujar en la imagen
        draw = ImageDraw.ImageDraw(image)
        # Define el texto y el estilo de la epígrafe
        artist_name = "Kay"
        artwork_title = "Las Hijas"
        creation_year = "2023"
        additional_info = "la lola en pan bimbo y la mona estirada"
        text = f"{artist_name}\n{creation_year}\n{artwork_title}\n{additional_info}"
        font = ImageFont.truetype(
            "Orbitron-VariableFont_wght", 20
        )  # Puedes cambiar la fuente y el tamaño

        # Calcula la posición del texto en la imagen
        text_width, text_height = draw.textsize(text, font)
        x = 10  # Puedes ajustar la posición horizontal
        y = 10  # Puedes ajustar la posición vertical

        # Dibuja el texto en la imagen
        draw.text((x, y), text, fill="white", font=font)
        # Convierte la imagen a bytes y devuelve la respuesta HTTP
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        return HttpResponse(buffer.getvalue(), content_type="my_image.jpg")
    except IOError:
        return HttpResponse("Error al procesar la imagen")


def current_datetime_view(request):
    now = datetime.now()
    html = "{0}".format(now)
    return HttpResponse(html)


def saludo_view(request):
    style = """
        <style>
            @font-face {
                font-family: 'Orbitron-VariableFont_wght';
                src: url('/static/fonts/Orbitron-VariableFont_wght.ttf') format('truetype');
            }
            body {
                background-color: pink;
                font-family: 'Orbitron-VariableFont_wght', sans-serif;
                color: rgb(15, 7, 8);
                text-shadow: none !important;
            }
        </style>
    """
    emoji = "&#x1F339;"  # Emoji de rosa de HTML Unicode
    return HttpResponse(
        f"{style}<h1> Kai </h1><a href='https://www.instagram.com/kai.orosco/'>Sígueme en Instagram</a>"
    )


def show_gif(request):
    gif_path = os.path.join(settings.STATICFILES_DIRS[0], "images/gifkai.gif")
    with open(gif_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="image/gif")
        response["Content-Disposition"] = 'inline; filename="gifkai.gif"'
        response["Content-Transfer-Encoding"] = "binary"
        response["Cache-Control"] = "no-cache"
        response["X-Sendfile"] = gif_path
        response["Content-Length"] = os.path.getsize(gif_path)
        response.write(
            '<img src="data:image/gif;base64,{}" class="center" style="max-width:100%;">'.format(
                base64.b64encode(f.read()).decode("utf-8")
            )
        )
        return response


def show_gif_presentacion(request):
    gif_path = os.path.join(settings.STATICFILES_DIRS[0], "images/iniciogifkai.gif")
    with open(gif_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="image/gif")
        response["Content-Disposition"] = 'inline; filename="iniciogifkai.gif"'
        response["Content-Transfer-Encoding"] = "binary"
        response["Cache-Control"] = "no-cache"
        response["X-Sendfile"] = gif_path
        response["Content-Length"] = os.path.getsize(gif_path)
        response.write(
            '<img src="data:image/gif;base64,{}" class="center" style="max-width:100%;">'.format(
                base64.b64encode(f.read()).decode("utf-8")
            )
        )
        return response
