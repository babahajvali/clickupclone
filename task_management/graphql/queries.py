import graphene

from task_management.graphql.resolvers.account.get_accounts_resolver import \
    get_user_accounts_resolver
from task_management.graphql.resolvers.fields.get_field_resolver import \
    get_field_resolver
from task_management.graphql.resolvers.fields.get_task_field_values_resolver import \
    get_task_field_values_resolver
from task_management.graphql.resolvers.fields.get_template_fields_resolver import \
    get_fields_for_template_resolver
from task_management.graphql.resolvers.folder.get_folder import \
    get_folder_resolver
from task_management.graphql.resolvers.folder.get_sapce_folders import \
    get_space_folders_resolver
from task_management.graphql.resolvers.lists.get_folder_lists_resolver import \
    get_folder_lists_resolver
from task_management.graphql.resolvers.lists.get_list_resolver import \
    get_list_resolver
from task_management.graphql.resolvers.lists.get_space_lists import \
    get_space_lists_resolver
from task_management.graphql.resolvers.space.get_space_resolver import \
    get_space_resolver
from task_management.graphql.resolvers.space.get_workspace_spaces_resolver import \
    get_workspace_spaces_resolver
from task_management.graphql.resolvers.task.get_list_task_assignees_resolver import \
    get_list_task_assignees_resolver
from task_management.graphql.resolvers.task.get_list_tasks_resolver import \
    get_list_tasks_resolver
from task_management.graphql.resolvers.task.get_task_assignees_resolver import \
    get_task_assignees_resolver
from task_management.graphql.resolvers.task.get_task_resolver import \
    get_task_resolver
from task_management.graphql.resolvers.task.get_user_tasks_resolver import \
    get_user_tasks_resolver
from task_management.graphql.resolvers.task.task_filter_resolver import \
    task_filter_resolver
from task_management.graphql.resolvers.user.get_user_resolver import \
    get_user_profile_resolver
from task_management.graphql.resolvers.user.get_user_with_email_resolver import \
    get_user_with_email_resolver
from task_management.graphql.resolvers.views.get_list_views import \
    get_list_views_resolver
from task_management.graphql.resolvers.views.get_views_resolver import \
    get_all_views_resolver
from task_management.graphql.resolvers.workspace.get_user_workspaces import \
    get_user_workspace_resolver
from task_management.graphql.resolvers.workspace.get_workspace_members_resolver import \
    get_workspace_members_resolver
from task_management.graphql.resolvers.workspace.get_workspace_resolver import \
    get_workspace_resolver
from task_management.graphql.types.input_types import \
    GetUserProfileInputParams, GetWorkspaceInputParams, \
    GetWorkspaceSpacesInputParams, GetSpaceInputParams, \
    GetSpaceFoldersInputParams, GetFolderInputParams, GetListInputParams, \
    GetFolderListsInputParams, GetSpaceListsInputParams, \
    GetListTasksInputParams, GetTaskInputParams, TaskFilterInputParams, \
    GetTaskAssigneesInputParams, GetFieldsForTemplateInputParams, \
    GetFieldInputParams, GetListViewsInputParams, GetUserWorkspacesInputParams, \
    GetTaskFieldValuesInputParams, GetWorkspaceMemberInputParams, \
    GetUserTasksInputParams, GetListTaskAssigneesInputParams, \
    GetAccountsInputParams, GetUserWithEmailInputParams
from task_management.graphql.types.response_types import \
    GetUserProfileResponse, GetWorkspaceResponse, GetWorkspaceSpacesResponse, \
    GetSpaceResponse, GetSpaceFoldersResponse, GetFolderResponse, \
    GetListResponse, GetFolderListsResponse, GetSpaceListsResponse, \
    GetListTasksResponse, GetTaskResponse, TaskFilterResponse, \
    GetTaskAssigneesResponse, GetViewsResponse, GetFieldsForTemplateResponse, \
    GetFieldResponse, GetListViewsResponse, GetUserWorkspacesResponse, \
    GetTaskFieldValuesResponse, GetWorkspaceUsersResponse, \
    GetUserTasksResponse, GetListTaskAssigneesResponse, \
    GetAccountsResponse, GetUserWithEmailResponse


class GetUser(graphene.ObjectType):
    get_user_profile = graphene.Field(
        GetUserProfileResponse,
        params=GetUserProfileInputParams(required=True),
        resolver=get_user_profile_resolver
    )


class GetWorkspace(graphene.ObjectType):
    get_workspace = graphene.Field(
        GetWorkspaceResponse,
        params=GetWorkspaceInputParams(required=True),
        resolver=get_workspace_resolver
    )


