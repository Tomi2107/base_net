from django.core.exceptions import ImproperlyConfigured
from interactions.utils import enrich_items_with_save_state


class SavedByUserMixin:
    model_type = None
    context_object_name = None

    def get_context_data(self, **kwargs):
        print("🟡 SavedByUserMixin ejecutado en:", self.__class__.__name__)
        context = super().get_context_data(**kwargs)
        
        print("🟡 context_object_name:", self.context_object_name)
        print("🟡 model_type:", self.model_type)

        if not self.model_type:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} requiere model_type"
            )

        if not self.context_object_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} requiere context_object_name"
            )

        context[self.context_object_name] = enrich_items_with_save_state(
            context[self.context_object_name],
            self.request.user
        )

        return context
