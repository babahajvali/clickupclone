from django.core.cache import cache

from task_management.exceptions.custom_exceptions import InvalidOrderException
from task_management.exceptions.enums import Permissions, Visibility
from task_management.interactors.dtos import CreateListDTO, ListDTO, \
    UpdateListDTO, UserListPermissionDTO, CreateUserListPermissionDTO, \
    CreateTemplateDTO
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.folder_permission_storage_interface import \
    FolderPermissionStorageInterface
from task_management.interactors.storage_interface.folder_storage_interface import \
    FolderStorageInterface
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import \
    SpacePermissionStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import \
    TaskStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.template_interactors.create_template_interactor import \
    CreateTemplateInteractor
from task_management.interactors.validation_mixin import ValidationMixin
from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache


class ListInteractor(ValidationMixin):

    def __init__(self, list_storage: ListStorageInterface,
                 template_storage: TemplateStorageInterface,
                 task_storage: TaskStorageInterface,
                 field_storage: FieldStorageInterface,
                 folder_storage: FolderStorageInterface,
                 space_storage: SpaceStorageInterface,
                 list_permission_storage: ListPermissionStorageInterface,
                 folder_permission_storage: FolderPermissionStorageInterface,
                 space_permission_storage: SpacePermissionStorageInterface):
        self.list_storage = list_storage
        self.template_storage = template_storage
        self.field_storage = field_storage
        self.task_storage = task_storage
        self.folder_storage = folder_storage
        self.space_storage = space_storage
        self.list_permission_storage = list_permission_storage
        self.folder_permission_storage = folder_permission_storage
        self.space_permission_storage = space_permission_storage

    @invalidate_interactor_cache(cache_name="space_lists")
    @invalidate_interactor_cache(cache_name="folder_lists")
    def create_list(self, create_list_data: CreateListDTO) -> ListDTO:
        if create_list_data.folder_id is not None:
            self.validate_user_has_access_to_folder(
                user_id=create_list_data.created_by,
                folder_id=create_list_data.folder_id,
                permission_storage=self.folder_permission_storage
            )
            self.validate_folder_is_active(
                folder_id=create_list_data.folder_id,
                folder_storage=self.folder_storage
            )
        else:
            self.validate_user_has_access_to_space(
                user_id=create_list_data.created_by,
                space_id=create_list_data.space_id,
                permission_storage=self.space_permission_storage
            )

        self.validate_space_is_active(
            space_id=create_list_data.space_id,
            space_storage=self.space_storage
        )

        result = self.list_storage.create_list(
            create_list_data=create_list_data)

        self._create_list_users_permissions(
            list_id=result.list_id, space_id=result.space_id,
            created_by=result.created_by)
        template_interactor = CreateTemplateInteractor(
            list_storage=self.list_storage,
            template_storage=self.template_storage,
            permission_storage=self.list_permission_storage,
            field_storage=self.field_storage
        )
        create_template_dto = CreateTemplateDTO(
            name=create_list_data.name + " template",
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
        self.validate_user_has_access_to_list(
            user_id=user_id, list_id=update_list_data.list_id,
            permission_storage=self.list_permission_storage)

        if list_data.folder_id is not None:
            self.validate_folder_is_active(
                folder_id=list_data.folder_id,
                folder_storage=self.folder_storage
            )
        else:
            self.validate_space_is_active(
                space_id=list_data.space_id,
                space_storage=self.space_storage
            )

        return self.list_storage.update_list(update_list_data=update_list_data)

    @invalidate_interactor_cache(cache_name="folder_lists")
    def reorder_list_in_folder(self, folder_id: str, list_id: str, order: int,
                               user_id: str) -> ListDTO:
        self.validate_user_has_access_to_list(list_id=list_id,
                                              user_id=user_id,
                                              permission_storage=self.list_permission_storage)
        self.validate_list_is_active(list_id=list_id,
                                     list_storage=self.list_storage)
        self._validate_list_order_in_folder(folder_id=folder_id, order=order)

        return self.list_storage.reorder_list_in_folder(folder_id=folder_id,
                                                        list_id=list_id,
                                                        order=order)

    @invalidate_interactor_cache(cache_name="space_lists")
    def reorder_list_in_space(self, space_id: str, order: int, user_id: str,
                              list_id: str) -> ListDTO:
        self.validate_user_has_access_to_list(list_id=list_id, user_id=user_id,
                                              permission_storage=self.list_permission_storage)
        self.validate_list_is_active(list_id=list_id,
                                     list_storage=self.list_storage)
        self._validate_list_order_in_space(space_id=space_id, order=order)

        return self.list_storage.reorder_list_in_space(space_id=space_id,
                                                       list_id=list_id,
                                                       order=order)

    @invalidate_interactor_cache(cache_name="space_lists")
    @invalidate_interactor_cache(cache_name="folder_lists")
    def remove_list(self, list_id: str, user_id: str):
        self.validate_user_has_access_to_list(
            user_id=user_id,
            list_id=list_id,
            permission_storage=self.list_permission_storage
        )
        self.validate_list_is_active(
            list_id=list_id,
            list_storage=self.list_storage
        )

        return self.list_storage.remove_list(list_id=list_id)

    @invalidate_interactor_cache(cache_name="space_lists")
    def set_list_visibility(self, list_id: str, visibility: Visibility,
                            user_id: str) -> ListDTO:
        self.validate_user_has_access_to_list(list_id=list_id, user_id=user_id,
                                              permission_storage=self.list_permission_storage)
        self.validate_list_is_active(list_id=list_id,
                                     list_storage=self.list_storage)
        self._validate_visibility_type(visibility=visibility.value)

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

    # Helping functions

    def _create_list_users_permissions(self, list_id: str, space_id: str,
                                       created_by: str) -> list[
        UserListPermissionDTO]:
        space_user_permissions = self.space_permission_storage.get_space_permissions(
            space_id=space_id)
        list_user_permissions = []

        for each in space_user_permissions:
            if each.permission_type == Permissions.FULL_EDIT.value:
                user_permission = CreateUserListPermissionDTO(
                    list_id=list_id,
                    user_id=each.user_id,
                    permission_type=Permissions.FULL_EDIT,
                    added_by=created_by,
                )
            elif each.permission_type == Permissions.COMMENT.value:
                user_permission = CreateUserListPermissionDTO(
                    list_id=list_id,
                    user_id=each.user_id,
                    permission_type=Permissions.COMMENT,
                    added_by=created_by,
                )
            else:
                user_permission = CreateUserListPermissionDTO(
                    list_id=list_id,
                    user_id=each.user_id,
                    permission_type=Permissions.VIEW,
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
