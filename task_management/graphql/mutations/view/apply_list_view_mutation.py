import graphene

from task_management.exceptions import custom_exceptions
from task_management.exceptions.enums import ViewType
from task_management.graphql.types.error_types import \
    ModificationNotAllowedType, ListNotFoundType, ViewNotFoundType, \
    DeletedListType, UserNotWorkspaceMemberType
from task_management.graphql.types.input_types import CreateListViewInputParams
from task_management.graphql.types.response_types import ApplyListViewResponse
from task_management.graphql.types.types import ListViewType
from task_management.interactors.dtos import CreateListViewDTO
from task_management.interactors.views.create_list_view_interactor import \
    CreateListViewInteractor
from task_management.storages import ListStorage, ListViewStorage, \
    WorkspaceStorage


class ApplyListViewMutation(graphene.Mutation):
    class Arguments:
        params = CreateListViewInputParams(required=True)

    Output = ApplyListViewResponse

    @staticmethod
    def mutate(root, info, params):
        list_storage = ListStorage()
        view_storage = ListViewStorage()
        workspace_storage = WorkspaceStorage()

        interactor = CreateListViewInteractor(
            list_storage=list_storage,
            view_storage=view_storage,
            workspace_storage=workspace_storage
        )

        try:
            create_list_view_dto = CreateListViewDTO(
                view_name=params.view_name,
                view_type=ViewType(params.view_type),
                list_id=params.list_id,
                created_by=info.context.user_id,
            )

            list_view_dto = interactor.create_list_view(
                create_list_view_dto=create_list_view_dto)

            return ListViewType(
                id=list_view_dto.id,
                view_name=list_view_dto.view_name,
                view_type=list_view_dto.view_type,
                list_id=list_view_dto.list_id,
                created_by=list_view_dto.created_by,
                is_active=list_view_dto.is_active
            )
        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.ListNotFound as e:
            return ListNotFoundType(list_id=e.list_id)

        except custom_exceptions.ViewNotFound as e:
            return ViewNotFoundType(view_id=e.view_type)

        except custom_exceptions.ListIsDeleted as e:
            return DeletedListType(list_id=e.list_id)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)
