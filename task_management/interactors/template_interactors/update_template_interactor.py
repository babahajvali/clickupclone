from task_management.exceptions.custom_exceptions import \
    AlreadyExistedTemplateNameException
from task_management.interactors.dtos import UpdateTemplateDTO
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class UpdateTemplateInteractor(ValidationMixin):

    def __init__(self, list_storage: ListStorageInterface,
                 template_storage: TemplateStorageInterface,
                 permission_storage: ListPermissionStorageInterface):
        self.list_storage = list_storage
        self.template_storage = template_storage
        self.permission_storage = permission_storage

    def update_template(self, update_template_data: UpdateTemplateDTO):
        self.check_template_exist(template_id=update_template_data.template_id,
                                  template_storage=self.template_storage)
        self.check_list_exists_and_status(list_id=update_template_data.list_id,
                                          list_storage=self.list_storage)
        self.check_user_has_access_to_list_modification(
            user_id=update_template_data.created_by,list_id=update_template_data.list_id,
            permission_storage=self.permission_storage)
        self.check_template_name_exist(
            template_name=update_template_data.name,
            template_id=update_template_data.template_id)

        return self.template_storage.update_template(update_template_data=update_template_data)

    def check_template_name_exist(self,template_name: str, template_id: str):
        is_exist = self.template_storage.check_template_name_exist_except_this_template(
            template_name=template_name, template_id=template_id)

        if is_exist:
            raise AlreadyExistedTemplateNameException(
                template_name=template_name)