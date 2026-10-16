---
title: etcd frente a otros almacenes clave-valor
weight: 2875
description: Historia y uso de etcd y comparación con otras herramientas
categories: [Concepto]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/why.md"
---

El nombre «etcd» nació de dos ideas: la carpeta «/etc» de unix y los sistemas «d»istribuidos. La carpeta «/etc» es un lugar para almacenar datos de configuración de un único sistema, mientras que etcd almacena información de configuración para sistemas distribuidos a gran escala. Por eso, un «/etc» «d»istribuido es «etcd».

etcd está diseñado como un sustrato general para sistemas distribuidos a gran escala. Se trata de sistemas que nunca tolerarán la operación con cerebro dividido (split-brain) y que están dispuestos a sacrificar disponibilidad para lograr ese fin. etcd almacena metadatos de forma consistente y tolerante a fallos. Un clúster de etcd está pensado para proporcionar almacenamiento clave-valor con la mejor estabilidad, fiabilidad, escalabilidad y rendimiento de su clase.

Los sistemas distribuidos usan etcd como almacén clave-valor consistente para la gestión de configuración, el descubrimiento de servicios y la coordinación de trabajo distribuido. Muchas [organizaciones][production-users] usan etcd para implementar sistemas en producción como planificadores de contenedores, servicios de descubrimiento de servicios y almacenamiento de datos distribuido. Los patrones distribuidos comunes que usan etcd incluyen la [elección de líder][etcd-etcdctl-elect], los [bloqueos distribuidos][etcd-etcdctl-lock] y la supervisión de la vivacidad de las máquinas.

## Casos de uso {#use-cases}

- Container Linux de CoreOS: Las aplicaciones que se ejecutan en [Container Linux][container-linux] obtienen actualizaciones automáticas del kernel de Linux sin tiempo de inactividad. Container Linux usa [locksmith] para coordinar las actualizaciones. Locksmith implementa un semáforo distribuido sobre etcd para garantizar que solo un subconjunto de un clúster se esté reiniciando en un momento dado.
- [Kubernetes][kubernetes] almacena datos de configuración en etcd para el descubrimiento de servicios y la gestión del clúster; la consistencia de etcd es crucial para planificar y operar los servicios correctamente. El servidor de API de Kubernetes persiste el estado del clúster en etcd. Usa la API de observación de etcd para supervisar el clúster y desplegar cambios críticos de configuración.

## Cuadro comparativo {#comparison-chart}

Quizá etcd ya parezca una buena opción, pero como con todas las decisiones tecnológicas, procede con cautela. Ten en cuenta que esta documentación está escrita por el equipo de etcd. Aunque lo ideal es una comparación desapasionada de la tecnología y las características, la experiencia y los sesgos de los autores obviamente favorecen a etcd. Usa solo como se indica.

La tabla siguiente es una referencia rápida práctica para detectar de un vistazo las diferencias entre etcd y sus alternativas más populares. Hay más comentarios y detalles de cada columna en las secciones que siguen a la tabla.

