from task_management.interactors.dtos import UpdateFieldDTO, FieldDTO, \
    FieldTypeEnum
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.permission_storage_interface import \
    PermissionStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class UpdateFieldInteractor(ValidationMixin):

    def __init__(self, user_storage: UserStorageInterface,
                 field_storage: FieldStorageInterface,
                 permission_storage: PermissionStorageInterface,
                 template_storage: TemplateStorageInterface):
        self.user_storage = user_storage
        self.field_storage = field_storage
        self.permission_storage = permission_storage
        self.template_storage = template_storage

    def update_field(self, update_field_data: UpdateFieldDTO) -> FieldDTO:
        field_type = update_field_data.field_type.value if update_field_data.field_type.value else update_field_data.field_type

        self.validate_field(field_id=update_field_data.field_id,
                            template_id=update_field_data.template_id,
                            field_storage=self.field_storage)
        self.check_user_exist(user_id=update_field_data.created_by,
                              user_storage=self.user_storage)
        self.check_template_exist(template_id=update_field_data.template_id,
                                  template_storage=self.template_storage)
        self.check_user_has_access_to_create_field(
            user_id=update_field_data.created_by,
            permission_storage=self.permission_storage)
        self.check_field_type(field_type=update_field_data.field_type.value)
        self.check_field_name_exist(field_id=update_field_data.field_id,
                                    field_name=update_field_data.field_name,
                                    template_id=update_field_data.template_id,
                                    field_storage=self.field_storage)
        self.check_field_order_is_valid(field_order=update_field_data.order,
                                        template_id=update_field_data.template_id,
                                        field_storage=self.field_storage)
        self.validate_field_config_and_default(field_type=field_type,
                                               config=update_field_data.config)

        return self.field_storage.update_field(
            update_field_data=update_field_data)
