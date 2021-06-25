from django.db.models import Q
from rest_framework.viewsets import ModelViewSet

from .models import News
from .serializers import NewsSerializer
from .filters import NewsFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
class NewsViewSet(ModelViewSet):
    model = News
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60*60))
    def dispatch(self, *args, **kwargs):
        return super(NewsViewSet, self).dispatch(*args, **kwargs)

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
    #     return News.objects.none()
