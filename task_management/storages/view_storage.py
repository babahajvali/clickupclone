from task_management.exceptions.enums import ViewTypes
from task_management.interactors.dtos import ViewDTO, CreateViewDTO, \
    UpdateViewDTO
from task_management.interactors.storage_interfaces.view_storage_interface import \
    ViewStorageInterface
from task_management.models import View, User


class ViewStorage(ViewStorageInterface):
    @staticmethod
    def _view_dto(data: View) -> ViewDTO:
        view_type = ViewTypes(data.view_type)
        return ViewDTO(
            view_id=data.view_id,
            name=data.name,
            description=data.description,
            view_type=view_type,
            created_by=data.created_by.user_id,
        )

    def get_all_views(self) -> list[ViewDTO]:
        views = View.objects.all()
        return [self._view_dto(data=view_data) for view_data in views]

    def get_view(self, view_id: str) -> ViewDTO:
        view_data = View.objects.get(view_id=view_id)

        return self._view_dto(data=view_data)

    def create_view(self, create_view_data: CreateViewDTO) -> ViewDTO:
        user = User.objects.get(user_id=create_view_data.created_by)
        view_data = View.objects.create(
            name=create_view_data.name,
            view_type=create_view_data.view_type.value,
            description=create_view_data.description, created_by=user)

        return self._view_dto(data=view_data)

    def update_view(self, update_view_data: UpdateViewDTO) -> ViewDTO:
        view_data = View.objects.get(view_id=update_view_data.view_id)
        if update_view_data.name:
            view_data.name = update_view_data.name

        if update_view_data.description:
            view_data.description = update_view_data.description

        view_data.save()

        return self._view_dto(data=view_data)
