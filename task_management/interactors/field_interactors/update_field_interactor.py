from task_management.interactors.dtos import UpdateFieldDTO, FieldDTO
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class UpdateFieldInteractor(ValidationMixin):

    def __init__(self, field_storage: FieldStorageInterface,
                 permission_storage: ListPermissionStorageInterface,
                 template_storage: TemplateStorageInterface):
        self.field_storage = field_storage
        self.permission_storage = permission_storage
        self.template_storage = template_storage

    def update_field(self, update_field_data: UpdateFieldDTO) -> FieldDTO:
        ft = update_field_data.field_type
        field_type = ft.value if hasattr(ft, "value") else ft

        self.validate_field(field_id=update_field_data.field_id,
                            template_id=update_field_data.template_id,
                            field_storage=self.field_storage)
        list_id = self.check_template_exist(template_id=update_field_data.template_id,
                                  template_storage=self.template_storage)
        self.check_user_has_access_to_list_modification(
            user_id=update_field_data.created_by,list_id=list_id,
            permission_storage=self.permission_storage)
        self.check_field_type(field_type=field_type)
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
