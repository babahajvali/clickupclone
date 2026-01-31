import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import ListNotFoundType, \
    InactiveListType, ModificationNotAllowedType, InvalidOrderType
from task_management.graphql.types.input_types import \
    ReorderListInFolderInputParams
from task_management.graphql.types.response_types import \
    ReorderListInFolderResponse
from task_management.graphql.types.types import ListType
from task_management.interactors.list_interactors.list_interactors import \
    ListInteractor

from task_management.storages.list_storage import ListStorage
from task_management.storages.template_storage import TemplateStorage
from task_management.storages.task_storage import TaskStorage
from task_management.storages.field_storage import FieldStorage
from task_management.storages.folder_storage import FolderStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.list_permission_storage import \
    ListPermissionStorage
from task_management.storages.folder_permission_storage import \
    FolderPermissionStorage
from task_management.storages.space_permission_storage import \
    SpacePermissionStorage


class ReorderListInFolderMutation(graphene.Mutation):
    class Arguments:
        params = ReorderListInFolderInputParams(required=True)

    Output = ReorderListInFolderResponse

    @staticmethod
    def mutate(root, info, params):
        list_storage = ListStorage()
        template_storage = TemplateStorage()
        task_storage = TaskStorage()
        field_storage = FieldStorage()
        folder_storage = FolderStorage()
        space_storage = SpaceStorage()
        list_permission_storage = ListPermissionStorage()
        folder_permission_storage = FolderPermissionStorage()
        space_permission_storage = SpacePermissionStorage()

        interactor = ListInteractor(
            list_storage=list_storage,
            template_storage=template_storage,
            task_storage=task_storage,
            field_storage=field_storage,
            folder_storage=folder_storage,
            space_storage=space_storage,
            list_permission_storage=list_permission_storage,
            folder_permission_storage=folder_permission_storage,
            space_permission_storage=space_permission_storage
        )

        try:
            result = interactor.reorder_list_in_folder(
                folder_id=params.folder_id,
                list_id=params.list_id,
                order=params.order,
                user_id=info.context.user_id
            )

            return ListType(
                list_id=result.list_id,
                name=result.name,
                description=result.description,
                space_id=result.space_id,
                is_active=result.is_active,
                order=result.order,
                is_private=result.is_private,
                created_by=result.created_by,
                folder_id=result.folder_id if result.folder_id else None
            )

        except custom_exceptions.ListNotFoundException as e:
            return ListNotFoundType(list_id=e.list_id)

        except custom_exceptions.InactiveListException as e:
            return InactiveListType(list_id=e.list_id)

        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.InvalidOrderException as e:
            return InvalidOrderType(order=e.order)
