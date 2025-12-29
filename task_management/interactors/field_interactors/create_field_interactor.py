from task_management.interactors.dtos import CreateFieldDTO, FieldDTO, \
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


class CreateFieldInteractor(ValidationMixin):

    def __init__(self, field_storage: FieldStorageInterface,
                 user_storage: UserStorageInterface,
                 template_storage: TemplateStorageInterface,
                 permission_storage: PermissionStorageInterface):
        self.field_storage = field_storage
        self.user_storage = user_storage
        self.template_storage = template_storage
        self.permission_storage = permission_storage

    def create_field(self, create_field_data: CreateFieldDTO) -> FieldDTO:
        field_type = (
            create_field_data.field_type.value
            if isinstance(create_field_data.field_type, FieldTypeEnum)
            else create_field_data.field_type
        )
        self.check_user_exist(user_id=create_field_data.created_by,
                              user_storage=self.user_storage)
        self.check_template_exist(template_id=create_field_data.template_id,
                                  template_storage=self.template_storage)
        self.check_user_has_access_to_create_field(
            user_id=create_field_data.created_by,
            permission_storage=self.permission_storage)
        self.check_field_type(
            field_type=field_type)
        self.check_already_existed_field_name(
            field_name=create_field_data.field_name,
            template_id=create_field_data.template_id,
            field_storage=self.field_storage)
        self.check_field_order_is_valid(field_order=create_field_data.order,
                                        template_id=create_field_data.template_id,
                                        field_storage=self.field_storage)

        return self.field_storage.create_field(
            create_field_data=create_field_data)
