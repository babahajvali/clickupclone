from task_management.interactors.dtos import UpdateTemplateDTO
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.permission_storage_interface import \
    PermissionStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class UpdateTemplateInteractor(ValidationMixin):

    def __init__(self, list_storage: ListStorageInterface,
                 user_storage: UserStorageInterface,
                 template_storage: TemplateStorageInterface,
                 permission_storage: PermissionStorageInterface):
        self.list_storage = list_storage
        self.user_storage = user_storage
        self.template_storage = template_storage
        self.permission_storage = permission_storage

    def update_template(self, update_template_data: UpdateTemplateDTO):
        self.check_template_exist(template_id=update_template_data.template_id,
                                  template_storage=self.template_storage)
        self.check_user_exist(user_id=update_template_data.created_by,
                              user_storage=self.user_storage)
        self.check_list_exists(list_id=update_template_data.list_id,
                               list_storage=self.list_storage)
        self.check_user_has_access_to_create_template(
            user_id=update_template_data.created_by,
            permission_storage=self.permission_storage)
        self.check_template_name_exist(
            template_name=update_template_data.name,
            template_id=update_template_data.template_id,
            template_storage=self.template_storage)
        if update_template_data.is_default:
            self.check_default_template_exists(
                template_name=update_template_data.name,
                template_storage=self.template_storage)

        return self.template_storage.update_template(update_template_data=update_template_data)
