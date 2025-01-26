from drf_spectacular.utils import extend_schema, OpenApiExample


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

pay_bill_view = {
    'post': extend_schema(
        summary="Pay a bill",
        description="Pay a bill. Permission: Only bill owners can access this endpoint.",
        responses={
            400: "Bill already paid or overdue",
            302: "Redirect to payment gateway"
        },
        examples=[
            OpenApiExample(
                name='Bill already paid',
                description='Bill already paid',
                value={'message': 'Bill already paid'},
                status_codes=[400],
                response_only=True,
            ),
            OpenApiExample(
                name='Bill is overdue',
                description='Bill is overdue',
                value={'message': 'Bill is overdue.'},
                status_codes=[400],
                response_only=True,
            ),
            OpenApiExample(
                name='Redirect to payment gateway',
                description='Redirect to payment gateway',
                value=None,
                status_codes=[302],
                response_only=True,
            ),
        ]
    )
}
