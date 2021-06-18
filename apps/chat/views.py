from django.db.models import Q
from rest_framework.viewsets import ModelViewSet

from .models import Chat
from .serializers import ChatSerializer
from .filters import ChatFilter


class ChatViewSet(ModelViewSet):
    model = Chat
    queryset = Chat.objects.order_by("-time")
    serializer_class = ChatSerializer
    #filterset_class = ChatFilter

    # def get_queryset(self):
    #     queryset = self.queryset.all()
    #     user = self.request.user
    #     # super user or student
    #     if isinstance(user, User):
    #         # super user can view all
    #         if user.is_superuser:
    #             return queryset
    #         return queryset.filter(profile__user = user)
    #     # staff
    #     if isinstance(user, Staff):
    #         return queryset.filter(
    #             session__course__branch__organization=self.request.user.organization
    #         )
    #     # anonymous user can't see anything
    #     return Chat.objects.none()
