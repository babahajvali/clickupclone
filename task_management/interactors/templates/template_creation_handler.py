from django.db import transaction

from task_management.constants.field_constants import FIXED_FIELDS
from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import CreateTemplateDTO, CreateFieldDTO, \
    TemplateDTO
from task_management.interactors.storage_interfaces import \
    TemplateStorageInterface, ListStorageInterface, FieldStorageInterface, \
    WorkspaceStorageInterface
from task_management.interactors.templates.create_template_interactor import \
    CreateTemplateInteractor


class TemplateCreationHandler:

    def __init__(
            self, template_storage: TemplateStorageInterface,
            list_storage: ListStorageInterface,
            field_storage: FieldStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        self.template_storage = template_storage
        self.list_storage = list_storage
        self.field_storage = field_storage
        self.workspace_storage = workspace_storage

    @transaction.atomic
    def handle_template_creation(
            self, create_template_dto: CreateTemplateDTO) -> TemplateDTO:
        template_dto = self._create_template(
            create_template_dto=create_template_dto
        )

        self._create_template_fixed_fields(
            template_id=template_dto.template_id,
            user_id=template_dto.created_by)

        return template_dto

    def _create_template(
            self, create_template_dto: CreateTemplateDTO) -> TemplateDTO:
        create_template_interactor = CreateTemplateInteractor(
            template_storage=self.template_storage,
            list_storage=self.list_storage,
            workspace_storage=self.workspace_storage
        )

        return create_template_interactor.create_template(
            create_template_dto=create_template_dto
        )

    def _create_template_fixed_fields(self, template_id: str, user_id: str):
        fixed_fields = []
        for field in FIXED_FIELDS:
            create_field_dto = CreateFieldDTO(
                field_type=FieldType(field["field_type"]),
                field_name=field["field_name"],
                description=field.get("description", ""),
                template_id=template_id,
                config=field.get("config", {}),
                is_required=field.get("is_required", False),
                created_by_user_id=user_id
            )
            fixed_fields.append(create_field_dto)

        self.field_storage.create_bulk_fields(create_field_dtos=fixed_fields)
