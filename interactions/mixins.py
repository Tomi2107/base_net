from django.contrib.contenttypes.models import ContentType
from interactions.models import SavedItem
from django.core.exceptions import ImproperlyConfigured

class SavedByUserMixin:
    model_type = None
    context_object_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if not self.model_type:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} requiere model_type"
            )
        if not self.context_object_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} requiere context_object_name"
            )

        # 👉 nombre del modelo para URLs
        model_name = f"{self.model_type._meta.app_label}.{self.model_type.__name__}"

        if user.is_authenticated:
            ct = ContentType.objects.get_for_model(self.model_type)

            for obj in context[self.context_object_name]:
                obj.model_name = model_name   # 🔥 ACÁ
                obj.is_saved_by_user = SavedItem.objects.filter(
                    user=user,
                    content_type=ct,
                    object_id=obj.id
                ).exists()
        else:
            for obj in context[self.context_object_name]:
                obj.model_name = model_name
                obj.is_saved_by_user = False

        return context



