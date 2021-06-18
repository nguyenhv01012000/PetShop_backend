"""
ASGI config for petshop project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import apps.chatbot.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "petshop.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.chatbot.routing.websocket_urlpatterns
        )
    ),
})
