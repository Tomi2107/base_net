from django import forms
from .models import FosterAvailability


class FosterAvailabilityForm(forms.ModelForm):

    class Meta:
        model = FosterAvailability
        fields = [
            "is_adult",
            "animal_type",
            "animal_other",
            "health_condition",
            "notes",
        ]

        widgets = {
            "notes": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Contá qué tipo de espacio tenés, experiencia, etc."
            })
        }

    def clean_is_adult(self):
        value = self.cleaned_data.get("is_adult")
        if not value:
            raise forms.ValidationError("Debés ser mayor de 18 años.")
        return value
