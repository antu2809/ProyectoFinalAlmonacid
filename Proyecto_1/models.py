from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.contrib import admin

class CustomUser(AbstractUser):
    # Campos y métodos adicionales del modelo User
    edad = models.IntegerField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    # Otros campos y métodos de tu modelo

    # Solución al conflicto de accesores inversos
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')
    
class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/')
    description = models.TextField()
    website = models.URLField()
    field1 = models.URLField(blank=True, null=True) 
    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.titulo


class Artwork(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    artist = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='artwork_images/')
    video = models.URLField(blank=True)
    audio = models.FileField(verbose_name='Archivo de audio', upload_to='audios/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cbu = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
class SavedArtwork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    
       
class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    message = models.CharField(max_length=255)
    image = models.ImageField(upload_to='messages/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Purchase(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

