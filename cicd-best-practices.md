# Best practices to follow for deployment or change management

1. Antes de cada cambio verificar que los backup se esten realizando. No es necesario que sea algo super complicado con un simple script de shell que realice el un dump como un step es mas que suficiente.
> Hint: para Helm hay que revisar o garantizar un proceso que no se pueda actualizar de manera manual. 
> Hint2: los rollbacks de Helm se realizan desde los revisions y no del APP.VERSION
2. Planificar los cambios antes de implementarlos. Decidir el flujo de la implementacion e idenficicar las dependencias dentro de los microservicios de antemano.
3. Siempre que sea posible realizar un test de la implementacion (dry-run).
4. Revisar los cambios y la estrategia de deployment. Una de las cosas que mas me han ayudado en estos ultimos años para desarrollar soluciones de ciclo de vidas de la aplicaciones y componentes es un una en la que idealmente no solamente el codigo es revisado sino tambien el tipo de configuracion que va a cambiar.
5. Notificar a las partes interesadas, incluso si se trata de una implementacion sin tiempo de inactividad.
6. Siempre tener un plan de rollback. Uno de los aspectos mas dificiles con los que me encontre fue poder reproducir ambientes en los que tenga que probar el rollback pero tener la experiencia de poder hacerlo ayuda de manera astronomica al momento en que nos encontramos un problema. 
