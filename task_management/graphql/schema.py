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
    ReorderField, ApplyListView, RemoveListView, UpdateFieldValue, \
    ForgotPassword, ResetPassword, ValidateResetToken, UpdateAccount
from task_management.graphql.mutations.subscription_mutations import \
    SubscriptionMutations
from task_management.graphql.queries import GetUser, GetWorkspace, \
    GetWorkspaceSpaces, GetSpace, GetSpaceFolders, GetFolder, GetList, \
    GetFolderLists, GetSpaceLists, GetTaskFilters, GetTask, GetListTasks, \
    GetTaskAssignees, GetViews, GetTemplateFields, GetField, GetListViews, \
    GetUserWorkspaces, GetTaskValues, GetWorkspaceMembers, GetUserTasks, \
    GetListTaskAssignees, GetAccounts, GetUserWithEmail
from task_management.graphql.subscription_queries import SubscriptionQueries

QUERY_CLASSES = [GetUser, GetWorkspace, GetWorkspaceSpaces, GetSpace,
                 GetSpaceFolders, GetFolder, GetList, GetFolderLists,
                 GetSpaceLists, GetTaskFilters, GetTask, GetListTasks,
                 GetTaskAssignees, GetViews, GetTemplateFields, GetField,
                 GetListViews, GetUserWorkspaces, GetTaskValues,
                 GetWorkspaceMembers, GetUserTasks, GetListTaskAssignees,
                 GetAccounts, GetUserWithEmail]

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
                    ResetPassword, UpdateFieldValue, ForgotPassword,
                    ValidateResetToken, UpdateAccount]


class Query(*QUERY_CLASSES,SubscriptionQueries, graphene.ObjectType):
    pass


class Mutation(*MUTATION_CLASSES,SubscriptionMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
