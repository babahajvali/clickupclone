import graphene

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
from task_management.graphql.resolvers.task.get_list_tasks_resolver import \
    get_list_tasks_resolver
from task_management.graphql.resolvers.task.get_task_resolver import \
    get_task_resolver
from task_management.graphql.resolvers.task.task_filter_resolver import \
    task_filter_resolver
from task_management.graphql.resolvers.user.get_user_resolver import \
    get_user_profile_resolver
from task_management.graphql.resolvers.workspace.get_workspace_resolver import \
    get_workspace_resolver
from task_management.graphql.types.input_types import \
    GetUserProfileInputParams, GetWorkspaceInputParams, \
    GetWorkspaceSpacesInputParams, GetSpaceInputParams, \
    GetSpaceFoldersInputParams, GetFolderInputParams, GetListInputParams, \
    GetFolderListsInputParams, GetSpaceListsInputParams, \
    GetListTasksInputParams, GetTaskInputParams, TaskFilterInputParams
from task_management.graphql.types.response_types import \
    GetUserProfileResponse, GetWorkspaceResponse, GetWorkspaceSpacesResponse, \
    GetSpaceResponse, GetSpaceFoldersResponse, GetFolderResponse, \
    GetListResponse, GetFolderListsResponse, GetSpaceListsResponse, \
    GetListTasksResponse, GetTaskResponse, TaskFilterResponse


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