|  | etcd | ZooKeeper | Consul | NewSQL (Cloud Spanner, CockroachDB, TiDB) |
| --- | --- | --- | --- | --- |
| Primitivas de concurrencia |  [RPC de bloqueo][etcd-v3lock], [RPC de elección][etcd-v3election], [bloqueos de línea de comandos][etcd-etcdctl-lock], [elecciones de línea de comandos][etcd-etcdctl-elect], [recetas][etcd-recipe]  en go | [Recetas de curator][curator] externas en Java | [API de bloqueo nativa][consul-lock] | [Raras][newsql-leader], si existen |
| Lecturas linealizables | [Sí][etcd-linread] | No | [Sí][consul-linread] | A veces |
| Control de concurrencia multiversión | [Sí][etcd-mvcc] | No | No | A veces |
| Transacciones | [Comparación de campos, lectura, escritura][etcd-txn] | [Comprobaciones de versión, escritura][zk-txn] | [Comparación de campos, bloqueo, lectura, escritura][consul-txn]  | Estilo SQL |
| Notificación de cambios | [Intervalos de claves históricos y actuales][etcd-watch] | [Claves y directorios actuales][zk-watch] | [Claves y prefijos actuales][consul-watch] | Disparadores (a veces) |
| Permisos de usuario | [Basados en roles][etcd-rbac] | [ACL][zk-acl] | [ACL][consul-acl] | Varía ([GRANT][cockroach-grant] por tabla, [roles][spanner-roles] por base de datos) |
| API HTTP/JSON | [Sí][etcd-json] | No | [Sí][consul-json] | Rara vez |
| Reconfiguración de la composición | [Sí][etcd-reconfig] | [>3.5.0][zk-reconfig] | [Sí][consul-reconfig] | Sí |
| Tamaño máximo fiable de la base de datos | Varios gigabytes | Cientos de megabytes (a veces varios gigabytes) | Cientos de MB | Terabytes+ |
| Latencia mínima de linealización de lectura | RTT de red | Sin linealización de lectura | RTT + fsync | Barreras de reloj (atómicas, NTP) |

### ZooKeeper {#zookeeper}

ZooKeeper resuelve el mismo problema que etcd: la coordinación de sistemas distribuidos y el almacenamiento de metadatos. Sin embargo, etcd tiene el lujo de la retrospectiva adquirida con la experiencia de ingeniería y operativa con el diseño y la implementación de ZooKeeper. Las lecciones aprendidas de Zookeeper sin duda informaron el diseño de etcd, ayudándolo a soportar sistemas a gran escala como Kubernetes. Las mejoras que etcd hizo sobre Zookeeper incluyen:

* Reconfiguración dinámica de la composición del clúster
* Lectura/escritura estables bajo carga alta
* Un modelo de datos de control de concurrencia multiversión
* Supervisión fiable de claves que nunca descarta eventos silenciosamente
* Primitivas de concesión que desacoplan las conexiones de las sesiones
* API para bloqueos compartidos distribuidos seguros

Además, etcd admite una amplia gama de lenguajes y marcos de trabajo listos para usar. Mientras que Zookeeper tiene su propio protocolo RPC Jute personalizado, exclusivo de Zookeeper, que limita sus [enlaces de lenguaje admitidos][zk-bindings], el protocolo de cliente de etcd está construido sobre [gRPC][grpc], un marco RPC popular con enlaces de lenguaje para go, C++, Java y más. Asimismo, gRPC puede serializarse en JSON sobre HTTP, de modo que incluso utilidades generales de línea de comandos como `curl` pueden comunicarse con él. Como los sistemas pueden elegir entre diversas opciones, se construyen sobre etcd con herramientas nativas en lugar de alrededor de etcd con un único conjunto fijo de tecnologías.

Considerando las características, el soporte y la estabilidad, las aplicaciones nuevas que planeen usar Zookeeper como almacén clave-valor consistente harían bien en elegir etcd en su lugar.

### Consul {#consul}

Consul es un marco de descubrimiento de servicios de extremo a extremo. Proporciona comprobación de salud, detección de fallos y servicios DNS integrados. Además, Consul expone un almacén clave-valor con API HTTP RESTful. [Tal como está en Consul 1.0][dbtester-comparison-results], el sistema de almacenamiento no escala tan bien como otros sistemas como etcd o Zookeeper en operaciones clave-valor; los sistemas que requieren millones de claves sufrirán latencias altas y presión de memoria. A la API clave-valor le faltan, sobre todo, claves multiversión, transacciones condicionales y observaciones de flujo fiables.

etcd y Consul resuelven problemas diferentes. Si buscas un almacén clave-valor consistente distribuido, etcd es una mejor opción que Consul. Si buscas descubrimiento de servicios de clúster de extremo a extremo, etcd no tendrá características suficientes; elige Kubernetes, Consul o SmartStack.

