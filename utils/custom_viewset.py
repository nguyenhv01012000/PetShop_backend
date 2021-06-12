from django.http import Http404
from rest_framework.viewsets import ModelViewSet

class CustomizeModelViewSet(ModelViewSet):
    not_found_exception = None
    def retrieve(self, request, *args, **kwargs):
        try:
            return super(ModelViewSet, self).retrieve(request, *args, **kwargs)
        except Http404:
            raise self.not_found_exception

    def destroy(self, request, *args, **kwargs):
        try:
            return super(ModelViewSet, self).destroy(request, *args, **kwargs)
        except Http404:
            raise self.not_found_exception

    def update(self, request, *args, **kwargs):
        try:
            return super(ModelViewSet, self).update(request, *args, **kwargs)
        except Http404:
            raise self.not_found_exception

    def partial_update(self, request, *args, **kwargs):
        try:
            return super(ModelViewSet, self).partial_update(request, *args, **kwargs)
        except Http404:
            raise self.not_found_exception

    