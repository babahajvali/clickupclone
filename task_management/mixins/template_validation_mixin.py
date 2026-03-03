from task_management.exceptions.custom_exceptions import \
    TemplateNotFound, EmptyTemplateName
from task_management.interactors.storage_interfaces import \
    TemplateStorageInterface


class TemplateValidationMixin:

    def __init__(self, template_storage: TemplateStorageInterface):
        self.template_storage = template_storage

    def check_template_exists(self, template_id: str):
        is_exists = self.template_storage.validate_template_exists(
            template_id=template_id)

        is_template_not_found = not is_exists
        if is_template_not_found:
            raise TemplateNotFound(template_id=template_id)

    @staticmethod
    def check_template_name_not_empty(template_name: str):
        is_name_empty = not template_name or not template_name.strip()
        if is_name_empty:
            raise EmptyTemplateName(name=template_name)
