from django.conf import settings
from django.db import models

class StoreItem(models.Model):

    ITEM_TYPE_CHOICES = (
        ("product", "Producto"),
        ("service", "Servicio"),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="store_items"
    )

    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="store/items/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def save_model(self):
        return "storeitem"

    def __str__(self):
        return self.title
