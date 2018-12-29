from kubernetes import config, client
import logging

log = logging.getLogger(__name__)

#This should be moved to ouroboros
#This assumes kubernetes config is located in ~/.kube/config
def setupClient():
    config.load_kube_config

def getNamespaceDeployments(namespace):
    if(isNamespace(namespace)):
        api_instance = client.ExtensionsV1beta1Api()
        return api_instance.list_namespaced_deployment(namespace=namespace).items
    else:
        return None

def updateDeployment(imageTag, deploymentName, namespace):
    api_instance = client.ExtensionsV1beta1Api()
    deployments = api_instance.list_namespaced_deployment(namespace=namespace)
    for deployment in deployments:
        if deployment.metadata.name == deploymentName:
            deployment.spec.template.spec.containers[0].image = imageTag
            api_instance.patch_namespaced_deployment(deployment.metadata.name,namespace,deployment)
        else:
            for deployment in deployments:
                old_containers = deployment.spec.template.spec.containers
                new_containers= []
                for container in old_containers:
                    base_image = container.image.split(":")[0]
                    container.image = base_image + ":latest"
                    new_containers.append(container)
                deployment.spec.template.spec.containers = new_containers
                    

def getAllNamespaces():
    api_instance = client.CoreV1Api()
    return api_instance.list_namespace(watch=False).items

def isNamespace(namespace):
    namespaces = getAllNamespaces()
    if namespace in namespaces:
        return True
    return False