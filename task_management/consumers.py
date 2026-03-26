from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from task_management.storages import ListStorage, TaskStorage, WorkspaceStorage


class TaskUpdatesConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope.get("user_id")
        self.task_id = self.scope["url_route"]["kwargs"].get("task_id")
        self.list_id = self.scope["url_route"]["kwargs"].get("list_id")

        if not self.user_id:
            await self.close(code=4401)
            return

        self.group_name = await self._get_group_name()
        if not self.group_name:
            await self.close(code=4403)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_json({
            "type": "subscription.ready",
            "group": self.group_name,
        })

    async def disconnect(self, close_code):
        if hasattr(self, "group_name") and self.group_name:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name,
            )

    async def receive_json(self, content, **kwargs):
        if content.get("type") == "ping":
            await self.send_json({"type": "pong"})

    async def task_field_value_updated(self, event):
        await self.send_json(event["payload"])

    @database_sync_to_async
    def _get_group_name(self) -> str | None:
        workspace_storage = WorkspaceStorage()

        if self.task_id:
            task_storage = TaskStorage()
            workspace_id = task_storage.get_workspace_id_from_task_id(
                task_id=self.task_id
            )
            if not workspace_id:
                return None

            membership = workspace_storage.get_workspace_member(
                workspace_id=workspace_id,
                user_id=self.user_id,
            )
            if not membership or not membership.is_active:
                return None

            return f"task_{self.task_id}"

        if self.list_id:
            list_storage = ListStorage()
            workspace_id = list_storage.get_workspace_id_by_list_id(
                list_id=self.list_id
            )
            membership = workspace_storage.get_workspace_member(
                workspace_id=workspace_id,
                user_id=self.user_id,
            )
            if not membership or not membership.is_active:
                return None

            return f"list_{self.list_id}"

        return None
