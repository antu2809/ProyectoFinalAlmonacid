from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.contrib import admin
from django.conf import settings

class CustomUser(AbstractUser):
    edad = models.IntegerField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def _str_(self):
        return self.username
    
class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    image  = models.ImageField(upload_to='profile_images/')
    description = models.TextField()
    website = models.URLField()
    field1 = models.URLField(blank=True, null=True) 
    
    def _str_(self):
        return self.user.username

class Artwork(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    artist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='artwork_images/')
    video = models.URLField(blank=True)
    audio = models.FileField(verbose_name='Archivo de audio', upload_to='audios/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cbu = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True) 
       
class UserMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    message = models.CharField(max_length=255)
    image = models.ImageField(upload_to='messages/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Purchase(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
class SavedArtwork(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

