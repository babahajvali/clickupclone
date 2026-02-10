from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import ListNotFoundType, \
    InactiveListType
from task_management.graphql.types.types import ListType
from task_management.interactors.list_interactors.list_interactors import \
    ListInteractor
from task_management.storages.field_storage import FieldStorage
from task_management.storages.folder_permission_storage import \
    FolderPermissionStorage
from task_management.storages.folder_storage import FolderStorage
from task_management.storages.list_permission_storage import \
    ListPermissionStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_permission_storage import \
    SpacePermissionStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.template_storage import TemplateStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage


def get_list_resolver(root, info, params):
    list_storage = ListStorage()
    template_storage = TemplateStorage()
    field_storage = FieldStorage()
    folder_storage = FolderStorage()
    space_storage = SpaceStorage()
    list_permission_storage = ListPermissionStorage()
    workspace_member_storage = WorkspaceMemberStorage()

    interactor = ListInteractor(
        list_storage=list_storage,
        template_storage=template_storage,
        field_storage=field_storage,
        folder_storage=folder_storage,
        space_storage=space_storage,
        list_permission_storage=list_permission_storage,
        workspace_member_storage=workspace_member_storage
    )

    try:
        list_data = interactor.get_list(list_id=params.list_id)

        list_output = ListType(
            list_id=list_data.list_id,
            name=list_data.name,
            description=list_data.description,
            space_id=list_data.space_id,
            is_active=list_data.is_active,
            order=list_data.order,
            is_private=list_data.is_private,
            created_by=list_data.created_by,
            folder_id=list_data.folder_id if list_data.folder_id else None
        )

        return list_output

    except custom_exceptions.ListNotFoundException as e:
        return ListNotFoundType(list_id=e.list_id)
    except custom_exceptions.InactiveListException as e:
        return InactiveListType(list_id=e.list_id)
