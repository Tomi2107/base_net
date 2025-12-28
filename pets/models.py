# pets/models.py
from django.conf import settings
from django.db import models


class Pet(models.Model):

    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('lost', 'Perdido'),
        ('dating', 'Busca pareja'),
        ('transit', 'Disponible para tránsito'),
    ]

    SPECIES_CHOICES = [
        ('dog', 'Perro'),
        ('cat', 'Gato'),
    ]

    SIZE_CHOICES = [
        ('small', 'Chico'),
        ('medium', 'Mediano'),
        ('large', 'Grande'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pets'
    )

    name = models.CharField(max_length=50)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=80, blank=True)
    color = models.CharField(max_length=80)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='normal'
    )

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"
