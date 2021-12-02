# OOM Killed en JVM (Sizing)
## TL;DR
Configurar -Xmx -Xms argumentos, puede hacerse desde variables de entornos o en el entrypoint de la imagen para reservar los recursos de antemano.

Request debe ser al menos mayor que el -Xmx y asegurarse de darle espacio de crecimiento tanto para la JVM y OS. Cuanto? Depende de muchos factores, pero por ejemplo simple microservicio probablemente este bien con un ~25% por encima del -Xmx. Para esto es necesario tener en claro la arquitectura de nuestra aplicación ya que  entran en juego variables como la utilización de tmpfs o uso de memoria por fuera del heap que contribuyen al uso de recursos.

Configurar limits muy por encima de nuestro request para manejar picos de carga en las que el pode hace uso de la "memoria disponible". Si obtener esa memoria adicional es una necesidad para que la aplicación haga su trabajo, reservarla por adelantado es imperativo.

## Introducción
Desde el equipo entendemos que la asignación de recursos sea uno de los temas más difíciles y frecuentes para equipos/personas que son nuevas a las plataformas de containers. La configuración del cluster es relativamente agresiva para promover pequeñas aplicaciones o microservicios que puedan escalar horizontalmente y esto se debe a que en 90% de los casos performa mejor y de esta manera nos permite repartir los recursos a todos de una manera equitativa. Sabemos también que los equipos de desarrollo son un poco liberales al asignar memoria a la JVM ya que vienen de un paradigma en el cual tienen una vm sola para ellos con sus recursos definidos, y que al pasar a un cluster de pronto se encuentran a sus pods fallando bajo algún flavor de OOM Killed.

## Que son los request y los limites?
Cuando hacemos un despliegue desde Gitlab nuestra aplicación le solicita al kube-scheduler un nodo en el cual nuestro pod pueda ejecutarse. Este va a buscar bajo múltiples criterios donde los más básicos son que tenga suficiente memoria y CPU para correr el container. Requests estipula la mínima cantidad de recursos que necesita nuestro pod para ejecutarse. El kube-scheduler solamente asignará nuestro pod en nodos apropiados para ello y en caso de no encontrar un nodo que tenga el request solicitado nuestro pod quedará en estado Pending y podrá verse tanto en el pod (mientras el replication controller continue intentando realizar el deploy) o dentro de la opción events dentro de la consola.

Pero un request no es un limite, una vez que el pod se encuentra corriendo y el container necesita recursos adicionales puede solicitarles a dicho nodo. Esta elasticidad es esencial para manejar picos de carga, pero también crea un riesgo en que los pods queden acaparando demasiados recursos que no utilicen. Limits es donde esto se controla para establecer un máximo de recursos que cada container de un pod puede consumir.

Para el desarrollador el request es una garantia ofrecida por Openshift de que el pod va a tener un minima cantidad de requersos, y el limit es una obligación de estar por debajo de la cantidad de recursos que es forzado por el kernel. En otras palabras, los containers no pueden depende en 

Configurando memory request and limits para los containes que corren en su cluster, usted puede hacer eficiente el uso de recursos disponible en sus nodos. Teniendo los request bajos de sus pods, le da una buena chance de que sea asginado a un nodo. Tendiendo un limite configurado mayor al del request usted conseguira dos cosas:
+ El pod pueda tener picos de carga donde el uso de la memoria que está disponible.
+ La cantidad de memoria un pod pueda usar durante el pico de carga es limitada por una cantidad razonable.
> Fuente https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/#motivation-for-memory-requests-and-limits

## Caso ejemplo
Supongamos tenemos el siguiente dockerfile:
```
FROM openjdk:8u181-jre-slim
...
ENTRYPOINT exec java -Xmx1512m -Xms1g [...] -cp app:app/lib/* com.schibsted.algoasi.algomas
```
y los siguientes recursos dentro del deploymentconfig:
```
resources:
  limits:
    memory: 1Gi
    cpu: 1
  requests:
    memory: 10Mi
    cpu: 10m
```

