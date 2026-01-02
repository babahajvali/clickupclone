from task_management.interactors.dtos import FieldDTO
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class GetFieldForTemplateInteractor(ValidationMixin):
    def __init__(self, field_storage: FieldStorageInterface,
                 template_storage: TemplateStorageInterface):
        self.field_storage = field_storage
        self.template_storage = template_storage
    
    def get_field_for_template(self,template_id: str) -> list[FieldDTO]:
        self.check_template_exist(template_id=template_id,template_storage=self.template_storage)
        
        return self.field_storage.get_fields_for_template(template_id=template_id)