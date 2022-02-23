# coda19-jupyterhub

Jupyterhub instance used in openshift to do data analysis in the coda19 ecosystem.
The hub is protected by the coda19 keycloak instance.

The base used for this repository is https://github.com/jupyter-on-openshift/jupyterhub-quickstart

# Jupyterhub openshift image stream (Dockerhub)
docker build -f "images\jupyterhub\Dockerfile" -t coda19-jupyterhub:latest "images\jupyterhub"
docker tag coda19-jupyterhub:latest coda19/coda19-jupyterhub:latest
docker push coda19/coda19-jupyterhub:latest

oc apply -f ./images/jupyterhub/image-streams/jupyterhub.json

# Notebooks openshift build images (source to image)
oc apply -f ./images/minimal-notebook/build-configs/s2i-minimal-notebook.json
oc apply -f ./images/scipy-notebook/build-configs/s2i-scipy-notebook.json
oc apply -f ./images/tensorflow-notebook/build-configs/s2i-tensorflow-notebook.json

# Create docker database (developpement purposes only)
oc apply -f ./templates/jupyterhub-db.yaml
oc new-app --template jupyterhub-db --param-file=os-db-dv.env

# Create project openshift
oc apply -f ./templates/jupyterhub-deployer.yaml

oc new-app --template jupyterhub-deployer --param-file=os-dv.env
(Note: must update config maps to use jupyter_config.py and then redeploi jupyterhub)

# Openshift cleanup
oc delete all,configmap,pvc,serviceaccount,rolebinding --selector app=coda19-hub-jupyter

# Persisten volume user storage
oc delete pv jupyterhub-user
oc apply -f ./user-persistent-volume.yaml