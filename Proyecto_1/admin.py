from django.contrib import admin 
from .models import CustomUser, Post, Profile, Artwork, SavedArtwork, UserMessage, Purchase

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'edad', 'direccion']
    list_filter = ['is_staff', 'is_superuser']
    search_fields = ['username', 'email']

admin.site.register(CustomUser, CustomUserAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'user', 'fecha_creacion']
    list_filter = ['user']
    search_fields = ['titulo', 'contenido']

admin.site.register(Post, PostAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'description', 'website']
    search_fields = ['user__username']

admin.site.register(Profile, ProfileAdmin)

class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'cbu')
    list_filter = ('cbu',)
    search_fields = ('title', 'description', 'cbu')

admin.site.register(Artwork, ArtworkAdmin)

class SavedArtworkAdmin(admin.ModelAdmin):
    list_display = ['user', 'artwork', 'saved_at']
    list_filter = ['user', 'artwork']
    search_fields = ['user__username']

admin.site.register(SavedArtwork, SavedArtworkAdmin)

class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'created_at']
    list_filter = ['user']
    search_fields = ['user__username', 'message']

admin.site.register(UserMessage, UserMessageAdmin)

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['artwork', 'buyer', 'quantity', 'total_price', 'created_at']
    list_filter = ['artwork', 'buyer']
    search_fields = ['artwork__title', 'buyer__username']

admin.site.register(Purchase, PurchaseAdmin)