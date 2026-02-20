import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import \
    ModificationNotAllowedType, ListNotFoundType, ViewNotFoundType, \
    InactiveListType
from task_management.graphql.types.input_types import ApplyListViewInputParams
from task_management.graphql.types.response_types import ApplyListViewResponse
from task_management.graphql.types.types import ListViewType
from task_management.interactors.views.list_view_interactor import \
    ListViewInteractor
from task_management.storages import ListStorage, ViewStorage, WorkspaceStorage


class ApplyListViewMutation(graphene.Mutation):
    class Arguments:
        params = ApplyListViewInputParams(required=True)

    Output = ApplyListViewResponse

    @staticmethod
    def mutate(root, info, params):
        list_storage = ListStorage()
        view_storage = ViewStorage()
        workspace_storage = WorkspaceStorage()
        

        interactor = ListViewInteractor(
            list_storage=list_storage,
            view_storage=view_storage,
            workspace_storage=workspace_storage
        )

        try:

            result = interactor.apply_view_for_list(list_id=params.list_id,
                                                    view_id=params.view_id,
                                                    user_id=info.context.user_id)

            return ListViewType(
                id=result.id,
                view_id=result.view_id,
                list_id=result.list_id,
                applied_by=result.applied_by,
                is_active=result.is_active
            )
        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)
        except custom_exceptions.ListNotFound as e:
            return ListNotFoundType(list_id=e.list_id)
        except custom_exceptions.ViewNotFound as e:
            return ViewNotFoundType(view_id=e.view_id)
        except custom_exceptions.InactiveList as e:
            return InactiveListType(list_id=e.list_id)
