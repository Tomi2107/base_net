from django import forms
from .models import Group

class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = [
            "name",
            "description",
            "location",
            "privacy",
            "image",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Nombre del grupo",
            }),
            "description": forms.Textarea(attrs={
                "class": "input",
                "rows": 3,
                "placeholder": "Descripción del grupo",
            }),
            "location": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Ciudad / Zona",
            }),
            "privacy": forms.Select(attrs={
                "class": "input",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "input",
            }),
        }
