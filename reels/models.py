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

    @property
    def save_model(self):
        return "reels.Reel"
# interactions/models.py

User = settings.AUTH_USER_MODEL

class SavedReel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Reel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "item")

    def __str__(self):
        return f"{self.user} saved {self.item}"
