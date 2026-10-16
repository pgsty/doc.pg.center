---
title: Reconfiguración en tiempo de ejecución
weight: 4700
description: soporte de etcd para la reconfiguración incremental en tiempo de ejecución
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/runtime-configuration.md"
---

etcd incorpora soporte para la reconfiguración incremental en tiempo de ejecución, lo que permite a los usuarios actualizar la pertenencia del clúster en tiempo de ejecución.

Las solicitudes de reconfiguración solo pueden procesarse cuando funciona una mayoría de los miembros del clúster. Es **muy recomendable** tener siempre un clúster de tamaño mayor que dos en producción. No es seguro eliminar un miembro de un clúster de dos miembros. La mayoría de un clúster de dos miembros también es dos. Si se produce un fallo durante el proceso de eliminación, el clúster podría no ser capaz de avanzar y necesitar [reiniciarse tras un fallo de mayoría][majority failure].

Para comprender mejor el diseño detrás de la reconfiguración en tiempo de ejecución, lee [el documento de reconfiguración en tiempo de ejecución][runtime-reconf].

## Casos de uso de la reconfiguración {#reconfiguration-use-cases}

Esta sección recorre algunas razones habituales para reconfigurar un clúster. La mayoría de estas razones simplemente implican combinaciones de añadir o eliminar un miembro, que se explican más abajo en [Operaciones de reconfiguración del clúster][cluster-reconf].

### Rotación o actualización de varias máquinas {#cycle-or-upgrade-multiple-machines}

Si varios miembros del clúster deben moverse debido a mantenimiento planificado (actualizaciones de hardware, tiempos de inactividad de red, etc.), se recomienda modificar los miembros de uno en uno.

Es seguro eliminar al líder, aunque hay un breve periodo de inactividad mientras se realiza el proceso de elección. Si el clúster contiene más de 50MB de datos v2, se recomienda [migrar el directorio de datos del miembro][member migration].

### Cambiar el tamaño del clúster {#change-the-cluster-size}

Aumentar el tamaño del clúster puede mejorar la [tolerancia a fallos][fault tolerance table] y proporcionar mejor rendimiento de lectura. Dado que los clientes pueden leer desde cualquier miembro, aumentar el número de miembros incrementa la tasa total de lecturas serializables.

Reducir el tamaño del clúster puede mejorar el rendimiento de escritura del clúster, a cambio de una resiliencia menor. Las escrituras en el clúster se replican en una mayoría de los miembros del clúster antes de considerarse confirmadas. Reducir el tamaño del clúster reduce la mayoría, y cada escritura se confirma más rápidamente.

### Reemplazar una máquina fallida {#replace-a-failed-machine}

Si una máquina falla debido a un fallo de hardware, corrupción del directorio de datos o alguna otra situación fatal, debe reemplazarse cuanto antes. Las máquinas que han fallado pero no se han eliminado afectan negativamente al cuórum y reducen la tolerancia a un fallo adicional.

Para reemplazar la máquina, sigue las instrucciones para [eliminar el miembro][remove member] del clúster y luego [añadir un nuevo miembro][add member] en su lugar. Si el clúster contiene más de 50MB, se recomienda [migrar el directorio de datos del miembro fallido][member migration] si todavía es accesible.

### Reiniciar el clúster tras un fallo de mayoría {#restart-cluster-from-majority-failure}

Si se pierde la mayoría del clúster o todos los nodos han cambiado de dirección IP, es necesaria una acción manual para recuperarse de forma segura. Los pasos básicos del proceso de recuperación incluyen [crear un clúster nuevo usando los datos antiguos][disaster recovery], forzar que un solo miembro actúe como líder y, finalmente, usar la configuración en tiempo de ejecución para [añadir nuevos miembros][add member] a este clúster nuevo de uno en uno.

### Recuperar el clúster de un fallo de minoría {#recover-cluster-from-minority-failure}

