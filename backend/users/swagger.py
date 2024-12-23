from drf_spectacular.utils import extend_schema


current_user_profile = {
    'get': extend_schema(
        summary='Get current user profile',
        description='Permission: This endpoint is only accessible to authenticated users.',
    )
}

description = 'Permission: Admin can get/update any user profile. Users can get/update their own profile.'
user_profile = {
    'put': extend_schema(
        summary='Update user profile by id',
        description=description,
    ),
    'patch': extend_schema(
        summary='Partial update user profile by id',
        description=description,
    ),
    'get': extend_schema(
        summary='Get user profile by id',
        description=description,
    )
}

current_user_reserves_view = {
    'get': extend_schema(
        summary="List current user's reservations",
        description="Retrieve a list of reservations for the currently authenticated user. Permission: Only authenticated users can access their own reservations."
    ),
    'post': extend_schema(
        summary="Create a reservation for the current user",
        description="Create a new reservation for the currently authenticated user. Permission: Only authenticated users can create reservations."
    )
}

user_reserves_view = {
    'get': extend_schema(
        summary="List reservations for a specific user",
        description="Retrieve a list of reservations for a specific user by user ID. Permission: Only admin users can access this endpoint."
    )
}
