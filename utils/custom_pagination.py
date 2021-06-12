from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"


class CustomCursorPagination(pagination.CursorPagination):
    page_size_query_param = 'limit'
    ordering = "-created_at"

    def paginate_queryset(self, queryset, request, view=None):
        self.total = queryset.count()
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': len(self.page),
            'total': self.total,
            'results': data
        })
