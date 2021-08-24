Chapter 6. Testing Service Resilience with Chaos Testing

# Throwing HTTP Errors
## Chaos Testing of network reliablity and latency
Although microservice-based applications are highly scalable, they also suffer from common problems or fallacies associated with distributed computing.

Chaos Testing is the process of testing a microservices-based application in production or in an environment similar to production by introducing random errors to verify that the steps taken to handle these problems are correct. 

You can use service mesh traffic management capabilities to introduce latency spikes or connection errors in your application so that you can perform chaos testing.

### Throwing HTTP Errors

Use the `HTTPFaultInjection.Abort` object on path `spec.http.fault.abort` to inject errors into the `VirtualService`. These requires two configuration values:
+ **httpStatus** status code returned on abort. It's a literal number representing the HTTP status code.
+ **porcentage** of total request to abort which is configured using a `doble` value, rangin from 0.0 for a 0% to 100.0 for 100%

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
      fault: #1
        abort: #2
          percentage: #3
            value: 20.0
          httpStatus: 400 #4
```

1. The `HTTPFaultInjection` configuration object responsible for all the faults injected into the service.
2. The `HTTPFaultInjection.Abort` configuration object responsible for the error injection configuration.
3. Percentage of the connections to abort.
4. The HTTP status code to return on abort.

When testing your application with HTTP errors, the percentage of failed requests can be lower than your configured value. This is because the virtual service resources contain automatic retries of failed requests.

# Creating Delays in Services
Similar to network errors, network latency must be tested in your application to avoid unexpected errors. During chaos testing you can inject artificial delays into services to simulate latency, verifying that the application handles these problems gracefully.

To inject delays in a VirtualService resource, use the HTTPFaultInjection.Delay object inside the HTTPFaultInjection configuration object and requires two configuration values:
+ **fixedDelay** to add to the conection which it's a value of time (h/m/s/ms).
+ **percentage** of totalrequest into which the delay is injected, using a `doble` value, rangin from 0.0 for a 0% to 100.0 for 100%

### Example
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
    fault: #1
      delay: #2
        percentage: #3
          value: 10.0
        fixedDelay: 400ms #4
```
In the given example we added a 400 ms delay to the 10% of connections to the example-svc service. 

