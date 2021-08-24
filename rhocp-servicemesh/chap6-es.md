Chapter 6. Testeando Resiliencia de Servicios con Chaos Testing

# Throwing HTTP Errors
## Chaos Testing de resilencia y latencia de red
Aunque las aplicaciones basadas en microservicios son altamente escalables, también adolecen de problemas o falacias comunes asociados con la computación distribuida.

Chaos Testing es el proceso de probar una aplicación basada en microservicios en producción o en un entorno similar a la producción mediante la introducción de errores aleatorios para verificar que los pasos tomados para manejar estos problemas sean correctos.

Puede utilizar las capacidades de gestión del tráfico de Service Mesh para introducir picos de latencia o errores de conexión en su aplicación para poder realizar pruebas de caos.

### Throwing HTTP Errors
Use el `HTTPFaultInjection.Abort` objeto en el path `spec.http.fault.abort` para injectar errores en el `VirtualService`. 

Esto requiere de dos valores de configuracion:
+ **httpStatus** status code que devuelve en el fallo.
+ **porcentage** de un total de request para fallar.
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

1. El objeto de configuración `HTTPFaultInjection` responsable de todas las fallas inyectadas en el servicio.
2. El objeto de configuración `HTTPFaultInjection.Abort` responsable de la configuración de inyección de error.
3. Porcentaje de conexiones a abortar.
4. El status code HTTP para devolver al fallar.

Al probar su aplicación con errores HTTP, el porcentaje de solicitudes fallidas puede ser menor que su valor configurado. Esto se debe a que los recursos del `VirtualService` contienen reintentos automáticos de solicitudes fallidas.

# Creando Delays en Servicios
De manera similar a los errores de red, la latencia de la red debe probarse en su aplicación para evitar errores inesperados. Durante las pruebas de caos, puede inyectar retrasos artificiales en los servicios para simular la latencia, verificando que la aplicación maneje estos problemas correctamente.

Para inyectar retrasos en un recurso `VirtualService`, use el objeto` HTTPFaultInjection.Delay` dentro del objeto de configuración `HTTPFaultInjection` y requiere dos valores de configuración:
+ **FixedDelay** para agregar a la conexión que es un valor de tiempo (h/m/s/ms).
+ **porcentaje** de la solicitud total en la que se inyecta el retraso.

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
En el ejemplo dado, agregamos un retraso de 400 ms al 10% de las conexiones al servicio example-svc.

