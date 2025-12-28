from django.conf import settings
from django.db import models

class Reel(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reels"
    )

    video = models.FileField(upload_to="reels/videos/")
    caption = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Reel de {self.author}"
