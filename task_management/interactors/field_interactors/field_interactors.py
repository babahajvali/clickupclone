from task_management.exceptions.custom_exceptions import \
    FieldNotFoundException, InvalidOrderException
from task_management.interactors.dtos import CreateFieldDTO, FieldDTO, \
    UpdateFieldDTO
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
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
        ft = create_field_data.field_type
        field_type = ft.value if hasattr(ft, "value") else ft

        list_id = self.check_template_exist(template_id=create_field_data.template_id,
                                  template_storage=self.template_storage)
        self.check_user_has_access_to_list_modification(
            user_id=create_field_data.created_by,list_id=list_id,
            permission_storage=self.permission_storage)
        self.check_field_type(field_type=field_type)
        self.check_already_existed_field_name(
            field_name=create_field_data.field_name,
            template_id=create_field_data.template_id,
            field_storage=self.field_storage)
        self.check_field_order_is_valid(field_order=create_field_data.order,
                                        template_id=create_field_data.template_id,
                                        field_storage=self.field_storage)
        self.validate_field_config_and_default(field_type=field_type,
                                               config=create_field_data.config)

        return self.field_storage.create_field(
            create_field_data=create_field_data)

    def update_field(self, update_field_data: UpdateFieldDTO) -> FieldDTO:
        ft = update_field_data.field_type
        field_type = ft.value if hasattr(ft, "value") else ft

        self._validate_field(field_id=update_field_data.field_id,
                             template_id=update_field_data.template_id)
        list_id = self.check_template_exist(
            template_id=update_field_data.template_id,
            template_storage=self.template_storage)
        self.check_user_has_access_to_list_modification(
            user_id=update_field_data.created_by, list_id=list_id,
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

    def reorder_field(self, field_id: str, template_id: str, new_order: int,
                      user_id: str) -> list[FieldDTO]:
        self._validate_field_order(template_id=template_id,order=new_order)
        list_id = self.check_template_exist(template_id=template_id,
                                            template_storage=self.template_storage)
        self.check_user_has_access_to_list_modification(list_id=list_id,
                                                        user_id=user_id,
                                                        permission_storage=self.permission_storage)
        self._validate_field(field_id=field_id, template_id=template_id)

        return self.field_storage.reorder_fields(field_id=field_id,
                                                 template_id=template_id,
                                                 new_order=new_order)

    def _validate_field(self, field_id: str, template_id: str):
        is_exist = self.field_storage.check_field_exist(field_id=field_id,
                                                        template_id=template_id)

        if not is_exist:
            raise FieldNotFoundException(field_id=field_id)

    def _validate_field_order(self, template_id: str, order: int):
        if order < 1:
            raise InvalidOrderException(order=order)

        fields_count = self.field_storage.template_fields_count(
            template_id=template_id)

        if order > fields_count:
            raise InvalidOrderException(order=order)

    def get_fields_for_template(self, template_id: str) -> list[FieldDTO]:
        self.check_template_exist(template_id=template_id,
                                  template_storage=self.template_storage)

        return self.field_storage.get_fields_for_template(
            template_id=template_id)
