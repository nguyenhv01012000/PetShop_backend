from django_filters import rest_framework as filters

from .models import Chat


class ChatFilter(filters.FilterSet):
    profile = filters.NumberFilter(field_name="profile__pk")
    session = filters.NumberFilter(field_name="session__pk")
    course = filters.NumberFilter(field_name="session__course__pk")

    class Meta:
        model = Chat
        fields = ["profile", "course", "session"]
