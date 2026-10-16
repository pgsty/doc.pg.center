---
title: Actualizar etcd de la versión 3.0 a la 3.1
weight: 6850
description: Procesos, listas de verificación y notas sobre la actualización de etcd de la versión 3.0 a la 3.1
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_1.md"
---

En el caso general, actualizar de etcd 3.0 a 3.1 puede hacerse sin tiempo de inactividad, mediante una actualización gradual:
 - uno por uno, detén los procesos etcd v3.0 y reemplázalos por procesos etcd v3.1
 - tras ejecutar todos los procesos v3.1, las nuevas funcionalidades de v3.1 están disponibles para el clúster

Antes de [iniciar una actualización](#upgrade-procedure), lee el resto de esta guía para prepararte.

### Listas de verificación para la actualización {#upgrade-checklists}

> [!WARNING]
> Al [migrar desde v2 sin datos v3](https://github.com/etcd-io/etcd/issues/9480), el servidor etcd v3.2+ entra en pánico cuando etcd restaura desde instantáneas existentes pero no existe un archivo v3 `ETCD_DATA_DIR/member/snap/db`. Esto ocurre cuando el servidor había migrado desde v2 sin datos v3 previos. Esto también evita la pérdida accidental de datos v3 (por ejemplo, el archivo `db` podría haberse movido). etcd exige que la operación posterior a la migración a v3 solo pueda realizarse con datos v3. No actualices a versiones v3 más recientes hasta que el servidor v3.0 contenga datos v3.

#### Monitorización {#monitoring}

Las siguientes métricas de v3.0.x han quedado obsoletas en favor de [go-grpc-prometheus](https://github.com/grpc-ecosystem/go-grpc-prometheus):

- `etcd_grpc_requests_total`
- `etcd_grpc_requests_failed_total`
- `etcd_grpc_active_streams`
- `etcd_grpc_unary_requests_duration_seconds`

#### Requisitos de actualización {#upgrade-requirements}

Para actualizar un despliegue etcd existente a 3.1, el clúster en ejecución debe ser la versión 3.0 o superior. Si es anterior a 3.0, [actualiza primero a 3.0](/es/etcd/upgrades/upgrade_3_0) antes de actualizar a 3.1.

Además, para garantizar una actualización gradual sin contratiempos, el clúster en ejecución debe estar en buen estado. Comprueba el estado del clúster con el comando `etcdctl endpoint health` antes de continuar.

#### Preparación {#preparation}

Antes de actualizar etcd, prueba siempre en un entorno de preproducción los servicios que dependen de etcd antes de desplegar la actualización en el entorno de producción.

Antes de comenzar, [haz una copia de seguridad de los datos de etcd](/es/etcd/op-guide/maintenance/#snapshot-backup). Si algo sale mal con la actualización, es posible usar esta copia de seguridad para [revertir la actualización](#downgrade) y volver a la versión de etcd existente. Ten en cuenta que el comando `snapshot` solo hace copia de seguridad de los datos v3. Para los datos v2, consulta [copia de seguridad del almacén de datos v2](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

#### Versiones mixtas {#mixed-versions}

Durante la actualización, un clúster etcd admite versiones mixtas de miembros etcd y opera con el protocolo de la versión común más baja. El clúster solo se considera actualizado cuando todos sus miembros se han actualizado a la versión 3.1. Internamente, los miembros etcd negocian entre sí para determinar la versión global del clúster, que controla la versión notificada y las funcionalidades admitidas.

#### Limitaciones {#limitations}

Nota: Si el clúster solo tiene datos v3 y ningún dato v2, no está sujeto a esta limitación.

Si el clúster sirve un conjunto de datos v2 de más de 50MB, cada miembro recién actualizado puede tardar hasta dos minutos en ponerse al día con el clúster existente. Comprueba el tamaño de una instantánea reciente para estimar el tamaño total de los datos. Dicho de otro modo, lo más seguro es esperar 2 minutos entre la actualización de cada miembro.

Para un tamaño total de datos mucho mayor, de 100MB o más, este proceso único puede tardar aún más tiempo. Los administradores de clústeres etcd muy grandes de esta magnitud pueden contactar libremente con el [equipo de etcd][etcd-contact] antes de actualizar, y estaremos encantados de asesorar sobre el procedimiento.

#### Revertir la actualización {#downgrade}

Si todos los miembros se han actualizado a v3.1, el clúster quedará actualizado a v3.1, y revertir la actualización desde este estado completado **no es posible**. Sin embargo, si un solo miembro sigue en v3.0, el clúster y sus operaciones siguen siendo «v3.0», y desde este estado de clúster mixto es posible volver a utilizar un binario etcd v3.0 en todos los miembros.

Haz una [copia de seguridad del directorio de datos](/es/etcd/op-guide/maintenance#snapshot-backup) de todos los miembros etcd para que revertir el clúster a la versión anterior siga siendo posible incluso después de que se haya actualizado por completo.

### Procedimiento de actualización {#upgrade-procedure}

Este ejemplo muestra cómo actualizar un clúster etcd v3.0 de 3 miembros que se ejecuta en una máquina local.

#### 1. Comprueba los requisitos de actualización {#1-check-upgrade-requirements}

¿Está el clúster en buen estado y ejecutando la versión v3.0.x?

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.0.16","etcdcluster":"3.0.0"}
```

#### 2. Detén el proceso etcd existente {#2-stop-the-existing-etcd-process}

Cuando se detiene cada proceso etcd, los demás miembros del clúster registrarán errores predecibles. Esto es normal, ya que la conexión con un miembro del clúster se ha roto (temporalmente):

```
2017-01-17 09:34:18.352662 I | raft: raft.node: 1640829d9eea5cfb elected leader 1640829d9eea5cfb at term 5
2017-01-17 09:34:18.359630 W | etcdserver: failed to reach the peerURL(http://localhost:2380) of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
2017-01-17 09:34:18.359679 W | etcdserver: cannot get the version of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
2017-01-17 09:34:18.548116 W | rafthttp: lost the TCP streaming connection with peer fd32987dcd0511e0 (stream Message writer)
2017-01-17 09:34:19.147816 W | rafthttp: lost the TCP streaming connection with peer fd32987dcd0511e0 (stream MsgApp v2 writer)
2017-01-17 09:34:34.364907 W | etcdserver: failed to reach the peerURL(http://localhost:2380) of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
```

En este punto es buena idea [hacer una copia de seguridad de los datos de etcd](/es/etcd/op-guide/maintenance#snapshot-backup) para disponer de una vía de retorno en caso de que surjan problemas:

```
$ etcdctl snapshot save backup.db
```

#### 3. Sustituye el binario por etcd v3.1 e inicia el nuevo proceso etcd {#3-drop-in-etcd-v31-binary-and-start-the-new-etcd-process}

El nuevo etcd v3.1 publicará su información en el clúster:

```
2017-01-17 09:36:00.996590 I | etcdserver: published {Name:my-etcd-1 ClientURLs:[http://localhost:2379]} to cluster 46bc3ce73049e678
```

Comprueba que cada miembro, y después el clúster completo, queda en buen estado con el nuevo binario etcd v3.1:

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321671ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

Los miembros actualizados registrarán avisos como el siguiente hasta que todo el clúster esté actualizado. Esto es de esperar y cesará cuando todos los miembros del clúster etcd se hayan actualizado a v3.1:

```
2017-01-17 09:36:38.406268 W | etcdserver: the local etcd version 3.0.16 is not up-to-date
2017-01-17 09:36:38.406295 W | etcdserver: member fd32987dcd0511e0 has a higher version 3.1.0
2017-01-17 09:36:42.407695 W | etcdserver: the local etcd version 3.0.16 is not up-to-date
2017-01-17 09:36:42.407730 W | etcdserver: member fd32987dcd0511e0 has a higher version 3.1.0
```

#### 4. Repite del paso 2 al paso 3 para todos los demás miembros {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Finalizar {#5-finish}

Cuando todos los miembros estén actualizados, el clúster notificará la actualización correcta a 3.1:

```
2017-01-17 09:37:03.100015 I | etcdserver: updating the cluster version from 3.0 to 3.1
2017-01-17 09:37:03.104263 N | etcdserver/membership: updated the cluster version from 3.0 to 3.1
2017-01-17 09:37:03.104374 I | etcdserver/api: enabled capabilities for version 3.1
```

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 2.312897ms
localhost:22379 is healthy: successfully committed proposal: took = 2.553476ms
localhost:32379 is healthy: successfully committed proposal: took = 2.516902ms
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
