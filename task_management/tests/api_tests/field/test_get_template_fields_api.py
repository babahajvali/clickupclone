import pytest

from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import FieldDTO
from task_management.tests.api_tests.field import BaseGetTemplateFields


def get_template_id_by_list_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.get_template_id_by_list_id"
    )


def validate_template_exists_mock(mocker):
    return mocker.patch(
        "task_management.storages.template_storage.TemplateStorage.validate_template_exists"
    )


def get_fields_for_template_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.get_fields_for_template"
    )


def create_field_dto(*, field_id: str, field_name: str, order: int) -> FieldDTO:
    return FieldDTO(
        field_id=field_id,
        field_type=FieldType.TEXT,
        description="Field description",
        template_id="tpl_1",
        field_name=field_name,
        is_deleted=False,
        order=order,
        config={"max_length": 50},
        is_required=True,
        created_by="user_1",
    )


@pytest.mark.django_db
class TestGetTemplateFieldsAPI(BaseGetTemplateFields):

    def test_get_template_fields_successfully(self, snapshot, mocker):
        template_id = get_template_id_by_list_id_mock(mocker)
        template_id.return_value = "tpl_1"

        template_exists = validate_template_exists_mock(mocker)
        template_exists.return_value = True

        fields = get_fields_for_template_mock(mocker)
        fields.return_value = [
            create_field_dto(field_id="field_1", field_name="Priority", order=1),
            create_field_dto(field_id="field_2", field_name="Status", order=2),
        ]

        variables = {"params": {"listId": "list_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )

    def test_get_template_fields_template_not_found(self, snapshot, mocker):
        template_id = get_template_id_by_list_id_mock(mocker)
        template_id.return_value = "tpl_404"

        template_exists = validate_template_exists_mock(mocker)
        template_exists.return_value = False

        variables = {"params": {"listId": "list_404"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )
