FROM python:3

RUN apt-get update;
RUN apt-get install -y npm
RUN npm install -g configurable-http-proxy

RUN mkdir -p /home/dev/notebooks

RUN python -m venv /opt/jupyterhub
RUN /opt/jupyterhub/bin/pip install --upgrade --no-cache-dir jupyterhub==1.0.0 jupyter notebook pip
RUN /opt/jupyterhub/bin/pip install oauthenticator

# Remove DHS_KEY too small error because of bad configuration of python:3 with keycloak
RUN rm /etc/ssl/openssl.cnf

# # Install valeria authenticator package
# COPY . /usr/local/src/valeria_authenticator
# RUN cd /usr/local/src/valeria_authenticator; /opt/jupyterhub/bin/python setup.py develop

ENTRYPOINT /opt/jupyterhub/bin/jupyterhub --config /etc/jupyterhub/conf/jupyterhub_config.py