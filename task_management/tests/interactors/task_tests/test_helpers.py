from task_management.exceptions.enums import Role
from task_management.interactors.dtos import (
    CreateTaskDTO,
    TaskAssigneeDTO,
    TaskDTO,
    UserTasksDTO,
    WorkspaceMemberDTO,
)


def make_permission(role: Role = Role.MEMBER) -> WorkspaceMemberDTO:
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_1",
        role=role,
        user_id="user_1",
        is_active=True,
        added_by="admin_1",
    )


def make_list(is_deleted: bool = False):
    return type("List", (), {"is_deleted": is_deleted})()


def make_task(
        task_id: str = "task_1",
        title: str = "Task Title",
        description: str = "Task description",
        list_id: str = "list_1",
        order: int = 1,
        created_by: str = "user_1",
        is_deleted: bool = False,
) -> TaskDTO:
    return TaskDTO(
        task_id=task_id,
        title=title,
        description=description,
        list_id=list_id,
        order=order,
        created_by=created_by,
        is_deleted=is_deleted,
    )


def make_create_task_input() -> CreateTaskDTO:
    return CreateTaskDTO(
        title="New Task",
        description="Task description",
        list_id="list_1",
        created_by="user_1",
    )


def make_user(is_active: bool = True):
    return type("User", (), {"is_active": is_active})()


def make_task_data(is_deleted: bool = False):
    return type("Task", (), {"is_deleted": is_deleted, "list_id": "list_1"})()


def make_task_assignee(
        assign_id: str = "assign_1",
        task_id: str = "task_1",
        user_id: str = "user_2",
        assigned_by: str = "user_1",
        is_active: bool = True,
) -> TaskAssigneeDTO:
    return TaskAssigneeDTO(
        assign_id=assign_id,
        task_id=task_id,
        user_id=user_id,
        assigned_by=assigned_by,
        is_active=is_active,
    )


def make_user_tasks() -> UserTasksDTO:
    return UserTasksDTO(
        user_id="user_2",
        tasks=[
            TaskDTO(
                task_id="task_1",
                title="Task 1",
                description="Task 1 description",
                list_id="list_1",
                order=1,
                created_by="user_1",
                is_deleted=False,
            ),
            TaskDTO(
                task_id="task_2",
                title="Task 2",
                description="Task 2 description",
                list_id="list_1",
                order=2,
                created_by="user_1",
                is_deleted=False,
            ),
        ],
    )
