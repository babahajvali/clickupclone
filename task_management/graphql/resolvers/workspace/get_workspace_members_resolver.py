from task_management.graphql.types.types import WorkspaceUserType, \
    WorkspaceUsersType
from task_management.models import WorkspaceMember



def get_workspace_members_resolver(root, info, params):
    workspace_id = params.workspace_id

    members = WorkspaceMember.objects.filter(workspace_id=workspace_id,is_active=True)

    result = [ WorkspaceUserType(
        id=each.pk,
        workspace_id=workspace_id,
        user_id=each.user.user_id,
        role=each.role,
        is_active=each.is_active,
        added_by=each.added_by.user_id,
        full_name=each.user.full_name,
        email=each.user.email,
        image_url=each.user.image_url
    ) for each in members]

    return WorkspaceUsersType(workspace_users=result)