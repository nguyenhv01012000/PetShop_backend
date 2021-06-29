from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from .models import Chat, Contact
from .utils import get_user_contact
from .serializers import ChatSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
User = get_user_model()

#Used for read-only endpoints to represent a collection of model instances.
#Provides a get method handler.
class ChatListView(ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.AllowAny, )


    # @method_decorator(vary_on_cookie)
    # @method_decorator(cache_page(60*60))
    # def dispatch(self, *args, **kwargs):
    #     return super(ChatListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = Chat.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            contact = get_user_contact(username)
            queryset = contact.chats.all()
        return queryset

#Used for read-only endpoints to represent a signle of model instances.
#Provides a get method handler.
class ChatDetailView(RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.AllowAny, )

#Provides a post method handler.
class ChatCreateView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    #permission_classes = (permissions.IsAuthenticated, )

#Provides put and patch method handlers.
class ChatUpdateView(UpdateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )

#Provides a delete method handler.
class ChatDeleteView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )
