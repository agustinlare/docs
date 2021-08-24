Chapter 5. Desplegando Aplicaicones con OpenShift Service Mesh

# Describiendo Canary Releases
Los Canary Releases utilizan un enfoque de implementación progresivo y seguro en el que ambas versiones de la aplicación, la antigua y la nueva, se ejecutan en paralelo hasta que la nueva versión está completamente validada y lista para todos los usuarios. La nueva versión, también llamada canary, inicialmente recibe solo una pequeña cantidad de todo el tráfico de aplicaciones. Por lo tanto, si algo sale mal con esta nueva versión de la aplicación, un número mínimo de usuarios se verá afectado. A medida que gana confianza en el funcionamiento del canario, dirige progresivamente más tráfico hacia él.

[canary_release_animation.mp4](../_resources/0916131199c247849c52be03b2b4e605.mp4)

### Casos de uso
Despliegues canary son una buena estrategia siempre que desee tener más control y aumentar el nivel de confianza en sus implementaciones. Los siguientes casos son escenarios en los que un enfoque de canary release tiene sentido:

+ Su aplicación maneja cargas elevadas y desea realizar pruebas de carga o estrés en una nueva versión.
+ Desea validar la nueva versión con un grupo reducido de usuarios para analizar cómo esto afecta sus indicadores clave de rendimiento. Los grupos de usuarios se pueden definir según diferentes condiciones, como el tipo de usuario o la ubicación. Por ejemplo, un escenario común es la liberación de canarios solo para usuarios internos o clientes de confianza.
+ Necesita una estrategia segura para implementar una nueva versión crítica.

## Desplegando un Canary Release with OpenShift Service Mesh
Istio ofrece varias políticas de enrutamiento de tráfico, por lo que no está restringido a una estrategia basada en el porcentaje de tráfico.

Los `VirtualServices`, en combinación con las `DestionationRules`, pueden definir rutas de tráfico para cada versión. Cada versión se publica como una implementación y está representada por un subbset de `DestinationRules`, que filtra los puntos finales del servicio para esa versión.

![f08e132f67d2eedb13983b10e5c8702b.png](../_resources/1b95479d8c1541c78c5a91fc85d2adc3.png)

La imagen anterior muestra cómo se relacionan estos recursos de configuración en el escenario de canary.

### Ejemplo
Desplegamos una aplicación llamada `myapp` que se parece a lo siguiente:
```
apiVersion: v1
kind: Service
metadata:
  labels:
    app: myapp
  name: myapp
spec:
  selector:
    app: myapp
  ...
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-v1
spec:
  ...
  template:
    metadata:
      labels:
        app: myapp
        version: v1
      annotations:
        sidecar.istio.io/inject: "true"
    spec:
        ...
```

Preste especial atención a la etiqueta `version` del `deployment`. Las etiquetas son la propiedad principal que se utiliza para identificar la versión de la aplicación y para dividir el tráfico entre versiones. También tenga en cuenta que debe habilitar la inyección del sidecar Envoy configurando la anotación `sidecar.istio.io/inject` en"`true`". Esto permite que la aplicación utilice las funciones de enrutamiento de Istio.

**Canary Release** 
Para desplegar un Canary Release, debe crear un nuevo deployment para la nueva versión y dividir el tráfico entre las versiones mediante un `VirtualService` y un `DestinationRule`.
```
kind: Deployment
metadata:
  name: myapp-v2
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: myapp
        version: v2
      annotations:
        sidecar.istio.io/inject: "true"
    spec:
      containers:
        ...
```
Como se muestra en el deployment previo usamos un unique name nuevo para este deployment y el label usado es el mismo que el del viejo deployment por lo que el servicio esta al tanto de que una nueva version pertenece a la misma aplicacion que la anterior version, y especificamos un nuevo valor del label version para que Service Mesh pueda distinguir entre versiones cuando routee trafico.

Creamos un `DestinationRule` para definir un subset que respente cada version.

```
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
spec:
  host: myapp #1
  subsets:
    - name: v1 #2
      labels:
        version: v1
    - name: v2 #3
      labels:
        version: v2
```
La `DestionationRule` define la siguiente configuración:
1. El nombre del servicio objetivo.
2. Un subset para v1, etiquetas de filtrado especificadas en la implementación de myapp-v1. En este caso, la versión: v1.
3. Un subset para v2, etiquetas de filtrado especificadas en la implementación de myapp-v2. En este caso, la versión: v2.

Creamos un `VirtualService` para deinfir el traifco redireccionado para cada versión. Asociando cada subconjunto con una ruta destino y agregamos la carga.
```
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
    - "*"
  gateways:
    - my-gateway
  http:
    - route:
      - destination:
          host: myapp #1
          subset: v1 #2
          port:
            number: 3000
        weight: 90 #3
      - destination:
          host: myapp
          subset: v2
          port:
            number: 3000
        weight: 10
```
Hay dos configuraciones de destino definidas en este `VirtualService`, una para cada versión. v1 recibe el 90% del tráfico, mientras que v2 recibe el 10% restante. Cada destino debe contener la siguiente información:

