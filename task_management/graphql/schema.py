import graphene

from task_management.graphql.mutations import CreateAccount, CreateUser, \
    UpdateUser, BlockUser, UserLogin, TransferAccount, DeleteAccount, \
    CreateWorkspace, TransferWorkspace, DeleteWorkspace, UpdateWorkspace, \
    CreateSpace, UpdateSpace, DeleteSpace, ReorderSpace, SetSpaceVisibility, \
    CreateFolder, UpdateFolder, DeleteFolder, ReorderFolder, \
    SetFolderVisibility, CreateList, UpdateList, DeleteList, \
    ReorderListInFolder, SetListVisibility, ReorderListInSpace, CreateTask, \
    UpdateTask, ReorderTask, DeleteTask, CreateView, AddMemberToWorkspace, \
    ChangeWorkspaceMemberRole, RemoveMemberFromWorkspace, TaskAssignee, \
    RemoveTaskAssignee, UpdateView, UpdateField, CreateField, DeleteField, \
    ReorderField, ApplyListView, RemoveListView, AddAccountMember, \
    ChangeAccountMemberRole, RemoveAccountMember
from task_management.graphql.queries import GetUser, GetWorkspace, \
    GetWorkspaceSpaces, GetSpace, GetSpaceFolders, GetFolder, GetList, \
    GetFolderLists, GetSpaceLists, GetTaskFilters, GetTask, GetListTasks, \
    GetTaskAssignees, GetViews, GetTemplateFields, GetField, GetListViews, \
    GetUserWorkspaces

QUERY_CLASSES = [GetUser, GetWorkspace, GetWorkspaceSpaces, GetSpace,
                 GetSpaceFolders, GetFolder, GetList, GetFolderLists,
                 GetSpaceLists, GetTaskFilters, GetTask, GetListTasks,
                 GetTaskAssignees, GetViews, GetTemplateFields, GetField,
                 GetListViews, GetUserWorkspaces]

MUTATION_CLASSES = [CreateAccount, CreateUser, UpdateUser, BlockUser,
                    UserLogin, TransferAccount, DeleteAccount, CreateWorkspace,
                    TransferWorkspace, DeleteWorkspace, UpdateWorkspace,
                    CreateSpace, UpdateSpace, SetSpaceVisibility, ReorderSpace,
                    DeleteSpace, CreateFolder, UpdateFolder, DeleteFolder,
                    ReorderFolder, SetFolderVisibility, CreateList, UpdateList,
                    DeleteList, ReorderListInFolder, SetListVisibility,
                    ReorderListInSpace, CreateTask, UpdateTask, ReorderTask,
                    DeleteTask, CreateView, AddMemberToWorkspace, TaskAssignee,
                    ChangeWorkspaceMemberRole, RemoveMemberFromWorkspace,
                    RemoveTaskAssignee, UpdateView, UpdateField, CreateField,
                    DeleteField, ReorderField, ApplyListView, RemoveListView,
                    AddAccountMember, ChangeAccountMemberRole,
                    RemoveAccountMember]


class Query(*QUERY_CLASSES, graphene.ObjectType):
    pass


class Mutation(*MUTATION_CLASSES, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
