import graphene

from task_management.exceptions import custom_exceptions
from task_management.exceptions.enums import Role
from task_management.graphql.types.error_types import WorkspaceNotFoundType, \
    InactiveWorkspaceType, UserNotFoundType, InactiveUserType, \
    UnexpectedRoleType
from task_management.graphql.types.input_types import \
    AddMemberToWorkspaceInputParams
from task_management.graphql.types.response_types import \
    AddMemberToWorkspaceResponse
from task_management.graphql.types.types import WorkspaceMemberType
from task_management.interactors.dtos import AddMemberToWorkspaceDTO
from task_management.interactors.workspace.workspace_member_interactor import \
    WorkspaceMemberInteractor
from task_management.storages import WorkspaceStorage, UserStorage


class AddMemberToWorkspaceMutation(graphene.Mutation):
    class Arguments:
        params = AddMemberToWorkspaceInputParams(required=True)

    Output = AddMemberToWorkspaceResponse

    @staticmethod
    def mutate(root, info, params):
        workspace_storage = WorkspaceStorage()
        user_storage = UserStorage()

        interactor = WorkspaceMemberInteractor(
            workspace_storage=workspace_storage,
            user_storage=user_storage,
        )

        try:

            workspace_member_dto = AddMemberToWorkspaceDTO(
                workspace_id=params.workspace_id,
                user_id=params.user_id,
                role=Role(params.role),
                added_by=info.context.user_id
            )

            result = interactor.add_member_to_workspace(workspace_member_dto)

            return WorkspaceMemberType(
                id=result.id,
                workspace_id=result.workspace_id,
                user_id=result.user_id,
                role=result.role.value,
                is_active=result.is_active,
                added_by=result.added_by
            )

        except custom_exceptions.WorkspaceNotFound as e:
            return WorkspaceNotFoundType(workspace_id=e.workspace_id)

        except custom_exceptions.InactiveWorkspace as e:
            return InactiveWorkspaceType(workspace_id=e.workspace_id)

        except custom_exceptions.UserNotFound as e:
            return UserNotFoundType(user_id=e.user_id)

        except custom_exceptions.InactiveUser as e:
            return InactiveUserType(user_id=e.user_id)

        except custom_exceptions.UnexpectedRole as e:
            return UnexpectedRoleType(role=e.role)
