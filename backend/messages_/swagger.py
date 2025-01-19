from drf_spectacular.utils import extend_schema

message_create_view = {
    'post': extend_schema(
        summary="Create a message",
        description="Create a new message. Permission: Only authenticated users can create messages."
    )
}

message_list_view = {
    'get': extend_schema(
        summary="List all messages",
        description="Retrieve a list of all messages. Permission: Only admin users can list messages."
    )
}

message_detail_view = {
    'get': extend_schema(
        summary="Retrieve a message",
        description="Retrieve details of a specific message by ID. Permission: Only admin users can retrieve messages."
    ),
    'put': extend_schema(
        summary="Update a message",
        description="Update a specific message by ID. Permission: Only admin users can update messages."
    ),
    'delete': extend_schema(
        summary="Delete a message",
        description="Delete a specific message by ID. Permission: Only admin users can delete messages."
    )
}