Si se pierde un miembro específico, equivale a reemplazar una máquina fallida. Los pasos se describen en [Reemplazar una máquina fallida](/es/etcd/op-guide/runtime-configuration/#replace-a-failed-machine).

## Operaciones de reconfiguración del clúster {#cluster-reconfiguration-operations}

Con estos casos de uso en mente, se pueden describir las operaciones involucradas para cada uno.

Antes de realizar cualquier cambio, debe estar disponible una mayoría simple (cuórum) de los miembros de etcd. Este es esencialmente el mismo requisito que para cualquier tipo de escritura en etcd.

Todos los cambios en el clúster deben hacerse secuencialmente:

* Para actualizar las peerURLs de un solo miembro, emite una operación de actualización
* Para reemplazar un único miembro sano, elimina el miembro antiguo y luego añade un miembro nuevo
* Para pasar de 3 a 5 miembros, emite dos operaciones de adición
* Para pasar de 5 a 3, emite dos operaciones de eliminación

Todos estos ejemplos usan la herramienta de línea de comandos `etcdctl` que viene con etcd. Para cambiar la pertenencia sin `etcdctl`, usa la [API de miembros gRPC v3][member-api-grpc].

### Actualizar un miembro {#update-a-member}

#### Actualizar las URLs de cliente anunciadas {#update-advertise-client-urls}

Para actualizar las URLs de cliente anunciadas de un miembro, simplemente reinicia ese miembro con el indicador de URLs de cliente actualizado (`--advertise-client-urls`) o la variable de entorno (`ETCD_ADVERTISE_CLIENT_URLS`) actualizada. El miembro reiniciado publicará por sí mismo las URLs actualizadas. Una URL de cliente actualizada incorrectamente no afectará a la salud del clúster de etcd.

#### Actualizar las URLs de par anunciadas {#update-advertise-peer-urls}

Para actualizar las URLs de par anunciadas de un miembro, primero actualízalas explícitamente mediante el comando member y luego reinicia el miembro. Esta acción adicional es necesaria porque actualizar las URLs de par modifica la configuración de todo el clúster y puede afectar a la salud del clúster de etcd.

Para actualizar las URLs de par anunciadas, primero encuentra el ID del miembro objetivo. Para listar todos los miembros con `etcdctl`:

```sh
$ etcdctl member list
6e3bd23ae5f1eae0: name=node2 peerURLs=http://localhost:23802 clientURLs=http://127.0.0.1:23792
924e2e83e93f2560: name=node3 peerURLs=http://localhost:23803 clientURLs=http://127.0.0.1:23793
a8266ecf031671f3: name=node1 peerURLs=http://localhost:23801 clientURLs=http://127.0.0.1:23791
```

Este ejemplo hará `update` del miembro con ID a8266ecf031671f3 y cambiará su valor de peerURLs a `http://10.0.1.10:2380`:

```sh
$ etcdctl member update a8266ecf031671f3 --peer-urls=http://10.0.1.10:2380
Updated member with ID a8266ecf031671f3 in cluster
```

### Eliminar un miembro {#remove-a-member}

Supongamos que el ID del miembro a eliminar es a8266ecf031671f3. Usa el comando `remove` para realizar la eliminación:

```sh
$ etcdctl member remove a8266ecf031671f3
Removed member a8266ecf031671f3 from cluster
```

El miembro objetivo se detendrá por sí mismo en este punto e imprimirá la eliminación en el registro:

```
etcd: this member has been permanently removed from the cluster. Exiting.
```

Es seguro eliminar al líder; sin embargo, el clúster estará inactivo mientras se elige a un nuevo líder. Esta duración es normalmente el periodo del tiempo de espera de elección más el proceso de votación.

### Añadir un nuevo miembro {#add-a-new-member}

Añadir un miembro es un proceso de dos pasos:

 * Añade el nuevo miembro al clúster mediante la [API de miembros gRPC v3][member-api-grpc] o el comando `etcdctl member add`.
 * Inicia el nuevo miembro con la nueva configuración del clúster, incluyendo una lista de los miembros actualizados (miembros existentes + el miembro nuevo).

`etcdctl` añade un nuevo miembro al clúster especificando el [nombre][conf-name] del miembro y las [URLs de par anunciadas][conf-adv-peer]:

```sh
$ etcdctl member add infra3 --peer-urls=http://10.0.1.13:2380
added member 9bf1b35fc7761a23 to cluster

ETCD_NAME="infra3"
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
ETCD_INITIAL_CLUSTER_STATE=existing
```

`etcdctl` ha informado al clúster sobre el nuevo miembro y ha mostrado las variables de entorno necesarias para iniciarlo con éxito. Ahora inicia el nuevo proceso de etcd con los indicadores pertinentes para el miembro nuevo:

```sh
$ export ETCD_NAME="infra3"
$ export ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
$ export ETCD_INITIAL_CLUSTER_STATE=existing
$ etcd --listen-client-urls http://10.0.1.13:2379 --advertise-client-urls http://10.0.1.13:2379 --listen-peer-urls http://10.0.1.13:2380 --initial-advertise-peer-urls http://10.0.1.13:2380 --data-dir %data_dir%
```

El nuevo miembro se ejecutará como parte del clúster y comenzará inmediatamente a ponerse al día con el resto del clúster.

Si se añaden varios miembros, la mejor práctica es configurar un solo miembro cada vez y verificar que arranca correctamente antes de añadir más miembros nuevos. Si se añade un miembro nuevo a un clúster de 1 nodo, el clúster no puede avanzar antes de que el miembro nuevo arranque, porque necesita dos miembros como mayoría para acordar el consenso. Este comportamiento solo ocurre entre el momento en que `etcdctl member add` informa al clúster sobre el nuevo miembro y el momento en que el nuevo miembro establece con éxito una conexión con el existente.

#### Añadir un nuevo miembro como learner {#add-a-new-member-as-learner}

A partir de v3.4, etcd admite añadir un nuevo miembro como learner / miembro sin derecho a voto.
La motivación y el diseño se pueden encontrar en el [documento de diseño][design-learner].
Para hacer más seguro el proceso de añadir un nuevo miembro,
y para reducir el tiempo de inactividad del clúster cuando se añade el nuevo miembro, se recomienda que el nuevo miembro se añada al clúster
como learner hasta que se ponga al día. Esto puede describirse como un proceso de tres pasos:

 * Añade el nuevo miembro como learner mediante la [API de miembros gRPC][member-api-grpc] o el comando `etcdctl member add --learner`.

 * Inicia el nuevo miembro con la nueva configuración del clúster, incluyendo una lista de los miembros actualizados (miembros existentes + el miembro nuevo).
 Este paso es exactamente el mismo que el anterior.

 * Promociona el learner recién añadido a miembro con derecho a voto mediante la [API de miembros gRPC][member-api-grpc] o el comando `etcdctl member promote`.
 El servidor de etcd valida la solicitud de promoción para garantizar su seguridad operativa.
 Solo después de que su registro de raft haya alcanzado al del líder puede el learner promocionarse a miembro con derecho a voto.
 Si un miembro learner no ha alcanzado el registro de raft del líder, la solicitud de promoción del miembro fallará
 (consulta la sección [casos de error al promover un miembro][error cases when promoting a member] para más detalles).
 En este caso, el usuario debe esperar y volver a intentarlo más tarde.

En v3.4, el servidor de etcd limita a uno el número de learners que puede tener un clúster. La consideración principal es limitar la
carga de trabajo extra sobre el líder debido a la propagación de datos del líder al learner.

Usa `etcdctl member add` con el indicador `--learner` para añadir un nuevo miembro al clúster como learner.

```sh
$ etcdctl member add infra3 --peer-urls=http://10.0.1.13:2380 --learner
Member 9bf1b35fc7761a23 added to cluster a7ef944b95711739

ETCD_NAME="infra3"
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
ETCD_INITIAL_CLUSTER_STATE=existing
```

Una vez iniciado el nuevo proceso de etcd para el miembro learner recién añadido, usa `etcdctl member promote` para promocionar el learner a miembro con derecho a voto.
```
$ etcdctl member promote 9bf1b35fc7761a23
Member 9e29bbaa45d74461 promoted in cluster a7ef944b95711739
```

#### Casos de error al añadir miembros {#error-cases-when-adding-members}

En el siguiente caso, un host nuevo no está incluido en la lista de nodos enumerados. Si este es un clúster nuevo, el nodo debe añadirse a la lista de miembros iniciales del clúster.

```sh
$ etcd --name infra3 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state existing
etcdserver: assign ids error: the member count is unequal
exit 1
```

En este ejemplo de fallo, el miembro arranca con una dirección (10.0.1.14:2380) que difiere de la dirección de par registrada (10.0.1.13:2380):

```sh
$ etcd --name infra4 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra4=http://10.0.1.14:2380 \
  --initial-cluster-state existing
etcdserver: assign ids error: unmatched member while checking PeerURLs
exit 1
```

Si etcd arranca usando el directorio de datos de un miembro eliminado, etcd sale automáticamente si se conecta a cualquier miembro activo del clúster:

```sh
$ etcd
etcd: this member has been permanently removed from the cluster. Exiting.
exit 1
```

#### Casos de error al añadir un miembro learner {#error-cases-when-adding-a-learner-member}

No se puede añadir un learner al clúster si el clúster ya tiene 1 learner (v3.4).
```
$ etcdctl member add infra4 --peer-urls=http://10.0.1.14:2380 --learner
Error: etcdserver: too many learner members in cluster
```

#### Casos de error al promover un miembro learner {#error-cases-when-promoting-a-learner-member}

Un learner solo puede promocionarse a miembro con derecho a voto si está sincronizado con el líder.
```
$ etcdctl member promote 9bf1b35fc7761a23
Error: etcdserver: can only promote a learner member which is in sync with leader
```

Promocionar un miembro que no es learner fallará.
```
$ etcdctl member promote 9bf1b35fc7761a23
Error: etcdserver: can only promote a learner member
```

Promocionar un miembro que no existe en el clúster fallará.
```
$ etcdctl member promote 12345abcde
Error: etcdserver: member not found
```


### Modo de comprobación estricta de la reconfiguración (`-strict-reconfig-check`) {#strict-reconfiguration-check-mode--strict-reconfig-check}

Como se ha descrito anteriormente, la mejor práctica para añadir nuevos miembros es configurar un solo miembro cada vez y verificar que arranca correctamente antes de añadir más miembros nuevos. Este enfoque paso a paso es muy importante porque si los miembros recién añadidos no están configurados correctamente (por ejemplo, si las URLs de par son incorrectas), el clúster puede perder el cuórum. La pérdida de cuórum ocurre porque el miembro recién añadido se cuenta en el cuórum aunque ese miembro no sea accesible desde los demás miembros existentes. También puede producirse una pérdida de cuórum si hay un problema de conectividad o problemas operativos.

Para evitar este problema, etcd proporciona la opción `-strict-reconfig-check`. Si se pasa esta opción a etcd, etcd rechaza las solicitudes de reconfiguración si el número de miembros iniciados va a ser menor que un cuórum del clúster reconfigurado.

Está activada por defecto.

[add member]: #add-a-new-member
[cluster-reconf]: #cluster-reconfiguration-operations
[conf-adv-peer]: /es/etcd/op-guide/configuration#clustering
[conf-name]: /es/etcd/op-guide/configuration#member
[design-learner]: /es/etcd/learning/design-learner
[disaster recovery]: /es/etcd/op-guide/recovery
[error cases when promoting a member]: #error-cases-when-promoting-a-learner-member
[fault tolerance table]: https://etcd.io/docs/v2.3/admin_guide/#fault-tolerance-table
[majority failure]: #restart-cluster-from-majority-failure
[member migration]: https://etcd.io/docs/v2.3/admin_guide/#member-migration
[member-api]: https://etcd.io/docs/v2.3/members_api/
[member-api-grpc]: /es/etcd/dev-guide/api_reference_v3/
[remove member]: #remove-a-member
[runtime-reconf]: /es/etcd/op-guide/runtime-reconf-design/
