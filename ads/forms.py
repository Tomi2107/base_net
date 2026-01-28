# ads/forms.py
from django import forms
from .models import Ad

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = [
            "title",
            "image",
            "link",
            "ad_type",
            "zones",
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full p-2 border rounded",
                "placeholder": "Título del anuncio"
            }),
            "link": forms.URLInput(attrs={
                "class": "w-full p-2 border rounded",
                "placeholder": "https://..."
            }),
            "ad_type": forms.Select(attrs={
                "class": "w-full p-2 border rounded"
            }),
            "zones": forms.SelectMultiple(attrs={
                "class": "w-full p-2 border rounded"
            }),
        }
