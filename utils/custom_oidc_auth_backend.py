import logging
import json
from datetime import datetime
from calendar import timegm
from josepy.b64 import b64decode
from django.contrib.auth.models import AnonymousUser
from django.utils.encoding import force_bytes
from django.core.exceptions import SuspiciousOperation
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from rest_framework import exceptions
from django.utils.timezone import now
from config.settings.base import (
    ACTIVATED_HOUR_TRIAL,
    AUTHORIZATION_ISSUER,
    ENABLE_TRIAL_HOURS,
)


logger = logging.getLogger(__name__)


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def verify_claims(self, claims):
        """
        Token claim verification must be for authorization on each API scope, 
        but since all APIs use same middleware, we can place here.
        Authentication is simply authorization with identity resources provided
        Please look at OIDC_RP_SCOPES OIDCAuthenticationBackend.verify_claims
        Original backend requires email in claim if relay party scopes contains email
        Reason: This is first-party app, then authentication means full permission on user resources
        """

        # verify validity time range: nbf < now() < exp
        now = timegm(datetime.utcnow().utctimetuple())
        nbf = int(claims["nbf"])
        exp = int(claims["exp"])
        if nbf > now or exp < now:
            return False

        # verify issuer
        if claims["iss"] != AUTHORIZATION_ISSUER:
            return False
        
        # verify audience
        if claims["aud"] != "eclass":
            return False

        return True

    def _update_user_information(self, user, claims):
        need_update = False

        user_email = claims.get("email", None)
        user_email_verified = (
            claims.get("email_verified", False) if user_email else False
        )
        user_email_field = user_email if user_email_verified else None
        user_phone = claims.get("phone_number", None)
        user_phone_verified = (
            claims.get("phone_number_verified", False) if user_phone else False
        )
        user_phone_field = user_phone if user_phone_verified else None
        user_idp = claims.get("idp", "local")

        if user.custom_info is not None:
            user_custom_info = user.custom_info
        else:
            user_custom_info = {"name": claims.get("name", None)}

        user_custom_info["name"] = claims.get("name", None)

        if user_email and not user_email_verified:
            user_custom_info["email"] = user_email

        if user_phone and not user_phone_verified:
            user_custom_info["phone"] = user_phone

        # update email
        if user.email != user_email_field:
            user.email = user_email_field
            need_update = True

        # update email_verified
        if user.email_verified != user_email_verified:
            user.email_verified = user_email_verified
            need_update = True

        # update phone
        if user.phone != user_phone_field:
            user.phone = user_phone_field
            need_update = True

        # update phone_verified
        if user.phone_verified != user_phone_verified:
            user.phone_verified = user_phone_verified
            need_update = True

        # idp, not sure if we need to update this ...
        if user.idp != user_idp:
            user.idp = user_idp
            need_update = True  # set to False if don't need to update this

        # custom information
        if user.custom_info != user_custom_info:
            user.custom_info = user_custom_info
            need_update = True

        if need_update:
            user.save()

    def get_or_create_user(self, access_token, id_token, payload):
        payload_data = None
        try:
            token = force_bytes(access_token)
            if self.OIDC_RP_SIGN_ALGO.startswith("RS"):
                if self.OIDC_RP_IDP_SIGN_KEY is not None:
                    key = self.OIDC_RP_IDP_SIGN_KEY
                else:
                    try:
                        key = self.retrieve_matching_jwk(token)
                    except ValueError as unpack_exception:
                        return None
                    except Exception as retrieve_key_exception:
                        return None
            else:
                key = self.OIDC_RP_CLIENT_SECRET

            try:
                payload_data = self.get_payload_data(token, key)
            except ValueError as unpack_exception:
                return None
            except Exception as decode_exception:
                return None
            else:
                payload_data = json.loads(payload_data.decode("utf-8"))

        except Exception as exc:
            logger.exception(exc)
            return None

        user = None
        if self.verify_claims(payload_data):
            # Try get user from sub field
            sub = int(payload_data["sub"])
            try:  # email and phone now optional and changable but fid is required
                user = self.UserModel.objects.get(fid=sub)
                self._update_user_information(user, payload_data)
            except self.UserModel.DoesNotExist:
                email          = payload_data.get("email", None)
                email_verified = payload_data.get("email_verified", False) if email else False
                phone          = payload_data.get("phone_number", None)
                phone_verified = payload_data.get("phone_number_verified", False) if phone else False
                idp            = payload_data.get("idp", "local")

                custom_info = {
                    "name": payload_data.get("name", None)
                }

                if email_verified:
                    if self.UserModel.objects.filter(email=email):
                        raise exceptions.APIException('Email already exists', code='email_exists')
                else:
                    if email:
                        custom_info["email"] = email
                
                if phone_verified:
                    if self.UserModel.objects.filter(phone=phone):
                        raise exceptions.APIException('Phone already exists', code='phone_exists')
                else:
                    if phone:
                        custom_info["phone"] = phone
                    
                user = self.UserModel(
                    fid=sub,
                    email=email if email_verified else None,
                    email_verified=email_verified,
                    phone=phone if phone_verified else None,
                    phone_verified=phone_verified,
                    idp=idp,
                    custom_info=custom_info,
                )

                user.save()

            # use sub and idp provide in token instead of saved one
            self._validate_activation(user, payload_data)

            # assign preferred_username to username
            user.username = payload_data.get("preferred_username", None)

            return user

        else:
            raise SuspiciousOperation("Claims verification failed")

    def _validate_activation(self, user, claims):

        email = claims.get("email", None)
        email_verified = claims.get("email_verified", False) if email else False
        phone = claims.get("phone_number", None)
        phone_verified = claims.get("phone_number_verified", False) if phone else False
        idp = claims.get("idp", "local")

        # verify email/phone

        if ENABLE_TRIAL_HOURS == 1:
            if not (email_verified or phone_verified or idp != "local"):
                creation_duration = now() - user.date_joined
                if ACTIVATED_HOUR_TRIAL < creation_duration.total_seconds() / 3600:
                    raise exceptions.APIException(
                        "Your account haven't been verified!",
                        "account_verification_failed",
                    )
