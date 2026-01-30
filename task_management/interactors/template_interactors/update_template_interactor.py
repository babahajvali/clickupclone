from task_management.interactors.dtos import UpdateTemplateDTO, TemplateDTO
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class UpdateTemplateInteractor(ValidationMixin):

    def __init__(self, list_storage: ListStorageInterface,
                 template_storage: TemplateStorageInterface,
                 permission_storage: ListPermissionStorageInterface):
        self.list_storage = list_storage
        self.template_storage = template_storage
        self.permission_storage = permission_storage

    def update_template(self, update_template_data: UpdateTemplateDTO,
                        user_id: str) -> TemplateDTO:
        template_data = self.template_storage.get_template_by_id(
            template_id=update_template_data.template_id)
        self.get_template_list_id(template_id=update_template_data.template_id,
                                  template_storage=self.template_storage)
        self.validate_list_is_active(list_id=template_data.list_id,
                                     list_storage=self.list_storage)
        self.validate_user_has_access_to_list(
            user_id=user_id, list_id=template_data.list_id,
            permission_storage=self.permission_storage)

        return self.template_storage.update_template(
            update_template_data=update_template_data)

