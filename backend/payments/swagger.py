from drf_spectacular.utils import extend_schema


bill_list_view = {
    'get': extend_schema(
        summary="List all bills",
        description="Retrieve a list of all bills. Permission: Only admin users can access this endpoint."
    )
}

bill_detail_view = {
    'get': extend_schema(
        summary="Retrieve a bill",
        description="Retrieve a bill. Permission: Only admin users and bill owners can access this endpoint."
    )
}
