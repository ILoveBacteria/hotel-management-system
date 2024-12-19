from drf_spectacular.utils import extend_schema


room_viewset = {
    'list': extend_schema(
        summary="List all rooms",
        description="Retrieve a list of all rooms. Permission: Admin users can manage rooms, while others have read-only access."
    ),
    'retrieve': extend_schema(
        summary="Retrieve a room",
        description="Retrieve details of a specific room by ID. Permission: Admin users can manage rooms, while others have read-only access."
    ),
    'destroy': extend_schema(
        summary="Delete a room",
        description="Delete a specific room by ID. Permission: Only admin users can delete rooms."
    ),
    'update': extend_schema(
        summary="Update a room",
        description="Update a specific room by ID. Permission: Only admin users can update rooms."
    )
}

room_type_viewset = {
    'list': extend_schema(
        summary="List all room types",
        description="Retrieve a list of all room types. Permission: Admin users can manage room types, while others have read-only access."
    ),
    'retrieve': extend_schema(
        summary="Retrieve a room type",
        description="Retrieve details of a specific room type by ID. Permission: Admin users can manage room types, while others have read-only access."
    ),
    'create': extend_schema(
        summary="Create a room type",
        description="Create a new room type. Permission: Only admin users can create room types."
    ),
    'update': extend_schema(
        summary="Update a room type",
        description="Update a specific room type by ID. Permission: Only admin users can update room types."
    ),
    'destroy': extend_schema(
        summary="Delete a room type",
        description="Delete a specific room type by ID. Permission: Only admin users can delete room types."
    )
}

room_image_viewset = {
    'list': extend_schema(
        summary="List all room images",
        description="Retrieve a list of all room images. Permission: Admin users can manage room images, while others have read-only access."
    ),
    'retrieve': extend_schema(
        summary="Retrieve a room image",
        description="Retrieve details of a specific room image by ID. Permission: Admin users can manage room images, while others have read-only access."
    ),
    'destroy': extend_schema(
        summary="Delete a room image",
        description="Delete a specific room image by ID. Permission: Only admin users can delete room images."
    ),
    'update': extend_schema(
        summary="Update a room image",
        description="Update a specific room image by ID. Permission: Only admin users can update room images."
    )
}

room_type_image_viewset = {
    'list': extend_schema(
        summary="List images for a room type",
        description="Retrieve all images associated with a specific room type. Permission: Admin users can manage images, while others have read-only access."
    ),
    'retrieve': extend_schema(
        summary="Retrieve a room type image",
        description="Retrieve details of a specific image associated with a room type. Permission: Admin users can manage images, while others have read-only access."
    ),
    'create': extend_schema(
        summary="Add an image to a room type",
        description="Add a new image to a specific room type. Permission: Only admin users can add images."
    )
}

room_type_inventory_viewset = {
    'list': extend_schema(
        summary="List inventory for a room type",
        description="Retrieve all rooms in the inventory for a specific room type. Permission: Admin users can manage inventory, while others have read-only access."
    ),
    'retrieve': extend_schema(
        summary="Retrieve inventory for a room type",
        description="Retrieve details of a specific room in the inventory for a room type. Permission: Admin users can manage inventory, while others have read-only access."
    ),
    'create': extend_schema(
        summary="Add inventory to a room type",
        description="Add a new room to the inventory for a specific room type. Permission: Only admin users can add inventory."
    )
}