### NewSQL (Cloud Spanner, CockroachDB, TiDB) {#newsql-cloud-spanner-cockroachdb-tidb}

Tanto etcd como las bases de datos NewSQL (por ejemplo, [Cockroach][cockroach], [TiDB][tidb], [Google Spanner][spanner]) proporcionan garantías fuertes de consistencia de datos con alta disponibilidad. Sin embargo, los parámetros de diseño de sistema radicalmente diferentes dan lugar a API de cliente y características de rendimiento notablemente distintas.

Las bases de datos NewSQL están pensadas para escalar horizontalmente entre centros de datos. Estos sistemas normalmente particionan los datos en múltiples grupos de replicación consistentes (shards), potencialmente distantes, almacenando conjuntos de datos del orden de terabytes o más. Este tipo de escalado las hace malas candidatas para la coordinación distribuida, ya que tienen latencias largas por esperar a los relojes y esperan actualizaciones con grafos de dependencias mayormente localizados. Los datos se organizan en tablas, incluidas funciones de consulta de estilo SQL con semántica más rica que etcd, pero al coste de una complejidad adicional para procesar, planificar y optimizar consultas.

En resumen, elige etcd para almacenar metadatos o coordinar aplicaciones distribuidas. Si se almacenan más de unos pocos GB de datos o se necesitan consultas SQL completas, elige una base de datos NewSQL.

## Uso de etcd para metadatos {#using-etcd-for-metadata}

etcd replica todos los datos dentro de un único grupo de replicación consistente. Para almacenar hasta unos pocos GB de datos con orden consistente, este es el enfoque más eficiente. A cada modificación del estado del clúster, que puede cambiar múltiples claves, se le asigna un ID único global, llamado revisión en etcd, proveniente de un contador que aumenta de forma monótona para razonar sobre el orden. Como solo hay un único grupo de replicación, la solicitud de modificación solo necesita pasar por el protocolo de raft para confirmarse. Al limitar el consenso a un grupo de replicación, etcd obtiene consistencia distribuida con un protocolo simple a la vez que logra baja latencia y una alta tasa de procesamiento.

La replicación detrás de etcd no puede escalar horizontalmente porque carece de particionado (sharding) de datos. En contraste, las bases de datos NewSQL suelen particionar los datos en múltiples grupos de replicación consistentes, almacenando conjuntos de datos del orden de terabytes o más. Sin embargo, para asignar a cada modificación un ID único y creciente global, cada solicitud debe pasar por un protocolo de coordinación adicional entre grupos de replicación. Este paso extra de coordinación puede entrar en conflicto con el ID global, forzando a las solicitudes ordenadas a reintentar. El resultado es un enfoque más complicado y, típicamente, con peor rendimiento que etcd para el orden estricto.

Si una aplicación razona principalmente sobre metadatos o sobre el orden de los metadatos, por ejemplo para coordinar procesos, elige etcd. Si la aplicación necesita un almacén de datos grande distribuido entre múltiples centros de datos y no depende fuertemente de propiedades fuertes de orden global, elige una base de datos NewSQL.

## Uso de etcd para la coordinación distribuida {#using-etcd-for-distributed-coordination}

etcd tiene primitivas de coordinación distribuida como observaciones de eventos, concesiones, elecciones y bloqueos compartidos distribuidos listas para usar (ten en cuenta que, en el caso del bloqueo compartido distribuido, los usuarios deben conocer sus propiedades no obvias. Los detalles se describen más abajo). Estas primitivas están mantenidas y soportadas por los desarrolladores de etcd; dejar estas primitivas a bibliotecas externas esquiva la responsabilidad de desarrollar software distribuido fundamental, dejando esencialmente el sistema incompleto. Las bases de datos NewSQL suelen esperar que estas primitivas de coordinación distribuida las escriban terceros. Asimismo, ZooKeeper es conocido por tener una [biblioteca][curator] separada e independiente de recetas de coordinación. Consul, que proporciona una API de bloqueo nativa, llega hasta disculparse porque no es «[un método a prueba de balas][consul-bulletproof]».

