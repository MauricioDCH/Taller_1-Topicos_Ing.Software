"""
#############################################################
## ANTES DE NORMALIZAR EL MODELO DE USUARIO
#############################################################

from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    weight = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    restrictions = models.JSONField()

    def __str__(self):
        return self

#############################################################
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Modelo de Restricción
class Restriction(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Restriction Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Restriction"
        verbose_name_plural = "Restrictions"

# Modelo de Usuario Personalizado
class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)], 
        verbose_name="Age"
    )
    weight = models.FloatField(blank=True, null=True, verbose_name="Weight (kg)")
    height = models.FloatField(blank=True, null=True, verbose_name="Height (cm)")
    restrictions = models.ManyToManyField(Restriction, blank=True, verbose_name="Dietary Restrictions")

    # Resolver el conflicto agregando `related_name`
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Cambia el reverse accessor para evitar el conflicto
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Cambia el reverse accessor para evitar el conflicto
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
