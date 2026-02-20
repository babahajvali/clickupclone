from django.db import transaction

from task_management.constants.field_constants import FIXED_FIELDS
from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import CreateTemplateDTO, CreateFieldDTO, \
    TemplateDTO
from task_management.interactors.storage_interfaces import \
    TemplateStorageInterface, ListStorageInterface, FieldStorageInterface, \
    WorkspaceStorageInterface
from task_management.interactors.templates.template_interactor import \
    TemplateInteractor


class TemplateCreationHandler:

    def __init__(self, template_storage: TemplateStorageInterface,
                 list_storage: ListStorageInterface,
                 field_storage: FieldStorageInterface,
                 workspace_storage: WorkspaceStorageInterface, ):
        self.template_storage = template_storage
        self.list_storage = list_storage
        self.field_storage = field_storage
        self.workspace_storage = workspace_storage

    @transaction.atomic
    def handle_template(self, template_data: CreateTemplateDTO) -> TemplateDTO:
        template_obj = self._create_template(template_data=template_data)

        self._create_template_fixed_fields(
            template_id=template_obj.template_id,
            user_id=template_obj.created_by)

        return template_obj

    def _create_template(self, template_data: CreateTemplateDTO):
        template_interactor = TemplateInteractor(
            template_storage=self.template_storage,
            list_storage=self.list_storage,
            workspace_storage=self.workspace_storage
        )

        return template_interactor.create_template(template_data=template_data)

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
        self.field_storage.create_bulk_fields(fields_data=fixed_fields)
