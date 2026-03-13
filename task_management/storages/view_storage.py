from typing import Optional

from task_management.exceptions.enums import ViewType
from task_management.interactors.dtos import ViewDTO, CreateViewDTO, \
    ListViewDTO
from task_management.interactors.storage_interfaces.view_storage_interface import \
    ViewStorageInterface
from task_management.models import View, ListView


class ViewStorage(ViewStorageInterface):
    @staticmethod
    def _convert_view_to_dto(view_obj: View) -> ViewDTO:
        view_type = ViewType(view_obj.view_type)
        return ViewDTO(
            view_id=view_obj.view_id,
            name=view_obj.name,
            description=view_obj.description,
            view_type=view_type,
            created_by=view_obj.created_by_id,
        )

    @staticmethod
    def _convert_list_view_to_dto(list_view_obj: ListView) -> ListViewDTO:
        return ListViewDTO(
            id=list_view_obj.pk,
            list_id=list_view_obj.list_id,
            view_id=list_view_obj.view_id,
            applied_by=list_view_obj.applied_by_id,
            is_active=list_view_obj.is_active,
        )

    def get_all_views(self) -> list[ViewDTO]:
        view_objs = View.objects.all()
        return [self._convert_view_to_dto(view_obj=view_obj)
                for view_obj in view_objs]

    def get_view(self, view_id: str) -> ViewDTO:
        view_obj = View.objects.get(view_id=view_id)

        return self._convert_view_to_dto(view_obj=view_obj)

    def create_view(self, create_view_dto: CreateViewDTO) -> ViewDTO:
        view_obj = View.objects.create(
            name=create_view_dto.name,
            view_type=create_view_dto.view_type.value,
            description=create_view_dto.description,
            created_by_id=create_view_dto.created_by)

        return self._convert_view_to_dto(view_obj=view_obj)

    def update_view(
            self, view_id: str, name: Optional[str],
            description: Optional[str]) -> ViewDTO:

        view_properties = {}

        if name is not None:
            view_properties["name"] = name

        if description is not None:
            view_properties["description"] = description

        View.objects.filter(view_id=view_id).update(**view_properties)
        return self.get_view(view_id=view_id)

    def is_view_exists(self, view_id: str) -> bool:

        return View.objects.filter(view_id=view_id).exists()

    def create_list_view(
            self, list_id: str, view_id: str, user_id: str) -> ListViewDTO:
        list_view_obj = ListView.objects.create(
            list_id=list_id, view_id=view_id, applied_by_id=user_id)

        return self._convert_list_view_to_dto(list_view_obj=list_view_obj)

    def remove_list_view(self, view_id: str, list_id: str):
        ListView.objects.filter(list_id=list_id, view_id=view_id).update(
            is_active=False)

        return self.get_list_view(list_id=list_id, view_id=view_id)

    def get_list_views(self, list_id: str) -> list[ListViewDTO]:

        list_view_objs = ListView.objects.filter(
            list_id=list_id, is_active=True)

        return [self._convert_list_view_to_dto(list_view_obj=list_view_obj)
                for list_view_obj in list_view_objs]

    def is_list_view_exist(self, list_id: str, view_id: str) -> bool:
        return ListView.objects.filter(
            list_id=list_id, view_id=view_id).exists()

    def get_list_view(self, list_id: str, view_id: str) -> ListViewDTO | None:
        list_view_dto = ListView.objects.filter(
            list_id=list_id, view_id=view_id, is_active=True).first()

        if list_view_dto is None:
            return None

        return self._convert_list_view_to_dto(list_view_obj=list_view_dto)

    def get_list_view_id(self, view_type: str) -> str:
        return View.objects.filter(view_type=view_type).values_list(
            'view_id', flat=True).first()
