from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import SpaceNotFoundType, \
    InactiveSpaceType
from task_management.graphql.types.types import ListType, ListsType
from task_management.interactors.list_interactors.list_interactors import \
    ListInteractor
from task_management.storages.list_storage import ListStorage
from task_management.storages.template_storage import TemplateStorage
from task_management.storages.field_storage import FieldStorage
from task_management.storages.folder_storage import FolderStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.list_permission_storage import ListPermissionStorage
from task_management.storages.folder_permission_storage import FolderPermissionStorage
from task_management.storages.space_permission_storage import SpacePermissionStorage


def get_space_lists_resolver(root, info, params):
    space_id = params.space_id

    list_storage = ListStorage()
    template_storage = TemplateStorage()
    field_storage = FieldStorage()
    folder_storage = FolderStorage()
    space_storage = SpaceStorage()
    list_permission_storage = ListPermissionStorage()
    folder_permission_storage = FolderPermissionStorage()
    space_permission_storage = SpacePermissionStorage()

    interactor = ListInteractor(
        list_storage=list_storage,
        template_storage=template_storage,
        field_storage=field_storage,
        folder_storage=folder_storage,
        space_storage=space_storage,
        list_permission_storage=list_permission_storage,
        folder_permission_storage=folder_permission_storage,
        space_permission_storage=space_permission_storage
    )

    try:
        lists_data = interactor.get_space_lists(space_id=space_id)

        lists_output = [
            ListType(
                list_id=list_item.list_id,
                name=list_item.name,
                description=list_item.description,
                space_id=list_item.space_id,
                is_active=list_item.is_active,
                order=list_item.order,
                is_private=list_item.is_private,
                created_by=list_item.created_by,
                folder_id=list_item.folder_id if list_item.folder_id else None
            ) for list_item in lists_data
        ]

        return ListsType(lists=lists_output)

    except custom_exceptions.SpaceNotFoundException as e:
        return SpaceNotFoundType(space_id=e.space_id)

    except custom_exceptions.InactiveSpaceException as e:
        return InactiveSpaceType(space_id=e.space_id)