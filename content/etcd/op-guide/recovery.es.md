---
title: Recuperación ante desastres
weight: 4275
description: funcionalidades de instantánea y restauración de etcd v3
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/recovery.md"
---

etcd está diseñado para resistir fallos de máquina. Un clúster de etcd se recupera automáticamente de fallos temporales (por ejemplo, reinicios de máquina) y tolera hasta *(N-1)/2* fallos permanentes en un clúster de N miembros. Cuando un miembro falla de forma permanente, ya sea por un fallo de hardware o por corrupción del disco, pierde el acceso al clúster. Si el clúster pierde permanentemente más de *(N-1)/2* miembros, sufre un fallo catastrófico y pierde el cuórum de forma irrevocable. Una vez perdido el cuórum, el clúster no puede alcanzar consenso y, por lo tanto, no puede seguir aceptando actualizaciones.

Para recuperarse de un fallo catastrófico, etcd v3 proporciona funcionalidades de instantánea y restauración para recrear el clúster sin pérdida de datos de las claves v3. Para recuperar las claves v2, consulta la [guía de administración v2][v2_recover].

[v2_recover]: https://etcd.io/docs/v2.3/admin_guide#disaster-recovery

## Instantánea del espacio de claves {#snapshotting-the-keyspace}

Para recuperar un clúster primero se necesita una instantánea del espacio de claves de un miembro de etcd. Se puede tomar una instantánea de un miembro en ejecución con el comando `etcdctl snapshot save` o copiando el archivo `member/snap/db` de un directorio de datos de etcd. Por ejemplo, el siguiente comando guarda una instantánea del espacio de claves servido por `$ENDPOINT` en el archivo `snapshot.db`:

```sh
$ ETCDCTL_API=3 etcdctl --endpoints $ENDPOINT snapshot save snapshot.db
```

Ten en cuenta que tomar la instantánea desde el archivo `member/snap/db` puede perder datos que aún no se han escrito, pero que están incluidos en la carpeta wal (write-ahead-log).

## Estado de una instantánea {#status-of-a-snapshot}

Para saber qué revisión y qué hash contiene una instantánea determinada, puedes usar el comando `etcdutl snapshot status`:

```sh
$ etcdutl snapshot status snapshot.db -w table
+---------+----------+------------+------------+
|  HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+---------+----------+------------+------------+
| 7ef846e |   485261 |      11642 |      94 MB |
+---------+----------+------------+------------+
```

## Restauración de un clúster {#restoring-a-cluster}

### Diferencia de revisión {#revision-difference}

Al restaurar un clúster, los clientes existentes pueden percibir que la revisión retrocede cientos o miles de unidades. Esto se debe a que una instantánea determinada solo contiene el linaje de datos hasta el momento en que se tomó, mientras que el estado actual ya podría estar más avanzado.

Esto es un problema especialmente al ejecutar Kubernetes sobre etcd, donde los controladores y operadores pueden usar los llamados `informers`, que actúan como cachés locales y reciben notificaciones de actualizaciones mediante watches. Restaurar a una revisión más antigua puede no refrescar correctamente las cachés, lo que provoca un comportamiento impredecible e inconsistente en los controladores.

Al restaurar a partir de una instantánea en el contexto de: consumidores conocidos de la API de watch, copias en caché locales de los datos de etcd o el uso de Kubernetes en general, es muy recomendable restaurar mediante los «incrementos de revisión» que se describen a continuación.

### Restauración a partir de una instantánea {#restoring-from-snapshot}

Para restaurar un clúster, lo único necesario es un único archivo de instantánea «db». La restauración de un clúster con `etcdutl snapshot restore` crea nuevos directorios de datos de etcd; todos los miembros deben restaurar usando la misma instantánea. La restauración sobrescribe algunos metadatos de la instantánea (concretamente, el ID de miembro y el ID de clúster); el miembro pierde su identidad anterior. Esta sobrescritura de metadatos evita que el nuevo miembro se una inadvertidamente a un clúster existente. Por lo tanto, para iniciar un clúster a partir de una instantánea, la restauración debe iniciar un clúster lógico nuevo.

Una restauración sencilla se puede ejecutar así:

```sh
$ etcdutl snapshot restore snapshot.db --data-dir output-dir
```

### Comprobaciones de integridad {#integrity-checks}

La integridad de la instantánea puede verificarse opcionalmente en el momento de la restauración. Si la instantánea se toma con `etcdctl snapshot save`, contendrá un hash de integridad que `etcdutl snapshot restore` comprueba. Si la instantánea se copia desde el directorio de datos, no hay hash de integridad y solo se restaurará usando `--skip-hash-check`.


