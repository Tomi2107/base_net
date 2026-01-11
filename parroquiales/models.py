from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ParroquialPost(models.Model):

    SERVICE_CHOICES = [
        ("vet", "Veterinaria"),
        ("grooming", "Peluquería"),
        ("walker", "Paseadores"),
        ("discounts", "Descuentos"),
        ("food", "Alimentos"),
        ("clinics", "Clínicas"),
    ]

    title = models.CharField(max_length=120)
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    zone = models.CharField(max_length=120)
    content = models.TextField()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="parroquial_posts"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.zone}"

    @property
    def save_model(self):
        return "parroquiales.ParroquialPost"