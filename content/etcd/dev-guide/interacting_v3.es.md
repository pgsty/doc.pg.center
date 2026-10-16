---
title: Interacción con etcd
weight: 3250
description: "etcdctl: una herramienta de línea de comandos para interactuar con el servidor etcd"
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/interacting_v3.md"
---

Los usuarios interactúan con etcd sobre todo escribiendo o leyendo el valor de una clave. Esta sección describe cómo hacerlo usando etcdctl, una herramienta de línea de comandos para interactuar con el servidor etcd. Los conceptos descritos aquí deberían aplicarse también a las API de gRPC o a las API de las bibliotecas cliente.

etcdctl v3.7 usa la API v3. La API v2 y la selección de versión mediante `ETCDCTL_API` se han eliminado.

> [!NOTE]
> Los ejemplos siguientes conservan salidas históricas de comandos, por lo que los números de versión mostrados pueden diferir de los de tu instalación. Las versiones antiguas de etcd mantenían las claves v2 y v3 en almacenes separados; migra cualquier dato heredado de v2 antes de actualizar a v3.7.


## Buscar las versiones {#find-versions}

La versión de etcdctl y la versión de la API del servidor pueden ser útiles para encontrar los comandos apropiados que se usarán para realizar diversas operaciones en etcd.

Este es el comando para encontrar las versiones:

```bash
$ etcdctl version
etcdctl version: 3.1.0-alpha.0+git
API version: 3.1
```

## Escribir una clave {#write-a-key}

Las aplicaciones almacenan claves en el clúster de etcd escribiendo en claves. Cada clave almacenada se replica en todos los miembros del clúster de etcd mediante el protocolo Raft para lograr consistencia y fiabilidad.

Este es el comando para establecer el valor de la clave `foo` en `bar`:

```bash
$ etcdctl put foo bar
OK
```

También se puede establecer una clave para un intervalo de tiempo determinado asociándole una concesión.

Este es el comando para establecer el valor de la clave `foo1` en `bar1` durante 10s.

```bash
$ etcdctl put foo1 bar1 --lease=1234abcd
OK
```

> [!NOTE]
> El ID de concesión `1234abcd` del comando anterior se refiere al ID devuelto al crear la concesión de 10s. Este ID puede entonces asociarse a la clave.

## Leer claves {#read-keys}

Las aplicaciones pueden leer valores de claves de un clúster de etcd. Las consultas pueden leer una sola clave o un rango de claves.

Supón que el clúster de etcd ha almacenado las claves siguientes:

```bash
foo = bar
foo1 = bar1
foo2 = bar2
foo3 = bar3
```

Este es el comando para leer el valor de la clave `foo`:

```bash
$ etcdctl get foo
foo
bar
```

Este es el comando para leer el valor de la clave `foo` en formato hexadecimal:

```bash
$ etcdctl get foo --hex
\x66\x6f\x6f          # Key
\x62\x61\x72          # Value
```

Este es el comando para leer únicamente el valor de la clave `foo`:

```bash
$ etcdctl get foo --print-value-only
bar
```

Este es el comando para recorrer las claves desde `foo` hasta `foo3`:

```bash
$ etcdctl get foo foo3
foo
bar
foo1
bar1
foo2
bar2
```

> [!NOTE]
> `foo3` queda excluida porque el rango es el intervalo semiabierto `[foo, foo3)`, que excluye `foo3`.

Este es el comando para recorrer todas las claves con el prefijo `foo`:

```bash
$ etcdctl get --prefix foo
foo
bar
foo1
bar1
foo2
bar2
foo3
bar3
```

Este es el comando para recorrer todas las claves con el prefijo `foo`, limitando el número de resultados a 2:

```bash
$ etcdctl get --prefix --limit=2 foo
foo
bar
foo1
bar1
```