Desde el vamos la JVM asignará 10Mi de memory heap, consumiendo toda la capacidad de ese container que obtuvimos del request. Dado que la JVM necesita recursos adicionales (code cache, off-heap, thread stack, etc) al igual que un sistema operativo, nuestros containers nacen con menor capacidad. Es claro que el request es demasiado bajo, aunque el limit le da el suficiente espacio para prevenir un OOM Killed.

## La importancia de setear -Xmx y -Xms
En cualquier versión de 8u121 para abajo, existe un issue en el que el container intentara iniciar con una heap memory por encima del limit del container y este fallara. Sin embargo este problema únicamente pasa cuando la JVM tiene que calcular el máximo y mínimo de heap size. En este caso nosotros estamos pasando los argumentos -Xmx y -Xms especificando cuántos recursos debe utilizar la JVM.

## tmpfs - "Todo queda en la memoria"
Otra de las cosas a tener en consideración son los tmpfs mounts. Estos volúmenes se ven como cualquier otro directorio en nuestro filesystem pero realmente estos quedan en memoria y contribuyen al consumo de memoria total. Suponiendo que tenemos una aplicación que usa un cache interno persistido en disco y utilizamos el /tmp mount para evitar IO overhead, lo cual es una buena idea y ademas lo utilizamos para el almacenamiento de logs, si no monitoreamos el tamaño de esto podemos llegar a encontrarnos con un consumo de memoria mayor al de nuestro limit provocando un OOM Killed. Este es un error tipico que sucede cuando nos migramos de vm's a containers. En este caso lo primero que deberiamos hacer es reubicar nuestro cache a un disco, prefiriendo mas IO load y menos consumo de memoria, y como segundo rotar lo suficiente nuestros logs y mantenerlos en un tamaño razonable.

En este enlace dejo consejos para superar IO overhead en microservicos.

## Memory compartida dentro de la JVM
Por ahora nos concentramos en la heap memory, pero sabemos que la JVM realiza otra cosas por lo que debemos revisar cuál es el uso real de memoria del proceso JVM. 

Aclaracion: Los datos que se muestran a continuacion pueden verse con mayor facilidad a traves de un dashboard de grafana. Pueden comunicarse con el equipo de BRE sobre estos.

```
$ agustinlare@jvm-dummy-leaked-5pv34u:/# cat /proc/1/status | grep Rss
RssAnon:         3677552 kB
RssFile:           15500 kB
RssShmem:           5032 kB
```

Estos tres procesos (comúnmente) suman el total de RSS (Resident Set Size) la cual nos dice la memoria que tiene el proceso de la JVM en este momento y vemos que está consumiendo 3.6Gi de nuestros 4Gi limit.

También podemos fijarnos en el OS de por sí. Esta información podemos encontrarla en el tree de /sys/fs/cgroup

```
$ agustinlare@jvm-dummy-leaked-5pv34u:/# cat /sys/fs/cgroup/memory/memory.stat
cache 435699712
rss 3778998272
rss_huge 3632267264
shmem 9814016
mapped_file 5349376
dirty 143360
writeback 8192
swap 0
pgpgin 2766200501
pgpgout 2766061173
pgfault 2467595
pgmajfault 379
inactive_anon 2650112
active_anon 3786137600
inactive_file 198434816
active_file 227450880
unevictable 0
hierarchical_memory_limit 4294967296
hierarchical_memsw_limit 8589934592
total_cache 435699712
total_rss 3778998272
total_rss_huge 3632267264
total_shmem 9814016
total_mapped_file 5349376
total_dirty 143360
total_writeback 8192
total_swap 0
total_pgpgin 2766200501
total_pgpgout 2766061173
total_pgfault 2467595
total_pgmajfault 379
total_inactive_anon 2650112
total_active_anon 3786137600
total_inactive_file 198434816
total_active_file 227450880
total_unevictable 0
```

La `rss` total de nuestro container se calcula con `rss` + mapped_files, ~3.8Gi. Esto nos deja unos ~200Mi de sobra dentro de nuestro container, por lo que muy probablemente ante un pico de carga lleguemos a nuestro limit o incluso queramos pasar de este.

cat /sys/fs/cgroup/memory/memory.failcnt nos va a decir cuántas veces llegamos al límite de uso de recursos.
