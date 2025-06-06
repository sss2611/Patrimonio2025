from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=False)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    area = models.CharField(max_length=50, choices=[
        ('Historia', 'Historia'),
        ('Bellas Artes', 'Bellas Artes'),
        ('Antropología', 'Antropología'),
        ('Staff', 'Staff')
    ], blank=True, null=True)
    
    admitido = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group', related_name='customuser_groups', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='customuser_permissions', blank=True
    )

    def save(self, *args, **kwargs):
        if self.is_superuser:  # Solo los superusuarios no necesitan área
           self.area = None
           self.is_staff = True 
        elif self.area == "Staff":  
            self.is_staff = True
        else:
            self.is_staff = False #para evitar que cualquier usuario tenga permisos de staff
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre or 'Sin nombre'} {self.apellido or ''} ({self.username})"

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'nombre', 'apellido', 'email', 'password', 'area']

class Noticia(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    portada = models.ImageField(upload_to='noticias_portadas/', null=True, blank=True)

    def __str__(self):
        return self.titulo