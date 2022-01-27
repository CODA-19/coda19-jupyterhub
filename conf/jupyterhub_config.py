
from oauthenticator.oauth2 import OAuthLoginHandler
from tornado.auth import OAuth2Mixin
import os

from oauthenticator.generic import GenericOAuthenticator


class CodaAuthenticator(GenericOAuthenticator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def pre_spawn_start(self, user, spawner):
        auth_state = await user.get_auth_state()
        if not auth_state:
            self.log.warning("AUTH_STATE NOT ENABLED?")
            return
        spawner.environment['OAUTH_TOKEN'] = auth_state['access_token']

    async def authenticate(self, handler, data=None):
        authentication = await super().authenticate(handler, data)
        self.log.debug(f'authentication={authentication}')
        return authentication


c.OAuthenticator.oauth_callback_url = 'http://localhost:8000/hub/oauth_callback'


class KeycloakMixin(OAuth2Mixin):
    # callback_url
    _OAUTH_AUTHORIZE_URL = '{}/auth'.format(os.environ['OAUTH_URL'])
    _OAUTH_ACCESS_TOKEN_URL = '{}/token'.format(os.environ['OAUTH_URL'])

# Note: will be in ansible script


class KeycloakLoginHandler(OAuthLoginHandler, KeycloakMixin):
    pass


class ConcreteCodaAuthenticator(CodaAuthenticator):
    login_service = 'Keycloak'
    login_handler = KeycloakLoginHandler
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    userdata_method = 'GET'
    userdata_params = {"state": "state"}

    authorize_url = '{}/auth'.format(os.environ['OAUTH_URL'])
    token_url = '{}/token'.format(os.environ['OAUTH_URL'])
    userdata_url = '{}/userinfo'.format(os.environ['OAUTH_URL'])

    scope = ['openid']
    username_key = "preferred_username"


# Activation
c.JupyterHub.authenticator_class = ConcreteCodaAuthenticator
c.Application.log_level = 'DEBUG'
