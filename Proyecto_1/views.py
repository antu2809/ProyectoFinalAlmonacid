import base64, datetime, os, requests, social_django, urllib.parse, PIL.Image, random
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.template import loader
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from utils import current_datetime_view, saludo_view, show_image
from django.conf import settings
from io import BytesIO
from django.urls import reverse, include, NoReverseMatch
from django.shortcuts import redirect, get_object_or_404
from django.templatetags.static import static
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from django.db.models import Sum
from django.http import HttpResponseNotFound
from django.http import JsonResponse
from .models import Artwork, CustomUser , Profile, UserMessage, SavedArtwork, Purchase
from .forms import SignupForm, LoginForm, ProfileForm, MessageForm
from .forms import ArtworkForm, BusquedaForm

imagen = PIL.Image.open(r"C:\Users\antua\OneDrive\Escritorio\Tercera-pre-entrega-Almonacid\Proyecto_11\static\images\my_image.jpg")
imagen.show()

def about_view(request):
    data = {
        'title': 'Acerca de mi',
        'description': 'Soy un alumno inicial de Ingenieria en computacion y éste en mi primer proyecto de desarrollo web destinado a la venta de obras de arte de todo tipo',
        'contact_email': 'antu.almonacid@alu.ing.unlp.edu.ar',
    }
    return render(request, 'about.html', data)


def show_gif_presentacion(request):
    gif_path = os.path.join(settings.STATIC_ROOT, "images/lagaleriarosa.gif")
    with open(gif_path, "rb") as f:
        gif_binary = f.read()
        gif_base64 = base64.b64encode(gif_binary).decode("utf-8")
        response = HttpResponse(gif_binary, content_type="image/gif")
        response["Content-Disposition"] = 'inline; filename="lagaleriarosa.gif"'
        response["Content-Transfer-Encoding"] = "binary"
        response["Cache-Control"] = "no-cache"
        response["Content-Length"] = os.path.getsize(gif_path)
        response.write(
            '<img src="data:image/gif;base64,{}{}" class="center" style="max-width:100%;">'.format(
                gif_base64,
                "?cache_bust=" + str(random.randint(1, 10000))  # add cache-busting parameter
            )
        )
        return response



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
    artworks = Artwork.objects.order_by('created_at')
    context = {
        "instagram_info": instagram_info,
        "current_datetime_html": current_datetime_html,
        "show_image_html": show_image_html,
        "saludo_html": saludo_html,
        "gifkai_url": gifkai_url,
        "artworks": artworks, 
        "form" : form,
        "search_results": search_results
    }
    if search_results:
        context["search_results"] = search_results
        
    return render(request, 'combined.html', context) 
    

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
           form.save()
        return redirect('login_view')
    else:
        form = SignupForm()
    context = {'form': form}
    return render(request, 'signup.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirije a create_profile si es su primer inicio de sesion 
                if not hasattr(user, 'profile'):
                    return redirect('create_profile')
                return redirect('profile_view')
            else:
                form.add_error(None, 'Nombre de usuario o contraseña inválida')
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'login.html', context)

@login_required
def create_profile(request):
    if request.method == 'POST':
        user = CustomUser.objects.create(username=request.user.username + '_profile')
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            # Guardar la imagen de perfil en el usuario
            user.profile_image = profile.image
            user.save()

            return redirect('profile_view')
    else:
        form = ProfileForm()
    context = {'form': form}
    return render(request, 'create_profile.html', context)

@login_required
def profile_view(request):
    profile = request.user.profile.first()

    profile_image_url = None
    try:
        if profile.profile_image:  # Verifica si hay un archivo asociado a profile_image
            profile_image_url = profile.profile_image.url
    except AttributeError:
        pass

    context = {
        'profile': profile,
        'profile_image_url': profile_image_url
    }
    return render(request, 'profile.html', context)


@login_required 
def logout_view(request):
    if request.method == 'POST': 
      logout(request) 
      return redirect('login_view') 
    else: 
      return render(request, 'logout.html')

@login_required
def messages_view(request):
    user_messages = UserMessage.objects.filter(user=request.user.id)
    context = {'messages': user_messages}
    return render(request, 'messages.html', context)

@login_required
def send_message(request, pk):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            sender = request.user
            receiver = get_object_or_404(CustomUser, id=pk)
            artwork_id = pk 
            try:
                artwork = Artwork.objects.get(id=artwork_id)
            except Artwork.DoesNotExist:
                return HttpResponse('El Artwork no existe')
            message.sender = sender
            message.receiver = receiver
            message.artwork = artwork
            message.save()
            return redirect('artwork_detail', pk=message.artwork.id)
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form})

