from task_management.interactors.dtos import CreateTemplateDTO, TemplateDTO, \
    CreateFieldDTO, DEFAULT_FIELDS
from task_management.interactors.field_interactors.create_field_interactor import \
    CreateFieldInteractor
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.permission_storage_interface import \
    PermissionStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class CreateTemplateInteractor(ValidationMixin):

    def __init__(self, user_storage: UserStorageInterface,
                 field_storage: FieldStorageInterface,
                 permission_storage: PermissionStorageInterface,
                 template_storage: TemplateStorageInterface,
                 list_storage: ListStorageInterface):
        self.user_storage = user_storage
        self.field_storage = field_storage
        self.permission_storage = permission_storage
        self.template_storage = template_storage
        self.list_storage = list_storage

    def create_template(self, template_data: CreateTemplateDTO) -> TemplateDTO:
        self.check_user_exist(user_id=template_data.created_by,
                              user_storage=self.user_storage)
        self.check_list_exists_and_status(list_id=template_data.list_id,
                                          list_storage=self.list_storage)
        self.check_user_has_access_to_create_template(
            user_id=template_data.created_by,
            permission_storage=self.permission_storage)
        self.check_already_existed_template_name(
            template_name=template_data.name,
            template_storage=self.template_storage)
        if template_data.is_default:
            self.check_default_template_exists(
                template_name=template_data.name,
                template_storage=self.template_storage)

        result = self.template_storage.create_template(template_data)
        self.create_template_default_fields(template_id=result.template_id,
                created_by=result.created_by)

        return result

    def create_template_default_fields(self, template_id: str, created_by: str):

        create_field_interactor = CreateFieldInteractor(
            template_storage=self.template_storage,
            permission_storage=self.permission_storage,
            field_storage=self.field_storage)

        for field in DEFAULT_FIELDS:
            create_field_dto = CreateFieldDTO(
                field_type=field["field_type"],
                field_name=field["field_name"],
                description=field.get("description", ""),
                template_id=template_id,
                order=field["order"],
                config=field.get("config", {}),
                is_required=field.get("is_required", False),
                created_by=created_by
            )

            create_field_interactor.create_field(create_field_dto)