### Restauración con incremento de revisión {#restoring-with-revision-bump}

Para garantizar que las revisiones nunca disminuyan tras una restauración, puedes suministrar la opción `--bump-revision`. Esta opción recibe un entero de 64 bits que indica cuántas revisiones hay que añadir a la revisión actual de la instantánea. Dado que cada escritura en etcd incrementa la revisión en uno, puedes cubrir una instantánea con una semana de antigüedad incrementando en 1'000'000'000, suponiendo que etcd se ejecute con menos de 1500 escrituras por segundo.

En el contexto de los controladores de Kubernetes, es importante además marcar todas las revisiones, incluido el incremento, como compactadas usando `--mark-compacted`. Esto garantiza que todos los watches se terminen y que etcd no responda a solicitudes sobre revisiones ocurridas después de tomar la instantánea, invalidando eficazmente las cachés de los informers.

Una invocación completa puede tener este aspecto:

```sh
$ etcdutl snapshot restore snapshot.db --bump-revision 1000000000 --mark-compacted --data-dir output-dir
```

### Restauración con pertenencia actualizada {#restoring-with-updated-membership}

Los miembros de un clúster de etcd se almacenan en el propio etcd y se mantienen mediante el algoritmo de consenso raft. Cuando el cuórum se pierde por completo, es posible que quieras reconsiderar dónde y cómo se forma el nuevo clúster, por ejemplo, en un conjunto de miembros completamente nuevo.

Al restaurar a partir de una instantánea, puedes suministrar directamente la nueva pertenencia en el almacén de datos de la siguiente manera:

```sh
$ etcdutl snapshot restore snapshot.db \
  --name m1 \
  --data-dir m1.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host1:2380
```

Esto garantiza que el clúster recién construido solo se conecte a los demás miembros restaurados con el token dado y no a miembros antiguos que aún podrían estar activos e intentar conectarse.

Alternativamente, al iniciar etcd, puedes suministrar `--force-new-cluster` para sobrescribir la pertenencia del clúster conservando los datos de aplicación existentes. Ten en cuenta que esto está muy desaconsejado porque provocará un panic si otros miembros del clúster anterior siguen activos. Asegúrate de guardar instantáneas periódicamente.


### Ejemplo de extremo a extremo {#end-2-end-example}

Toma una instantánea de un clúster en ejecución usando:

```sh
$ etcdctl snapshot save snapshot.db
```

Continuando con el ejemplo anterior, lo siguiente crea nuevos directorios de datos de etcd (`m1.etcd`, `m2.etcd`, `m3.etcd`) para un clúster de tres miembros:

```sh
$ etcdutl snapshot restore snapshot.db \
  --name m1 \
  --data-dir m1_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host1:2380
$ etcdutl snapshot restore snapshot.db \
  --name m2 \
  --data-dir m2_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host2:2380
$ etcdutl snapshot restore snapshot.db \
  --name m3 \
  --data-dir m3_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host3:2380
```

A continuación, inicia `etcd` con los nuevos directorios de datos:

```sh
$ etcd \
  --name m1 \
  --data-dir m1_data_dir.etcd \
  --listen-client-urls http://host1:2379 \
  --advertise-client-urls http://host1:2379 \
  --listen-peer-urls http://host1:2380 &
$ etcd \
  --name m2 \
  --data-dir m2_data_dir.etcd \
  --listen-client-urls http://host2:2379 \
  --advertise-client-urls http://host2:2379 \
  --listen-peer-urls http://host2:2380 &
$ etcd \
  --name m3 \
  --data-dir m3_data_dir.etcd \
  --listen-client-urls http://host3:2379 \
  --advertise-client-urls http://host3:2379 \
  --listen-peer-urls http://host3:2380 &
```

Ahora el clúster de etcd restaurado debería estar disponible y sirviendo el espacio de claves de la instantánea.

A partir de etcd v3.6, los usuarios solo pueden usar `etcdctl` para llevar los datos a una instantánea, pero deben usar `etcdutl` para restaurar datos a partir de una instantánea. Si no se especifica `--data-dir`, el valor predeterminado de `--data-dir` es `<name>.etcd` (donde `<name>` es el valor de `--name`). Por ejemplo, si no se proporcionó `--data-dir` y los miembros se llamaban `m1`, `m2` y `m3`, los directorios `--data-dir` serían `m1.etcd`, `m2.etcd` y `m3.etcd`.
