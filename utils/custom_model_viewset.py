from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class DynamicFieldViewMixin:
    permission_classes = [AllowAny]
    permission_classes_by_action = {}
    model_class = None 

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_fields(self):
        return []

    def get_default_queryset(self):
        return self.model_class.objects.all()       

    def get_queryset(self):
        return getattr(self,
                       f'get_{self.action}_queryset',
                       self.model_class.objects.none)()

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        kwargs['context']['action'] = self.action
        serializer_class = self.get_serializer_class()
        return serializer_class(*args,
                                fields=getattr(
                                    self, f'get_{self.action}_fields', self.get_fields
                                )(),
                                **kwargs)

class DynamicFieldModelViewSet(DynamicFieldViewMixin,
                                viewsets.ModelViewSet):
    pass


class DynamicFieldReadOnlyModelViewSet(DynamicFieldViewMixin,
                                       viewsets.ReadOnlyModelViewSet):
    pass
