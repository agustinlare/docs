# TL;DR - Startup, liveness y readiness probe ejemplos & commons mistakes

Como se comento anteriormente en `Kubernetes` existen tres tipos de simples `controladores` para ejecutar `probes` y pueden ser utilizados en cualquiera de los `probes`, `startup` - `readiness` - `liveness`.

## Errores comune
## *Startup loops*
Si bien es recomendable tener este tipo de probe, especialmente en aplicaciones legacy o cualquier otra que requiera de cierto tiempo en alistarse es realmente importante que parametros deben ser configurados correctamente o de lo contrario puede romper con la disponibilidad de la aplicación. Si esta mal configurado puede causar loops de restart infinitos. Asumamos que tenemos una aplicación corriendo en Java y esta aplicación toma un tiempo hasta estar lista para recibir alistarse. Si no permitimos el tiempo necesario para que el `startup probe` responda de manera exitosa, `kubelet` puede llegar a reiniciar el `container` prematuramente, causando un loop.

## *Liveness loops*
Asumamos que nuestra aplicación necesita leer una larga cantidad de información en cache una vez cada tanto. Falta de respuesta en dicho momento puede causar un falso positivo porque el probe puede fallar. En este caso, la falla del liveness probe va a reiniciar el contenedor y probablemente, va a entrar en un continuo ciclo de reinicios. En este escenario seria mejor la utilizacion del readiness, el pod solo se retirara del servicio para ejecutar las tareas de mantenimiento y, una vez que este listo para recibir trafico puede comenzar a responder a los probe.

Liveness endpoints de nuestro microservico que alcanzan los probes, deben verificar los requisitos minimos absolutos que muestra que la aplicación se esta ejecutando. De esta forma, las comprobaciones de actividad se realizan correctamente, el pod no se reiniciara y nos aseguraremos de que el trafico del servicio fluya como debería.

## *Readiness*
Supongamos que tenemos configurado el readiness de tipo HTTPGet y nuestra aplicación revisa la conexión con una base de datos antes de contestar el probe. Y supongamos que hay un problema en la base de datos por un problema en ella misma, en este caso todos los pods van a a estar inalcanzables a menos que la conexión base de datos se restablezca sola. Este no es un comportamiento recomendable para este tipo de prueba. lo recomendable seria alimentar de este error al frontend y notificar al usuario de una indisponibilidad, ya que incluso incrementar el failureThreshold puede que no nos evite un error en cascada.

Supongamos que tenemos almacenado un key/value utilizado para el cache y que el endpoint del probe tambien verifica la conexión. La aplicación puede estar ejecutandose sin la key/value, ya que solo se ralentizará, pero ejecutara una consulta completa de la base de datos cada vez que necesito acceder a los datos. En este caso, si el probe falla debido a que el key/value no esta disponible, toda la aplicación estará inactiva durante algún tiempo, hasta que arregle el almacenamiento, lo cual no es deseable.

## Ejemplos
## *Exec probe*
Este tipo de probe ejecuta un comando dentro del contenedor como un *health check*; el *exit code* determinara si este fue exitoso
```
exec:
  command:
  - cat
  - /etc/nginx/nginx.conf
```

## *TCP Probe* 
Revisa si el puerto especificado se encuentra abierto o no; es exitoso ante un puerto abierto 
```
tcpSocket:
  host:
  port: 80
```

## *HTTP Probe*
Este envia un *HTTPGet* request con los parametros definidos  y posee otros opciones:
+ *host*: Host/IP a la cual enviar el request (default: pod id)
+ *schema*: Esquema que se utiliza al realizar el request (default: http)
+ *path*: Path
+ *httpHeaders*: Cualquier array o headers definidos como una tupla de header/valor
+ *port*: Puerto al cual conectarse

```
httpGet:
  host:
  scheme: HTTP
  path: /
  httpHeaders:
  - name: Host
    value: myapplication1.com
  port: 80
```