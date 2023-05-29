from django import forms
from .models import Cliente, Artwork, Orden

class ClienteForm(forms.ModelForm):
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'direccion']

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'image', 'description', 'precio']

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['cliente', 'artwork', 'fecha', 'cantidad']
        
class BusquedaForm(forms.Form):
    search_text = forms.CharField(label='Buscar')

