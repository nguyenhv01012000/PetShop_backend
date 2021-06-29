from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .models import Chat, Contact

User = get_user_model()


def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('timestamp').all()


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    if Contact.objects.filter(user=user).count() == 0:
        contact = Contact(user=user)
        contact.save()
    return get_object_or_404(Contact, user=user)


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)