1. El nombre de host del servicio. Debe ser el mismo que el campo de host definido en la `DestinationRule`.
2. El nombre de uno de los subset definidos en la `DestionationRule` asociada.
3. El porcentaje de tráfico enrutado a la versión.

Si necesita enrutar el tráfico con criterios más avanzados, puede usar `spec.http.match` para el tráfico HTTP o `spec.tcp.match` para el tráfico TCP.

### Dividir Trafico usando Kiali
Con Kiali, puede editar la configuración de las funciones de gestión del tráfico de Istio para controlar los Canary Releases. En particular, puede editar archivos de recursos en formato yaml para modificar la configuración de los recursos de Istio. También puede utilizar asistentes de gestión de tráfico para equilibrar el tráfico entre versiones en una interfaz fácil de usar.

[Kiali: Service mesh observability and configuration](https://kiali.io/documentation/v1.24/features/#_istio_wizards)

# Desplegar una Aplicacion con Mirror Launch
## Probar en Produccion
Al lanzar nuevas versiones de servicios, a menudo es necesario probar las nuevas versiones de los servicios en un entorno de producción. Las pruebas en producción son importantes porque es difícil simular cargas de trabajo de producción o datos de producción realistas en entornos de prueba o de ensayo.

Las pruebas en producción consisten en:
+ Implementar la nueva versión del servicio en un entorno de producción junto con la versión existente del servicio.
+ Envío de una copia del tráfico de producción tanto al nuevo servicio como al existente. Esto se conoce como duplicación de tráfico.
+ Verificación del correcto comportamiento del nuevo servicio.

La duplicación de tráfico permite probar el nuevo servicio en producción, con solicitudes de producción, sin interrupción del servicio, y mantener sincronizado el estado de ambas versiones de los servicios con estado.

## Mirroring in OpenShift Service Mesh
OpenShift Service Mesh utiliza los recursos de `DestinationRule` para definir subsets (generalmente versiones de servicio) y la entrada de `destino` en los recursos de `VirtualService` para enrutar las solicitudes entre subsets. OpenShift Service Mesh proporciona duplicación de tráfico mediante el uso de los mismos recursos de `DestinationRule` e introduciendo una entrada de` duplicación` en la ruta de `VirtualService`:

```
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my_virtual_service
spec:
  hosts:
    - target_host
  http:
  - route:
    - destination:
        host: old_service_name
        subset: old_subset
    mirror: #1
      host: new_service_name #2
      subset: new_subset #3
```

1. La entrada mirror define el servicio al que Istio está enviando copias de solicitud.
2. El nombre del servicio que recibe el tráfico espejado.
3. El subset de hosts que reciben el tráfico espejado, como se define en la `DestinationRule`

Istio no distingue si el host reflejado es un servicio interno o externo. Istio puede mirrorear el tráfico a cualquier servicio con un recurso `VirtualService` relacionado.

### Mirroring un Porcentaje del Trafico 
Hay situaciones en las que no es necesario o deseable reflejar todo el tráfico en el nuevo servicio. Por ejemplo, cuando no se requiere mantener el último estado del servicio, o cuando reducir el tráfico entre servicios es más importante que probar todas las solicitudes. En esas situaciones, Istio y OpenShift Service Mesh permiten definir un porcentaje del tráfico reflejado:
```
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my_virtual_service
spec:
  hosts:
    - target_host
  http:
  - route:
    - destination:
        host: old_service_name
        subset: old_subset
    mirror:
      host: new_service_name
      subset: new_subset
    mirror_percent: 10
```
En el ejemplo anterior, solo el 10% de las solicitudes enviadas a `old_service_name` se reflejan en `new_service_name`.

## Selección de la estrategia de implementación adecuada
Los Canary Releases y la duplicación de tráfico son estrategias de implementación que le ayudan a validar el lanzamiento de nuevas versiones de servicio. Dependiendo de su plan de implementación y prueba, es posible que desee utilizar uno u otro. Para elegir la estrategia correcta, siga estas pautas:

+ Utilice Canary Release cuando desee implementar una nueva versión directamente en producción mientras minimiza el riesgo. Además, elija esta estrategia si necesita introducir usuarios reales en el proceso de validación de la nueva versión. Al elegir las versiones de Canary, acepta que una pequeña parte de sus usuarios pueden experimentar problemas derivados de la nueva versión.
+ Utilice el Mirroring de tráfico cuando desee probar la nueva versión con carga de producción sin que la versión esté disponible para el público. Por ejemplo, la duplicación de tráfico puede ser adecuada si desea probar cómo responde la aplicación al 100% de la carga de producción. Este enfoque es menos riesgoso que los Canary Releases. Si algo sale mal, no afecta a los usuarios. Sin embargo, el mirroring de tráfico también es más limitada, porque no puede incluir usuarios reales en el proceso de validación.

Combinar ambas estrategias también es una opción interesante. En primer lugar, utiliza la duplicación de tráfico para validar que la nueva versión funcione correctamente con el tráfico de producción. A continuación, implementa la nueva versión como canario para comenzar a validarla con usuarios reales.

