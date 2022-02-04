# coda19-jupyterhub

Jupyterhub instance used in openshift to do data analysis in the coda19 ecosystem.
The hub is protected by the coda19 keycloak instance.

# Create project openshift
oc apply -f ./templates/jupyterhub-builder.yaml
oc apply -f ./templates/jupyterhub-deployer.yaml

oc new-app --template jupyterhub-deployer --param-file=os-dv.env
(Note: must update config maps to use jupyter_config.py)

# Openshift cleanup
oc delete all,configmap,pvc,serviceaccount,rolebinding --selector app=jupyterhub

# Persistent volume db (Temporary)
oc delete pv jupyterhub-db
oc apply -f ./db-persistent-volume.yaml

# Persisten volume user storage
oc delete pv jupyterhub-user
oc apply -f ./user-persistent-volume.yaml