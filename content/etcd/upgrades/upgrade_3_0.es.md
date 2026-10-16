---
title: Actualizar etcd de la versión 2.3 a la 3.0
weight: 6900
description: Procesos, listas de verificación y notas sobre la actualización de etcd de la versión 2.3 a la 3.0
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_0.md"
---

En el caso general, actualizar de etcd 2.3 a 3.0 puede hacerse sin tiempo de inactividad, mediante una actualización gradual:
 - uno por uno, detén los procesos etcd v2.3 y reemplázalos por procesos etcd v3.0
 - tras ejecutar todos los procesos v3.0, las nuevas funcionalidades de v3.0 están disponibles para el clúster

Antes de [iniciar una actualización](#upgrade-procedure), lee el resto de esta guía para prepararte.

### Listas de verificación para la actualización {#upgrade-checklists}

> [!WARNING]
> Al [migrar desde v2 sin datos v3](https://github.com/etcd-io/etcd/issues/9480), el servidor etcd v3.2+ entra en pánico cuando etcd restaura desde instantáneas existentes pero no existe un archivo v3 `ETCD_DATA_DIR/member/snap/db`. Esto ocurre cuando el servidor había migrado desde v2 sin datos v3 previos. Esto también evita la pérdida accidental de datos v3 (por ejemplo, el archivo `db` podría haberse movido). etcd exige que la operación posterior a la migración a v3 solo pueda realizarse con datos v3. No actualices a versiones v3 más recientes hasta que el servidor v3.0 contenga datos v3.

#### Requisitos de actualización {#upgrade-requirements}

Para actualizar un despliegue etcd existente a 3.0, el clúster en ejecución debe ser la versión 2.3 o superior. Si es anterior a 2.3, actualiza primero a la versión [2.3](https://github.com/etcd-io/etcd/releases/tag/v2.3.8) antes de actualizar a 3.0.

Además, para garantizar una actualización gradual sin contratiempos, el clúster en ejecución debe estar en buen estado. Comprueba el estado del clúster con el comando `etcdctl cluster-health` antes de continuar.

#### Preparación {#preparation}

Antes de actualizar etcd, prueba siempre en un entorno de preproducción los servicios que dependen de etcd antes de desplegar la actualización en el entorno de producción.

Antes de comenzar, [haz una copia de seguridad del directorio de datos de etcd](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore). Si algo sale mal con la actualización, es posible usar esta copia de seguridad para [revertir la actualización](#downgrade) y volver a la versión de etcd existente.

#### Versiones mixtas {#mixed-versions}

Durante la actualización, un clúster etcd admite versiones mixtas de miembros etcd y opera con el protocolo de la versión común más baja. El clúster solo se considera actualizado cuando todos sus miembros se han actualizado a la versión 3.0. Internamente, los miembros etcd negocian entre sí para determinar la versión global del clúster, que controla la versión notificada y las funcionalidades admitidas.

#### Limitaciones {#limitations}

El miembro recién actualizado puede tardar hasta 2 minutos en ponerse al día con el clúster existente cuando el tamaño total de los datos es mayor de 50MB. Comprueba el tamaño de una instantánea reciente para estimar el tamaño total de los datos. Dicho de otro modo, lo más seguro es esperar 2 minutos entre la actualización de cada miembro.

Para un tamaño total de datos mucho mayor, de 100MB o más, este proceso único puede tardar aún más tiempo. Los administradores de clústeres etcd muy grandes de esta magnitud pueden contactar libremente con el [equipo de etcd][etcd-contact] antes de actualizar, y estaremos encantados de asesorar sobre el procedimiento.

#### Revertir la actualización {#downgrade}

Si todos los miembros se han actualizado a v3.0, el clúster quedará actualizado a v3.0, y revertir la actualización desde este estado completado **no es posible**. Sin embargo, si un solo miembro sigue en v2.3, el clúster y sus operaciones siguen siendo «v2.3», y desde este estado de clúster mixto es posible volver a utilizar un binario etcd v2.3 en todos los miembros.

Haz una [copia de seguridad del directorio de datos](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore) de todos los miembros etcd para que revertir el clúster a la versión anterior siga siendo posible incluso después de que se haya actualizado por completo.

### Procedimiento de actualización {#upgrade-procedure}

Este ejemplo detalla la actualización de un clúster etcd v2.3 de tres miembros que se ejecuta en una máquina local.

#### 1. Comprueba los requisitos de actualización. {#1-check-upgrade-requirements}

¿Está el clúster en buen estado y ejecutando la versión v.2.3.x?

```
$ etcdctl cluster-health
member 6e3bd23ae5f1eae0 is healthy: got healthy result from http://localhost:22379
member 924e2e83e93f2560 is healthy: got healthy result from http://localhost:32379
member 8211f1d0f64f3269 is healthy: got healthy result from http://localhost:12379
cluster is healthy

$ curl http://localhost:2379/version
{"etcdserver":"2.3.x","etcdcluster":"2.3.8"}
```

#### 2. Detén el proceso etcd existente {#2-stop-the-existing-etcd-process}

Cuando se detiene cada proceso etcd, los demás miembros del clúster registrarán errores predecibles. Esto es normal, ya que la conexión con un miembro del clúster se ha roto (temporalmente):

```
2016-06-27 15:21:48.624124 E | rafthttp: failed to dial 8211f1d0f64f3269 on stream Message (dial tcp 127.0.0.1:12380: getsockopt: connection refused)
2016-06-27 15:21:48.624175 I | rafthttp: the connection with 8211f1d0f64f3269 became inactive
```

En este punto es buena idea [hacer una copia de seguridad del directorio de datos de etcd](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore) para disponer de una vía de retorno en caso de que surjan problemas:

```
$ etcdctl backup \
      --data-dir /var/lib/etcd \
      --backup-dir /tmp/etcd_backup
```

#### 3. Sustituye el binario por etcd v3.0 e inicia el nuevo proceso etcd {#3-drop-in-etcd-v30-binary-and-start-the-new-etcd-process}

El nuevo etcd v3.0 publicará su información en el clúster:

```
09:58:25.938673 I | etcdserver: published {Name:infra1 ClientURLs:[http://localhost:12379]} to cluster 524400597fb1d5f6
```

Comprueba que cada miembro, y después el clúster completo, queda en buen estado con el nuevo binario etcd v3.0:

```
$ etcdctl cluster-health
member 6e3bd23ae5f1eae0 is healthy: got healthy result from http://localhost:22379
member 924e2e83e93f2560 is healthy: got healthy result from http://localhost:32379
member 8211f1d0f64f3269 is healthy: got healthy result from http://localhost:12379
cluster is healthy
```


Los miembros actualizados registrarán avisos como el siguiente hasta que todo el clúster esté actualizado. Esto es de esperar y cesará cuando todos los miembros del clúster etcd se hayan actualizado a v3.0:

```
2016-06-27 15:22:05.679644 W | etcdserver: the local etcd version 2.3.7 is not up-to-date
2016-06-27 15:22:05.679660 W | etcdserver: member 8211f1d0f64f3269 has a higher version 3.0.0
```

#### 4. Repite del paso 2 al paso 3 para todos los demás miembros {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Finalizar {#5-finish}

Cuando todos los miembros estén actualizados, el clúster notificará la actualización correcta a 3.0:

```
2016-06-27 15:22:19.873751 N | membership: updated the cluster version from 2.3 to 3.0
2016-06-27 15:22:19.914574 I | api: enabled capabilities for version 3.0.0
```

```
$ ETCDCTL_API=3 etcdctl endpoint health
127.0.0.1:12379 is healthy: successfully committed proposal: took = 18.440155ms
127.0.0.1:32379 is healthy: successfully committed proposal: took = 13.651368ms
127.0.0.1:22379 is healthy: successfully committed proposal: took = 18.513301ms
```

## Consideraciones adicionales {#further-considerations}

- Las variables de entorno de etcdctl se han actualizado. Si `ETCDCTL_API=2 etcdctl cluster-health` funciona correctamente pero `ETCDCTL_API=3 etcdctl endpoints health` responde con `Error:  grpc: timed out when dialing`, asegúrate de usar los [nuevos nombres de variables](https://github.com/etcd-io/etcd/tree/main/etcdctl#etcdctl).

## Problemas conocidos {#known-issues}

- etcd &lt; v3.1 no funciona correctamente si se compila con Go &gt; v1.7. Consulta la [incidencia 6951](https://github.com/etcd-io/etcd/issues/6951) para obtener más información.
- Si un error como `transport: http2Client.notifyError got notified that the client transport was broken unexpected EOF.` aparece en los registros del servidor etcd, asegúrate de que etcd sea una versión precompilada o esté compilada con (etcd v3.1+ &amp; go v1.7+) o (etcd &lt;v3.1 &amp; go v1.6.x).
- Añadir un nodo v3 a un clúster v2.3 durante las actualizaciones no está soportado y podría provocar pánicos. Consulta la [incidencia 7249](https://github.com/etcd-io/etcd/issues/7429) para obtener más información. Las versiones mixtas de miembros etcd solo están permitidas durante la migración a v3. Termina las actualizaciones antes de hacer cualquier cambio en la composición del clúster.

[etcd-contact]: https://groups.google.com/g/etcd-dev
