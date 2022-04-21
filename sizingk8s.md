# Sizear Kubernetes deberia considerarse trabajo insalubre

Hoy se nos presenta una disyuntiva al momento de elegir la correcta configuracion no solo para el despliegue y ciclo de vida de las aplicaciones sino para el sizing correcto del cluster. El famoso balance entre performance/estabilidad/resiliencia.

El problema hoy recide en una limitante presente en todas las apliciones tanto containerizadas como no de Java y es que al momento en que levantan estas levantan, consumen muy por encima de los limites que establecimos de 300m por pod. En algunos casos hemos podido llegar a ver que alcanzan hasta 5 veces ese tamaño en los ambientes en que no tienen este tipo de restriccion, y es aqui donde empiezan los problemas que nos han reportado:

1. El pod responde 503 durante un periodo luego de haberse desplegado (resiliencia)
2. Los request estan por encima de los timeouts default de aplicaciones (5s) (performance)

Pareciera sencillo verdad? Asignar mas recursos al limit de CPU y este problema no se vuelve a presentar... pero esto nos trae otro problema:

3. Nodos fallando del cluster ante el alto consumo de CPU (estabilidad)

Obviamente va a depende a quien le preguntamos cual de estas tres es la que hay que priorizar por lo que la unica conclucion viable es la de "comprometer" una solucion entre las tres. 

Liberar el los limites de recursos pueden solucionar el problema 1 y 2, pero asi mismo generar el problema 3, y a nadie le gusta un cluster el cual deja de responder ya sea la razon que fuere, cuando no responde todos perdemos...
Poner limites bajos, para que la aplicaciones levanten para que el cluster tenga los recursos mas que suficiente para cubrir los limites de las aplicaciones para que este este estable, nos va a traer problemas de performance y resiliencia en las aplicaciones y hasta incluso puede inferir en caso de que este mal configurado el readinessProbe de estabilidad del cluster tambien, ya que el api-server para el HPA comienza a evaluar solo aquellos pods que alguna vez estuvieron en estado Ready 1/1 para la evaluacion de consumo, asi disparando replicas que no necesita al inicio y allocando recursos que despues de 5 minutos van a des-escalarce.

## Demoliendo hoteles

*Contexto*

Si bien no pude realizar pruebas de stress, si pude ver un movimiento "normal" de algunas de las aplicaciones en las que aplique, o sugeri aplicar algun cambio el y mayor momento en que las aplicaciones consumen esa barbaridad de CPU es al cuando Java comienza a cargar objetos al inicio del spring boot. Luego este consumo se normaliza y en momento idle suele rondar los 4m ~ 12m de idle y con algunas pegadas concurrentes aumenta sin stresar demasiado las aplicaciones de 60m ~ 160m, cuando ya empiezan a escalar nuevos pods. 

*"Vamos por partes" dijo Jack el destripador*

El problema 1, las aplicaciones responde 503 ni bien empiezan. Facil ponerle un readinessProbe para evitar esto. Pero me encontre con que el springboot tardaba mucho en levantar y es logico suponer porque le estamos poniendo un limite a la cantidad de CPU que utilizan. Pero supongamos solo por ahora que con agregar un `initialDelayseconds` de 180 arregla el problema, aunque nos trae problemas de resiliencia ya que, por ejemplo, al momento de hacer un update en una aplicacion que tiene 4 pods, va a tardar 12 minutos en realizar el cambio de pods completos, o 3 minutos por cada replica nueva del HPA.

El problema 2, si bien se arreglo subiendo un poco los recursos, en algunos casos especificos 1 core entero, despues este realmente no hace a un problema ya que no volvi a ver que alcanzara el limit despues de que comenzaba. Esto no solamente mejoro los tiempos de respuesta de los request sino que pudimos bajar a 60 el `initialDelayseconds`. Dos pajaros de una piedra... sigue siendo un monton 60 segundos, pero de esta manera al menos estamos de acuerdo en que el cluster va a tener la estabilidad y resiliencia (problema 3) para poder asignar estos recursos que necesitan las aplicaciones, de nuevo, por lo que pude observar.

## Es cuestion de elegir el veneno

El tema es que no podemos tener todos los puntos contentos, sino encontrar el balance entre ellos

Una posicion conservadora podria ser la de asignar a todas las app 2 core y bajarles a todo el readinessProbe para que las aplicaciones levanten y respondan rapido pero vienen acompañadas de un costo. Por ejemplo asignar limits y request por igual asegurandonos que las aplicaciones pueden manejar los picos de trabajo, pero haciendo mas dificil que si tenemos muchas replicas haya lugar para todos los pods quedando estos en Pending hasta que el autoscaler provisione nuevos nodos donde poner esos pods malgastando recursos por que la mayoria del tiempo estarian los pods en idle.

Mi posicion es un poco mas flexible pero viene con un riesgo mas alto, y mas aun dado que no realizamos pruebas de stress, pero haciendo las paces en que puedo tener cierto porcentaje de overcommitment de recursos, sabiendo que es muy improbable que todas las aplicaciones tengan picos de consumo al mismo tiempo, me permite darle limits mas altos (500m ~ 1000m) para el momento en que levanta spring boot y bancarme que los tiempos de rollout no sea el optimo por el CPU throttling (memory tira OOM y mueve los pods de lugar, proceso llamado eviction), pero no tan altos como si les dejara el 300m, con un request razonable para el idle/workload medio sin provocar el provisionamiento automatico de nuevos nodos, por lo tanto, no reduciendo costos, sino "sacandole el jugo".

> Fan fact:  Mientras mas se produce el CPU throttling, la demora termina siendo exponencial por lo que demora en factor X en realizar la misma tarea.
