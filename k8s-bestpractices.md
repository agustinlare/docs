# Kubernetes Best Practices

1. Utilizar `namespaces` para organizar y aisarla recurssos dentro de un cluster para mejorar la administracion y la escalabilidad de las aplicaciones.
2. `ConfigMaps` y `Secrets` son esenciales para manejar configuracion y secretos de manera segura y eficiente.
3. Configurar `limits` y `requests` apropiadamente de recursos para que los pods tengan los suficientes para correr de manera eficiente.
4. `Liveness` y `readiness` probe son herramientas claves para detectar y recuperarse de errores ([Kuberenetes Probes: Startup, Liveness & Readiness](https://github.com/agustinlare/docs/blob/master/k8s-probes/probes.md#kuberenetes-probes-startup-liveness--readiness)).
5. `RollingUpdates` y `RollBacks` son strategias de deployment cruciales a la hora de actualizar aplicaciones para garantizar una minima cantidad de downtime.
6. Monitorear los recursos del cluster y la performance ayuda a la identificacion de problemas y cuellos de botella.
7. El escalamiento automatico con `HorizontalPodAutoscaler` asegura que las aplicaciones puedan encargarse de la carga.
8. Adptar particuas apropiadas de seguridad como setgmentacion de red, utilizacion de role-based acccess control (`RBAC`), y utilizacion de protocolos seguros de comunicacion entre componentes es vital para mantener la seguridad del cluster.
9. Realizar backups con regualidad, almacenar configuracion y secretos del cluster es importante ante un evento de disaster recovery.
10. Versionar y tagging imagenes de containers ayuda a poder realizar faciles rollbacks y seguimiento de nuestras aplicaciones.
