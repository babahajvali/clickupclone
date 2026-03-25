from typing import Optional

from task_management.exceptions.enums import ListEntityType
from task_management.interactors.dtos import TemplateDTO, CreateTemplateDTO
from task_management.interactors.storage_interfaces.template_storage_interface import \
    TemplateStorageInterface
from task_management.models import Template, Space, Folder


class TemplateStorage(TemplateStorageInterface):

    @staticmethod
    def _convert_template_to_dto(template_obj: Template) -> TemplateDTO:
        return TemplateDTO(
            template_id=template_obj.template_id,
            name=template_obj.name,
            description=template_obj.description,
            list_id=template_obj.list_id,
            created_by=template_obj.list.created_by_id,
        )

    def get_template(self, template_id: str) -> TemplateDTO | None:
        template_obj = Template.objects.filter(template_id=template_id).first()

        if template_obj is None:
            return None

        return self._convert_template_to_dto(template_obj=template_obj)

    def create_template(
            self, create_template_dto: CreateTemplateDTO) -> TemplateDTO:

        template_obj = Template.objects.create(
            name=create_template_dto.name,
            description=create_template_dto.description,
            list_id=create_template_dto.list_id)

        return self._convert_template_to_dto(template_obj=template_obj)

    def validate_template_exists(self, template_id: str) -> bool:
        return Template.objects.filter(template_id=template_id).exists()

    def update_template(
            self, template_id: str, name: Optional[str],
            description: Optional[str]) -> TemplateDTO:

        template_properties = {}

        if name is not None:
            template_properties["name"] = name

        if description is not None:
            template_properties["description"] = description

        Template.objects.filter(template_id=template_id).update(
            **template_properties)

        return self.get_template(template_id=template_id)

    def get_workspace_id_from_template_id(
            self, template_id: str) -> str | None:
        template_obj = Template.objects.select_related("list").values(
            "list__entity_type", "list__entity_id",
        ).filter(template_id=template_id).first()

        if template_obj is None:
            return None

        entity_type = template_obj["list__entity_type"]
        entity_id = template_obj["list__entity_id"]

        if entity_type == ListEntityType.SPACE.value:
            return str(Space.objects.values_list(
                "workspace_id", flat=True
            ).get(space_id=entity_id))

        return str(Folder.objects.values_list(
            "space__workspace_id", flat=True
        ).get(folder_id=entity_id))
