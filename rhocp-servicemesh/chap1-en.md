Chapter 1. Introducing Red Hat OpenShift Service Mesh

# Introduction

**Service mesh** is a technology designed to address microservice architecture problems. Service mesh creates a centralized point to control features for many or all microservices in an application.

Operates at the network communication level. That is, service mesh components capture or intercept traffic to and from microservices, either modifying requests, redirecting them, or creating new requests to other services. Consequently, service mesh provides additional features without requiring code-level changes.

![4e7caaace053e2c43c317f26fb9635ff.png](../_resources/8e5b58ad106b421bbbf066749de8ed42.png)

**OpenShift Service Mesh** incorporates and extends several open source projects and orchestrates them to provide an improved developer experience:

**Istio** is the core implementation of the service mesh architecture for the Kubernetes platform. Istio creates a control plane that centralizes service mesh capabilities and a data plane that creates the structure of the mesh.

The data plane controls communications between services by injecting sidecar containers that capture traffic between microservices.

**Maistra** is an open-source project based on Istio that adapts Istio features to the edge cases of deployment in OpenShift Container Platform. Maistra also adds extended features to Istio, such as simplified multitenancy, explicit sidecar injection, and the use of OpenShift routes instead of Kubernetes ingress.

**Jaeger** is an open source traceability server that centralizes and displays traces associated with a single request. A trace contains information about all services that a request reached. Maistra is responsible for sending the traces to Jaeger and Jaeger is responsible for displaying traces. Microservices in the mesh are responsible for generating request headers needed for other components to generate and aggregate traces.

**ElasticSearch** is an open source, distributed, JSON-based search and analytics engine. Jaeger uses ElasticSearch for storing and indexing the tracing data. ElasticSearch is an optional component for Red Hat OpenShift Service Mesh.

**Kiali** provides service mesh observability. Discovers microservices in the service mesh and their their interactions and visually represents them. It also captures information about communication and services, such as the protocols used, service versions, and failure statistics. 

**Prometheus** is used by OpenShift Service Mesh to store telemetry information from services. Kiali depends on Prometheus to obtain metrics, health status, and mesh topology.

**Grafana** can be used to analyze service mesh metrics. Grafana provides mesh administrators with advanced query and metrics analysis.

# Dificultades en microservicios
Microservice architectures are a method of dividing traditional, monolithic enterprise applications into a set of small, modular services. Using a microservice approach to application development means that each part of your application can scale more easily, is more maintainable, and is ideal for deployment on a cloud platform. This approach has been successful in recent years, including at large companies such as Netflix and Amazon.

Despite introducing many benefits, microservices create several architectural challenges that administrators and developers must understand in order to build a robust and resilient microservices application.

Some of these challenges are related to the development of the microservices themselves.

**Development challenges**
An early issue developers run into is service discovery. Because services are often changing their IP address, each service needs to be easily discoverable and referred to by a static name. Another issue developers encounter is developing for elasticity, or the ability to scale up or down in response to demand. To support elasticity, and leverage one of the most critical benefits of a microservice architecture, developers need to design a system that is scalable as well as have an orchestration solution that appropriately responds to demand.

**Security challenges**
Because microservice architectures imply a high degree of communication, authentication becomes a critical feature. Microservices must validate the requests are authorized, and reject unauthorized requests.

**Operation challenges**
In microservice architectures, a failing microservice or element may cascade the failure, causing a large impact on the application. Microservices must be resilient to failures of peers or dependencies to avoid service failures and service-level agreement (SLA) breaks.

As applications grow, monitoring becomes difficult. In contrast to a monolithic architecture, microservices are by nature distributed, which can make consolidating information challenging.

Developers and administrators require operational features, such as:
+ Monitoring: measuring microservices performance and usage.
+ Centralized logging: capturing and relating logs from all microservices.
+ Tracing: correlating requests to multiple microservices belonging to the same user transaction.

Commonly, developers would implement features such as service resilience in code. This leads to duplicated code and creation of poor separation between service code and network management.

When applications consist of only a few microservices, replicating the same code is not a major problem. When the number of microservices increases, however, maintenance and the ability to make changes grows exponentially more difficult.

# Architecture
Red Hat OpenShift Service Mesh consists of two logical components, a control plane, and a data plane. The following diagram shows the components in the data plane and the control plane:

![7515f13dc5c21c0e16728015526f8132.png](../_resources/b37ec747fa5c4d7384a4a003fe17bd5e.png)

The data plane consists of a set of proxies, which are deployed alongside applications in an OpenShift cluster. The proxies are deployed as sidecars, an auxiliary container running in the same pod as the application, and providing some supplementary functionality.

The control plane manages and configures the proxies. It enforces access control and usage policies and collects metrics from the proxies in the service mesh.

## Data Plane Components
The data plane consists of:
+ A set of **Envoy proxies**.
+ The *istio-agent* component running in each Envoy proxy.

The Envoy proxy is the main component in the data plane. It handles all data flowing between the services in a service mesh. The Envoy proxy also collects all metrics related to the services in the mesh.

![285b04c5b5900e3b142cd7e4154a3753.png](../_resources/889b652f1c5b409f98c7a3be5e2bb5ff.png)

The *istio-agent* component, known also as the *Istio Pilot agent*, is part of every Envoy proxy. It helps to bootstrap the Envoy proxy container during startup. Additionally, it maintains other functions, such as:
+ Automating certificate rotation by communicating with the control plane components.
+ Automating routing information.
+ Automating DNS domain configuration.

Each Envoy proxy contains the pilot-agent binary that controls the Istio Pilot agent.

The control plane can automatically inject an instance of the Envoy proxy as a sidecar to a service whenever that service is deployed to a project that is managed by OpenShift Service Mesh. All incoming (ingress) and outgoing (egress) network traffic between services flows through the proxies.

The service offloads functionality such as access control, network routing and rate limiting, ingress and egress traffic control to the service mesh.

The data plane in a service mesh performs the following tasks:
+ Service discovery: Tracks the services deployed in a mesh.
+ Health checks: Track the state (healthy or unhealthy) of the services deployed in a mesh.
+ Traffic shaping and routing: Control the flow of network data between services. Includes tasks such as throttling the amount of traffic, routing based on content, circuit breaking, controlling the amount of traffic that should be routed among multiple versions of a service, load balancing and more.
+ Security: Perform authentication and authorization, and secure communication using mutual transport layer security (mTLS) between services in a mesh.
+ Metrics and Telemetry: Gather metrics, logs, and distributed tracing information from services in the mesh.

**Control Plan Components**
The control plane manages the configuration and policies for the service mesh. The control plane does not directly handle the network traffic in the mesh, but maintains configuration and policies that are enforced by the data plane.

The control plane consists of the istiod deployment. The istiod deployment consists of a single binary that contains a number of APIs used by the OpenShift Service Mesh.

Istiod contains the APIs and functionality of the following components:
+ Pilot: Maintains the configuration data for the service mesh. Provides service discovery for the Envoy proxy sidecars, traffic management capabilities for intelligent routing (for example, A/B tests), and resiliency (timeouts, retries, and circuit breakers).
+ Citadel: Issues and rotates TLS certificates. Provides authentication for inter-service communication, with built-in identity and credential management. You can enforce policies based on service identity rather than relying on network details such as IP addresses and host names.
+ Galley: Monitors the service mesh configuration and then validates, processes, and distributes the configuration to the proxies.