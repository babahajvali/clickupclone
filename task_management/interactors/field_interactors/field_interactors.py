from task_management.exceptions.custom_exceptions import \
    InvalidOrderException, MissingFieldConfigException
from task_management.exceptions.enums import FieldTypes
from task_management.interactors.dtos import CreateFieldDTO, FieldDTO, \
    UpdateFieldDTO
from task_management.interactors.storage_interfaces.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interfaces.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interfaces.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interfaces.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.storage_interfaces.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin
from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache


class FieldInteractor(ValidationMixin):

    def __init__(self, field_storage: FieldStorageInterface,
                 template_storage: TemplateStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface,
                 list_storage: ListStorageInterface,
                 space_storage: SpaceStorageInterface):
        self.field_storage = field_storage
        self.template_storage = template_storage
        self.workspace_member_storage = workspace_member_storage
        self.list_storage = list_storage
        self.space_storage = space_storage

    @invalidate_interactor_cache(cache_name="fields")
    def create_field(self, create_field_data: CreateFieldDTO) -> FieldDTO:
        list_id = self.get_template_list_id(
            template_id=create_field_data.template_id,
            template_storage=self.template_storage)
        space_id = self.list_storage.get_list_space_id(list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=create_field_data.created_by,
            workspace_member_storage=self.workspace_member_storage)
        self.validate_field_type(field_type=create_field_data.field_type.value)
        self.validate_field_name_not_exists(
            field_name=create_field_data.field_name,
            template_id=create_field_data.template_id,
            field_storage=self.field_storage)
        if create_field_data.field_type.value == FieldTypes.DROPDOWN.value and not create_field_data.config:
            raise MissingFieldConfigException(
                field_type=create_field_data.field_type.value)

        if create_field_data.config:
            self.validate_field_config(
                field_type=create_field_data.field_type.value,
                config=create_field_data.config)

        return self.field_storage.create_field(
            create_field_data=create_field_data)

    @invalidate_interactor_cache(cache_name="fields")
    def update_field(self, update_field_data: UpdateFieldDTO,
                     user_id: str) -> FieldDTO:
        self.validate_field(field_id=update_field_data.field_id,
                            field_storage=self.field_storage)
        field_data = self.field_storage.get_field_by_id(
            update_field_data.field_id)
        list_id = self.get_template_list_id(
            template_id=field_data.template_id,
            template_storage=self.template_storage)
        space_id = self.list_storage.get_list_space_id(list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id,
            workspace_member_storage=self.workspace_member_storage)
        self.validate_field_name_except_current(
            field_id=update_field_data.field_id,
            field_name=update_field_data.field_name,
            template_id=field_data.template_id,
            field_storage=self.field_storage)
        self.validate_field_config(field_type=field_data.field_type.value,
                                   config=update_field_data.config)

        return self.field_storage.update_field(
            update_field_data=update_field_data)

    @invalidate_interactor_cache(cache_name="fields")
    def reorder_field(self, field_id: str, template_id: str, new_order: int,
                      user_id: str) -> FieldDTO:
        self._validate_field_order(template_id=template_id, order=new_order)
        list_id = self.get_template_list_id(template_id=template_id,
                                            template_storage=self.template_storage)
        space_id = self.list_storage.get_list_space_id(list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id,
            workspace_member_storage=self.workspace_member_storage)
        self.validate_field(field_id=field_id,
                            field_storage=self.field_storage)

        return self.field_storage.reorder_fields(field_id=field_id,
                                                 template_id=template_id,
                                                 new_order=new_order)

    @invalidate_interactor_cache(cache_name="fields")
    def delete_field(self, field_id: str, user_id: str) -> FieldDTO:
        self.validate_field(field_id=field_id,
                            field_storage=self.field_storage)
        field_data = self.field_storage.get_field_by_id(field_id=field_id)
        list_id = self.get_template_list_id(
            template_id=field_data.template_id,
            template_storage=self.template_storage)
        space_id = self.list_storage.get_list_space_id(list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id,
            workspace_member_storage=self.workspace_member_storage)

        return self.field_storage.delete_field(field_id=field_id)

    @interactor_cache(cache_name="fields", timeout=5 * 60)
    def get_fields_for_template(self, list_id: str) -> list[FieldDTO]:
        self.validate_list_is_active(list_id=list_id,
                                     list_storage=self.list_storage)
        template_id = self.list_storage.get_template_id_by_list_id(
            list_id=list_id)
        self.get_template_list_id(template_id=template_id,
                                  template_storage=self.template_storage)

        return self.field_storage.get_fields_for_template(
            template_id=template_id)

    def get_field(self, field_id: str) -> FieldDTO:
        self.validate_field(field_id=field_id,
                            field_storage=self.field_storage)

        return self.field_storage.get_field_by_id(field_id=field_id)

    def _validate_field_order(self, template_id: str, order: int):
        if order < 1:
            raise InvalidOrderException(order=order)

        fields_count = self.field_storage.template_fields_count(
            template_id=template_id)

        if order > fields_count:
            raise InvalidOrderException(order=order)
