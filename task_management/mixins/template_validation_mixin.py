from task_management.exceptions.custom_exceptions import \
    TemplateNotFoundException
from task_management.interactors.storage_interfaces import \
    TemplateStorageInterface


class TemplateValidationMixin:

    def __init__(self, template_storage: TemplateStorageInterface, **kwargs):
        self.template_storage = template_storage
        super().__init__(**kwargs)

    def check_template_exists(self, template_id: str):
        is_exists = self.template_storage.validate_template_exists(
            template_id=template_id)

        is_template_not_found = not is_exists
        if is_template_not_found:
            raise TemplateNotFoundException(template_id=template_id)
