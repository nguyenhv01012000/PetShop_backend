from django.db.models import Q
from rest_framework.viewsets import ModelViewSet

from .models import Order
from .serializers import OrderSerializer
from .filters import OrderFilter


class OrderViewSet(ModelViewSet):
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    #filterset_class = OrderFilter

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
    #     return Order.objects.none()
