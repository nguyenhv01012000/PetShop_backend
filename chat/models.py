from django.db import models

class Chat(models.Model):
    userInfo = models.JSONField(null=True)
    chatName = models.TextField(blank=True, null=True)
    chatEmail = models.TextField(blank=True, null=True)
    chatContent = models.JSONField(null=True)
    text = models.TextField(blank=True, null=True)
    sessionId = models.CharField(max_length=100, null=True, blank=True)
    time = models.DateTimeField(auto_now=True)

