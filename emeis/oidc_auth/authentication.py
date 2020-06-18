import base64
import functools
import hashlib

import requests
from django.core.cache import cache
from django.core.exceptions import SuspiciousOperation
from django.utils.encoding import force_bytes
from mozilla_django_oidc.auth import LOGGER, OIDCAuthenticationBackend


class EmeisAuthenticationBackend(OIDCAuthenticationBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.OIDC_USERNAME_CLAIM = self.get_settings("OIDC_USERNAME_CLAIM")
        self.OIDC_EMAIL_CLAIM = self.get_settings("OIDC_EMAIL_CLAIM")
        self.OIDC_OP_INTROSPECT_ENDPOINT = self.get_settings(
            "OIDC_OP_INTROSPECT_ENDPOINT"
        )
        self.OIDC_BEARER_TOKEN_REVALIDATION_TIME = self.get_settings(
            "OIDC_BEARER_TOKEN_REVALIDATION_TIME"
        )
        self.OIDC_VERIFY_SSL = self.get_settings("OIDC_VERIFY_SSL", True)

    def get_introspection(self, access_token, id_token, payload):
        """Return user details dictionary."""

        basic = base64.b64encode(
            f"{self.OIDC_RP_CLIENT_ID}:{self.OIDC_RP_CLIENT_SECRET}".encode("utf-8")
        ).decode()
        headers = {
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.post(
            self.OIDC_OP_INTROSPECT_ENDPOINT,
            verify=self.OIDC_VERIFY_SSL,
            headers=headers,
            data={"token": access_token},
        )
        response.raise_for_status()
        return response.json()

    def get_userinfo_or_introspection(self, access_token) -> dict:
        try:
            claims = self.cached_request(
                self.get_userinfo, access_token, "auth.userinfo"
            )
        except requests.HTTPError as e:
            if not (
                e.response.status_code in [401, 403]
                and self.OIDC_OP_INTROSPECT_ENDPOINT
            ):
                raise e

            # check introspection if userinfo fails (confidental client)
            claims = self.cached_request(
                self.get_introspection, access_token, "auth.introspection"
            )
            if "client_id" not in claims:
                raise SuspiciousOperation("client_id not present in introspection")

        return claims

    def get_or_create_user(self, access_token, id_token, payload):
        """Verify claims and return user, otherwise raise an Exception."""

        claims = self.get_userinfo_or_introspection(access_token)
        username = self.get_username(claims)
        users = self.filter_users_by_claims(claims)

        if len(users) == 1:
            if self.get_settings("OIDC_UPDATE_USER", False):
                return self.update_user(users[0], claims)
            return users[0]
        elif self.get_settings("OIDC_CREATE_USER", False):
            return self.create_user(claims)
        else:
            LOGGER.debug(
                "Login failed: No user with username %s found, and "
                "OIDC_CREATE_USER is False",
                username,
            )
            return None

    def filter_users_by_claims(self, claims):
        return self.UserModel.objects.filter(username=self.get_username(claims))

    def cached_request(self, method, token, cache_prefix):
        token_hash = hashlib.sha256(force_bytes(token)).hexdigest()

        func = functools.partial(method, token, None, None)

        return cache.get_or_set(
            f"{cache_prefix}.{token_hash}",
            func,
            timeout=self.OIDC_BEARER_TOKEN_REVALIDATION_TIME,
        )

    def get_username(self, claims):
        try:
            return claims[self.OIDC_USERNAME_CLAIM]
        except KeyError:
            raise SuspiciousOperation("Couldn't find username claim")

    def create_user(self, claims):
        """Return object for a newly created user account."""
        email = claims.get(self.OIDC_EMAIL_CLAIM)
        username = self.get_username(claims)
        return self.UserModel.objects.create(username=username, email=email)

    def update_user(self, user, claims):
        """Update existing user with new claims, if necessary save, and return user."""
        email = claims.get(self.OIDC_EMAIL_CLAIM)
        if email and user.email != email:
            user.email = email
            user.save()
        return user
