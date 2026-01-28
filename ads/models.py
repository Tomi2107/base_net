from django.db import models
from django.conf import settings
from django.utils import timezone

class Zone(models.Model):
    name = models.CharField(max_length=100)  # CABA, Zona Norte
    province = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.province})"

class Ad(models.Model):
    FEED = "feed"
    SIDEBAR = "sidebar"

    AD_TYPE_CHOICES = [
        (FEED, "Feed (posteo)"),
        (SIDEBAR, "Sidebar"),
    ]

    advertiser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ads"
    )

    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="ads/", blank=True, null=True)
    link = models.URLField(blank=True)

    ad_type = models.CharField(
        max_length=20,
        choices=AD_TYPE_CHOICES,
        default="feed"
    )

    zones = models.ManyToManyField(Zone, blank=True)

    approved = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    views = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_active(self):
        today = timezone.now().date()
        return (
            self.active
            and self.approved
            and self.start_date <= today <= self.end_date
        )

    def __str__(self):
        return self.title
    



