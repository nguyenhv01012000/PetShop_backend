"""petshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from apps.order.views import OrderViewSet
from apps.products.views import CategoryViewSet, ProductViewSet
from apps.news.views import NewsViewSet
# from chat.views import ChatViewSet
from apps.accounts.views import RegisterAPI,LoginAPI, UserViewSet
from django.contrib import admin
from django.urls import path, include
from knox import views as knox_views
from rest_framework.routers import SimpleRouter

api_router = SimpleRouter(trailing_slash=False)

#users
api_router.register("users", UserViewSet, basename="users")
# api_router.register("chat", ChatViewSet, basename="chat")
api_router.register("news", NewsViewSet, basename="news")
api_router.register("user", UserViewSet, basename="user")
api_router.register("product", ProductViewSet, basename="product")
api_router.register("category", CategoryViewSet, basename="product")
api_router.register("order", OrderViewSet, basename="order")





urlpatterns = [
    path('admin/', admin.site.urls),
    path(r"api/", include(api_router.urls)),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('chat/', include('apps.chatbot.urls', namespace='chatbot')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
