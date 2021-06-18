from django.contrib import admin

# Register your models here.
from .models import Message, Chat, Contact

admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(Contact)