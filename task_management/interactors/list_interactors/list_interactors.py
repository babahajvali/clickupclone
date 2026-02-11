from task_management.exceptions.custom_exceptions import InvalidOrderException
from task_management.exceptions.enums import Permissions, Visibility, Role
from task_management.interactors.dtos import CreateListDTO, ListDTO, \
    UpdateListDTO, UserListPermissionDTO, CreateUserListPermissionDTO, \
    CreateTemplateDTO
from task_management.interactors.storage_interfaces.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interfaces.folder_storage_interface import \
    FolderStorageInterface
from task_management.interactors.storage_interfaces.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interfaces.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interfaces.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interfaces.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.storage_interfaces.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.template_interactors.create_template_interactor import \
    CreateTemplateInteractor
from task_management.interactors.validation_mixin import ValidationMixin
from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache


class ListInteractor(ValidationMixin):

    def __init__(self, list_storage: ListStorageInterface,
                 template_storage: TemplateStorageInterface,
                 field_storage: FieldStorageInterface,
                 folder_storage: FolderStorageInterface,
                 space_storage: SpaceStorageInterface,
                 list_permission_storage: ListPermissionStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface, ):
        self.list_storage = list_storage
        self.template_storage = template_storage
        self.field_storage = field_storage
        self.folder_storage = folder_storage
        self.space_storage = space_storage
        self.list_permission_storage = list_permission_storage
        self.workspace_member_storage = workspace_member_storage

    @invalidate_interactor_cache(cache_name="space_lists")
    @invalidate_interactor_cache(cache_name="folder_lists")
    def create_list(self, create_list_data: CreateListDTO) -> ListDTO:
        self.validate_space_is_active(
            space_id=create_list_data.space_id,
            space_storage=self.space_storage
        )
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=create_list_data.space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id,
            user_id=create_list_data.created_by,
            workspace_member_storage=self.workspace_member_storage)

        result = self.list_storage.create_list(
            create_list_data=create_list_data)
        if create_list_data.is_private:
            self._add_users_in_list_permission(
                list_id=result.list_id, workspace_id=workspace_id,
                created_by=result.created_by)
        else:
            user_permission = CreateUserListPermissionDTO(
                list_id=result.list_id,
                user_id=result.created_by,
                permission_type=Permissions.FULL_EDIT,
                added_by=result.created_by,
            )
            self.list_permission_storage.create_list_users_permissions(
                user_permissions=[user_permission])

        template_interactor = CreateTemplateInteractor(
            list_storage=self.list_storage,
            template_storage=self.template_storage,
            workspace_member_storage=self.workspace_member_storage,
            field_storage=self.field_storage,
            space_storage=self.space_storage
        )
        create_template_dto = CreateTemplateDTO(
            name=f"{create_list_data.name} template",
            description=create_list_data.description,
            list_id=result.list_id,
            created_by=result.created_by
        )
        template_interactor.create_template(template_data=create_template_dto)

        return result

    @invalidate_interactor_cache(cache_name="space_lists")
    @invalidate_interactor_cache(cache_name="folder_lists")
    def update_list(self, update_list_data: UpdateListDTO,
                    user_id: str) -> ListDTO:
        self.validate_list_is_active(
            list_id=update_list_data.list_id,
            list_storage=self.list_storage)

        list_data = self.list_storage.get_list(
            list_id=update_list_data.list_id)

        if list_data.folder_id is not None:
            self.validate_folder_is_active(
                folder_id=list_data.folder_id,
                folder_storage=self.folder_storage
            )
        self.validate_space_is_active(
            space_id=list_data.space_id,
            space_storage=self.space_storage
        )
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=list_data.space_id)

        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id,
            workspace_member_storage=self.workspace_member_storage)

        return self.list_storage.update_list(update_list_data=update_list_data)

    @invalidate_interactor_cache(cache_name="folder_lists")
    def reorder_list_in_folder(self, folder_id: str, list_id: str, order: int,
                               user_id: str) -> ListDTO:
        self.validate_list_is_active(list_id=list_id,
                                     list_storage=self.list_storage)
        space_id = self.folder_storage.get_folder_space_id(folder_id=folder_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id,
            workspace_member_storage=self.workspace_member_storage)
        self._validate_list_order_in_folder(folder_id=folder_id, order=order)

        return self.list_storage.reorder_list_in_folder(folder_id=folder_id,
                                                        list_id=list_id,
                                                        order=order)

    @invalidate_interactor_cache(cache_name="space_lists")
    def reorder_list_in_space(self, space_id: str, order: int, user_id: str,
                              list_id: str) -> ListDTO:
        self.validate_list_is_active(list_id=list_id,
                                     list_storage=self.list_storage)
        self._validate_list_order_in_space(space_id=space_id, order=order)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id,
            workspace_member_storage=self.workspace_member_storage)

        return self.list_storage.reorder_list_in_space(space_id=space_id,
                                                       list_id=list_id,
                                                       order=order)

    @invalidate_interactor_cache(cache_name="space_lists")
    @invalidate_interactor_cache(cache_name="folder_lists")
    def remove_list(self, list_id: str, user_id: str):
        self.validate_list_is_active(
            list_id=list_id,
            list_storage=self.list_storage
        )
        space_id = self.list_storage.get_list_space_id(list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id,
            workspace_member_storage=self.workspace_member_storage)

        return self.list_storage.remove_list(list_id=list_id)

    @invalidate_interactor_cache(cache_name="space_lists")
    def set_list_visibility(self, list_id: str, visibility: Visibility,
                            user_id: str) -> ListDTO:
        self.validate_list_is_active(list_id=list_id,
                                     list_storage=self.list_storage)
        self._validate_visibility_type(visibility=visibility.value)
        space_id = self.list_storage.get_list_space_id(list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id,
            workspace_member_storage=self.workspace_member_storage)

        if visibility == Visibility.PUBLIC:
            return self.list_storage.make_list_public(list_id=list_id)

        return self.list_storage.make_list_private(list_id=list_id)

    def get_list(self, list_id: str):
        self.validate_list_is_active(list_id=list_id,
                                     list_storage=self.list_storage)

        return self.list_storage.get_list(list_id=list_id)

    # Permission section
    @interactor_cache(timeout=30 * 60, cache_name="list_permissions")
    def get_list_permissions(self, list_id: str) -> list[
        UserListPermissionDTO]:
        self.validate_list_is_active(list_id=list_id,
                                     list_storage=self.list_storage)

        return self.list_permission_storage.get_list_permissions(
            list_id=list_id)

    @interactor_cache(timeout=5 * 60, cache_name="folder_lists")
    def get_folder_lists(self, folder_id: str):
        self.validate_folder_is_active(folder_id=folder_id,
                                       folder_storage=self.folder_storage)
        return self.list_storage.get_folder_lists(folder_ids=[folder_id])

    @interactor_cache(timeout=30 * 60, cache_name="space_lists")
    def get_space_lists(self, space_id: str):
        self.validate_space_is_active(space_id=space_id,
                                      space_storage=self.space_storage)
        return self.list_storage.get_space_lists(space_ids=[space_id])

    def add_user_in_space_permission(self,
                                     user_permission_data: CreateUserListPermissionDTO):
        self.validate_list_is_active(list_id=user_permission_data.list_id,
                                     list_storage=self.list_storage)
        space_id = self.list_storage.get_list_space_id(
            list_id=user_permission_data.list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_permission_data.user_id,
            workspace_member_storage=self.workspace_member_storage)

        return self.list_permission_storage.create_list_users_permissions(
            user_permissions=[user_permission_data])

    # Helping functions

    def _add_users_in_list_permission(self, list_id: str, workspace_id: str,
                                      created_by: str) -> list[
        UserListPermissionDTO]:
        workspace_members = self.workspace_member_storage.get_workspace_members(
            workspace_id=workspace_id)
        list_user_permissions = []

        for each in workspace_members:
            if each.role == Role.GUEST:
                user_permission = CreateUserListPermissionDTO(
                    list_id=list_id,
                    user_id=each.user_id,
                    permission_type=Permissions.VIEW,
                    added_by=created_by,
                )
            else:
                user_permission = CreateUserListPermissionDTO(
                    list_id=list_id,
                    user_id=each.user_id,
                    permission_type=Permissions.FULL_EDIT,
                    added_by=created_by,
                )

            list_user_permissions.append(user_permission)

        return self.list_permission_storage.create_list_users_permissions(
            user_permissions=list_user_permissions)

    def _validate_list_order_in_folder(self, folder_id: str, order: int):
        if order < 1:
            raise InvalidOrderException(order=order)

        lists_count = self.list_storage.get_folder_lists_count(
            folder_id=folder_id)

        if order > lists_count:
            raise InvalidOrderException(order=order)

    def _validate_list_order_in_space(self, space_id: str, order: int):
        if order < 1:
            raise InvalidOrderException(order=order)
        lists_count = self.list_storage.get_space_lists_count(
            space_id=space_id)

        if order > lists_count:
            raise InvalidOrderException(order=order)
