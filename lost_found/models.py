from django.conf import settings
from django.db import models


class LostFoundPost(models.Model):

    STATUS_CHOICES = [
        ("lost", "Perdido"),
        ("found", "Encontrado"),
    ]

    ANIMAL_CHOICES = [
        ("dog", "Perro"),
        ("cat", "Gato"),
        ("bird", "Pájaro"),
        ("other", "Otro"),
    ]

    SIZE_CHOICES = [
        ("xs", "Muy chico"),
        ("s", "Chico"),
        ("m", "Mediano"),
        ("l", "Grande"),
        ("xl", "Muy grande"),
    ]

    PATTERN_CHOICES = [
        ("liso", "Liso"),
        ("manchas", "Manchas"),
        ("rayas", "Rayas"),
    ]
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lost_found_posts"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    animal_type = models.CharField(
        max_length=20,
        choices=ANIMAL_CHOICES
    )

    animal_other = models.CharField(
        max_length=50,
        blank=True
    )

    size = models.CharField(
        max_length=5,
        choices=SIZE_CHOICES
    )

    color = models.CharField(
        max_length=50
    )

    pattern = models.CharField(
        max_length=20,
        choices=PATTERN_CHOICES,
        default="liso"
    )

    place = models.CharField(
        max_length=100
    )

    description = models.TextField()

    created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.get_status_display()} · {self.get_animal_type_display()}"

    @property
    def save_model(self):
        return "lost_found.LostFoundPost"

class LostFoundImage(models.Model):

    post = models.ForeignKey(
        LostFoundPost,
        related_name="images",
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to="lost_found/"
    )

    def __str__(self):
        return f"Imagen de post #{self.post.id}"

