# coda19-jupyterhub

Jupyterhub instance used in openshift to do data analysis in the coda19 ecosystem.
The hub is protected by the coda19 keycloak instance.

# Create project openshift
oc apply -f ./templates/jupyterhub-builder.yaml
oc apply -f ./templates/jupyterhub-deployer.yaml
oc apply -f ./templates/jupyterhub-quickstart.yaml
oc apply -f ./templates/jupyterhub-workspace.yaml

oc new-app --template jupyterhub-deployer

# With jupyterhub_config.py
oc new-app --template jupyterhub-deployer --param JUPYTERHUB_CONFIG="$(cat minimal_jupyterhub_config.py)"
(Note: must update config maps as file passe in environnement variable is single lines)

# Openshift cleanup
oc delete all,configmap,pvc,serviceaccount,rolebinding --selector app=jupyterhub

# Persistent volume (Temporary)
oc delete pv jupyterhub-db
oc apply -f ./persistent-volume.yaml