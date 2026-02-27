from task_management.decorators.caching_decorators import interactor_cache
from task_management.interactors.dtos import FieldDTO
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface, TemplateStorageInterface
from task_management.mixins import TemplateValidationMixin


class GetTemplateFieldsInteractor:

    def __init__(self, field_storage: FieldStorageInterface,
                 template_storage: TemplateStorageInterface):
        self.field_storage = field_storage
        self.template_storage = template_storage

    @property
    def template_mixin(self) -> TemplateValidationMixin:
        return TemplateValidationMixin(template_storage=self.template_storage)

    @interactor_cache(cache_name="fields", timeout=5 * 60)
    def get_template_fields(self, template_id: str) -> list[FieldDTO]:
        self.template_mixin.check_template_exists(template_id=template_id)

        return self.field_storage.get_fields_for_template(
            template_id=template_id)
