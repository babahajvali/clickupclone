from task_management.exceptions.enums import FieldTypes
from task_management.interactors.dtos import CreateTemplateDTO, TemplateDTO, \
    CreateFieldDTO
from task_management.constants.field_constants import FIXED_FIELDS
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


class CreateTemplateInteractor(ValidationMixin):

    def __init__(self, field_storage: FieldStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface,
                 template_storage: TemplateStorageInterface,
                 list_storage: ListStorageInterface,
                 space_storage: SpaceStorageInterface, ):
        self.field_storage = field_storage
        self.workspace_member_storage = workspace_member_storage
        self.template_storage = template_storage
        self.list_storage = list_storage
        self.space_storage = space_storage

    def create_template(self, template_data: CreateTemplateDTO) -> TemplateDTO:
        self.validate_list_is_active(list_id=template_data.list_id,
                                     list_storage=self.list_storage)
        space_id = self.list_storage.get_list_space_id(
            list_id=template_data.list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=template_data.created_by,
            workspace_member_storage=self.workspace_member_storage)

        result = self.template_storage.create_template(template_data)
        self.create_template_fixed_fields(template_id=result.template_id,
                                          created_by=result.created_by)

        return result

    def create_template_fixed_fields(self, template_id: str,
                                     created_by: str):
        fixed_fields = []
        for field in FIXED_FIELDS:
            create_field_dto = CreateFieldDTO(
                field_type=FieldTypes(field["field_type"]),
                field_name=field["field_name"],
                description=field.get("description", ""),
                template_id=template_id,
                config=field.get("config", {}),
                is_required=field.get("is_required", False),
                created_by=created_by
            )
            fixed_fields.append(create_field_dto)
        self.field_storage.create_bulk_fields(fields_data=fixed_fields)
