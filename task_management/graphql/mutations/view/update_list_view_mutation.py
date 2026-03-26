import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import ListViewNotFound, \
    EmptyViewNameType, UserNotWorkspaceMemberType, ModificationNotAllowedType
from task_management.graphql.types.input_types import UpdateListViewInputParams
from task_management.graphql.types.response_types import UpdateListViewResponse
from task_management.graphql.types.types import ListViewType
from task_management.interactors.list_views.update_list_view_intercator import \
    UpdateListViewInteractor
from task_management.storages import ListStorage, ListViewStorage, \
    WorkspaceStorage


class UpdateListViewMutation(graphene.Mutation):
    class Arguments:
        params = UpdateListViewInputParams(required=True)

    Output = UpdateListViewResponse

    @staticmethod
    def mutate(root, info, params):
        list_storage = ListStorage()
        view_storage = ListViewStorage()
        workspace_storage = WorkspaceStorage()

        update_list_view_interactor = UpdateListViewInteractor(
            list_storage=list_storage,
            view_storage=view_storage,
            workspace_storage=workspace_storage
        )

        try:
            list_view_dto = update_list_view_interactor.update_list_view(
                list_view_id=params.list_view_id,
                view_name=params.view_name,
                user_id=info.context.user_id,
            )

            return ListViewType(
                id=list_view_dto.id,
                view_name=list_view_dto.view_name,
                view_type=list_view_dto.view_type,
                list_id=list_view_dto.list_id,
                created_by=list_view_dto.created_by,
                is_active=list_view_dto.is_active
            )

        except custom_exceptions.ListViewNotFound as e:
            return ListViewNotFound(list_view_id=e.list_view_id)

        except custom_exceptions.EmptyViewName as e:
            return EmptyViewNameType(view_name=e.view_name)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)
