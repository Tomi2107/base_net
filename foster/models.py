from django.conf import settings
from django.db import models


class FosterAvailability(models.Model):

    ANIMAL_CHOICES = [
        ("dog", "Perro"),
        ("cat", "Gato"),
        ("other", "Otro"),
    ]

    HEALTH_CHOICES = [
        ("healthy", "Sano"),
        ("injured", "Herido"),
        ("sick", "Enfermo"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="foster_availability"
    )

    is_active = models.BooleanField(default=False)

    is_adult = models.BooleanField(
        verbose_name="Soy mayor de 18 años"
    )

    animal_type = models.CharField(
        max_length=20,
        choices=ANIMAL_CHOICES
    )

    animal_other = models.CharField(
        max_length=50,
        blank=True
    )

    health_condition = models.CharField(
        max_length=20,
        choices=HEALTH_CHOICES
    )

    notes = models.TextField(
        blank=True,
        help_text="Espacio disponible, experiencia, condiciones, etc."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} · Tránsito"
