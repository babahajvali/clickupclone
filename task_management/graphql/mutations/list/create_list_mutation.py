import graphene

from task_management.exceptions import custom_exceptions
from task_management.exceptions.enums import ListEntityType
from task_management.graphql.types.error_types import SpaceNotFoundType, \
    DeletedSpaceType, FolderNotFoundType, DeletedFolderType, \
    ModificationNotAllowedType, EmptyListNameType, UserNotWorkspaceMemberType
from task_management.graphql.types.input_types import CreateListInputParams
from task_management.graphql.types.response_types import CreateListResponse
from task_management.graphql.types.types import ListType
from task_management.interactors.dtos import CreateListDTO
from task_management.interactors.lists.list_creation_handler import \
    ListCreationHandler
from task_management.storages import ListStorage, FolderStorage, SpaceStorage, \
    WorkspaceStorage, FieldStorage, TemplateStorage, ViewStorage


class CreateListMutation(graphene.Mutation):
    class Arguments:
        params = CreateListInputParams(required=True)

    Output = CreateListResponse

    @staticmethod
    def mutate(root, info, params):
        list_storage = ListStorage()
        folder_storage = FolderStorage()
        space_storage = SpaceStorage()
        workspace_storage = WorkspaceStorage()
        field_storage = FieldStorage()
        template_storage = TemplateStorage()
        view_storage = ViewStorage()

        interactor = ListCreationHandler(
            list_storage=list_storage,
            folder_storage=folder_storage,
            space_storage=space_storage,
            workspace_storage=workspace_storage,
            field_storage=field_storage,
            template_storage=template_storage,
            view_storage=view_storage,
        )

        try:
            entity_type = ListEntityType(params.entity_type)

            create_list_data = CreateListDTO(
                name=params.name,
                description=params.description,
                entity_type=entity_type,
                entity_id=params.entity_id,
                created_by=info.context.user_id,
                is_private=params.is_private,
            )

            result = interactor.handle_list_creation(
                list_data=create_list_data)

            return ListType(
                list_id=result.list_id,
                name=result.name,
                description=result.description,
                entity_type=result.entity_type.value,
                is_deleted=result.is_deleted,
                order=result.order,
                is_private=result.is_private,
                created_by=result.created_by,
                entity_id=result.entity_id,
            )

        except custom_exceptions.EmptyListName as e:
            return EmptyListNameType(list_name=e.list_name)

        except custom_exceptions.SpaceNotFound as e:
            return SpaceNotFoundType(space_id=e.space_id)

        except custom_exceptions.DeletedSpaceFound as e:
            return DeletedSpaceType(space_id=e.space_id)

        except custom_exceptions.FolderNotFound as e:
            return FolderNotFoundType(folder_id=e.folder_id)

        except custom_exceptions.DeletedFolderException as e:
            return DeletedFolderType(folder_id=e.folder_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)
