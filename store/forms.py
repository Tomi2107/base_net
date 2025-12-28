from django import forms
from .models import StoreItem

class StoreItemForm(forms.ModelForm):

    class Meta:
        model = StoreItem
        fields = [
            "title",
            "description",
            "price",
            "item_type",
            "location",
            "image",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Título del producto o servicio",
            }),
            "description": forms.Textarea(attrs={
                "class": "input",
                "rows": 3,
                "placeholder": "Descripción",
            }),
            "price": forms.NumberInput(attrs={
                "class": "input",
                "placeholder": "Precio",
            }),
            "item_type": forms.Select(attrs={
                "class": "input",
            }),
            "location": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Zona / Ciudad",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "input",
            }),
        }
