from typing import Optional

from task_management.interactors.dtos import TemplateDTO, CreateTemplateDTO
from task_management.interactors.storage_interfaces.template_storage_interface import \
    TemplateStorageInterface
from task_management.models import Template


class TemplateStorage(TemplateStorageInterface):

    @staticmethod
    def _template_dto(data: Template) -> TemplateDTO:
        return TemplateDTO(
            template_id=data.template_id,
            name=data.name,
            description=data.description,
            list_id=data.list.list_id,
            created_by=data.list.created_by.user_id,
        )

    def get_template(self, template_id: str) -> TemplateDTO:
        template_data = Template.objects.get(template_id=template_id)

        return self._template_dto(data=template_data)

    def create_template(self, template_data: CreateTemplateDTO) -> TemplateDTO:

        template_data = Template.objects.create(
            name=template_data.name, description=template_data.description,
            list_id=template_data.list_id)

        return self._template_dto(data=template_data)

    def validate_template_exists(self, template_id: str) -> bool:
        return Template.objects.filter(template_id=template_id).exists()

    def update_template(
            self, template_id: str, name: Optional[str],
            description: Optional[str]) -> TemplateDTO:

        template_data = Template.objects.get(template_id=template_id)

        is_name_provided = name is not None
        if is_name_provided:
            template_data.name = name

        is_description_provided = description is not None
        if is_description_provided:
            template_data.description = description

        template_data.save()

        return self._template_dto(data=template_data)

    def get_template_list_id(self, template_id: str) -> str:
        return Template.objects.filter(list_id=template_id).values_list(
            'list_id', flat=True)[0]

    def get_workspace_id_from_template_id(
            self, template_id: str) -> str | None:
        template_data = Template.objects.select_related(
            "list__space__workspace").filter(
            template_id=template_id).first()

        if template_data is None:
            return None

        return template_data.list.space.workspace.workspace_id
