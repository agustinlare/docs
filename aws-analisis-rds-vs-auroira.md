# Postgres

## TL;DR

+ Multi-AZ
+ Manejo de backups
+ Point-in-time recovery
+ Replicacion
+ Monitoreo
+ Autoescalamiento de storage

|  | RDS | Aurora |
| ---|----|---|
| Storage limit| 64 Tib | 128 Tib|
| IOPS | 3000 | 80000 |
| Replicacion | Simple replication | 6 instancias Multi-az Volumen Cluster|
| Resize chunks | 5 Gib o 10%| 10 Gib |
| Failover delay (seg) | 60~120  | 30 |
| HA & DR | Multi-AZ cross-region standby secondary instance | Multi-AZ cross-region active reader instances |
| Backup's | + Ventana de bacup  <br> + Impacto de performance <br> + PITR (point-in-time recovery) | + Incremental <br> + Backup a nivel storage, por lo que no genera impacto de performance <br> + PITR <br> + Mejores tiempo de restore |
|uuid-ossp|Yes|Yes|
|pgcrypto|Yes|Yes|
|postgis|Yes|Yes|

> *RDS es ideal para small-to-medium cargas de trabajo. Funciona mejor en bases con conexiones concurrentes limitadas. Aurora es recomendable cuando se esta migrando de motores comeraciales como Oracle o SQL Server porque provee mejor performance con un precio mas bajo que estos.*

> *Aurora Serverless encaja bien con aplicacion que no esperan trafico regularmente, como desarrollo o testing. Incluso ofrece opciones para reducir capacidad a cero durante periodos de no uso (esta configuracion no es recomendable para ambientes productivos ya que la demora para reaprovisionar capacidad computacional).*
> Si bien parece Aurora ser una mejor opcion que RDS, si no se elige el caso de uso correcto puede resultar en altos costos.
> Por ejemplo, una aplicacion que espera trafico constante severo en una instancia r5.large seria equivalente a 8 ACU. En este caso Aurora Serverless seria 65% mas caro. Tampoco podria hacer uso de instancias reservadas mientras que con RDS podria reducir el costo considerablemente dependiendo el tipo de instancias y el largo de su compromiso.


## Storage

RDS utiliza EBS replicado con un slave o secondary multi-AZ support tanto para la DB como para los logs, soporta hasta 64Tib y autoescala de a chunks de 5Gib o 10% del actual storage. Puede consistir tanto de General Storage que puede alcanzar hasta los 3000 IOPS o de Provisioned IOPS que puede provisionar entre un rango de 1000~80000 iops

Aurora utiliza un sistema de storage custom de virtual clusters volumes de SSD's que consiste en la copia de data en multiples AZ en una misma region. El incremento de storage es automatico a medida que la DB crece y se hace de a 10 Gib chunks hasta 128 Tib. Especialmente recomendable para workflows de alta concurrencia.

## Failover

RDS failover consiste en deteccion de fallas, propagacion de DNS y crash recovery. El tiempo de recuperacion depende en cuanto demora en realizarse el crash recovery pero suele estar entre los 60 ~ 120 segundos mientras que en aurora el crash recovery y el DNS propagation se realiza en paralelo y suele demorar alrededor de 10 ~ 15 segundos y en total dentro de los 30 segundos. 
Este ultimo es altamente recomendable para aplicacion que tienen tolerancia mayores a 60 segundos de downtime

**tl;dr**: La demora es inversamente proporcional al costo/hr en Aurora.

## HA & Disaster recovery

RDS tiene replicacion Multi-AZ  syncroniza a una instancia standby replica (secondary) en una diferente AZ a la primaria. Backups automaticos tomados de la instancia primaria. Incidentes como falla en la instancia primaria, storage failure y network failure desencadenan el failover para transformar la instancia secundaria en la nueva primaria.

