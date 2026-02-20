from django.db import transaction

from task_management.exceptions.enums import Permissions, ViewTypes
from task_management.interactors.dtos import CreateListDTO, ListDTO, \
    CreateListPermissionDTO, CreateTemplateDTO, UserListPermissionDTO, \
    ListViewDTO, TemplateDTO
from task_management.interactors.lists.list_interactor import \
    ListInteractor
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, SpaceStorageInterface, FolderStorageInterface, \
    TemplateStorageInterface, FieldStorageInterface, \
    WorkspaceStorageInterface, ViewStorageInterface
from task_management.interactors.templates.template_creation_handler import \
    TemplateCreationHandler
from task_management.interactors.views.list_view_interactor import \
    ListViewInteractor


class ListCreationHandler:

    def __init__(self, list_storage: ListStorageInterface,
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
    def handle_list_creation(self, list_data: CreateListDTO) -> ListDTO:
        list_obj = self._create_list(list_data=list_data)

        if list_obj.is_private:
            self._create_list_permission_for_created_by_user(
                list_id=list_obj.list_id, user_id=list_obj.created_by
            )

        create_template_dto = CreateTemplateDTO(
            name=f"{list_obj.name} template",
            description=list_obj.description,
            list_id=list_obj.list_id,
            created_by=list_obj.created_by
        )

        self._create_default_template(template_data=create_template_dto)
        view_id = self.view_storage.get_list_view_id(
            view_type=ViewTypes.LIST.value
        )

        self._create_default_list_view(
            list_id=list_obj.list_id, view_id=view_id,
            user_id=list_obj.created_by
        )

        return list_obj

    def _get_list_interactor(self):
        list_interactor = ListInteractor(
            list_storage=self.list_storage,
            space_storage=self.space_storage,
            folder_storage=self.folder_storage,
            workspace_storage=self.workspace_storage
        )

        return list_interactor

    def _create_list(self, list_data: CreateListDTO) -> ListDTO:
        list_interactor = self._get_list_interactor()

        return list_interactor.create_list(list_data=list_data)

    def _create_list_permission_for_created_by_user(
            self, list_id: str, user_id: str) -> UserListPermissionDTO:
        list_interactor = self._get_list_interactor()
        permission_data = CreateListPermissionDTO(
            list_id=list_id,
            user_id=user_id,
            permission_type=Permissions.FULL_EDIT,
            added_by=user_id
        )
        return list_interactor.add_user_in_list_permission(
            user_permission_data=permission_data
        )

    def _create_default_template(
            self, template_data: CreateTemplateDTO) -> TemplateDTO:
        template_creation_handler = TemplateCreationHandler(
            template_storage=self.template_storage,
            list_storage=self.list_storage,
            field_storage=self.field_storage,
            workspace_storage=self.workspace_storage
        )

        return template_creation_handler.handle_template(
            template_data=template_data)

    def _create_default_list_view(
            self, view_id: str, list_id: str, user_id: str) -> ListViewDTO:
        list_view_interactor = ListViewInteractor(
            list_storage=self.list_storage,
            view_storage=self.view_storage,
            workspace_storage=self.workspace_storage
        )

        return list_view_interactor.apply_view_for_list(
            list_id=list_id, view_id=view_id, user_id=user_id)
