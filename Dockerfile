FROM jupyterhub/jupyterhub

# Settup ssl certificate
RUN apt-get update && apt-get upgrade -y

RUN openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -nodes \
  -keyout /srv/jupyterhub/jhubssl.key \
  -out /srv/jupyterhub/jhubssl.crt \
  -subj "/C=DE/ST=xx/L=xx/O=TUHH/OU=xx/CN=xxxx Self-Signed" \
  -addext "subjectAltName=DNS:localhost,DNS:jhub,DNS:jupyterhub,IP:127.0.0.1" \
  && cp /srv/jupyterhub/jhubssl.crt /usr/local/share/ca-certificates/ \
  && chmod 644 /usr/local/share/ca-certificates/jhubssl.crt \
  && dpkg-reconfigure ca-certificates \
  && update-ca-certificates --fresh

ENV PYCURL_SSL_LIBRARY=openssl
RUN apt-get -y install python3-dev gcc curl libcurl3-openssl-dev \
  && pip install --no-input --ignore-installed --force-reinstall pycurl

# Setup jupyterhub
ADD /conf/jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

RUN pip install jupyter oauthenticator

# # User configuration
RUN useradd -ms /bin/bash jupyteruser
RUN useradd -ms /bin/bash testuser