import base64
import datetime
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.template import loader
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from utils import current_datetime_view, saludo_view, show_image
from django.conf import settings
from io import BytesIO
import os
from django.urls import reverse
from django.urls import include
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.http import JsonResponse
import PIL.Image
from .models import Artwork
from .models import Cliente
from .models import Orden
from .models import Page
from .models import Profile
from .models import Blog
from .models import UserMessage
from .forms import ClienteForm
from .forms import BusquedaForm
from .forms import PageForm
from .forms import ProfileForm
from .forms import SignupForm
from .forms import LoginForm
from .forms import ArtworkForm
from .forms import ContactForm

imagen = PIL.Image.open(r"C:\Users\antua\OneDrive\Escritorio\Tercera-pre-entrega-Almonacid\Proyecto.1\static\images\my_image.jpg")
imagen.show()

def about_view(request):
    data = {
        'title': 'Acerca de mi',
        'description': 'Soy un alumno inicial de Ingenieria en computacion y éste en mi primer proyecto de desarrollo web destinado a la venta de obras de arte de todo tipo',
        'contact_email': 'antu.almonacid@alu.ing.unlp.edu.ar',
    }
    return render(request, 'about.html', data)

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts/login/')
    else:
        form = SignupForm()
    context = {'form': form}
    return render(request, 'signup.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Authenticate the user and redirect to the user profile
            username = form.cleaned_data.get('username')
            request.session['username'] = username # Storing username in session for demonstration purposes
            return redirect('accounts:profile')

    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'login.html', context)

def profile_view(request):
    if 'username' not in request.session:
        return redirect('login') # Redirect to login if username not present in session
    username = request.session['username']
    profile = get_object_or_404(Profile, user__username=username)
    artworks = Artwork.objects.filter(artist=profile)
    context = {'profile': profile, 'artworks': artworks}
    return render(request, 'profile.html', context)

def logout_view(request):
    # Cerrar la sesión del usuario y redirigir a la página de inicio de sesión
    return redirect('login')

def messages_view(request):
    # Obtener los mensajes del usuario y mostrarlos en la plantilla
    user_messages = UserMessage.objects.filter(user=request.user.id)
    context = {'messages': user_messages}
    return render(request, 'messages.html', context)


def home_view(request):
    # Lógica para procesar la solicitud de la vista home
    
    # Obtener los clientes desde la base de datos
    clientes = Cliente.objects.all()
    
    # Obtener los datos necesarios para mostrar en la vista
    nombres_clientes = [cliente.nombre for cliente in clientes]
    total_clientes = len(clientes)
    
    # Crear el contexto con los datos para pasar a la plantilla
    context = {
        'nombres_clientes': nombres_clientes,
        'total_clientes': total_clientes
    }
    
    return render(request, 'home.html', context)



def upload_artwork_view(request):
    form = ArtworkForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        artwork = form.save(commit=False)
        artwork.artist = request.user.profile
        artwork.save()
        messages.success(request, '¡Obra de arte creada con éxito!')
        return redirect('profile')
    context = {'form': form}
    return render(request, 'upload_artwork.html', context)


def update_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    context = {'form': form}
    return render(request, 'update_profile.html', context)

def add_artwork(request):
    if request.method == 'POST':
        artwork = Artwork(owner=request.user)
        artwork.title = request.POST.get('title')
        artwork.description = request.POST.get('description')
        artwork.price = request.POST.get('price')
        artwork.image = request.FILES.get('image')
        artwork.save()
        return redirect('profile')
    else:
        return render(request, 'add_artwork.html')

@require_POST
def like_artwork(request):
    artwork_id = request.POST.get('artwork_id')
    artwork = Artwork.objects.get(id=artwork_id)
    artwork.likes += 1
    artwork.save()
    return JsonResponse({'likes': artwork.likes})

@require_POST
def buy_artwork(request):
    artwork_id = request.POST.get('artwork_id')
    artwork = Artwork


