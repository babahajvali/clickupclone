import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import \
    ModificationNotAllowedType, UnexpectedRoleType, InactiveUserType, \
    UserNotFoundType, InactiveWorkspaceType, WorkspaceNotFoundType
from task_management.graphql.types.input_types import \
    ChangeWorkspaceMemberRoleInputParams
from task_management.graphql.types.response_types import \
    AddMemberToWorkspaceResponse
from task_management.graphql.types.types import WorkspaceMemberType
from task_management.interactors.workspace.workspace_member_interactor import \
    WorkspaceMemberInteractor
from task_management.storages import WorkspaceStorage, UserStorage


class ChangeMemberRoleMutation(graphene.Mutation):
    class Arguments:
        params = ChangeWorkspaceMemberRoleInputParams(required=True)

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
            result = interactor.change_member_role(
                workspace_id=params.workspace_id,
                user_id=params.user_id,
                role=params.role,
                changed_by=info.context.user_id
            )

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

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)
