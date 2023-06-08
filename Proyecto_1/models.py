from django.db import models
from django.contrib.auth.models import User
import django.apps
from django.conf import settings
from importlib import import_module
import sys
model_name = "MiModelo"

if model_name not in django.apps.apps.all_models["Proyecto_11"]:
    module_name = f"{settings.BASE_DIR}.models"
    import_module(module_name)
    module = sys.modules[module_name]
    module.register()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/')
    description = models.TextField()
    website = models.URLField()
    # Agrega los campos que necesites para la clase Profile
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField()
    field3 = models.BooleanField(default=False)

class Artwork(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    artist = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='artworks/', blank=True)
    video = models.URLField(blank=True)
    audio = models.FileField(upload_to='audios/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)

class Orden(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    fecha = models.DateField()
    cantidad = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total = self.artwork.price * self.cantidad  
        super().save(*args, **kwargs)

class Blog(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    image = models.ImageField(upload_to='blog_images/')

class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # Agrega los campos que necesites para la clase Page
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField()
    field3 = models.BooleanField(default=False)
    
    
class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title

class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)  

class Purchase(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)