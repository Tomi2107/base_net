from django.conf import settings
from django.db import models

class Group(models.Model):

    PRIVACY_CHOICES = (
        ("public", "Público"),
        ("private", "Privado"),
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_groups"
    )

    name = models.CharField(max_length=120)
    description = models.TextField()
    location = models.CharField(max_length=100)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES)
    image = models.ImageField(upload_to="groups/images/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def save_model(self):
        return "groups.Group"