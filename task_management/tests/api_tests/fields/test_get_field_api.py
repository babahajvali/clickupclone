import pytest

from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import FieldDTO
from task_management.tests.api_tests.fields import BaseGetField


def get_field_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.get_field")


def create_field_dto() -> FieldDTO:
    return FieldDTO(
        field_id="field_1",
        field_type=FieldType.TEXT,
        description="Task priority",
        template_id="tpl_1",
        field_name="Priority",
        is_deleted=False,
        order=2,
        config={"max_length": 10},
        is_required=True,
        created_by="user_1",
    )


@pytest.mark.django_db
class TestGetFieldAPI(BaseGetField):

    def test_get_field_successfully(self, snapshot, mocker):
        field_data = get_field_mock(mocker)
        field_data.return_value = create_field_dto()

        variables = {"params": {"fieldId": "field_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )

    def test_get_field_not_found(self, snapshot, mocker):
        field_data = get_field_mock(mocker)
        field_data.return_value = None

        variables = {"params": {"fieldId": "field_404"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )
