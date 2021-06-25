from rest_framework import serializers
from rest_framework.exceptions import APIException
from .models import Chat, Contact
from .utils import get_user_contact

class ContactSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class ChatSerializer(serializers.ModelSerializer):
    participants = ContactSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('id', 'messages', 'participants')
        read_only = ('id')
    
    def create(self, validated_data):
        participants = validated_data.pop('participants')
        #check your list_friend
        check = []
        for username in participants:        
            contact = get_user_contact(username)
            for friend in contact.friends.all():
                check.append(friend.user.username)
            for participant in participants:
                if check.count(participant) == 0:
                    raise APIException("The person is not on your friends list")
            break
        #create Chat()
        chat = Chat()
        chat.save()    
        for username in participants:        
            contact = get_user_contact(username)
            chat.participants.add(contact)
        chat.save()
        
        return chat