class GetWorkspaceSpaces(graphene.ObjectType):
    get_workspace_spaces = graphene.Field(
        GetWorkspaceSpacesResponse,
        params=GetWorkspaceSpacesInputParams(required=True),
        resolver=get_workspace_spaces_resolver
    )


class GetSpace(graphene.ObjectType):
    get_space = graphene.Field(
        GetSpaceResponse,
        params=GetSpaceInputParams(required=True),
        resolver=get_space_resolver

    )


class GetSpaceFolders(graphene.ObjectType):
    get_space_folders = graphene.Field(
        GetSpaceFoldersResponse,
        params=GetSpaceFoldersInputParams(required=True),
        resolver=get_space_folders_resolver
    )


class GetFolder(graphene.ObjectType):
    get_folder = graphene.Field(
        GetFolderResponse,
        params=GetFolderInputParams(required=True),
        resolver=get_folder_resolver
    )


class GetList(graphene.ObjectType):
    get_list = graphene.Field(
        GetListResponse,
        params=GetListInputParams(required=True),
        resolver=get_list_resolver
    )


class GetFolderLists(graphene.ObjectType):
    get_folder_lists = graphene.Field(
        GetFolderListsResponse,
        params=GetFolderListsInputParams(required=True),
        resolver=get_folder_lists_resolver
    )


class GetSpaceLists(graphene.ObjectType):
    get_space_lists = graphene.Field(
        GetSpaceListsResponse,
        params=GetSpaceListsInputParams(required=True),
        resolver=get_space_lists_resolver
    )


class GetListTasks(graphene.ObjectType):
    get_list_tasks = graphene.Field(
        GetListTasksResponse,
        params=GetListTasksInputParams(required=True),
        resolver=get_list_tasks_resolver
    )


class GetTask(graphene.ObjectType):
    get_task = graphene.Field(
        GetTaskResponse,
        params=GetTaskInputParams(required=True),
        resolver=get_task_resolver
    )


class GetTaskFilters(graphene.ObjectType):
    get_task_filters = graphene.Field(
        TaskFilterResponse,
        params=TaskFilterInputParams(required=True),
        resolver=task_filter_resolver
    )


class GetTaskAssignees(graphene.ObjectType):
    get_task_assignees = graphene.Field(
        GetTaskAssigneesResponse,
        params=GetTaskAssigneesInputParams(required=True),
        resolver=get_task_assignees_resolver
    )


class GetViews(graphene.ObjectType):
    get_views = graphene.Field(
        GetViewsResponse,
        resolver=get_all_views_resolver
    )


class GetTemplateFields(graphene.ObjectType):
    get_template_fields = graphene.Field(
        GetFieldsForTemplateResponse,
        params=GetFieldsForTemplateInputParams(required=True),
        resolver=get_fields_for_template_resolver
    )


class GetField(graphene.ObjectType):
    get_fields = graphene.Field(
        GetFieldResponse,
        params=GetFieldInputParams(required=True),
        resolver=get_field_resolver
    )


class GetListViews(graphene.ObjectType):
    get_list_views = graphene.Field(
        GetListViewsResponse,
        params=GetListViewsInputParams(required=True),
        resolver=get_list_views_resolver
    )


class GetUserWorkspaces(graphene.ObjectType):
    get_user_workspaces = graphene.Field(
        GetUserWorkspacesResponse,
        params=GetUserWorkspacesInputParams(required=True),
        resolver=get_user_workspace_resolver
    )


class GetTaskValues(graphene.ObjectType):
    get_task_values = graphene.Field(
        GetTaskFieldValuesResponse,
        params=GetTaskFieldValuesInputParams(required=True),
        resolver=get_task_field_values_resolver
    )


class GetWorkspaceMembers(graphene.ObjectType):
    get_workspace_members = graphene.Field(
        GetWorkspaceUsersResponse,
        params=GetWorkspaceMemberInputParams(required=True),
        resolver=get_workspace_members_resolver
    )


class GetUserTasks(graphene.ObjectType):
    get_user_tasks = graphene.Field(
        GetUserTasksResponse,
        params=GetUserTasksInputParams(required=True),
        resolver=get_user_tasks_resolver
    )


class GetListTaskAssignees(graphene.ObjectType):
    get_list_task_assignees = graphene.Field(
        GetListTaskAssigneesResponse,
        params=GetListTaskAssigneesInputParams(required=True),
        resolver=get_list_task_assignees_resolver
    )



class GetAccounts(graphene.ObjectType):
    get_user_accounts = graphene.Field(
        GetAccountsResponse,
        resolver=get_user_accounts_resolver
    )


class GetUserWithEmail(graphene.ObjectType):
    get_user_with_email = graphene.Field(
        GetUserWithEmailResponse,
        params=GetUserWithEmailInputParams(required=True),
        resolver=get_user_with_email_resolver
    )