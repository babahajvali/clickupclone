from task_management.interactors.dtos import CreateTemplateDTO, TemplateDTO, \
    CreateFieldDTO, FIXED_FIELDS
from task_management.interactors.field_interactors.field_interactors import \
    FieldInteractor
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class CreateTemplateInteractor(ValidationMixin):

    def __init__(self, field_storage: FieldStorageInterface,
                 permission_storage: ListPermissionStorageInterface,
                 template_storage: TemplateStorageInterface,
                 list_storage: ListStorageInterface):
        self.field_storage = field_storage
        self.permission_storage = permission_storage
        self.template_storage = template_storage
        self.list_storage = list_storage

    def create_template(self, template_data: CreateTemplateDTO) -> TemplateDTO:
        self.validate_list_is_active(list_id=template_data.list_id,
                                     list_storage=self.list_storage)
        self.ensure_user_has_access_to_list(
            user_id=template_data.created_by, list_id=template_data.list_id,
            permission_storage=self.permission_storage)
        self.validate_template_name_not_exists(
            template_name=template_data.name, template_storage=self.template_storage)

        result = self.template_storage.create_template(template_data)
        self.create_template_default_fields(template_id=result.template_id,
                                            created_by=result.created_by)

        return result

    def create_template_default_fields(self, template_id: str,
                                       created_by: str):

        create_field_interactor = FieldInteractor(
            template_storage=self.template_storage,
            permission_storage=self.permission_storage,
            field_storage=self.field_storage)

        for field in FIXED_FIELDS:
            create_field_dto = CreateFieldDTO(
                field_type=field["field_type"],
                field_name=field["field_name"],
                description=field.get("description", ""),
                template_id=template_id,
                config=field.get("config", {}),
                is_required=field.get("is_required", False),
                created_by=created_by
            )

            create_field_interactor.create_field(create_field_dto)


