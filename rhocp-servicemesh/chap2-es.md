Chapter 2. Instalando Red Hat OpenShift Service Mesh

# Instalacion
OpenShift Service Mesh es instalado usando la consola web, or CLI, y un operador de Kubernetes. El proceso de instalación requiere primero instalar los operadores requeridos, luego implementar el control plane y finalmente crear un Service Mesh Member Roll.

OpenShift Service Mesh depende de los siguientes operadores:
+ Jaeger
+ Elasticsearch
+ Kiali
+ Service Mesh

![20a88538e3215f37e1caea66da5e51eb.png](../_resources/fc474b7a95ca4b6aac367766b7e32c13.png)

> Red Hat recomienda desplegar el control plane en un projecto separado.

### Creando a Service Mesh Member Roll

El `ServiceMeshMemberRoll` es un custom resource que define los proyectos que pertenecen a un control plane.

Pueden agregarse cualquier numero de projectos al `ServiceMeshMemberRoll`, sin embargo un proyecto puede ser unicamente agregardo a un control plane.

To create or edit a Service Mesh Member Roll, first navigate to the project where Red Hat OpenShift Service Mesh is installed, then navigate to the *Istio Service Mesh Member Roll* page, and finally review and configure installation parameters.

![98a635b6ae8c019afea304edd96c442a.png](../_resources/c54ad73813a544f88e0105d9f3dce1de.png)

