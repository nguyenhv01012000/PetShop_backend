from rest_framework.response import Response


def to_json(
    data=None,
    error=None,
    status=None,
    template_name=None,
    headers=None,
    exception=False,
    content_type=None,
):
    pre_data = {"data": data, "error": error}
    data = {k: v for k, v in pre_data.items() if v is not None}
    return Response(
        data=data, status=status, headers=headers, content_type=content_type
    )

