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

        self.log.debug(auth_state)
        spawner.environment['OAUTH_TOKEN'] = auth_state['access_token']

    async def authenticate(self, handler, data=None):
        authentication = await super().authenticate(handler, data)
        return authentication


c.OAuthenticator.oauth_callback_url = '{}/hub/oauth_callback'.format(os.environ['JUPYTERHUB_URL'])


class KeycloakMixin(OAuth2Mixin):
    # callback_url
    _OAUTH_AUTHORIZE_URL = '{}/auth'.format(os.environ['JUPYTERHUB_OAUTH_CLIENT_URL'])
    _OAUTH_ACCESS_TOKEN_URL = '{}/token'.format(os.environ['JUPYTERHUB_OAUTH_CLIENT_URL'])

# Note: will be in ansible script


class KeycloakLoginHandler(OAuthLoginHandler, KeycloakMixin):
    pass


class ConcreteCodaAuthenticator(CodaAuthenticator):
    login_service = 'Keycloak'
    login_handler = KeycloakLoginHandler
    client_id = os.environ['JUPYTERHUB_OAUTH_CLIENT_ID']
    client_secret = os.environ['JUPYTERHUB_OAUTH_CLIENT_SECRET']
    userdata_method = 'GET'
    userdata_params = {"state": "state"}

    authorize_url = '{}/auth'.format(os.environ['JUPYTERHUB_OAUTH_CLIENT_URL'])
    token_url = '{}/token'.format(os.environ['JUPYTERHUB_OAUTH_CLIENT_URL'])
    userdata_url = '{}/userinfo'.format(os.environ['JUPYTERHUB_OAUTH_CLIENT_URL'])

    scope = ['openid']
    username_key = "preferred_username"


# Activation
c.JupyterHub.authenticator_class = ConcreteCodaAuthenticator
c.Application.log_level = 'DEBUG'

# Persist auth state in single user instance
c.Authenticator.enable_auth_state = True

# Persisten volumes
c.KubeSpawner.user_storage_pvc_ensure = True

c.KubeSpawner.pvc_name_template = os.environ['NOTEBOOK_USER_PERSISTENT_VOLUME']
c.KubeSpawner.user_storage_capacity = '1Gi'

c.KubeSpawner.volumes = [
    {
        'name': 'data',
        'persistentVolumeClaim': {
            'claimName': c.KubeSpawner.pvc_name_template
        }
    }
]

c.KubeSpawner.volume_mounts = [
    {
        'name': 'data',
        'mountPath': '/opt/app-root/src'
    }
]

c.KubeSpawner.working_dir = '/opt/app-root/src/{username}'


# Kill idle notebooks
c.JupyterHub.services = [
    {
        'name': 'cull-idle',
        'admin': True,
        'command': ['cull-idle-servers', '--timeout=300'],
    }
]

# Jupyterlab
c.KubeSpawner.environment = { 'JUPYTER_ENABLE_LAB': 'true' }
c.Spawner.cmd=["jupyter-labhub"]


# Choice of image
c.KubeSpawner.profile_list = [
    {
        'display_name': 'Minimal Notebook 3.6',
        'default': True,
        'kubespawner_override': {
            'image_spec': 's2i-minimal-notebook:3.6'
        }
    },
    {
        'display_name': 'Scipy Notebook 3.6',
        'kubespawner_override': {
            'image_spec': 's2i-scipy-notebook:3.6'
        }
    }
]