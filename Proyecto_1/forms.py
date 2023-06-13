from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente, Artwork, Orden, Page, Profile , Purchase, CustomUser

class ClienteForm(forms.ModelForm):
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'direccion']

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'description', 'image', 'video', 'audio', 'price', 'is_published']


class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['cliente', 'artwork', 'fecha', 'cantidad']
        
class BusquedaForm(forms.Form):
    search_text = forms.CharField(label='Buscar')

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'content']

class ProfileForm(forms.ModelForm):
    field1 = forms.URLField(required=False)
    class Meta:
        model = Profile
        fields = ['user', 'image', 'description', 'website', 'field1']

class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
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
