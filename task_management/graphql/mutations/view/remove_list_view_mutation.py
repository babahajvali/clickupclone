import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import \
    ModificationNotAllowedType, ListViewNotFound, \
    UserNotWorkspaceMemberType
from task_management.graphql.types.input_types import RemoveListViewInputParams
from task_management.graphql.types.response_types import RemoveListViewResponse
from task_management.graphql.types.types import ListViewType
from task_management.interactors.views.remove_list_view_interactor import \
    RemoveListViewInteractor
from task_management.storages import ListStorage, ViewStorage, WorkspaceStorage


class RemoveListViewMutation(graphene.Mutation):
    class Arguments:
        params = RemoveListViewInputParams(required=True)

    Output = RemoveListViewResponse

    @staticmethod
    def mutate(root, info, params):
        list_storage = ListStorage()
        view_storage = ViewStorage()
        workspace_storage = WorkspaceStorage()

        interactor = RemoveListViewInteractor(
            list_storage=list_storage,
            view_storage=view_storage,
            workspace_storage=workspace_storage
        )

        try:
            list_view_dto = interactor.remove_view_for_list(
                list_view_id=params.list_view_id,
                user_id=info.context.user_id)

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

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)

        except custom_exceptions.ListViewNotFound as e:
            return ListViewNotFound(list_view_id=e.list_view_id)
