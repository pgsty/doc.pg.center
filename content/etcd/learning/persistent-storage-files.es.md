---
title: "Archivos de almacenamiento persistente de etcd"
weight: 2650
description: Referencia del formato y los archivos de almacenamiento persistente
categories: [Concepto]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/persistent-storage-files.md"
---

Este documento explica el formato de almacenamiento persistente de etcd: nomenclatura, contenido y herramientas que permiten a los desarrolladores inspeccionarlo. En el futuro, este documento debería ampliarse con los cambios del modelo de almacenamiento. Este documento va dirigido a los desarrolladores de etcd para ayudarles con sus necesidades de recuperación de datos.


## Prerrequisitos {#prerequisites}

Los artículos siguientes proporcionan información de fondo útil para este documento:

* [Descripción general del modelo de datos de etcd](/es/etcd/learning/data_model/)
* [Descripción general de Raft](https://raft.github.io/raft.pdf) (especialmente la sección «5.3 Replicación de registros»).


## Descripción general {#overview}

### Archivos de larga duración {#long-leaving-files}

<table>
  <tr>
    <th>Nombre del archivo</th>
    <th>Propósito general</th>
  </tr>

  <tr>
    <td><pre>./member/snap/db</pre></td>
    <td><strong>Un <a href="https://en.wikipedia.org/wiki/B%2B_tree">b+tree</a> de bbolt</strong> que almacena todos los datos aplicados, la información de autorización de la composición y los metadatos. Sabe cuál es el último índice del registro WAL aplicado (<a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92">"consistent_index"</a>).
    </td>
  </tr>

  <tr>
    <td><pre>./member/snap/0000000000000002-0000000000049425.snap
./member/snap/0000000000000002-0000000000061ace.snap</pre>
    </td>
    <td>
      <p>
        <strong>Instantáneas periódicas del almacén v2 heredado</strong>, que contienen:
        <ul>
          <li>información básica de la composición</li>
          <li>etcd-version</li>
        </ul>
      </p>
      <p>Desde etcd v3, el contenido es redundante respecto del contenido de los archivos /snap/db.</p>
      <p>Periódicamente (<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L87">30s</a>) estos archivos <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/server.go#L597">se purgan</a>, y se conservan los últimos <code>--max-snapshots=5</code>.</p>
   </td>
  </tr>

  <tr>
    <td><pre>/member/snap/000000000007a178.snap.db</pre></td>
    <td>
      <p>Una <strong>instantánea bbolt completa descargada</strong> del líder de etcd si la réplica estaba demasiado retrasada.</p>
      <p>Tiene el mismo tipo de contenido que el archivo (<code>./member/snap/db</code>).</p>
      <p>
        El archivo se usa en 2 escenarios:
        <ul>
          <li>En respuesta a la solicitud del líder de recuperarse desde la instantánea.</li>
          <li><a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L444">Durante el arranque del servidor</a>, cuando se encuentra la última instantánea (archivo .snap.db) y se detecta que tiene un índice más nuevo que el consistent_index del archivo <code>snap.db</code> actual.</li>
        </ul>
        Nota: Las instantáneas periódicas generadas en cada réplica solo se emiten en forma de archivo *.snap (no de archivo snap.db). Por lo tanto, no hay garantía de que la instantánea más reciente (en el registro WAL) tenga el archivo *.snap.db. Pero en tal caso, se espera que el backend (snap/db) sea más nuevo que la instantánea.
      </p>
      <p>
        El archivo <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L1236">no se elimina cuando termina la recuperación</a> (todo el contenido se traspasa al archivo ./member/snap/db). Periódicamente (<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L87">30s</a>) los archivos <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L774">se</a> purgan.
Aquí también se conservan <code>--max-snapshots=5</code>. Como estos archivos pueden ser de O(GBs), esto podría crear un riesgo de agotamiento del espacio en disco.
    </td>
  </tr>

  <tr>
    <td><pre>./member/wal/000000000000000f-00000000000b38c7.wal
./member/wal/000000000000000e-00000000000a7fe3.wal
./member/wal/000000000000000d-000000000009c70c.wal</pre>
    </td>
    <td>
      <p><strong>Registros de escritura anticipada (WAL) de Raft</strong>, que contienen transacciones recientes aceptadas por Raft, instantáneas periódicas o registros CRC.</p>
      <p>Se conservan los <code>--max-wals=5</code> archivos recientes. Cada uno de estos archivos ocupa <code>~64*10^6</code> bytes. El archivo se corta cuando supera este tamaño codificado de forma fija, por lo que los archivos podrían superar ligeramente ese tamaño (así que el <code>0.tmp</code> preasignado no ofrece protección completa contra el agotamiento del disco).</p>
      <p>Si las instantáneas son demasiado infrecuentes, puede haber más de <code>--max-wals=5</code>, ya que los bloqueos a nivel del sistema de archivos protegen los archivos evitando que se eliminen demasiado pronto.</p>
    </td>
  </tr>

  <tr>
    <td><pre>./member/wal/0.tmp (or .../1.tmp)</pre></td>
    <td>
      <strong>Espacio preasignado</strong> para el siguiente archivo de registro de escritura anticipada.
      Se usa para evitar que Raft se quede bloqueado por falta de capacidad de registros WAL sin la posibilidad de generar una alarma.
    </td>
  </tr>
</table>


### Archivos temporales {#temporary-files}

Durante el procesamiento interno de etcd, es posible que se encuentren varios archivos de vida corta:

<table>
  <tr>
    <th>Archivo</th>
    <th>Propósito general</th>
  </tr>
  <tr>
    <td><pre>./member/snap/0000000000000002-000000000007a178.snap.broken</pre></td>
    <td>
      <p>Los archivos de instantánea se renombran como «broken» cuando no se pueden <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/api/snap/snapshotter.go#L144">cargar</a>.<p>
      <!-- TODO: etcdserver/api/snap/snapshotter.go:148 -->
      <p>El intento de cargar el archivo más reciente ocurre cuando etcd está <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/server.go#L302">arrancando</a>.</p>
      <!-- TODO: etcdserver/server.go:428 -->
      <p>O durante los comandos backup/migrate de etcdctl.</p>
   </td>
  </tr>
  <tr>
    <td><pre>./member/snap/tmp071677638 (random suffix)</pre></td>
    <td>
      <p><a href="https://github.com/etcd-io/etcd/blob/ae9734ed278b7a1a7dfc82e800471ebbf9fce56f/etcdserver/api/snap/db.go#L39">Archivo temporal</a> (bbolt) creado en las réplicas en respuesta a la solicitud msgSnap del líder, es decir, a la exigencia del líder de recuperar el almacenamiento desde la instantánea dada.</p>
      <p>
        Tras la recuperación exitosa (completa) del contenido, el archivo se <a href="https://github.com/etcd-io/etcd/blob/ae9734ed278b7a1a7dfc82e800471ebbf9fce56f/etcdserver/api/snap/db.go#L55">renombra</a> a: <code>/member/snap/[SNAPSHOT-INDEX].snap.db</code>. En caso de que un servidor muera o se lo detenga en mitad de la descarga de los archivos, los archivos permanecen en el disco y nunca se limpian automáticamente. Pueden ser de un tamaño considerable (GBs).
      </p>
      <p>Ver <a href="https://github.com/etcd-io/etcd/issues/12837">etcd/issues/12837</a>. <strong>Corregido en etcd 3.5.</strong></p>
    </td>
  </tr>
  <tr>
    <td><pre>/member/snap/db.tmp.071677638 (random suffix)</pre></td>
    <td>
      <p>Un archivo temporal que contiene una copia del contenido del backend (/member/snap/db), durante el <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/mvcc/backend/backend.go#L373">proceso de desfragmentación</a>. Tras completarse el proceso con éxito, el archivo se renombra a /member/snap/db, reemplazando el backend original.</p>
      <p>Al arrancar el servidor de etcd, estos archivos se <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/api/snap/snapshotter.go#L217">purgan</a>.</p>
    </td>
  </tr>
</table>

## b+tree de bbolt: **member/snap/db** {#bbolt-btree-membersnapdb}

Este archivo contiene el contenido principal de etcd, aplicado hasta un punto específico del registro de Raft (ver [consistent_index](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92)).


### Organización física {#physical-organization}

El almacenamiento de better bolt está organizado físicamente como un [b+tree](https://en.wikipedia.org/wiki/B%2B_tree). Las páginas físicas del b-tree nunca se modifican in situ[^1]. En su lugar, el contenido se copia a una página nueva (recuperada de la lista de páginas libres) y la página antigua se añade a la lista de páginas libres tan pronto como no hay ninguna transacción abierta que pueda acceder a ella. Gracias a este proceso, una transacción RO abierta ve un estado histórico consistente del almacenamiento. La transacción RW es exclusiva y bloquea todas las demás transacciones RW.  \
Los valores grandes se almacenan en múltiples páginas contiguas. El proceso de recuperación de páginas, combinado con la necesidad de asignar áreas contiguas de páginas de distintos tamaños, puede llevar a una fragmentación creciente del almacenamiento bbolt.

El archivo bbolt nunca se reduce por sí solo. Solo en el proceso de desfragmentación, el archivo puede reescribirse a uno nuevo que tiene algún margen de páginas libres al final y un tamaño truncado.


### Organización lógica {#logical-organization}

El almacenamiento bbolt se divide en buckets. En cada bucket se almacenan claves (pares byte[]->value byte[]), en orden lexicográfico.  La lista siguiente representa los buckets usados por etcd (a partir de la versión 3.5) y las claves en uso.

<table>
  <tr>
    <th>Bucket</th>
    <th>Clave</th>
    <th>Valor de ejemplo</th>
    <th>Descripción</th>
  </tr>
  <tr>
    <td>alarm</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/etcdserverpb/rpc.proto#L976">rpcpb.Alarm</a>:
    {MemberID, Alarm: NONE|NOSPACE|CORRUPT}</code>
    </td>
    <td><code>nil</code></td>
    <td>Indica que se han diagnosticado problemas en uno de los miembros.</td>
  </tr>
  <tr>
    <td>auth</td>
    <td>"authRevision"</td>
    <td><code>""</code> (vacío) o <code>BigEndian.PutUint64</code></td>
    <td>
      <p>Cualquier cambio de Roles o Usuarios incrementa este campo al confirmar la transacción.</p>
      <p>
        El valor se usa únicamente para el <a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/v3_server.go#L461">bloqueo optimista durante</a> el proceso de autorización.
      </p>
    </td>
  </tr>
  <tr>
    <td>authRoles</td>
    <td>[roleName] como cadena</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/authpb/auth.proto#L38">authpb.Role</a></code> serializado (marshalled)</td>
    <td></td>
  </tr>
  <tr>
    <td>authUsers</td>
    <td>[userName] como cadena</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/authpb/auth.proto#L17">authpb.User</a></code> serializado (marshalled)</td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="2" >cluster</td>
    <td>"clusterVersion"</td>
    <td><code>"3.5.0"</code> (cadena)</td>
    <td>Versión <a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/etcdserver/server.go#L2314">minor</a> de la versión común de almacenamiento acordada por consenso.</td>
  </tr>
  <tr>
    <td>"downgrade"</td>
    <td>JSON: <pre>{
  "target-version": "3.4.0"
  "enabled": true/false
}</pre>
    </td>
    <td>
      <p>Persiste la intención configurada por la solicitud <code>Downgrade RPC</code> más reciente.</p>
      <p>Desde v3.5</p>
    </td>
  </tr>
  <tr>
    <td><strong>key</strong></td>
    <td>
      <p>[revisionId] codificado usando <a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub}</p>
      <p>Las eliminaciones de pares clave-valor se serializan (marshal) con 't' al final (como «Tombstone»)</p>
    </td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/mvccpb/kv.proto#L12"><code>mvccpb.KeyValue</code></a> proto serializado (marshalled) (<code>key, create_rev, mod_rev, version, value, lease id</code>)</td>
    <td></td>
  </tr>
  <tr>
    <td>lease</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/lease/leasepb/lease.proto#L13"><code>leasepb.Lease</code></a> proto serializado (marshalled) (ID, TTL, RemainingTTL)</td>
    <td>
      <p>Nota: LeaseCheckpoint solo extiende RemainingTTL. Solo el TTL procede del Grant original.</p>
      <p style="text-decoration:underline;">Nota 2: Persistimos los TTL en segundos (desde el «ahora» indefinido). ¡¡¡Un servidor en bucle de fallos no libera las concesiones!!!</p>
    </td>
  </tr>
  <tr>
    <td>members</td>
    <td>[memberId] en hexadecimal como cadena: <code>"8e9e05c52164694d"</code></td>
    <td>
      <em>Estructura <a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/api/membership/member.go#L43">Member</a> serializada como cadena JSON:</em>
      <pre>{
  "id":10276657743932975437,
  "peerURLs":[
  "<a href="http://localhost:2380">http://localhost:2380</a>"],
  "name":"default",
  "clientURLs": ["http://localhost:2379"]
}</pre>
    </td>
    <td>Información de la composición del clúster acordada.</td>
  </tr>
  <tr>
    <td>members_removed</td>
    <td>[memberId] en hexadecimal como cadena: <code>"8e9e05c52164694d"</code></td>
    <td><code>[]byte("removed")</code></td>
    <td>
      <p>IDs de todos los miembros eliminados. Se usa para validar que un miembro eliminado nunca vuelva a añadirse con el mismo id.</p>
      <p><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/api/membership/cluster.go#L251">Actualmente (3.4) el campo se lee del almacén V2 y nunca del V3</a>. Ver <a href="https://github.com/etcd-io/etcd/pull/12820">https://github.com/etcd-io/etcd/pull/12820</a></p>
    </td>
  </tr>
  <tr>
    <td rowspan="3"><strong>meta</strong></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92">"consistent_index"</a></td>
    <td>bytes de uint64 (BigEndian)</td>
    <td>Representa el desplazamiento de la última entrada WAL aplicada al almacenamiento de la base de datos bolt.</td>
  </tr>
  <tr>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore.go#L41">"scheduledCompactRev"</a></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub} codificado. (16 bytes)</td>
    <td>Se usa para reinicializar la compactación si se produjo un fallo después de una solicitud de compactación.</td>
  </tr>
  <tr>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore.go#L42">"finishedCompactRev"</a></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub} codificado. (16 bytes)</td>
    <td>Revisión en la que el almacén fue compactado recientemente con éxito (<a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54">https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54</a>)</td>
  </tr>
  <tr>
    <td></td>
    <td>"confState"</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/pull/12962">Desde etcd 3.5</a></td>
  </tr>
  <tr>
    <td></td>
    <td>"term"</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/pull/12964">Desde etcd 3.5</a></td>
  </tr>
  <tr>
    <td></td>
    <td>"storage-version"</td>
    <td></td>
    <td></td>
  </tr>
</table>


### Herramientas {#tools}


#### bbolt {#bbolt}

bbolt tiene una herramienta de línea de comandos que permite inspeccionar el contenido del archivo.

Ejemplos de uso:

##### Listar todos los buckets de un archivo bbolt dado: {#list-all-buckets-in-given-bbolt-file}

```
% go run go.etcd.io/bbolt/cmd/bbolt buckets ./default.etcd/member/snap/db
```


##### Leer un par clave/valor concreto: {#read-a-particular-keyvalue-pair}

```
% go run go.etcd.io/bbolt/cmd/bbolt get ./default.etcd/member/snap/db cluster clusterVersion
```


#### etcd-dump-db {#etcd-dump-db}

etcd-dump-db puede usarse para listar el contenido del backend v3 de etcd (bbolt).

```
% go run go.etcd.io/etcd/v3/tools/etcd-dump-db  list-bucket default.etcd
alarm
auth
...
```

Consulta más ejemplos en: [https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-db](https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-db)


## WAL: registro de escritura anticipada {#wal-write-ahead-log}

El registro de escritura anticipada es un almacenamiento persistente de Raft que se usa para guardar propuestas. Primero el líder almacena la propuesta en su registro y luego (de forma concurrente) la replica mediante el protocolo Raft a las réplicas. Cada réplica persiste la propuesta en su WAL antes de confirmarle al líder la replicación.

El registro WAL usado en etcd difiere del modelo canónico de Raft en 2 aspectos:

* No solo persiste entradas indexadas, sino también instantáneas de Raft (ligeras) y el hard-state. Así, todo el estado Raft del miembro puede recuperarse únicamente desde el registro WAL.
* Es de solo añadir (append-only). Las entradas no se sobrescriben in situ, sino que una entrada añadida más adelante en el archivo (con el mismo índice) sustituye a la anterior.


### Nombres de archivo {#file-names}

Los archivos de registro WAL se nombran usando el patrón siguiente:

```
"%016x-%016x.wal", seq, index
```

Ejemplo: `./member/wal/0000000000000010-00000000000bf1e6.wal`

Así, los nombres de archivo contienen codificado en hexadecimal:


* El número secuencial del archivo de registro WAL
* El índice de la primera entrada o instantánea del archivo.
  En particular, el primer archivo «0000000000000000-0000000000000000.wal» tiene el registro de instantánea inicial con index=0.

### Contenido físico {#physical-content}

El archivo de registro WAL contiene una secuencia de «[Frames](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/encoder.go#L62)» (tramas). Cada trama contiene:


1. Un uint64 codificado en [LittleEndian](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/encoder.go#L120)[^2] que contiene la longitud del [walpb.Record](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/walpb/record.proto#L11) (3) serializado (marshalled).
2. Relleno (padding): cierto número de bytes 0, de modo que la trama completa tenga un tamaño alineado (mod 8)
3. Datos del [walpb.Record](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/walpb/record.proto#L11) serializados (marshalled):
    1. [type](https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/storage/wal/wal.go#L39) - enumeración codificada como int que dirige la interpretación del campo data siguiente
    2. data - según el tipo, normalmente un proto serializado (marshalled)
    3. crc - suma de comprobación CRC-32 de todos los campos «data» combinados (sin type) en todos los registros de registro de esta réplica en particular desde la creación del registro WAL. Ten en cuenta que el CRC tiene en cuenta TODOS los registros (incluso si Raft no los confirmó).

Los archivos se «cortan» (se inicia un archivo nuevo) cuando el archivo actual supera los <code>64*10^6</code> bytes.


### Contenido lógico {#logical-content}

Los archivos de registro de escritura anticipada, en la capa lógica, contienen:

* `Raftpb.Entry: `propuestas recientes replicadas por el líder de Raft. Algunas de estas propuestas se consideran «committed» (confirmadas) y las demás están sujetas a ser lógicamente sobrescritas.
* `Raftpb.HardState(term,commit,vote): `información periódica (muy frecuente) sobre el índice de una entrada de registro que está «committed» (replicada a la mayoría de los servidores), por lo que está garantizada como no cambiada/sobrescrita y puede aplicarse a los backends (v2, v3). También contiene un «term» (indicador de si hubo cambios relacionados con elecciones) y un voto: el miembro por el que votó la réplica actual en el término actual.
* `walpb.Snapshot(term, index): `instantáneas periódicas del estado de Raft (sin contenido de la base de datos, solo el índice de registro de la instantánea y el término de Raft)
    * El contenido del almacén V2 se guarda en archivos *.store separados.
    * El contenido del almacén V3 se mantiene en el archivo bbolt y se convierte en una instantánea implícita en cuanto las entradas se aplican allí.
* Un registro de suma de comprobación crc32 (al principio de cada archivo), usado para reanudar la comprobación CRC del resto del archivo.
* `etcdserverpb.Metadata(node_id, cluster_id)` - identifica el clúster y la réplica que representa el registro.

Cada archivo de registro WAL se construye con (en orden):

1. Trama CRC-32 (crc acumulado de todos los archivos anteriores, 0 para el primer archivo).
2. Trama de metadatos (IDs de clúster y de réplica)
3. Solo para el archivo WAL inicial:

    * Trama de instantánea vacía (Index:0, Term: 0).
      El propósito de esta trama es mantener el invariante de que todas las entradas están «precedidas» por una instantánea.

   Para archivos WAL no iniciales (2.º o posterior):

    * Trama de HardState.

4. Mezcla de registros de entrada, hard-state e instantáneas

El registro WAL puede contener múltiples entradas con el mismo índice. Tal situación puede ocurrir en los casos descritos en la figura 7 del [artículo de Raft](http://web.stanford.edu/~ouster/cgi-bin/papers/raft-atc14.pdf). El registro WAL de etcd es de solo añadir, así que las entradas se sobrescriben añadiendo una entrada nueva con el mismo índice.

En particular, durante la lectura del WAL, [la lógica sobrescribe las entradas antiguas con entradas más nuevas](https://github.com/etcd-io/etcd/blob/release-3.4/wal/wal.go#L448-L462). Así, solo la última versión de las entradas con entry.index &lt;= HardState.commit puede considerarse final. Las entradas con índice > HardState.commit están sujetas a cambios.

Se espera que los «terms» del registro WAL sean monótonos.

Se espera que los «indexes» del registro WAL:

1. comiencen desde alguna instantánea
2. crezcan secuencialmente tras esa instantánea mientras permanezcan en el mismo «term»
3. si el término cambia, el índice puede disminuir, pero a un valor nuevo mayor que el último HardState.commit.
4. puede producirse una instantánea nueva con cualquier índice >= HardState.commit, lo que abre una secuencia nueva de índices.


![Archivos de almacenamiento persistente de etcd](/etcd/learning/img/persistent-storage-files-figure-01.png)


### Herramientas {#tools-1}


#### etcd-dump-logs {#etcd-dump-logs}

Los registros WAL de etcd pueden leerse con la herramienta [etcd-dump-logs](https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-logs):

```
% go install go.etcd.io/etcd/v3/tools/etcd-dump-logs@latest

% go run go.etcd.io/etcd/v3/tools/etcd-dump-logs --start-index=0 aname.etcd
```

Ten en cuenta que:

* La herramienta muestra solo las Entries, y no todos los registros WAL (Snapshots, HardStates) que hay en los archivos de registro WAL.
* La herramienta aplica automáticamente las «overrides» (sobrescrituras) sobre las entradas. Si una entrada fue sobrescrita (por una entrada más reciente bajo el mismo índice), la herramienta imprimirá solo el valor final.
* La herramienta también imprime entradas no confirmadas (de la cola del LOG), sin información sobre HardState.commitIndex, así que no se sabe si las entradas son finales o no.


## Instantáneas de (Store V2): **member/snap/{term}-{index}.snap** {#snapshots-of-store-v2-membersnapterm-indexsnap}


### Nombres de archivo: {#file-names-1}

**member/snap/{term}-{index}.snap**

Los nombres de archivo se generan [aquí](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snapshotter.go#L78) `("%016x-%016x.snap") `y usan 2 componentes codificados en hexadecimal:


* term -> término de Raft (período entre elecciones) en el momento en que se emite la instantánea
* index -> de la última propuesta aplicada en el momento en que se emite la instantánea

### Creación {#creation}

Los archivos *.snap los crea el método [Snapshotter.SaveSnap](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snapshotter.go#L68).

Hay 2 disparadores que controlan la creación de estos archivos:


* Se crea un archivo nuevo cada (aproximadamente) --snapshot-count= (por defecto 10,000 en v3.7.0) propuestas aplicadas. Es una aproximación, ya que podemos recibir propuestas por lotes y solo consideramos tomar la instantánea al final del lote; finalmente, el proceso de instantáneas se programa de forma asíncrona.
  El nombre de la opción (--snapshot-count) es bastante engañoso, ya que rige las [diferencias de valor de índice entre ](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/server.go#L1266)el índice de la última instantánea y el índice de la última propuesta aplicada.
* Raft solicita a la réplica restaurarse desde la instantánea. Cuando una réplica recibe la instantánea por cable como mensaje (msgSnap), también la guarda como punto de control (ligero) en el registro WAL. Esto garantiza que en la cola de los registros WAL siempre haya una instantánea válida seguida de entradas. Así se suprime la potencial falta de continuidad en los registros WAL.

Actualmente los archivos están aproximadamente[^3] asociados 1-1 con las entradas Snapshot de los registros WAL. Con la retirada del almacén v2 esperamos que estos archivos dejen de escribirse por completo (opt-in: 3.5.x,  obligatorio: 3.6.x).


### Contenido {#content}

El archivo contiene el proto [snapdb.snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snappb/snap.proto#L11) `(uint32 crc, bytes data)` serializado (marshalled),

que en el campo «data» contiene un [Raftpb.Snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L31):

(bytes data, SnapshotMetadata{index, term, [conf](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L99)} metadata),

Finalmente, los datos anidados contienen un [contenido del almacén v2](#exemplar-json-serialized-store-v2-content-in-etcd-34-snap-files) serializado en JSON.


En particular, hay:

* Término
* Índice
* Datos de la composición:
    * <code>/0/members/8e9e05c52164694d/attributes -> <strong>{\"name\":\"default\",\"clientURLs\":[\"http://localhost:2379\"]}</strong></code>
    * <code>/0/members/8e9e05c52164694d/RaftAttributes -> <strong>"{\"peerURLs\":[\"http://localhost:2380\"]}"</strong></code>
* Versión de almacenamiento: /0/version-> 3.5.0


### Herramientas {#tools-2}


#### protoc {#protoc}

El comando siguiente permite ver el contenido del archivo cuando se ejecuta desde el directorio raíz de etcd:


```
cat default.etcd/member/snap/0000000000000002-0000000000049425.snap |
  protoc --decode=snappb.snapshot \
    server/etcdserver/api/snap/snappb/snap.proto \
    -I $(go list -f '{{.Dir}}' github.com/gogo/protobuf/proto)/.. \
    -I . \
    -I $(go list -m -f '{{.Dir}}' github.com/gogo/protobuf)/protobuf
```


De forma análoga, puedes extraer el campo «data» y decodificarlo como [Raftpb.Snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L31).


### Contenido de ejemplo del almacén v2 serializado en JSON en los archivos *.snap de etcd 3.4: {#exemplar-json-serialized-store-v2-content-in-etcd-34-snap-files}

```json
{
  "Root":{
    "Path":"/",
    "CreatedIndex":0,
    "ModifiedIndex":0,
    "ExpireTime":"0001-01-01T00:00:00Z",
    "Value":"",
    "Children":{
      "0":{
        "Path":"/0",
        "CreatedIndex":0,
        "ModifiedIndex":0,
        "ExpireTime":"0001-01-01T00:00:00Z",
        "Value":"",
        "Children":{
          "members":{
            "Path":"/0/members",
            "CreatedIndex":1,
            "ModifiedIndex":1,
            "ExpireTime":"0001-01-01T00:00:00Z",
            "Value":"",
            "Children":{
              "8e9e05c52164694d":{
                "Path":"/0/members/8e9e05c52164694d",
                "CreatedIndex":1,
                "ModifiedIndex":1,
                "ExpireTime":"0001-01-01T00:00:00Z",
                "Value":"",
                "Children":{
                  "attributes":{
                    "Path":"/0/members/8e9e05c52164694d/attributes",
                    "CreatedIndex":2,
                    "ModifiedIndex":2,
                    "ExpireTime":"0001-01-01T00:00:00Z",
                    "Value":"{\"name\":\"default\",\"clientURLs\":[\"http://localhost:2379\"]}",
                    "Children":null
                  },
                  "RaftAttributes":{
                    "Path":"/0/members/8e9e05c52164694d/RaftAttributes",
                    "CreatedIndex":1,
                    "ModifiedIndex":1,
                    "ExpireTime":"0001-01-01T00:00:00Z",
                    "Value":"{\"peerURLs\":[\"http://localhost:2380\"]}",
                    "Children":null
                  }
                }
              }
            }
          },
          "version":{
            "Path":"/0/version",
            "CreatedIndex":3,
            "ModifiedIndex":3,
            "ExpireTime":"0001-01-01T00:00:00Z",
            "Value":"3.5.0",
            "Children":null
          }
        }
      },
      "1":{
        "Path":"/1",
        "CreatedIndex":0,
        "ModifiedIndex":0,
        "ExpireTime":"0001-01-01T00:00:00Z",
        "Value":"",
        "Children":{


        }
      }
    }
  },
  "WatcherHub":{
    "EventHistory":{
      "Queue":{
        "Events":[
          {
            "action":"create",
            "node":{
              "key":"/0/members/8e9e05c52164694d/RaftAttributes",
              "value":"{\"peerURLs\":[\"http://localhost:2380\"]}",
              "modifiedIndex":1,
              "createdIndex":1
            }
          },
          {
            "action":"set",
            "node":{
              "key":"/0/members/8e9e05c52164694d/attributes",
              "value":"{\"name\":\"default\",\"clientURLs\":[\"http://localhost:2379\"]}",
              "modifiedIndex":2,
              "createdIndex":2
            }
          },
          {
            "action":"set",
            "node":{
              "key":"/0/version",
              "value":"3.5.0",
              "modifiedIndex":3,
              "createdIndex":3
            }
          }
        ]
      }
    }
  }
}
```

## Cambios {#changes}

Esta sección está reservada para describir los cambios en los formatos de archivo introducidos entre distintas versiones de etcd.

[^1]:
     Las páginas de metadatos al principio del archivo bbolt se modifican in situ.

[^2]:
     Inconsistente, ya que la mayoría de los uint se escriben en bigendian

[^3]:
     La instantánea inicial (index:0) al principio del registro WAL no está asociada a ningún archivo *.snap. Además, los archivos *.snap antiguos (o los registros WAL) pueden purgarse.