En teoría, es posible construir estas primitivas sobre cualquier sistema de almacenamiento que proporcione consistencia fuerte. Sin embargo, los algoritmos tienden a ser sutiles; es fácil desarrollar un algoritmo de bloqueo que parece funcionar, solo para romperse de repente debido a efectos manada (thundering herd) y desviaciones de temporización. Además, otras primitivas soportadas por etcd, como la memoria transaccional, dependen del modelo de datos MVCC de etcd; la simple consistencia fuerte no basta.

Para la coordinación distribuida, elegir etcd puede ayudar a prevenir dolores de cabeza operativos y ahorrar esfuerzo de ingeniería.

### Notas sobre el uso del bloqueo y la concesión {#notes-on-the-usage-of-lock-and-lease}
etcd proporciona [API de bloqueo][etcd-v3lock] que se basan en [el mecanismo de concesión][lease] y [su implementación en etcd][etcdlease]. La idea básica del mecanismo de concesión es: un servidor otorga un token, llamado concesión (lease), a un cliente que lo solicita. Cuando el servidor otorga una concesión, asocia un TTL a la concesión. Cuando el servidor detecta el paso de un tiempo mayor que el TTL, revoca la concesión. Mientras el cliente mantenga una concesión no revocada, puede afirmar que posee el acceso a un recurso asociado a la concesión. En el caso de etcd, el recurso es una clave en el espacio de claves de etcd. etcd proporciona API de bloqueo con este esquema. Sin embargo, las API de bloqueo no pueden usarse por sí solas como mecanismo de exclusión mutua. Las API se llaman de bloqueo por [razones históricas][chubby]. Las API de bloqueo sí pueden usarse, sin embargo, como mecanismo de optimización de la exclusión mutua, como se describe a continuación.

El aspecto más importante del mecanismo de concesión es que el TTL se define como un intervalo de tiempo físico. Tanto el servidor como el cliente miden el paso del tiempo con sus propios relojes. Esto permite una situación en la que el servidor revoca la concesión pero el cliente sigue afirmando que posee la concesión.

Entonces, ¿cómo garantiza el mecanismo de concesión la exclusión mutua del mecanismo de bloqueo? En realidad, el mecanismo de concesión por sí mismo no garantiza la exclusión mutua. Poseer una concesión no puede garantizar que el poseedor tenga un bloqueo sobre el recurso.

En el caso de controlar los accesos mutuos a las claves del propio etcd con el bloqueo de etcd, la exclusión mutua se implementa basándose en el mecanismo de validación del número de versión (en otros sistemas como Consul a veces se llama compare and swap). En los RPC de etcd como `Put` o `Txn`, podemos especificar las condiciones requeridas sobre el número de revisión y el ID de concesión para las operaciones. Si no se satisfacen las condiciones, la operación puede fallar. Con este mecanismo, etcd proporciona bloqueo distribuido a los clientes. Significa que un cliente sabe que está adquiriendo el bloqueo de una clave cuando sus solicitudes son completadas con éxito por el clúster de etcd.

En la literatura sobre bloqueo distribuido se describen diseños similares:
* En [el artículo de Chubby][chubby] se introduce el concepto de *secuenciador* (sequencer). Interpretamos que el secuenciador es casi lo mismo que la combinación de número de revisión e ID de concesión de etcd.
* En [How to do distributed locking][fencing], Martin Kleppmann introdujo la idea del *fencing token* (token de vallado). Los autores interpretan que el fencing token es el número de revisión en el caso de etcd.
* En [Practical Uses of Synchronized Clocks in Distributed Systems][physicalclock] podemos encontrar la descripción de que Thor implementa un mecanismo de bloqueo distribuido basado en la validación del número de versión y la concesión.

¿Por qué etcd y otros sistemas proporcionan concesiones si proporcionan exclusión mutua basada en la validación del número de versión? Bueno, las concesiones proporcionan un mecanismo de optimización para reducir el número de solicitudes abortadas.

