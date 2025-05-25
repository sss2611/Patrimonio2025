from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=False)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    area = models.CharField(max_length=50, choices=[
        ('Historia', 'Historia'),
        ('Bellas Artes', 'Bellas Artes'),
        ('Antropología', 'Antropología')
    ], blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group', related_name='customuser_groups', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='customuser_permissions', blank=True
    )

    def save(self, *args, **kwargs):
        if self.is_superuser or self.is_staff and self.area is not None:
            self.area = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre or 'Sin nombre'} {self.apellido or ''} ({self.username})"
