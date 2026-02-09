import graphene

from task_management.exceptions import custom_exceptions
from task_management.exceptions.enums import ViewTypes
from task_management.graphql.types.error_types import ViewTypeNotFoundType
from task_management.graphql.types.input_types import CreateViewInputParams
from task_management.graphql.types.response_types import CreateViewResponse
from task_management.graphql.types.types import ViewType
from task_management.interactors.dtos import CreateViewDTO
from task_management.interactors.view_interactors.view_interactors import \
    ViewInteractor
from task_management.storages.list_permission_storage import \
    ListPermissionStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.view_storage import ViewStorage


class CreateViewMutation(graphene.Mutation):
    class Arguments:
        params = CreateViewInputParams(required=True)

    Output = CreateViewResponse

    @staticmethod
    def mutate(root, info, params):
        view_storage = ViewStorage()
        list_storage = ListStorage()
        list_permission_storage = ListPermissionStorage()

        interactor = ViewInteractor(
            view_storage=view_storage,
            list_storage=list_storage,
            permission_storage=list_permission_storage
        )

        try:
            view_type = ViewTypes(params.view_type)
            view_input = CreateViewDTO(
                name=params.name,
                description=params.description,
                view_type=view_type,
                created_by=info.context.user_id,
            )

            result = interactor.create_view(view_input)

            return ViewType(
                view_id=result.view_id,
                name=result.name,
                description=result.description,
                view_type=result.view_type.value,
                created_by=result.created_by
            )

        except custom_exceptions.ViewTypeNotFoundException as e:
            return ViewTypeNotFoundType(view_type=e.view_type)