Ten en cuenta que, en el caso de las claves de etcd, se pueden bloquear de forma eficiente gracias a los mecanismos de concesión y de validación del número de versión. Si los usuarios necesitan proteger recursos que no están relacionados con etcd, esos recursos deben proporcionar el mecanismo de validación del número de versión y la consistencia de réplicas como las claves de etcd. La característica de bloqueo del propio etcd no puede usarse para proteger recursos externos.

[chubby]: https://research.google/pubs/pub27897/
[cockroach]: https://github.com/cockroachdb/cockroach
[cockroach-grant]: https://www.cockroachlabs.com/docs/stable/grant.html
[consul-acl]: https://www.consul.io/docs/security/acl
[consul-bulletproof]: https://www.consul.io/docs/dynamic-app-config/sessions
[consul-json]: https://www.consul.io/api-docs#formatted-json-output
[consul-linread]: https://www.consul.io/api-docs#consistency
[consul-lock]: https://www.consul.io/commands/lock
[consul-reconfig]: https://developer.hashicorp.com/consul/tutorials/datacenter-operations/add-remove-servers
[consul-txn]: https://www.consul.io/api/kv#txn
[consul-watch]: https://www.consul.io/docs/dynamic-app-config/watches
[container-linux]: https://coreos.com/why
[curator]: http://curator.apache.org/
[dbtester-comparison-results]: https://github.com/coreos/dbtester/tree/master/test-results/2018Q1-02-etcd-zookeeper-consul
[etcd-commonname]: /es/etcd/op-guide/authentication/#using-tls-common-name
[etcd-etcdctl-elect]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#elect-options-election-name-proposal
[etcd-etcdctl-lock]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#lock-options-lockname-command-arg1-arg2-
[etcd-json]: /es/etcd/dev-guide/api_grpc_gateway/
[etcd-linread]: /es/etcd/learning/api_guarantees/#linearizability
[etcd-mvcc]: /es/etcd/learning/data_model/
[etcd-rbac]: /es/etcd/op-guide/authentication/rbac
[etcd-recipe]: https://godoc.org/github.com/etcd-io/etcd/client/v3/experimental/recipes
[etcd-reconfig]: /es/etcd/op-guide/runtime-configuration
[etcd-txn]: /es/etcd/learning/api/#transaction
[etcd-v3election]: https://pkg.go.dev/go.etcd.io/etcd/server/v3/etcdserver/api/v3election/v3electionpb
[etcd-v3lock]: https://pkg.go.dev/go.etcd.io/etcd/server/v3/etcdserver/api/v3lock/v3lockpb
[etcd-watch]: /es/etcd/learning/api/#watch-streams
[etcdlease]: https://godoc.org/github.com/etcd-io/etcd/client/v3/leasing
[fencing]: https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
[grpc]: https://www.grpc.io
[kubernetes]: https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/
[lease]: https://web.stanford.edu/class/cs240/readings/leases.pdf
[locksmith]: https://github.com/coreos/locksmith
[newsql-leader]: http://dl.acm.org/citation.cfm?id=2960999
[physicalclock]: https://web.archive.org/web/20190725151657/http://www.dainf.cefetpr.br/~tacla/SDII/PracticalUseOfClocks.pdf
[production-users]: https://github.com/etcd-io/etcd/blob/main/ADOPTERS.md
[spanner]: https://cloud.google.com/spanner/
[spanner-roles]: https://cloud.google.com/spanner/docs/iam#roles
[tidb]: https://github.com/pingcap/tidb
[zk-acl]: https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers.html#sc_ZooKeeperAccessControl
[zk-bindings]: https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers.html#ch_bindings
[zk-reconfig]: https://zookeeper.apache.org/doc/current/zookeeperReconfig.html
[zk-txn]: https://zookeeper.apache.org/doc/r3.4.3/api/org/apache/zookeeper/ZooKeeper.html#multi(java.lang.Iterable)
[zk-watch]: https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkWatches
