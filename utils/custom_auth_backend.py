import jwt

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header,
)
from django.contrib.auth.models import AnonymousUser
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from apps.users.models import User, Staff
from apps.organizations.models import Organization


class StaffModelAuthenticationBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        organization_name = kwargs.get("organization")
        try:
            staff = Staff.objects.get(
                username=username, organization__subpath=organization_name
            )
        except Staff.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            Staff().set_password(password)
        else:
            if staff.is_active is False:
                raise exceptions.APIException("User is locked.")
            if staff.check_password(password):
                return staff
        return


class JWTAuthentication(BaseAuthentication):
    keyword = "Bearer"

    TOKEN_ID = "id"
    NULL_TOKEN = "null"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth:
            return (AnonymousUser(), None)
        elif len(auth) == 1:
            raise exceptions.AuthenticationFailed(
                "Invalid token header. No credentials provided."
            )
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed("Invalid token header")
        elif auth[0].lower() != b"bearer":
            raise exceptions.AuthenticationFailed("Invalid token header")

        try:
            token = auth[1]
            if token == self.NULL_TOKEN:
                return (AnonymousUser(), None)
        except UnicodeError:
            raise exceptions.AuthenticationFailed(
                "Invalid token header. Token string should not contain invalid characters."
            )
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            staff_id = payload[self.TOKEN_ID]
            staff = Staff.objects.get(id=staff_id)
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed("ExpiredSignature")
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("DecodeError")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("InvalidTokenError")
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User does not exist")
        except Exception:
            return None
        return staff, token

    def authenticate_header(self, request):
        return self.keyword

