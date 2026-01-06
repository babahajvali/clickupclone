from task_management.exceptions.custom_exceptions import \
    FieldNotFoundException, InvalidOrderException
from task_management.interactors.dtos import CreateFieldDTO, FieldDTO, \
    UpdateFieldDTO
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.task_field_values_storage_interface import \
    FieldValueStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import \
    TaskStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class FieldInteractor(ValidationMixin):

    def __init__(self, field_storage: FieldStorageInterface,
                 template_storage: TemplateStorageInterface,
                 permission_storage: ListPermissionStorageInterface):
        self.field_storage = field_storage
        self.template_storage = template_storage
        self.permission_storage = permission_storage

    def create_field(self, create_field_data: CreateFieldDTO) -> FieldDTO:
        list_id = self.get_template_list_id(
            template_id=create_field_data.template_id,
            template_storage=self.template_storage)
        self.ensure_user_has_access_to_list(
            user_id=create_field_data.created_by, list_id=list_id,
            permission_storage=self.permission_storage)
        self.check_field_type(field_type=create_field_data.field_type)
        self.validate_field_name_not_exists(
            field_name=create_field_data.field_name,
            template_id=create_field_data.template_id,
            field_storage=self.field_storage)
        self.validate_field_config(field_type=create_field_data.field_type,
                                   config=create_field_data.config)

        return self.field_storage.create_field(create_field_data=create_field_data)

        return result

    def update_field(self, update_field_data: UpdateFieldDTO,
                     user_id: str) -> FieldDTO:
        self._validate_field(field_id=update_field_data.field_id)
        field_data = self.field_storage.get_field_by_id(
            update_field_data.field_id)
        list_id = self.get_template_list_id(
            template_id=field_data.template_id,
            template_storage=self.template_storage)
        self.ensure_user_has_access_to_list(
            user_id=user_id, list_id=list_id,
            permission_storage=self.permission_storage)
        self.ensure_field_name_unique(field_id=update_field_data.field_id,
                                      field_name=update_field_data.field_name,
                                      template_id=field_data.template_id,
                                      field_storage=self.field_storage)
        self.validate_field_config(field_type=field_data.field_type,
                                   config=update_field_data.config)

        return self.field_storage.update_field(update_field_data=update_field_data)

    def reorder_field(self, field_id: str, template_id: str, new_order: int,
                      user_id: str) -> list[FieldDTO]:
        self._validate_field_order(template_id=template_id, order=new_order)
        list_id = self.get_template_list_id(template_id=template_id,
                                            template_storage=self.template_storage)
        self.ensure_user_has_access_to_list(list_id=list_id,
                                            user_id=user_id,
                                            permission_storage=self.permission_storage)
        self._validate_field(field_id=field_id)

        return self.field_storage.reorder_fields(field_id=field_id,
                                                 template_id=template_id,
                                                 new_order=new_order)

    def get_fields_for_template(self, template_id: str) -> list[FieldDTO]:
        self.get_template_list_id(template_id=template_id,
                                  template_storage=self.template_storage)

        return self.field_storage.get_fields_for_template(
            template_id=template_id)

    def _validate_field(self, field_id: str):
        is_exist = self.field_storage.is_field_exists(field_id=field_id)

        if not is_exist:
            raise FieldNotFoundException(field_id=field_id)

    def _validate_field_order(self, template_id: str, order: int):
        if order < 1:
            raise InvalidOrderException(order=order)

        fields_count = self.field_storage.template_fields_count(
            template_id=template_id)

        if order > fields_count:
            raise InvalidOrderException(order=order)

