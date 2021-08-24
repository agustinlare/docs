Chapter 7. Building Resilient Services

# Describing Strategies for Resilient Services with OpenShift Service Mesh
Preparing for resilience is a way to make applications more reliable and ready to overcome some of these challenges. Istio takes reliability into account and includes resilience features as a part of its traffic management model. In particular, virtual services and destination rules enable you to configure flexible resilience strategies at different levels, such as the service level or the subset level.

Resilience strategies include:
+ Use **load balancing** to prevent service overloads by distributing the load among several service replicas sufficient to handle the load. To achieve resiliency with load balancing, you must have at least one redundant replica. Thus, if a replica fails, then the load balancer can redistribute all traffic among the rest of the healthy replicas without overwhelming them.
+ Instead of waiting indefinitely when these errors occur, establish a **time-out** after which the request is rejected
+ **Retries**: Services might be temporarily unavailable due to transient problems, such as network outages or momentary overloads. To address this situation, configure Istio to retry the initially failed request a given number of times.
+ When a service approaches its throughput capacity, additional requests can start failing. You can configure a **circuit breaker** to stop sending traffic to such service. The request fails fast and you protect the service from becoming overloaded, which can cause instability.

## Implementing Service Resilience with Load Balancing

To configure load balancing for resilience at the service level, you must use the `DestinationRule` configuration resource. Specifically, you must set the value of the `spec.trafficPolicy.loadBalancer.simple` field to one of the following algorithms:
+ **ROUND_ROBIN**: Request are sent to each host in turn to distribute the load evenly. This is the default algorithm.
+ **RANDOM**: Request are sent to hosts randmly. Under high loads, request are distributed randomly across instances.
+ **LEAST_CONN**: Request are sent to a host with the few connections. This algorithm picks two random hosts and chooses t he host with the fewest active connections.

### Example
You can define load balancing policies at the subset level, applying specific load balancers to different versions of the same service
```
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: my-destination-rule
spec:
  host: my-svc
  trafficPolicy: #1
    loadBalancer:
      simple: LEAST_CONN
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
    trafficPolicy: #2
      loadBalancer:
        simple: RANDOM
```
1. Traffic policy that applies the LEAST_CONN load balancer to the service.
2. Traffic policy that applies the RANDOM load balancer to the v2 subset, overriding the policy at the service level.

# Configuring Time-outs
OpenShift Service Mesh enables you to configure the time-out outside of your application code, in the Envoy proxy, by using virtual services or HTTP headers.

## Configuring Time-outs in OpenShift Service Mesh
Using OpenShift Service Mesh to manage time-outs enables you to maintain a separation of application business logic and network management.
In OpenShift Service Mesh, you can configure the time-outs using virtual services or HTTP headers without modifying your application code.
> The default time-out for HTTP connections in OpenShift Service Mesh is 15 seconds.

### Configuring Time-outs Using Virtual Services
Virtual services enable you to configure time-outs for all traffic routed to a service. You can apply a time-out setting by using the timeout field in the route rules and assigning a value measured in seconds.
```
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: a-service-vs
spec:
  hosts:
    - example-svc
  http:
    - route:
        - destination:
          host: preference
      timeout: 1s
```
In the preceding example, Envoy waits up to 1 second on any call to the example-svc service before returning a time-out error.

### Configuring Time-outs Using HTTP Headers
In OpenShift Service Mesh, you can use HTTP headers to modify Envoy behavior. The Envoy proxy can add, remove, or modify HTTP headers for incoming requests. When requests with HTTP headers modifying Envoy proxy behaviour are made from outside the mesh, the Envoy proxy ignores them.

In OpenShift Service Mesh, you can use the `PILOT_SIDECAR_USE_REMOTE_ADDRESS` flag to modify how Envoy determines the origin of a connection. Setting the value of `PILOT_SIDECAR_USE_REMOTE_ADDRESS` to `true`, allows you to configure time-outs using headers.

> WARNING: Changing Pilot settings can have unexpected consequences on the stability and behavior of your service mesh.

You can configure time-outs adding the x-envoy-upstream-rq-timeout-ms request HTTP header with a value assigned in milliseconds.

```
HTTP/1.1 200 OK
date: Wed, 13 May 2020 13:56:01 GMT
...output omitted...
x-envoy-upstream-rq-timeout-ms: 500
...output omitted...
```
The preceding example defines a time-out of 500 milliseconds that is only valid until the service responds to that request.

## Selecting Time-outs for Resilience
There is no standard way of calculating a precise value for the time-out, but there are several things to consider when defining a time-out value:
+ The value allows slow responses to arrive.
+ The value stops waiting for a response that is not returned.
+ A high value increases latency, especially in distributed systems.
+ A high value potentially increases computing resources waiting for a dead service to respond.

