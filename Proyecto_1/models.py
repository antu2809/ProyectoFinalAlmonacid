from django.db import models

class Artwork(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="my_image")
    description = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.BigAutoField(primary_key=True)

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
        self.total = self.artwork.price * self.cantidad  # Utiliza el campo "price" para calcular el total
        super().save(*args, **kwargs)

