from rest_framework.response import Response


def success(message, data=None, status_code=200):

    return Response(
        {
            "success": True,
            "message": message,
            "data": data,
        },
        status=status_code,
    )


def error(message, status_code=400):

    return Response(
        {
            "success": False,
            "message": message,
        },
        status=status_code,
    )