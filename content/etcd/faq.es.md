---
title: FAQ
weight: 1200
description: Preguntas frecuentes
icon: fa-solid fa-circle-question
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/faq.md"
---

## etcd, en general {#etcd-general}

### ¿Qué es etcd? {#what-is-etcd}

etcd es un almacén clave-valor distribuido y consistente. Se utiliza principalmente como un servicio de coordinación independiente, en sistemas distribuidos. Y está diseñado para contener pequeñas cantidades de datos que quepan por completo en memoria.

### ¿Cómo se pronuncia etcd? {#how-do-you-pronounce-etcd}

etcd se pronuncia **/ˈɛtsiːdiː/** y significa «directorio `etc` distribuido».

### ¿Tienen los clientes que enviar las solicitudes al líder de etcd? {#do-clients-have-to-send-requests-to-the-etcd-leader}

[Raft][raft] está basado en un líder; el líder gestiona todas las solicitudes de los clientes que necesitan el consenso del clúster. Sin embargo, el cliente no necesita saber qué nodo es el líder. Cualquier solicitud que requiera consenso y que se envíe a una réplica se reenvía automáticamente al líder. Las solicitudes que no requieren consenso (por ejemplo, las lecturas serializables) puede procesarlas cualquier miembro del clúster.

## Configuración {#configuration}

### ¿Cuál es la diferencia entre listen-<client,peer>-urls, advertise-client-urls y initial-advertise-peer-urls? {#what-is-the-difference-between-listen-clientpeer-urls-advertise-client-urls-or-initial-advertise-peer-urls}

`listen-client-urls` y `listen-peer-urls` especifican las direcciones locales a las que se vincula el servidor etcd para aceptar las conexiones entrantes. Para escuchar en un puerto en todas las interfaces, especifica `0.0.0.0` como dirección IP de escucha.

`advertise-client-urls` y `initial-advertise-peer-urls` especifican las direcciones que los clientes de etcd u otros miembros de etcd deben usar para contactar con el servidor etcd. Las direcciones anunciadas deben ser accesibles desde las máquinas remotas. No anuncies direcciones como `localhost` o `0.0.0.0` en una configuración de producción, ya que estas direcciones son inaccesibles desde las máquinas remotas.

### ¿Por qué cambiar `--listen-peer-urls` o `--initial-advertise-peer-urls` no actualiza las URLs de par anunciadas en `etcdctl member list`? {#why-doesnt-changing---listen-peer-urls-or---initial-advertise-peer-urls-update-the-advertised-peer-urls-in-etcdctl-member-list}

Las URLs de par anunciadas de un miembro provienen de `--initial-advertise-peer-urls` en el arranque inicial del clúster. Cambiar las URLs de escucha de pares o los pares iniciales anunciados después de arrancar el miembro no afectará a las URLs de par anunciadas exportadas, ya que los cambios deben pasar por el cuórum para evitar una división (split brain) de la configuración de pertenencia. Usa `etcdctl member update` para actualizar las URLs de pares de un miembro.

## Despliegue {#deployment}

### Requisitos del sistema {#system-requirements}

Dado que etcd escribe datos en el disco, su rendimiento depende en gran medida del rendimiento del disco. Por este motivo, se recomienda encarecidamente usar SSD. Para evaluar si un disco es lo bastante rápido para etcd, una posibilidad es utilizar una herramienta de benchmarking de disco como [fio][fio]. Para ver un ejemplo de cómo hacerlo, lee [aquí][fio-blog-post]. Para evitar la degradación del rendimiento o la sobrecarga involuntaria del almacén clave-valor, etcd impone una cuota de tamaño de almacenamiento configurable, fijada por defecto en 2GB. Para evitar el uso de swap o quedarse sin memoria, la máquina debería tener al menos tanta RAM como cubra la cuota. Un tamaño máximo de 8GB es lo sugerido para entornos normales, y etcd emite una advertencia al arrancar si el valor configurado lo excede. En CoreOS, un clúster de etcd se suele desplegar en máquinas dedicadas CoreOS Container Linux con procesadores de doble núcleo, 2GB de RAM y 80GB de SSD *como mínimo*. **Ten en cuenta que el rendimiento depende intrínsecamente de la carga de trabajo; prueba antes de un despliegue en producción**. Consulta [hardware][hardware-setup] para más recomendaciones.

El entorno de producción más estable es el sistema operativo Linux con arquitectura amd64; consulta [plataformas compatibles][supported-platform] para más información.

### ¿Por qué un número impar de miembros del clúster? {#why-an-odd-number-of-cluster-members}

Un clúster de etcd necesita que una mayoría de nodos, un cuórum, esté de acuerdo con las actualizaciones del estado del clúster. Para un clúster con n miembros, el cuórum es (n/2)+1. Para cualquier clúster de tamaño impar, añadir un nodo siempre aumenta el número de nodos necesarios para el cuórum. Aunque añadir un nodo a un clúster de tamaño impar parece mejor porque hay más máquinas, la tolerancia a fallos es peor, ya que puede fallar exactamente el mismo número de nodos sin perder el cuórum, pero hay más nodos que pueden fallar. Si el clúster está en un estado en el que no puede tolerar más fallos, añadir un nodo antes de eliminar nodos es peligroso, porque si el nuevo nodo no consigue registrarse en el clúster (por ejemplo, porque la dirección está mal configurada), el cuórum se perderá de forma permanente.

### ¿Cuál es el tamaño máximo de un clúster? {#what-is-maximum-cluster-size}

Teóricamente, no hay un límite estricto. Sin embargo, un clúster de etcd probablemente no debería tener más de siete nodos. El [servicio de bloqueo Google Chubby][chubby], similar a etcd y ampliamente desplegado dentro de Google durante muchos años, sugiere ejecutar cinco nodos. Un clúster de etcd de 5 miembros puede tolerar dos fallos de miembros, lo cual es suficiente en la mayoría de los casos. Aunque los clústeres más grandes ofrecen mejor tolerancia a fallos, el rendimiento de escritura se resiente porque los datos deben replicarse en más máquinas.

### ¿Qué es la tolerancia a fallos? {#what-is-failure-tolerance}

Un clúster de etcd funciona siempre que se pueda establecer un cuórum de miembros. Si el cuórum se pierde por fallos de red transitorios (por ejemplo, particiones), etcd se reanuda automáticamente y de forma segura una vez que la red se recupera y el cuórum se restablece; Raft garantiza la consistencia del clúster. Ante una pérdida de alimentación, etcd persiste el registro de Raft en el disco; etcd reproduce el registro hasta el punto del fallo y retoma su participación en el clúster. Ante un fallo de hardware permanente, el nodo puede eliminarse del clúster mediante la [reconfiguración en tiempo de ejecución][runtime reconfiguration].

Se recomienda tener un número impar de miembros en un clúster. Un clúster de tamaño impar tolera el mismo número de fallos que un clúster de tamaño par, pero con menos nodos. La diferencia se aprecia comparando clústeres de tamaño par e impar:

| Tamaño del clúster | Mayoría | Tolerancia a fallos |
|:-:|:-:|:-:|
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 3 | 2 | 1 |
| 4 | 3 | 1 |
| 5 | 3 | 2 |
| 6 | 4 | 2 |
| 7 | 4 | 3 |
| 8 | 5 | 3 |
| 9 | 5 | 4 |

Añadir un miembro para llevar el tamaño del clúster a un número par no aporta tolerancia a fallos adicional. Asimismo, durante una partición de red en dos, un número impar de miembros garantiza que siempre habrá una partición con mayoría que pueda seguir funcionando y ser la fuente de verdad cuando termine la partición.

### ¿Funciona etcd en despliegues entre regiones o entre centros de datos? {#does-etcd-work-in-cross-region-or-cross-data-center-deployments}

Desplegar etcd entre regiones mejora la tolerancia a fallos de etcd, ya que los miembros están en dominios de fallo separados. El coste es una mayor latencia de las solicitudes de consenso por cruzar los límites de los centros de datos. Dado que etcd depende de un cuórum de miembros para el consenso, la latencia derivada de cruzar centros de datos será bastante pronunciada porque al menos una mayoría de los miembros del clúster debe responder a las solicitudes de consenso. Además, los datos del clúster deben replicarse entre todos los pares, por lo que también habrá un coste de ancho de banda.

Con latencias más largas, la configuración predeterminada de etcd puede provocar elecciones frecuentes o tiempos de espera de latidos. Consulta [ajustes][tuning] para adaptar los tiempos de espera en despliegues de alta latencia.

## Operación {#operation}

### ¿Cómo hacer una copia de seguridad de un clúster de etcd? {#how-to-backup-a-etcd-cluster}

etcdctl proporciona un comando `snapshot` para crear copias de seguridad. Consulta [copia de seguridad][backup] para más detalles.

### ¿Debo añadir un miembro antes de eliminar un miembro en mal estado? {#should-i-add-a-member-before-removing-an-unhealthy-member}

Al reemplazar un nodo de etcd, es importante eliminar primero el miembro y después añadir su reemplazo.

etcd emplea un consenso distribuido basado en un modelo de cuórum; (n/2)+1 miembros, una mayoría, deben aceptar una propuesta antes de que pueda confirmarse en el clúster. Estas propuestas incluyen actualizaciones de pares clave-valor y cambios de pertenencia. Este modelo evita totalmente cualquier posibilidad de inconsistencia por división (split brain). El inconveniente es que la pérdida permanente del cuórum es catastrófica.

Cómo se aplica esto a la pertenencia: si un clúster de 3 miembros tiene 1 miembro caído, aún puede avanzar, porque el cuórum es 2 y 2 miembros siguen activos. Sin embargo, añadir un miembro nuevo a un clúster de 3 miembros aumentará el cuórum a 3, porque se requieren 3 votos para una mayoría de 4 miembros. Como el cuórum aumentó, este miembro extra no aporta nada en términos de tolerancia a fallos: el clúster sigue estando a un fallo de nodo de quedar irrecuperable.

Además, ese miembro nuevo es arriesgado, porque puede resultar estar mal configurado o ser incapaz de unirse al clúster. En ese caso no hay forma de recuperar el cuórum, porque el clúster tiene dos miembros caídos y dos miembros activos, pero necesita tres votos para cambiar la pertenencia y deshacer la adición fallida del miembro. Por defecto, etcd rechaza los intentos de añadir miembros que puedan dejar el clúster fuera de servicio de esta manera.

Por otro lado, si el miembro caído se elimina primero de la pertenencia al clúster, el número de miembros pasa a ser 2 y el cuórum se mantiene en 2. Tras esa eliminación, añadir un miembro nuevo también mantendrá el cuórum estable en 2. Así, aunque el nodo nuevo no pueda arrancar, todavía es posible eliminar al miembro nuevo mediante el cuórum sobre los miembros que siguen activos.

### ¿Por qué etcd no acepta mis cambios de pertenencia? {#why-wont-etcd-accept-my-membership-changes}

etcd establece `strict-reconfig-check` para rechazar las solicitudes de reconfiguración que provocarían una pérdida de cuórum. Abandonar el cuórum es realmente arriesgado (especialmente cuando el clúster ya está en mal estado). Aunque resulte tentador desactivar la comprobación de cuórum cuando hay pérdida de cuórum para añadir un miembro nuevo, esto podría conducir a una inconsistencia plena del clúster. Para muchas aplicaciones, esto empeorará aún más el problema (con la «corrupción de geometría del disco» como candidata a lo más aterrador).

### ¿Por qué etcd pierde su líder por picos de latencia del disco? {#why-does-etcd-lose-its-leader-from-disk-latency-spikes}

Esto es intencionado; la latencia del disco forma parte de la disponibilidad del líder. Supón que el líder del clúster tarda un minuto en hacer fsync de una actualización del registro de Raft en el disco, pero el clúster de etcd tiene un tiempo de espera de elección de un segundo. Aunque el líder pueda procesar mensajes de red dentro del intervalo de elección (por ejemplo, enviar latidos), en la práctica no está disponible porque no puede confirmar ninguna propuesta nueva; está esperando al disco lento. Si el clúster pierde con frecuencia su líder debido a latencias del disco, prueba a [ajustar][tuning] la configuración del disco o los parámetros de tiempo de etcd.

### ¿Qué significa la advertencia de etcd «request ignored (cluster ID mismatch)»? {#what-does-the-etcd-warning-request-ignored-cluster-id-mismatch-mean}

Cada clúster nuevo de etcd genera un nuevo identificador de clúster basado en la configuración inicial del clúster y un valor único de `initial-cluster-token` proporcionado por el usuario. Al tener identificadores de clúster únicos, etcd queda protegido frente a interacciones entre clústeres que podrían corromper el clúster.

Normalmente esta advertencia ocurre tras desmontar un clúster antiguo y reutilizar después algunas de las direcciones de par para el clúster nuevo. Si algún proceso etcd del clúster antiguo sigue ejecutándose, intentará contactar con el clúster nuevo. El clúster nuevo reconocerá un error de coincidencia del identificador de clúster; luego ignorará la solicitud y emitirá esta advertencia. Esta advertencia suele eliminarse asegurando que las direcciones de par entre clústeres distintos sean disjuntas.

### ¿Qué significa «mvcc: database space exceeded» y cómo lo corrijo? {#what-does-mvcc-database-space-exceeded-mean-and-how-do-i-fix-it}

El modelo de datos de [control de concurrencia multiversión][api-mvcc] de etcd mantiene un historial exacto del espacio de claves. Sin compactar periódicamente este historial (por ejemplo, configurando `--auto-compaction-mode` y `--auto-compaction-retention`), etcd acabará agotando su espacio de almacenamiento. Si a etcd le queda poco espacio de almacenamiento, activa una alarma de cuota de espacio para proteger el clúster de escrituras adicionales. Mientras la alarma esté activa, etcd responde a las solicitudes de escritura con el error `mvcc: database space exceeded`.

Para recuperarse de la alarma de cuota de espacio insuficiente:

1. [Compacta][maintenance-compact] el historial de etcd.
2. [Desfragmenta][maintenance-defragment] cada endpoint de etcd.
3. [Desactiva][maintenance-disarm] la alarma.

### ¿Qué significa la advertencia de etcd «etcdserver/api/v3rpc: transport: http2Server.HandleStreams failed to read frame: read tcp 127.0.0.1:2379->127.0.0.1:43020: read: connection reset by peer»? {#what-does-the-etcd-warning-etcdserverapiv3rpc-transport-http2serverhandlestreams-failed-to-read-frame-read-tcp-1270012379-12700143020-read-connection-reset-by-peer-mean}

Se trata de una advertencia del lado de gRPC cuando un servidor recibe un flag TCP RST con flujos del lado cliente cerrados prematuramente. Por ejemplo, un cliente cierra su conexión mientras el servidor gRPC aún no ha procesado todas las tramas HTTP/2 de la cola TCP. Pueden haberse perdido algunos datos en el lado del servidor, pero no hay problema siempre que la conexión del cliente ya se haya cerrado.

Solo las [versiones antiguas de gRPC](https://github.com/grpc/grpc-go/issues/1362) registran esto. Las versiones de etcd [>=v3.2.13 lo registran por defecto con nivel DEBUG](https://github.com/etcd-io/etcd/pull/9080), por lo que solo es visible con la opción `--log-level=debug` activada.

## Rendimiento {#performance}

### ¿Cómo debo hacer un benchmark de etcd? {#how-should-i-benchmark-etcd}

Prueba la herramienta [benchmark]. Los [resultados del benchmark][benchmark-result] actuales están disponibles para comparación.

### ¿Qué significa la advertencia de etcd «apply entries took too long»? {#what-does-the-etcd-warning-apply-entries-took-too-long-mean}

Después de que una mayoría de los miembros de etcd acepte confirmar una solicitud, cada servidor de etcd aplica la solicitud a su almacén de datos y persiste el resultado en el disco. Incluso con un disco mecánico lento o un disco de red virtualizado, como el EBS de Amazon o el PD de Google, aplicar una solicitud debería tardar normalmente menos de 50 milisegundos. Si la duración media de aplicación supera los 100 milisegundos, etcd advertirá que las entradas tardan demasiado en aplicarse.

Normalmente este problema lo causa un disco lento. El disco puede estar sufriendo contención entre etcd y otras aplicaciones, o simplemente ser demasiado lento (por ejemplo, un disco virtualizado compartido). Para descartar que un disco lento cause esta advertencia, supervisa  [backend_commit_duration_seconds][backend_commit_metrics] (la duración p99 debe ser inferior a 25ms) para confirmar que el disco es razonablemente rápido. Si el disco es demasiado lento, asignar un disco dedicado a etcd o usar un disco más rápido suele resolver el problema.

La segunda causa más común es la inanición de CPU. Si la supervisión del uso de CPU de la máquina muestra una utilización elevada, puede que no haya capacidad de cálculo suficiente para etcd. Mover etcd a una máquina dedicada, aumentar el aislamiento de recursos del proceso  mediante cgroups, o subir la prioridad del proceso del servidor etcd (renicing) suele resolver el problema.

Las solicitudes de usuario costosas que acceden a demasiadas claves (por ejemplo, obtener todo el espacio de claves) también pueden provocar latencias de aplicación largas. Acceder a menos de unos cientos de claves por solicitud, sin embargo, siempre debería tener buen rendimiento.

Si ninguna de las sugerencias anteriores elimina las advertencias, [abre un issue][new_issue] con registros detallados, información de supervisión, métricas y, opcionalmente, información de la carga de trabajo.

### ¿Qué significa la advertencia de etcd «failed to send out heartbeat on time»? {#what-does-the-etcd-warning-failed-to-send-out-heartbeat-on-time-mean}

etcd usa un protocolo de consenso basado en un líder para la replicación consistente de datos y la ejecución del registro. Los miembros del clúster eligen un único líder y todos los demás miembros se convierten en réplicas. El líder electo debe enviar periódicamente latidos a sus réplicas para mantener su liderazgo. Las réplicas deducen un fallo del líder si no reciben latidos dentro de un intervalo de elección y desencadenan una elección. Si un líder no envía sus latidos a tiempo pero sigue ejecutándose, la elección es espuria y probablemente se debe a recursos insuficientes. Para detectar estos fallos leves, si el líder omite dos intervalos de latido, etcd advertirá que no pudo enviar un latido a tiempo.

Normalmente este problema lo causa un disco lento. Antes de que el líder envíe latidos acompañados de metadatos, puede necesitar persistir esos metadatos en el disco. El disco puede estar sufriendo contención entre etcd y otras aplicaciones, o simplemente ser demasiado lento (por ejemplo, un disco virtualizado compartido). Para descartar que un disco lento cause esta advertencia, supervisa  [wal_fsync_duration_seconds][wal_fsync_duration_seconds] (la duración p99 debe ser inferior a 10ms) para confirmar que el disco es razonablemente rápido. Si el disco es demasiado lento, asignar un disco dedicado a etcd o usar un disco más rápido suele resolver el problema. Para determinar si un disco es lo bastante rápido para etcd, puede usarse una herramienta de benchmarking como [fio][fio]. Lee [aquí][fio-blog-post] un ejemplo.

La segunda causa más común es la inanición de CPU. Si la supervisión del uso de CPU de la máquina muestra una utilización elevada, puede que no haya capacidad de cálculo suficiente para etcd. Mover etcd a una máquina dedicada, aumentar el aislamiento de recursos del proceso  con cgroups, o subir la prioridad del proceso del servidor etcd (renicing) suele resolver el problema.

Una red lenta también puede causar este problema. Si las métricas de red entre las máquinas de etcd muestran latencias largas o una tasa de pérdida elevada, puede que no haya capacidad de red suficiente para etcd. Mover los miembros de etcd a una red menos congestionada suele resolver el problema. Sin embargo, si el clúster de etcd está desplegado entre centros de datos, es normal que haya latencias largas entre los miembros. Para tales despliegues, ajusta la configuración `heartbeat-interval` para que coincida aproximadamente con el tiempo de ida y vuelta entre las máquinas, y la configuración `election-timeout` para que sea al menos 5 * `heartbeat-interval`. Consulta la [documentación de ajuste][tuning] para más información.

Si ninguna de las sugerencias anteriores elimina las advertencias, [abre un issue][new_issue] con registros detallados, información de supervisión, métricas y, opcionalmente, información de la carga de trabajo.

### ¿Qué significa la advertencia de etcd «snapshotting is taking more than x seconds to finish ...»? {#what-does-the-etcd-warning-snapshotting-is-taking-more-than-x-seconds-to-finish--mean}

etcd envía una instantánea de su almacén clave-valor completo para refrescar las réplicas lentas y para las [copias de seguridad][backup]. Los tiempos de transferencia de instantáneas lentos aumentan el MTTR; si el clúster está ingiriendo datos con un rendimiento alto, las réplicas lentas pueden entrar en bloqueo activo (livelock) al necesitar una instantánea nueva antes de terminar de recibir una instantánea. Para detectar un rendimiento lento de instantáneas, etcd advierte cuando el envío de una instantánea tarda más de treinta segundos y excede el tiempo de transferencia esperado para una conexión de 1Gbps.


[api-mvcc]: /es/etcd/learning/api/#revisions
[backend_commit_metrics]: /es/etcd/metrics/#disk
[backup]: /es/etcd/op-guide/recovery/#snapshotting-the-keyspace
[benchmark]: https://github.com/etcd-io/etcd/tree/main/tools/benchmark
[benchmark-result]: /es/etcd/op-guide/performance/
[chubby]: http://static.googleusercontent.com/media/research.google.com/en//archive/chubby-osdi06.pdf
[fio]: https://github.com/axboe/fio
[fio-blog-post]: https://web.archive.org/web/20240726111518/https://prog.world/is-storage-speed-suitable-for-etcd-ask-fio/
[hardware-setup]: /es/etcd/op-guide/hardware/
[maintenance-compact]:  /es/etcd/op-guide/maintenance/#history-compaction-v3-api-key-value-database
[maintenance-defragment]: /es/etcd/op-guide/maintenance/#defragmentation
[maintenance-disarm]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#alarm-disarm
[new_issue]: https://github.com/etcd-io/etcd/issues/new
[raft]: https://raft.github.io/raft.pdf
[runtime reconfiguration]: /es/etcd/op-guide/runtime-configuration/
[supported-platform]: /es/etcd/op-guide/supported-platform/
[tuning]: /es/etcd/tuning/
[wal_fsync_duration_seconds]: /es/etcd/metrics/#disk
