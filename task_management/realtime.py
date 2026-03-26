from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def broadcast_task_field_value_updated(
        task_id: str,
        list_id: str,
        field_value_id: int,
        field_id: str,
        value,
        updated_by: str):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    payload = {
        "type": "task.field_value.updated",
        "taskId": task_id,
        "listId": list_id,
        "fieldValueId": field_value_id,
        "fieldId": field_id,
        "value": value,
        "updatedBy": updated_by,
    }

    event = {
        "type": "task_field_value_updated",
        "payload": payload,
    }

    async_to_sync(channel_layer.group_send)(f"task_{task_id}", event)
    async_to_sync(channel_layer.group_send)(f"list_{list_id}", event)