@login_required
def artwork_upload(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.user = request.user
            artwork.save()
            return redirect('profile_view')  # Redirigir a la página de perfil después de guardar la obra de arte
    else:
        form = ArtworkForm()
    return render(request, 'artwork_upload.html', {'form': form})

@login_required
@require_POST
def save_artwork(request, pk):
    artwork = Artwork.objects.get(pk=pk)
    user = request.user

    # Crea una nueva instancia de SavedArtwork si el usuario aún no ha guardado la obra de arte
    if not SavedArtwork.objects.filter(user=user, artwork=artwork).exists():
        saved_artwork = SavedArtwork.objects.create(user=user, artwork=artwork)
        return redirect('profile_view')  # Redirigir a la página de perfil después de guardar la obra de arte
    else:
        return HttpResponse('Ya ha guardado esta obra de arte')


purchase = None 
@login_required
def artwork_purchase(request, pk):
    artwork = Artwork.objects.get(pk=pk)

    # La compra solo se puede realizar una vez
    purchase_exists = Purchase.objects.filter(user=request.user, artwork=artwork).exists()
    if purchase_exists:
        return HttpResponse('Ya ha realizado la compra de esta obra de arte')

    # Verificar si el usuario tiene suficiente crédito
    user_profile = request.user.profile
    if user_profile.credit < artwork.price:
        return HttpResponse('Fondos insuficientes para realizar esta compra')

    # Deduct credit from user's account
    user_profile.credit -= artwork.price
    user_profile.save()

    # Crear un objeto de compra y guardar 
    purchase = Purchase(user=request.user, artwork=artwork)
    purchase.save()

    # Redirigir a la página de detalle de la obra de arte
    return redirect('artwork_detai.html', pk=pk)

# Para compartir Facebook
def share_facebook(request, id):
    full_url = request.build_absolute_uri(reverse('artwork_detail', args=[id]))
    urlparams = {'u': full_url}
    redirect_url = 'https://www.facebook.com/sharer/sharer.php?' + urllib.parse.urlencode(urlparams)
    return redirect(redirect_url)

# Para compartir Instagram
def share_instagram(request, id):
    full_url = request.build_absolute_uri(reverse('artwork_detail', args=[id]))
    urlparams = {'text': full_url}
    redirect_url = 'https://www.instagram.com/create/story/' + urllib.parse.urlencode(urlparams)
    return redirect(redirect_url)

# Para compartir TikTok
def share_tiktok(request, id):
    full_url = request.build_absolute_uri(reverse('artwork_detail', args=[id]))
    urlparams = {'u_code': full_url, 'lang': 'en'}
    redirect_url = 'https://www.tiktok.com/upload/?' + urllib.parse.urlencode(urlparams)
    return redirect(redirect_url)

# Copiar la dirección de la publicación
def copy_link(request, id):
    full_url = request.build_absolute_uri(reverse('artwork_detail', args=[id]))
    return HttpResponse('Enlace copiado correctamente')

@login_required
def artwork_detail(request, pk):
    artwork = Artwork.objects.get(pk=pk)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile
            message.receiver = artwork.artist
            message.artwork = artwork
            message.save()
            # Redirigir al usuario a la página de detalle de la obra de arte con un mensaje de confirmación
            return redirect('artwork_detail', pk=pk)

    else:
        form = MessageForm(initial={'receiver': artwork.artist.id})

    # Renderizar la plantilla con los datos necesarios
    context = {'artwork': artwork, 'form': form}
    return render(request, 'artwork_detail.html', context)

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

def delete_account_view(request):
           if request.method == 'POST':
               # Verificar si la contraseña ingresada es correcta
               current_password = request.POST.get('current_password')
               user = authenticate(username=request.user.username,
                                   password=current_password)

               if user is not None:
                   # Eliminar la cuenta del usuario actual
                   CustomUser.objects.get(username=request.user.username).delete()
                   return redirect('login')
               else:
                   # Mostrar un mensaje de error si la contraseña es incorrecta
                   return render(request, 'delete_account.html',
                                 {'error_message': 'Invalid password!'})

           else:
               return render(request, 'delete_account.html') #Mostrar la página de confirmación

def no_pages_view(request):
    error_message = "Lo sentimos, la página que buscas no existe."
    data = {
        'message': error_message,
        'support_email': 'antu.almonacid@alu.ing.unlp.edu.ar',
    }
    return render(request, 'no_pages.html', data)

def search_view(request):
    if request.method == 'GET':
        # Obtener el término de búsqueda ingresado por el cliente
        search_term = request.GET.get('q', '')
        
        # Realizar la lógica de búsqueda aquí
        
        # Devolver los resultados de búsqueda a la plantilla correspondiente
        return render(request, 'search_results.html', {'search_term': search_term})

def tienda(request):
    artworks = Artwork.objects.all()
    return render(request, "tienda.html", {"artworks": artworks})

def carrito(request):
    return render(request, 'carrito.html')

def custom_handler404(request, exception):
    return redirect(reverse("search_images"))


handler404 = custom_handler404

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
    saludo_html = "<h1>KAI</h1>"
    return HttpResponse(style + saludo_html)

   
def show_gif(request):
    gif_path = os.path.join(settings.STATICFILES_DIRS[0], "images/gifkai.gif")
    return HttpResponse(open(gif_path, 'rb').read(), content_type='image/gif')