Este es el comando para recorrer todas las claves con el prefijo `foo` usando la RPC [`RangeStream`](/es/etcd/learning/api/#rangestream). El resultado es idéntico al de una RPC unaria `Range`:

```bash
$ etcdctl get --stream --prefix foo
foo
bar
foo1
bar1
foo2
bar2
foo3
bar3
```

`--stream` no admite `--order`, `--sort-by` ni filtros de revisión.

## Leer versiones anteriores de las claves {#read-past-version-of-keys}

Las aplicaciones pueden querer leer versiones sustituidas de una clave. Por ejemplo, una aplicación puede querer revertir a una configuración antigua accediendo a una versión anterior de una clave. Alternativamente, una aplicación puede querer una vista consistente de varias claves a través de múltiples solicitudes accediendo al historial de claves.
Como cada modificación del almacén clave-valor del clúster de etcd incrementa la revisión global del clúster de etcd, una aplicación puede leer claves sustituidas proporcionando una revisión anterior de etcd.

Supón que un clúster de etcd ya tiene las claves siguientes:

```bash
foo = bar         # revision = 2
foo1 = bar1       # revision = 3
foo = bar_new     # revision = 4
foo1 = bar1_new   # revision = 5
```

Aquí hay un ejemplo para acceder a las versiones anteriores de las claves:

```bash
$ etcdctl get --prefix foo # access the most recent versions of keys
foo
bar_new
foo1
bar1_new

$ etcdctl get --prefix --rev=4 foo # access the versions of keys at revision 4
foo
bar_new
foo1
bar1

$ etcdctl get --prefix --rev=3 foo # access the versions of keys at revision 3
foo
bar
foo1
bar1

$ etcdctl get --prefix --rev=2 foo # access the versions of keys at revision 2
foo
bar

$ etcdctl get --prefix --rev=1 foo # access the versions of keys at revision 1
```

## Leer las claves cuyo valor en bytes es mayor o igual que el de la clave especificada {#read-keys-which-are-greater-than-or-equal-to-the-byte-value-of-the-specified-key}

Las aplicaciones pueden querer leer claves cuyo valor en bytes sea mayor o igual que el de la clave especificada.

Supón que un clúster de etcd ya tiene las claves siguientes:

```bash
a = 123
b = 456
z = 789
```

Este es el comando para leer las claves cuyo valor en bytes es mayor o igual que el de la clave `b` :

```bash
$ etcdctl get --from-key b
b
456
z
789
```

## Eliminar claves {#delete-keys}

Las aplicaciones pueden eliminar una clave o un rango de claves de un clúster de etcd.

Supón que un clúster de etcd ya tiene las claves siguientes:

```bash
foo = bar
foo1 = bar1
foo3 = bar3
zoo = val
zoo1 = val1
zoo2 = val2
a = 123
b = 456
z = 789
```

Este es el comando para eliminar la clave `foo`:

```bash
$ etcdctl del foo
1 # one key is deleted
```

Este es el comando para eliminar las claves en el rango de `foo` a `foo9`:

```bash
$ etcdctl del foo foo9
2 # two keys are deleted
```

Este es el comando para eliminar la clave `zoo` devolviendo el par clave-valor eliminado:

```bash
$ etcdctl del --prev-kv zoo
1   # one key is deleted
zoo # deleted key
val # the value of the deleted key
```

Este es el comando para eliminar las claves con prefijo `zoo`:

```bash
$ etcdctl del --prefix zoo
2 # two keys are deleted
```

Este es el comando para eliminar las claves cuyo valor en bytes es mayor o igual que el de la clave `b` :

```bash
$ etcdctl del --from-key b
2 # two keys are deleted
```

## Observar cambios en las claves {#watch-key-changes}

Las aplicaciones pueden observar una clave o un rango de claves para monitorizar cualquier actualización.

Este es el comando para observar la clave `foo`:

```bash
$ etcdctl watch foo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
```

Este es el comando para observar la clave `foo` en formato hexadecimal:

```bash
$ etcdctl watch foo --hex
# in another terminal: etcdctl put foo bar
PUT
\x66\x6f\x6f          # Key
\x62\x61\x72          # Value
```

Este es el comando para observar un rango de claves desde `foo` hasta `foo9`:

```bash
$ etcdctl watch foo foo9
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put foo1 bar1
PUT
foo1
bar1
```

Este es el comando para observar las claves con prefijo `foo`:

```bash
$ etcdctl watch --prefix foo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put fooz1 barz1
PUT
fooz1
barz1
```

Este es el comando para observar varias claves `foo` y `zoo`:

```bash
$ etcdctl watch -i
$ watch foo
$ watch zoo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put zoo val
PUT
zoo
val
```

## Observar cambios históricos de las claves {#watch-historical-changes-of-keys}

Las aplicaciones pueden querer observar cambios históricos de claves en etcd. Por ejemplo, una aplicación puede desear recibir todas las modificaciones de una clave; si la aplicación permanece conectada a etcd, `watch` es suficiente. Sin embargo, si falla la aplicación o etcd, puede producirse un cambio durante el fallo y la aplicación no recibirá la actualización en tiempo real. Para garantizar que la actualización se entregue, la aplicación debe poder observar cambios históricos de claves. Para ello, una aplicación puede especificar una revisión histórica en una observación, igual que al leer versiones anteriores de claves.

Supón que hemos terminado la siguiente secuencia de operaciones:

```bash
$ etcdctl put foo bar         # revision = 2
OK
$ etcdctl put foo1 bar1       # revision = 3
OK
$ etcdctl put foo bar_new     # revision = 4
OK
$ etcdctl put foo1 bar1_new   # revision = 5
OK
```

Este es un ejemplo para observar los cambios históricos:

```bash
# watch for changes on key `foo` since revision 2
$ etcdctl watch --rev=2 foo
PUT
foo
bar
PUT
foo
bar_new
```

```bash
# watch for changes on key `foo` since revision 3
$ etcdctl watch --rev=3 foo
PUT
foo
bar_new
```

Este es un ejemplo para observar solo desde el último cambio histórico:

```bash
# watch for changes on key `foo` and return last revision value along with modified value
$ etcdctl watch --prev-kv foo
# in another terminal: etcdctl put foo bar_latest
PUT
foo         # key
bar_new     # last value of foo key before modification
foo         # key
bar_latest  # value of foo key after modification
```

## Progreso de la observación {#watch-progress}

Las aplicaciones pueden querer comprobar el progreso de una observación para determinar qué tan actualizada está la secuencia de observación. Por ejemplo, si se usa una observación para actualizar una caché, puede ser útil saber si la caché está desactualizada en comparación con la revisión obtenida de una lectura por cuórum.

Se pueden emitir solicitudes de progreso con el comando «progress» en una sesión de observación interactiva para pedir al servidor etcd que envíe una actualización de notificación de progreso en la secuencia de observación:

```bash
$ etcdctl watch -i
$ watch a
$ progress
progress notify: 1
# in another terminal: etcdctl put x 0
# in another terminal: etcdctl put y 1
$ progress
progress notify: 3
```

> [!NOTE]
> El número de revisión de la respuesta de notificación de progreso es la revisión del nodo local del servidor etcd al que está conectada la secuencia de observación. Si este nodo está particionado y no forma parte del cuórum, esta revisión de notificación de progreso podría ser menor que la revisión devuelta por una lectura por cuórum contra un nodo del servidor etcd no particionado.

## Revisiones compactadas {#compacted-revisions}

Como mencionamos, etcd conserva revisiones para que las aplicaciones puedan leer versiones anteriores de las claves. Sin embargo, para evitar acumular una cantidad ilimitada de historial, es importante compactar las revisiones pasadas. Tras la compactación, etcd elimina las revisiones históricas, liberando recursos para uso futuro. Todos los datos sustituidos con revisiones anteriores a la revisión compactada dejarán de estar disponibles.

Este es el comando para compactar las revisiones:

```bash
$ etcdctl compact 5
compacted revision 5

# any revisions before the compacted one are not accessible
$ etcdctl get --rev=4 foo
Error:  rpc error: code = 11 desc = etcdserver: mvcc: required revision has been compacted
```

> [!NOTE]
> La revisión actual del servidor etcd puede encontrarse usando el comando get sobre cualquier clave (existente o no existente) en formato JSON. A continuación se muestra un ejemplo para mykey, que no existe en el servidor etcd:

```bash
$ etcdctl get mykey -w=json
{"header":{"cluster_id":14841639068965178418,"member_id":10276657743932975437,"revision":15,"raft_term":4}}
```

## Otorgar concesiones {#grant-leases}

Las aplicaciones pueden otorgar concesiones para claves desde un clúster de etcd. Cuando una clave se asocia a una concesión, su tiempo de vida queda ligado al de la concesión, que a su vez se rige por un tiempo de vida (TTL). Cada concesión tiene un valor mínimo de tiempo de vida (TTL) especificado por la aplicación en el momento del otorgamiento. El valor TTL real de la concesión es al menos el TTL mínimo y lo elige el clúster de etcd. Una vez que transcurre el TTL de una concesión, la concesión expira y todas las claves asociadas se eliminan.

Este es el comando para otorgar una concesión:

```bash
# grant a lease with 60 second TTL
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)

# attach key foo to lease 32695410dcc0ca06
$ etcdctl put --lease=32695410dcc0ca06 foo bar
OK
```

## Revocar concesiones {#revoke-leases}

Las aplicaciones revocan concesiones por ID de concesión. Revocar una concesión elimina todas las claves asociadas.

Supón que hemos terminado la siguiente secuencia de operaciones:

```bash
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)
$ etcdctl put --lease=32695410dcc0ca06 foo bar
OK
```

Este es el comando para revocar la misma concesión:

```bash
$ etcdctl lease revoke 32695410dcc0ca06
lease 32695410dcc0ca06 revoked

$ etcdctl get foo
# empty response since foo is deleted due to lease revocation
```

## Mantener vivas las concesiones {#keep-leases-alive}

Las aplicaciones pueden mantener viva una concesión renovando su TTL para que no expire.

Supón que hemos terminado la siguiente secuencia de operaciones:

```bash
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)
```

Este es el comando para mantener viva la misma concesión:

```bash
$ etcdctl lease keep-alive 32695410dcc0ca06
lease 32695410dcc0ca06 keepalived with TTL(60)
lease 32695410dcc0ca06 keepalived with TTL(60)
lease 32695410dcc0ca06 keepalived with TTL(60)
...
```

## Obtener información de la concesión {#get-lease-information}

Las aplicaciones pueden querer conocer información sobre las concesiones, para poder renovarlas o comprobar si la concesión sigue existiendo o ha expirado. Las aplicaciones también pueden querer conocer las claves a las que está asociada una concesión concreta.

Supón que hemos terminado la siguiente secuencia de operaciones:

```bash
# grant a lease with 500 second TTL
$ etcdctl lease grant 500
lease 694d5765fc71500b granted with TTL(500s)

# attach key zoo1 to lease 694d5765fc71500b
$ etcdctl put zoo1 val1 --lease=694d5765fc71500b
OK

# attach key zoo2 to lease 694d5765fc71500b
$ etcdctl put zoo2 val2 --lease=694d5765fc71500b
OK
```

Este es el comando para obtener información sobre la concesión:

```bash
$ etcdctl lease timetolive 694d5765fc71500b
lease 694d5765fc71500b granted with TTL(500s), remaining(258s)
```

Este es el comando para obtener información sobre la concesión junto con las claves asociadas a la concesión:

```bash
$ etcdctl lease timetolive --keys 694d5765fc71500b
lease 694d5765fc71500b granted with TTL(500s), remaining(132s), attached keys([zoo2 zoo1])

# if the lease has expired or does not exist it will give the below response:
Error:  etcdserver: requested lease not found
```
