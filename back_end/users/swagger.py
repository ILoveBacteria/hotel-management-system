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