Si bien aurora tambien soporta el despliegue Multi-AZ la replicacion syncroniza se realiza a traves de diferentes AZ a 6 nodos de storage diferentes asociaos al volume cluster. La syncronizacion se realiza a nivel de storage resultando en lag de miloseconds. Todas las instancias son activas y tiene backups automaticos desde la capa compartida de storage. 
Cuando Aurora detecta un problema en la instancia primaria o a nivel storage, activa una de las instancias reader y si no hay una replica provisionada intenta crear una nueva instancia de la base de datos de manera automatica. 
Aurora oferece cross-Regio replicacion con latencia por debajo del segundo y puede copiar y compartir snapshots a traves de distaintas cuentas de AWS para DRP's.

**tl;dr**: Si se utiliza replicacion en dos AZ y cross-Region lag no es un problema, RDS es suficiente.

## Backup

RDS realiza backups diarios durante una ventana. Existe un impacto de performance cuando el backup inicia en despliegue de single instance. Tambien realizar backups de logs transaccionales. Para PITR, el full backup es recuperado primero, seguido del WALs hasta el punto deseado. En bases de escritura interesa reproduciendo logs transaccionales puede llegar a demorar. Frecuentemente tomar backups manuales puede reducir PITR demoras.

Aurora backsup el cluster de volumene automaticamente y retiene estos por un tiempo deifinido. Estos son intecrementales por lo que puede restaurarse de manera rapida a un punto dentro del pereiodo de retencion. No hay impacto performance o. interrupcion en el servicio de la base durante el backup.

**tl;dr**: Para bases RPO y RTO sensibles y cargas sensibles a la degradacion de performance durante el backup Aurora es la mejor eleccion. Si la degradacion momentania en una sola AZ configuracion durante el backup y un RPO y RTO mas altos RDS es completamente adecuada. Pueden configurarse la ventana de backup para evitar esta degradacion durante picos de utilizacion. Si la configuracion es Multi-AZ, no hay degradacion ya que se toma de la instancia secundary.

## DB Instance classes

RDS soporta muchas instancias de propositos generales y de memoria optimizada. Aurora soporta instancias limitadas de T3, R4 y R5. Segun la region ambas soportan AWS Graviton2.

## Aurora Additional Features
+ Fast [database cloning](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Clone.html)
+ [Query plan managment](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Optimize.html) que permite controla como y cuando los query plan cambian.
+ [Cluster cache managment](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.cluster-cache-mgmt.html) mejora la performance de una nueva writer instance luego de un failover. Puede dseginar a una especifica replica como un failover target. En RDS luego del failover el buffer es construido desde cero, por lo que la performance se degrada ya que tiene que leer la informacion del disco en vez desde el buffer cache.
+ [Aurora Serverless](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless.html) inicia el despliegue automaticamente, escala y apaga basado en las necesidades de aplicaciones. Es una opcion apropiada para poco frecuente e intermitentes cargas de trabajo. RDS no soporta esto.


## Links y Fuentes
+ [Precios de Amazon RDS for PostgreSQL](https://aws.amazon.com/es/rds/postgresql/pricing/)
+ [Precios de Amazon Aurora](https://aws.amazon.com/es/rds/aurora/pricing/)
+ [Is Amazon RDS for PostgreSQL or Amazon Aurora PostgreSQL a better choice for me?](https://aws.amazon.com/es/blogs/database/is-amazon-rds-for-postgresql-or-amazon-aurora-postgresql-a-better-choice-for-me/)
+ [Aurora vs RDS: Why Choose Amazon Aurora Over Regular RDS](https://blog.shikisoft.com/why-choose-aurora-over-regular-rds/)
+ [When should I use Amazon RDS vs Aurora Serverless](https://searchcloudcomputing.techtarget.com/answer/When-should-I-use-Amazon-RDS-vs-Aurora-Serverless)
+ [PostgreSQL extensions supported on Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html#PostgreSQL.Concepts.General.FeatureSupport.Extensions)
+ [Extension versions for Amazon Aurora PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Extensions.html)