Time-outs are not the only solution to increase the reliability of your applications. You can combine time-outs with more advanced strategies like retries or circuit breakers.

# Configuring Retry
## Defining the Retry Pattern
The retry pattern is a behavioral design pattern that focuses on reducing transient, short-lived communication failures. Because networks can be unreliable, a microservice might encounter a number of issues during a communication request, such as:
+ A request is lost, mishandled, or dropped due to an overloaded network.
+ A target service experiences a temporary failure, for example, due to storage becoming temporarily disconnected.
+ A subset of target service pods experience a failure.
+ A request response takes longer than expected, resulting in the source service experiencing a time-out.

When a request fails due to any of the errors described above, a repeated request with identical parameters might still succeed. The retry pattern prevents propagation of such transient errors into the application. 

## Configuring Retries in OpenShift Service Mesh
### Configuring Retry Using Virtual Service
```
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: example-vs
spec:
  hosts:
  - example-svc
  http:
  - route:
    - destination:
        host: example-svc
        subset: v1
    retries: #1
      attempts: 3 #2
      perTryTimeout: 2s #3
      retryOn: 5xx,retriable-4xx #4
```

1. The HTTPRetry object responsible for configuring retries.
2. The number of times to resend a request.
3. A time-out value for each retry request. Valid values are in milliseconds ms, seconds s, minutes m, or hours h.
4. A policy that specifies conditions that cause failed requests to retry. The value is a list of comma-separated values.

Virtual services retry failed requests twice by default. To disable the retry configuration, set the attempts parameter of the retry configuration to 0. For example:

```
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: vs-with-no-retry
spec:
  hosts:
  - example-svc
  http:
  - retries:
      attempts: 0
    route:
    - destination:
        host: example-svc
```

### Selecting Retry Policies
The virtual service resource enables you to select one or more retry policies. The Envoy proxy evaluates each failed request using the retry policies. If the Envoy proxy matches a request with any of the selected policies, it retries that request.

OpenShift Service Mesh contains, among others, the following retry policies:
+ **5xx**:
This policy matches any response that contains the 5xx response code. Additionally, this policy matches any requests that do not get a response, such as due to a disconnect, reset, or a read time-out.

> Note that setting the x-envoy-upstream-rq-timeout-ms header overrides the configuration time-out. If a request violates a value set in this header, the response contains the 504 response code, but will not be matched by the 5xx policy.

+ **gateway-error**: This policy matches responses that contain the 502, 503, or 504 response codes.
+ **reset**:This policy matches requests without any response due to disconnect, reset, or read time-out.
+ **retriable-4xx**:
This policy matches request responses that contain the 409 response code.

Note that the list above is not exhaustive. When choosing a retry policy, it is a good practice to first analyze all failed requests in your application and choose the most specific policy for that case. For example, an application pod might take a long time to start, and responds to first requests with a time-out. You can mitigate the issue using the reset retry policy.

### Selecting Retry Parameters for Resiliency
There are no standard values for the retry configuration that are suitable for every environment. The following non-exhaustive list contains some of the considerations for selecting retry parameters:
+ An incorrect retry policy can substantially impact application performance. For example, if the back end application is incorrectly configured, and any requests result in a disconnect response, then retries only increase the overall number of retries with no benefits to the end-user.

+ Increasing the number of retries increases the potential probability for success at the cost of performance. A higher number of retries results in larger network saturation and can cause issues in busy environments.

+ Increasing the time-out value helps to reduce the load for compute-intensive services that can take longer to respond. However, increasing the time-out values also increases the overall latency of your system.

An incorrect retry setting makes your environment less resilient, and can accelerate performance issues in your environment. Other resilience patterns, such as the circuit breaker, can mitigate worst-case retry scenarios. Additionally, Red Hat recommends implementing monitoring to alert you to possible issues as soon as they occur.


# Configuring a Circuit Breaker
## Describing the Circuit Breaker
When a service experiences transient errors, those errors tend to occur continuously. Circuit Breaker uses this knowledge to temporarily avoid directing requests to a failing host. When a request is about to reach a failing host, the circuit breaks, sending a failure to the client without the need to wait for the host to respond. This ban is temporary, so the host receives new requests when normal function is restored.

![07b4ab5292c769f55d0927aa782b5b0d.png](../_resources/36ec042e991747db95e095834a3653c0.png)

Circuit Breaker classifies host failures as two kinds:
+ **Local origin**: Failures are service errors (usually HTTP codes above 500) generated by the service.
+ **Gateway origin**: Failures arise when the service is unreachable or unresponsive, hence it cannot be used.

