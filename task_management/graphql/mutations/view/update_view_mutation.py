import graphene

from task_management.exceptions import custom_exceptions
from task_management.exceptions.custom_exceptions import NothingToUpdateView
from task_management.graphql.types.error_types import ViewNotFoundType, \
    NothingToUpdateViewType
from task_management.graphql.types.input_types import UpdateViewInputParams
from task_management.graphql.types.response_types import UpdateViewResponse
from task_management.graphql.types.types import ViewType
from task_management.interactors.views.view_interactor import \
    ViewInteractor
from task_management.interactors.dtos import UpdateViewDTO
from task_management.storages import ViewStorage, ListStorage


class UpdateViewMutation(graphene.Mutation):
    class Arguments:
        params = UpdateViewInputParams(required=True)

    Output = UpdateViewResponse

    @staticmethod
    def mutate(root, info, params):
        view_storage = ViewStorage()
        list_storage = ListStorage()

        interactor = ViewInteractor(
            view_storage=view_storage,
            list_storage=list_storage
        )

        try:

            view_id=params.view_id
            name=params.name
            description=params.description


            result = interactor.update_view(
                view_id=view_id, name=name, description=description)

            return ViewType(
                view_id=str(result.view_id),
                name=result.name,
                description=result.description,
                view_type=result.view_type.value,
                created_by=str(result.created_by)
            )

        except custom_exceptions.ViewNotFound as e:
            return ViewNotFoundType(view_id=e.view_id)

        except custom_exceptions.NothingToUpdateView as e:
            return NothingToUpdateViewType(view_id=e.view_id)


