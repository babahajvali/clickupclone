from typing import Optional

from task_management.exceptions.custom_exceptions import InvalidOffset, \
    InvalidLimit, InvalidOrder, EmptyTaskTitle, NothingToUpdateTask
from task_management.interactors.dtos import FilterDTO
from task_management.interactors.storage_interfaces import TaskStorageInterface


class TaskValidator:

    def __init__(self, task_storage: TaskStorageInterface):
        self.task_storage = task_storage

    @staticmethod
    def check_filter_parameters(filter_data: FilterDTO):

        if filter_data.offset < 1:
            raise InvalidOffset(
                offset=filter_data.offset,
            )

        if filter_data.limit < 1:
            raise InvalidLimit(
                limit=filter_data.limit)

    def check_task_order(self, list_id: str, order: int):
        if order < 1:
            raise InvalidOrder(order=order)
        tasks_count = self.task_storage.get_tasks_count(
            list_id=list_id)

        if order > tasks_count:
            raise InvalidOrder(order=order)

    @staticmethod
    def check_task_title_not_empty(title: str):

        is_title_empty = not title or not title.strip()
        if is_title_empty:
            raise EmptyTaskTitle(title=title)

    def check_task_update_field_properties(
            self, task_id: str, title: Optional[str],
            description: Optional[str]):

        field_properties_to_update = {}

        is_title_provided = title is not None
        if is_title_provided:
            self.check_task_title_not_empty(title=title)
            field_properties_to_update['title'] = title

        is_description_provided = description is not None
        if is_description_provided:
            field_properties_to_update['description'] = description

        if not field_properties_to_update:
            raise NothingToUpdateTask(task_id=task_id)

    def reorder_task_positions(
            self, list_id: str, current_order: int, new_order: int):

        if new_order > current_order:
            self.task_storage.shift_tasks_down(
                list_id=list_id, current_order=current_order,
                new_order=new_order)
        else:
            self.task_storage.shift_tasks_up(
                list_id=list_id, current_order=current_order,
                new_order=new_order
            )