def blog_list_view(request):
    blogs = Blog.objects.all()
    formatted_blogs = []
    for blog in blogs:
        formatted_blogs.append({
            'title': blog.title,
            'author': blog.author.name,
            'content': blog.content[:100] + '...',
        })
    
    data = {
        'blogs': formatted_blogs,
        'page_title': 'Lista de blogs',
    }
    return render(request, 'blog_list.html', data)

def no_pages_view(request):
    error_message = "Lo sentimos, la página que buscas no existe."
    data = {
        'message': error_message,
        'support_email': 'antu.almonacid@alu.ing.unlp.edu.ar',
    }
    return render(request, 'no_pages.html', data)


def page_detail_view(request, pageId):
    pageId = 0  
    page = get_object_or_404(Page, id=pageId)
    context = {'page': page}
    return render(request, 'page_detail.html', context)

def create_page_view(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = PageForm()
    context = {'form': form}
    return render(request, 'create_page.html', context)

def edit_page_view(request, pageId):
    page = get_object_or_404(Page, id=pageId)
    if request.method == 'POST':
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            return redirect('page_detail', pageId=page.id)
    else:
        form = PageForm(instance=page)
    context = {'form': form, 'page': page}
    return render(request, 'edit_page.html', context)

def delete_page_view(request, pageId):
    page = get_object_or_404(Page, id=pageId)
    if request.method == 'POST':
        page.delete()
        return redirect('blog_list')
    context = {'page': page}
    return render(request, 'delete_page.html', context)


def generate_image(request):
    if request.method == 'POST' and request.FILES['image']:
        # Obtener el archivo de imagen cargado por el cliente
        uploaded_image = request.FILES['image']
        
        # Abrir la imagen utilizando PIL
        image = Image.open(uploaded_image)
        
        # Guardar la imagen en un archivo temporal
        image_path = 'temp_image.png'
        image.save(image_path)
        
        # Devolver la ruta de la imagen cargada
        return image_path
    
    # Si no se cargó ninguna imagen, se puede mostrar un mensaje de error o redirigir a otra página
    return "No se ha cargado ninguna imagen."

def search_view(request):
    if request.method == 'GET':
        # Obtener el término de búsqueda ingresado por el cliente
        search_term = request.GET.get('q', '')
        
        # Realizar la lógica de búsqueda aquí
        
        # Devolver los resultados de búsqueda a la plantilla correspondiente
        return render(request, 'search_results.html', {'search_term': search_term})


def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('carrito') 
    else:
        form = ClienteForm()
    
    context = {
        'form': form,
        'saludo_html': saludo(request),
        'about_html': about_view(request).content.decode(),
        'blog_list_html': blog_list_view(request).content.decode(),
        'no_pages_html': no_pages_view(request).content.decode(),
        'page_detail_html': page_detail_view(request, pageId=1).content.decode(),
        'create_page_html': create_page_view(request).content.decode(),
        'edit_page_html': edit_page_view(request, pageId=1).content.decode(),
        'delete_page_html': delete_page_view(request, pageId=1).content.decode(),
        'profile_html': profile_view(request).content.decode(),
        'update_profile_html': update_profile_view(request).content.decode(),
        'signup_html': signup_view(request).content.decode(),
        'login_html': login_view(request).content.decode(),
        'logout_html': logout_view(request).content.decode(),
        'home_html': home_view(request).content.decode(),
        'generate_image_html': generate_image(request).content.decode(),
        'search_html': search_view(request).content.decode(),
        # Agrega las demás vistas adicionales aquí
    }
    
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
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            profile_info = soup.find("meta", property="og:description")["content"]
            return profile_info
    except RequestException as err:
        print("Error de conexión:", err)
    return None
    


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
    return HttpResponse(saludo_texto)
   


def show_gif(request):
    gif_path = os.path.join(settings.STATICFILES_DIRS[0], "images/gifkai.gif")
    return HttpResponse(open(gif_path, 'rb').read(), content_type='image/gif')


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
