from django import forms
from .models import ParroquialPost


class ParroquialPostForm(forms.ModelForm):

    class Meta:
        model = ParroquialPost
        fields = ["title", "service_type", "zone", "content"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full p-2 rounded-lg border border-gray-300 "
                         "dark:bg-dark-main dark:border-dark-third dark:text-dark-txt",
                "placeholder": "Título corto"
            }),

            "service_type": forms.Select(attrs={
                "class": "w-full p-2 rounded-lg border border-gray-300 "
                         "dark:bg-dark-main dark:border-dark-third dark:text-dark-txt",
            }),

            "zone": forms.TextInput(attrs={
                "class": "w-full p-2 rounded-lg border border-gray-300 "
                         "dark:bg-dark-main dark:border-dark-third dark:text-dark-txt",
                "placeholder": "Zona / Barrio (opcional por ahora)"
            }),

            "content": forms.Textarea(attrs={
                "rows": 3,
                "class": "w-full p-2 rounded-lg border border-gray-300 "
                         "dark:bg-dark-main dark:border-dark-third dark:text-dark-txt",
                "placeholder": "Mensaje parroquial..."
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 👇 MUY IMPORTANTE
        # Evita que service_type se envíe vacío
        self.fields["service_type"].empty_label = "Seleccionar tipo de servicio"

        self.fields["service_type"].required = False
        # 👇 Para que no te bloquee ahora
        self.fields["zone"].required = False
