from task_management.exceptions.custom_exceptions import \
    EmptyWorkspaceName, \
    UnexpectedRole
from task_management.exceptions.enums import Role
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface


class WorkspaceValidator:

    def __init__(self, workspace_storage: WorkspaceStorageInterface):
        self.workspace_storage = workspace_storage

    @staticmethod
    def check_workspace_name_not_empty(workspace_name: str):
        is_name_empty = not workspace_name or not workspace_name.strip()

        if is_name_empty:
            raise EmptyWorkspaceName(workspace_name=workspace_name)

    @staticmethod
    def check_role(role: str):

        existed_roles = Role.get_values()
        is_role_invalid = role not in existed_roles

        if is_role_invalid:
            raise UnexpectedRole(role=role)
