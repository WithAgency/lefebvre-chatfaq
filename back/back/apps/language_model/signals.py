from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from back.apps.language_model.models import LLMConfig
from back.apps.language_model.tasks import llm_query_task


@receiver(post_save, sender=LLMConfig)
@receiver(post_delete, sender=LLMConfig)
def on_llm_config_or_dataset_change(instance, *args, **kwargs):
    llm_query_task.delay(None, None, None, None, None, True)
