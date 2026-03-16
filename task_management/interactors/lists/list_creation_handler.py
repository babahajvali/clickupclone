from django.db import transaction

from task_management.exceptions.enums import PermissionType, ViewType
from task_management.interactors.dtos import (
    CreateListDTO,
    ListDTO,
    CreateListPermissionDTO,
    CreateTemplateDTO,
    UserListPermissionDTO,
    ListViewDTO,
    TemplateDTO, CreateListViewDTO,
)
from task_management.interactors.lists.create_list_interactor import (
    CreateListInteractor,
)
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    SpaceStorageInterface,
    FolderStorageInterface,
    TemplateStorageInterface,
    FieldStorageInterface,
    WorkspaceStorageInterface,
    ViewStorageInterface,
)
from task_management.interactors.templates.template_creation_handler import (
    TemplateCreationHandler,
)


class ListCreationHandler:

    def __init__(
            self, list_storage: ListStorageInterface,
            space_storage: SpaceStorageInterface,
            folder_storage: FolderStorageInterface,
            template_storage: TemplateStorageInterface,
            field_storage: FieldStorageInterface,
            workspace_storage: WorkspaceStorageInterface,
            view_storage: ViewStorageInterface):
        self.list_storage = list_storage
        self.space_storage = space_storage
        self.folder_storage = folder_storage
        self.template_storage = template_storage
        self.field_storage = field_storage
        self.workspace_storage = workspace_storage
        self.view_storage = view_storage

    @transaction.atomic
    def handle_list_creation(self, create_list_dto: CreateListDTO) -> ListDTO:
        list_dto = self._create_list(create_list_dto=create_list_dto)

        if list_dto.is_private:
            self._create_list_permission_for_created_by_user(
                list_id=list_dto.list_id, user_id=list_dto.created_by
            )

        self._create_default_template(
            name=list_dto.name, list_id=list_dto.list_id,
            user_id=list_dto.created_by)

        create_list_view_dto = CreateListViewDTO(
            list_id=list_dto.list_id,
            view_name="List",
            view_type=ViewType.LIST,
            created_by=list_dto.created_by,
        )

        self._create_default_list_view(
            create_list_view_dto=create_list_view_dto
        )

        return list_dto

    def _create_list(self, create_list_dto: CreateListDTO) -> ListDTO:
        list_interactor = CreateListInteractor(
            list_storage=self.list_storage,
            space_storage=self.space_storage,
            folder_storage=self.folder_storage,
            workspace_storage=self.workspace_storage,
        )

        return list_interactor.create_list(create_list_dto=create_list_dto)

    def _create_list_permission_for_created_by_user(
            self, list_id: str, user_id: str) -> UserListPermissionDTO:
        user_permission_dto = CreateListPermissionDTO(
            list_id=list_id,
            user_id=user_id,
            permission_type=PermissionType.FULL_EDIT,
            added_by=user_id,
        )

        return self.list_storage.create_list_users_permission(
            user_permissions=[user_permission_dto]
        )[0]

    def _create_default_template(
            self, name: str, list_id: str, user_id: str) -> TemplateDTO:
        template_creation_handler = TemplateCreationHandler(
            template_storage=self.template_storage,
            list_storage=self.list_storage,
            field_storage=self.field_storage,
            workspace_storage=self.workspace_storage,
        )

        create_template_dto = CreateTemplateDTO(
            name=f"{name} template",
            description=None,
            list_id=list_id,
            created_by=user_id,
        )

        return template_creation_handler.handle_template_creation(
            create_template_dto=create_template_dto
        )

    def _create_default_list_view(
            self, create_list_view_dto: CreateListViewDTO) -> ListViewDTO:
        return self.view_storage.create_list_view(
            create_list_view_dto=create_list_view_dto
        )
