from typing import Optional

from task_management.exceptions.enums import ViewType
from task_management.interactors.dtos import ViewDTO, CreateViewDTO, \
    ListViewDTO
from task_management.interactors.storage_interfaces.view_storage_interface import \
    ViewStorageInterface
from task_management.models import View, ListView


class ViewStorage(ViewStorageInterface):
    @staticmethod
    def _convert_view_to_dto(data: View) -> ViewDTO:
        view_type = ViewType(data.view_type)
        return ViewDTO(
            view_id=data.view_id,
            name=data.name,
            description=data.description,
            view_type=view_type,
            created_by=data.created_by.user_id,
        )

    def get_all_views(self) -> list[ViewDTO]:
        views = View.objects.all()
        return [self._convert_view_to_dto(data=view_data) for view_data in
                views]

    def get_view(self, view_id: str) -> ViewDTO:
        view_data = View.objects.get(view_id=view_id)

        return self._convert_view_to_dto(data=view_data)

    def create_view(self, create_view_data: CreateViewDTO) -> ViewDTO:
        view_data = View.objects.create(
            name=create_view_data.name,
            view_type=create_view_data.view_type.value,
            description=create_view_data.description,
            created_by_id=create_view_data.created_by, )

        return self._convert_view_to_dto(data=view_data)

    def update_view(
            self, view_id: str, name: Optional[str],
            description: Optional[str]) -> ViewDTO:

        view_data = View.objects.get(view_id=view_id)

        is_name_provided = name is not None
        if is_name_provided:
            view_data.name = name

        is_description_provided = description is not None
        if is_description_provided:
            view_data.description = description

        view_data.save()

        return self._convert_view_to_dto(data=view_data)

    def check_view_exists(self, view_id: str) -> bool:

        return View.objects.filter(view_id=view_id).exists()

    def apply_view_for_list(
            self, list_id: str, view_id: str, user_id: str) -> ListViewDTO:
        list_view_data = ListView.objects.create(
            list_id=list_id, view_id=view_id, applied_by_id=user_id)
        return ListViewDTO(
            id=list_view_data.pk,
            list_id=list_view_data.list.list_id,
            view_id=list_view_data.view.view_id,
            applied_by=list_view_data.applied_by.user_id,
            is_active=list_view_data.is_active,
        )

    def remove_list_view(self, view_id: str, list_id: str):
        list_view_obj = ListView.objects.get(list_id=list_id, view_id=view_id)
        list_view_obj.is_active = False
        list_view_obj.save(update_fields=["is_active"])

        return ListViewDTO(
            id=list_view_obj.pk,
            list_id=list_id,
            view_id=view_id,
            applied_by=list_view_obj.applied_by.user_id,
            is_active=list_view_obj.is_active,
        )

    def get_list_views(self, list_id: str) -> list[ListViewDTO]:

        list_views = ListView.objects.filter(list_id=list_id, is_active=True)

        return [ListViewDTO(
            id=list_view_data.pk,
            list_id=list_view_data.list.list_id,
            view_id=list_view_data.view.view_id,
            applied_by=list_view_data.applied_by.user_id,
            is_active=list_view_data.is_active,
        ) for list_view_data in list_views]

    def is_list_view_exist(self, list_id: str, view_id: str) -> bool:
        return ListView.objects.filter(
            list_id=list_id, view_id=view_id).exists()

    def get_list_view(self, list_id: str, view_id: str) -> ListViewDTO | None:
        list_view_data = ListView.objects.filter(
            list_id=list_id, view_id=view_id, is_active=True).first()

        if list_view_data is None:
            return None

        return ListViewDTO(
            id=list_view_data.pk,
            list_id=list_view_data.list.list_id,
            view_id=list_view_data.view.view_id,
            applied_by=list_view_data.applied_by.user_id,
            is_active=list_view_data.is_active,
        )

    def get_list_view_id(self, view_type: str) -> str:
        view_data = View.objects.get(view_type=view_type)

        return view_data.view_id
