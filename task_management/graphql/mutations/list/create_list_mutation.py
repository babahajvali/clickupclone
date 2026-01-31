import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import SpaceNotFoundType, \
    InactiveSpaceType, FolderNotFoundType, InactiveFolderType, \
    ModificationNotAllowedType
from task_management.graphql.types.input_types import CreateListInputParams
from task_management.graphql.types.response_types import CreateListResponse
from task_management.graphql.types.types import ListType

from task_management.interactors.dtos import CreateListDTO
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


class CreateListMutation(graphene.Mutation):
    class Arguments:
        params = CreateListInputParams(required=True)

    Output = CreateListResponse

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
            create_list_data = CreateListDTO(
                name=params.name,
                description=params.description,
                space_id=params.space_id,
                created_by=info.context.user_id,
                is_private=params.is_private,
                folder_id=params.folder_id if params.folder_id else None
            )

            result = interactor.create_list(create_list_data=create_list_data)

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


        except custom_exceptions.SpaceNotFoundException as e:
            return SpaceNotFoundType(space_id=e.space_id)

        except custom_exceptions.InactiveSpaceException as e:
            return InactiveSpaceType(space_id=e.space_id)

        except custom_exceptions.FolderNotFoundException as e:
            return FolderNotFoundType(folder_id=e.folder_id)

        except custom_exceptions.InactiveFolderException as e:
            return InactiveFolderType(folder_id=e.folder_id)

        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)
