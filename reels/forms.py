from django import forms
from .models import Reel


class ReelForm(forms.ModelForm):

    class Meta:
        model = Reel
        fields = ["video", "caption"]

        widgets = {
            "video": forms.ClearableFileInput(attrs={
                "class": "input",
                "accept": "video/mp4,video/webm,video/ogg",
            }),
            "caption": forms.Textarea(attrs={
                "class": "input",
                "rows": 2,
                "placeholder": "Escribí una descripción (opcional)",
            }),
        }
