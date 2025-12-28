from django import forms
from .models import LostFoundPost

class LostFoundForm(forms.ModelForm):

    class Meta:
        model = LostFoundPost
        fields = [
            "status",
            "animal_type",
            "animal_other",
            "size",
            "color",
            "pattern",
            "place",
            "description",
        ]

    def __init__(self, *args, **kwargs):
        search_mode = kwargs.pop("search_mode", False)
        super().__init__(*args, **kwargs)

        if search_mode:
            # Todos opcionales para búsqueda
            for field in self.fields.values():
                field.required = False
