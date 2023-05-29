import base64
import datetime
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.template import loader
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from utils import current_datetime_view, saludo_view, show_image
from django.conf import settings
from io import BytesIO
import os
from django.urls import reverse
from django.shortcuts import redirect
from django.templatetags.static import static
from django.db.models import Q
from django.http import HttpResponseNotFound
import PIL.Image
from .models import Artwork
from .models import Cliente
from .models import Orden
from .forms import ClienteForm
from .forms import BusquedaForm

imagen = PIL.Image.open(r"C:\Users\antua\OneDrive\Escritorio\coderhouse.2023\Proyecto.1\static\images\my_image.jpg")
imagen.show()

def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('combined') 
    else:
        form = ClienteForm()
    
    context = {'form': form}
    return render(request, 'combined.html', context)  


def tienda(request):
    artworks = Artwork.objects.all()
    return render(request, "tienda.html", {"artworks": artworks})


def realizar_compra(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        artwork_id = request.POST.get('artwork_id')
        cantidad = int(request.POST.get('cantidad'))

        # Obtener la obra de arte
        artwork = Artwork.objects.get(id=artwork_id)

        # Realizar el cálculo del total
        precio = artwork.precio
        total = precio * cantidad

        # Aquí puedes realizar las operaciones necesarias con los datos de la compra

        # Crear una nueva instancia de Orden
        orden = Orden(
            artwork=artwork,
            cantidad=cantidad,
            total=total
        )
        orden.save()  # Guardar la orden en la base de datos

        # Redireccionar a una página de confirmación o a otra vista
        return redirect('confirmacion_compra')

    # Si es un método GET, simplemente renderizar la plantilla "realizar_compra.html"
    return render(request, "realizar_compra.html")
    # Redireccionar a la página de carrito
    return redirect('carrito')


def carrito(request):
    return render(request, 'carrito.html')

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
            "boton_color": "rgb(15, 7, 8)",
            "boton_url": "http://127.0.0.1:8000/combined/",
        },
    )


def get_instagram_info(request):
    url = "https://www.instagram.com/kai.orosco/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # Obtener información del perfil
    profile_info = soup.find("meta", property="og:description")["content"]
    return profile_info
    


def current_datetime(request):
    now = datetime.datetime.now()
    html = f"style='font-family: Orbitron-VariableFont_wght, sans-serif;'>Fecha y hora actual: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    return HttpResponse(html)


def show_image(request):
    image_path = os.path.join(settings.STATICFILES_DIRS[0], "images/my_image.jpg")
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
            os.path.join(
                settings.STATICFILES_DIRS[0], "fonts/Orbitron-VariableFont_wght.ttf"
            ),
            20,
        )
        text_width, text_height = draw.textsize(text, font)
        x = 10  
        y = 10  

        # Dibuja el texto en la imagen
        draw.text((x, y), text, fill="white", font=font)
        # Obtiene las dimensiones de la imagen
        width, height = image.size

        # Ajusta el tamaño de la imagen para que no cubra toda la pantalla
        if width > 1200 or height > 800:
            ratio = min(300 / width, 200 / height)
            width = int(width * ratio)
            height = int(height * ratio)
            image = image.resize((width, height), Image.ANTIALIAS)

        # Convierte la imagen a base64 para mostrarla en el navegador
        # Convierte la imagen a bytes y devuelve la respuesta HTTP
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        return HttpResponse(buffer.getvalue(), content_type="my_image/jpeg")
    except Exception as e:
        print(e)
        return HttpResponse("Error al mostrar la imagen")


def saludo(request):
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
    saludo_texto = "KAI"
    return saludo_texto
   


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


def combined_view(request):
    search_results = None

    if request.method == 'POST':
        form = BusquedaForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            # Realiza la búsqueda en la base de datos usando el valor de search_text
            search_results = Artwork.objects.filter(title__icontains=search_text)

    else:
        form = BusquedaForm()
    instagram_info = get_instagram_info(request)
    current_datetime_html = current_datetime_view(request).content.decode()
    show_image_html = show_image(request).content
    saludo_html = saludo(request)
    gifkai_url = static("gifkai.gif")
    template = loader.get_template("combined.html")
    context = {
        "instagram_info": instagram_info,
        "current_datetime_html": current_datetime_html,
        "show_image_html": show_image_html,
        "saludo_html": saludo_html,
        "gifkai_url": gifkai_url,
    }
    if search_results:
        context["search_results"] = search_results

    context = {
        'form': form,
        'search_results': search_results
    }
    
    return render(request, 'combined.html', {'saludo_html': saludo_html})
    