A Circuit Breaker identifies both kinds of failures and stops sending requests to the failing host, forwarding requests only to healthy hosts. This detection and marking them for eviction is called Outlier Detection.

### Selecting Circuit Breakers for Resilience
Circuit Breakers are useful to protect services prone to transient failures. Compute-intensive services, for example, receive more requests than they can respond to and may experience transient failures more often. Circuit Breakers redirect requests from the host as it starts failing or timing out, so the service has time recover from the increased load.

Other common examples of selecting Circuit Breakers for resilience are services that need to process requests sequentially. Those services usually store pending requests in a queue that they process in order. If this queue becomes too big, the service takes too much time to respond, degrading the service. Circuit Breakers detect those time-outs and give the host time to empty the queue.

## Configuring Circuit Breakers in Openshift Service Mesh
OpenShift Service Mesh implements Circuit Breakers at the host (network) level, not at the service level. That means OpenShift Service Mesh evicts failing hosts, not failing services nor subsets. This behavior allows services to keep functioning even if some subset or some hosts fail.
For example, if you have a service that points to three pods and one of them begins to fail, the eviction applies only to the failing pod. The service is still accessible and it will load balance requests among the two non-failing pods.

> Istio terminology, and consequently OpenShift Service Mesh terminology, can be confusing when referring to a host. In many situations, like in the DestinationRule resource, host refers to a service as an entry in the Kubernetes service registry. However, in the context of Circuit Breakers, host refers to a physical or virtual workload, usually a container.

### Managing Unhealthy Hosts
To enable a Circuit Breaker, include an `outlierDetection` entry in the DestinationRule resource related to the service:
```
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myDestinationRule
spec:
  host: myService 1
  trafficPolicy: 2
    outlierDetection:
      consecutive5xxErrors: 1 3
      interval: 1s 4
      baseEjectionTime: 3m 5
      maxEjectionPercent: 100 6
```

1. `host` does not refer to the physical host, but the service name. 
2. The `outlierDetection` entry belongs to a `trafficPolicy` object.
3. Defines how many `5xx` errors are allowed before evicting the host.
4. The time interval between checking error counts.
5. The *minimum* amount of host ejection time.
6. The *maximum* percentage of evicted hosts belonging to a service at any time.

The value for baseEjectionTime indicates the minimum eviction time for the host, not the actual time. The first time that OpenShift Service Mesh evicts the host, the eviction lasts for approximately the minimum time. Subsequent evictions multiply the baseEjectionTime by the number of times the host is evicted. For example, if baseEjectionTime is five seconds, then the first time the host is evicted, the eviction lasts five seconds. The second time that same host is evicted, the eviction lasts ten seconds. The third time, the eviction lasts fifteen seconds. And so on.

The maxEjectionPercent value limits the percentage of hosts that can simultaneously be in the evicted state. If the current percentage of evicted hosts is higher than this limit, OpenShift Service Mesh evicts no other hosts, even if they fail or are unavailable. This limit is useful to avoid the eviction of all the hosts for a service, making the service unavailable even if some hosts can respond. The default value for maxEjectionPercent is 10%.

### Configuring Connection Limits
Another technique to protect hosts from failing is limiting the number of simultaneous connections to the host. If hosts are prone to time-out or fail when they receive too many requests, limiting the number of connections helps prevent the host from crashing.

OpenShift Service Mesh enables applying those limits using a connectionPool entry in the DestinationRule:

```
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myDestinationRule
spec:
  host: myService
  trafficPolicy:
    connectionPool:
      tcp: #1
        maxConnections: 1 #2
        connectTimeout: 30ms #3
      http: #4
        http1MaxPendingRequests: 1 #5
        maxRequestsPerConnection: 1 #6
```

1. Connection pool settings are divided into `HTTP` and `TCP` settings for clarity.
2. Maximum number of simultaneous connections established to the host.
3. Maximum time to establish the connection.
4. Maximum number of requests pending service by the host.
5. Maximum number of requests permitted on a single connection. OpenShift Service Mesh reuses connections until reaching this limit, or the `tcp.tcpKeepalive` time is consumed.

When limiting the connections to a host, if the threshold is exceeded it will generate service failures, specifically, gateway failures. Those limits can be applied simultaneously with a Circuit Breaker. Failures generated by the connection limit are used by the Circuit Breaker to break the circuit and start eviction policies. However, connection limits and Circuit Breaker are independent traffic policies, and developers can use one of them without the other.

Connection pools apply to every host in the service. That means each host has a connection pool independent from other host pools. If the host depletes its connection pool, OpenShift Service Mesh establishes no more connections to that host, but continues using the rest of the hosts.

[Istio reference documentation for DestinationRule resources](https://istio.io/v1.6/docs/reference/config/networking/destination-rule/#DestinationRule)
