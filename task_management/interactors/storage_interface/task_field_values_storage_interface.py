from abc import ABC, abstractmethod

from task_management.interactors.dtos import UpdateFieldValueDTO, \
    TaskFieldValuesDTO, TaskFieldValueDTO, CreateFieldValueDTO


class FieldValueStorageInterface(ABC):

    @abstractmethod
    def set_task_field_value(self, field_value_data: UpdateFieldValueDTO) -> \
            TaskFieldValueDTO:
        # set field value
        pass

    @abstractmethod
    def get_field_values_by_task_ids(self, task_ids: list[str]) -> list[
        TaskFieldValuesDTO]:
        # get task field values
        pass

    @abstractmethod
    def create_bulk_field_values(self, bulk_field_values: list[
        CreateFieldValueDTO]):
        pass
