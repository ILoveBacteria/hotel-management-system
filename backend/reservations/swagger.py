from drf_spectacular.utils import extend_schema


reserve_list_view = {
    'get': extend_schema(
        summary="List all reservations",
        description="Retrieve a list of all reservations. Permission: Only admin users can access this endpoint."
    )
}

reserve_detail_view = {
    'get': extend_schema(
        summary="Retrieve a reservation",
        description="Retrieve details of a specific reservation by ID. Permission: Admin users can access any reservation, while owners can access their own reservations."
    ),
    'put': extend_schema(
        summary="Update a reservation",
        description="Update a specific reservation by ID. Permission: Only admin users can update any reservation."
    ),
    'patch': extend_schema(
        summary="Partially update a reservation",
        description="Partially update a specific reservation by ID. Permission: Only admin users can update any reservation."
    ),
    'delete': extend_schema(
        summary="Delete a reservation",
        description="Delete a specific reservation by ID. Permission: Only admin users can delete any reservation."
    )
}

cancel_reserve_view = {
    'post': extend_schema(
        summary="Cancel a reservation",
        description="Cancel a specific reservation. Permission: Admin users can cancel any reservation, while owners can cancel their own reservations."
    )
}
