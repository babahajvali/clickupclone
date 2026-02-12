from django.db import transaction

from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import CreateListDTO, ListDTO, \
    CreateUserListPermissionDTO, CreateTemplateDTO
from task_management.interactors.list.list_interactor import \
    ListInteractor
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, SpaceStorageInterface, FolderStorageInterface, \
    TemplateStorageInterface, FieldStorageInterface, \
    WorkspaceStorageInterface
from task_management.interactors.template.template_onboarding import \
    TemplateOnboardingHandler


class ListOnboardingHandler:

    def __init__(self, list_storage: ListStorageInterface,
                 space_storage: SpaceStorageInterface,
                 folder_storage: FolderStorageInterface,
                 template_storage: TemplateStorageInterface,
                 field_storage: FieldStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,):
        self.list_storage = list_storage
        self.space_storage = space_storage
        self.folder_storage = folder_storage
        self.template_storage = template_storage
        self.field_storage = field_storage
        self.workspace_storage = workspace_storage

    @transaction.atomic
    def handel_list(self, list_data: CreateListDTO) -> ListDTO:
        list_obj = self._create_list(list_data=list_data)

        if list_obj.is_private:
            self._create_space_permission_for_create_user(
                list_id=list_obj.list_id, user_id=list_obj.created_by)

        create_template_dto = CreateTemplateDTO(
            name=f"{list_obj.name} template",
            description=list_obj.description,
            list_id=list_obj.list_id,
            created_by=list_obj.created_by
        )

        self._create_default_template(template_data=create_template_dto)

        return list_obj

    def _get_list_interactor(self):
        list_interactor = ListInteractor(
            list_storage=self.list_storage,
            space_storage=self.space_storage,
            folder_storage=self.folder_storage,
            workspace_storage=self.workspace_storage,
        )
        return list_interactor

    def _create_list(self, list_data: CreateListDTO) -> ListDTO:
        list_interactor = self._get_list_interactor()

        return list_interactor.create_list(list_data=list_data)

    def _create_space_permission_for_create_user(self, list_id: str,
                                                 user_id: str):
        list_interactor = self._get_list_interactor()
        permission_data = CreateUserListPermissionDTO(
            list_id=list_id,
            user_id=user_id,
            permission_type=Permissions.FULL_EDIT,
            added_by=user_id,
        )
        return list_interactor.add_user_in_space_permission(
            user_permission_data=permission_data)

    def _create_default_template(self, template_data: CreateTemplateDTO):
        template_onboarding = TemplateOnboardingHandler(
            template_storage=self.template_storage,
            list_storage=self.list_storage,
            space_storage=self.space_storage,
            field_storage=self.field_storage,
            workspace_storage=self.workspace_storage,
        )

        return template_onboarding.handle(template_data=template_data)
