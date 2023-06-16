from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import  Artwork, Profile , Purchase, CustomUser, UserMessage

class ArtworkForm(forms.ModelForm):
    audio = forms.FileField(required=False)
    cbu = forms.CharField(label='CBU', max_length=50, required=True)
    class Meta:
        model = Artwork
        fields = ['title', 'description', 'image', 'video', 'audio', 'price', 'cbu']
        
class BusquedaForm(forms.Form):
    search_text = forms.CharField(label='Buscar')

class ProfileForm(forms.ModelForm):
    website2 = forms.URLField(required=False)
    class Meta:
        model = Profile
        fields = ['image', 'description', 'website', 'website2']

class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        
class LoginForm(forms.ModelForm): 
    
    class Meta: 
        model = CustomUser 
        fields = ['username', 'password']
        
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['quantity']
    
class ContactForm(forms.Form):
    name = forms.CharField(label='Nombre', max_length=100)
    email = forms.EmailField(label='Correo electrónico', max_length=150)
    message = forms.CharField(label='Mensaje', widget=forms.Textarea)

class MessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ['name', 'email', 'message', 'image']