---
title: "3. Sección global"
linkTitle: "3. Sección global"
weight: 140
description: "Seguridad del proceso, ajuste de rendimiento, depuración y parámetros del cliente HTTP"
icon: fa-solid fa-earth-americas
module: [HAPROXY]
categories: [Referencia]
aliases:
  - /haproxy/configuration/global/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 3"
---

Los parámetros de la sección "global" se aplican a todo el proceso y a menudo son específicos del
sistema operativo. Generalmente se configuran una sola vez y no necesitan modificarse una vez que
son correctos. Algunos de ellos tienen equivalentes en la línea de comandos.

Las siguientes palabras clave están soportadas en la sección "global":
- Gestión de procesos y seguridad

  - 51degrees-allow-unmatched
  - 51degrees-cache-size
  - 51degrees-data-file
  - 51degrees-difference
  - 51degrees-drift
  - 51degrees-property-name-list
  - 51degrees-property-separator
  - 51degrees-use-performance-graph
  - 51degrees-use-predictive-graph
  - ca-base
  - chroot
  - cluster-secret
  - cpu-affinity
  - cpu-map
  - cpu-policy
  - cpu-set
  - crt-base
  - daemon
  - default-path
  - description
  - deviceatlas-json-file
  - deviceatlas-log-level
  - deviceatlas-properties-cookie
  - deviceatlas-separator
  - dns-accept-family
  - expose-deprecated-directives
  - expose-experimental-directives
  - external-check
  - fd-hard-limit
  - gid
  - grace
  - group
  - h1-accept-payload-with-any-method
  - h1-case-adjust
  - h1-case-adjust-file
  - h1-do-not-close-on-insecure-transfer-encoding
  - h2-workaround-bogus-websocket-clients
  - hard-stop-after
  - harden.reject-privileged-ports.tcp
  - harden.reject-privileged-ports.quic
  - insecure-fork-wanted
  - insecure-setuid-wanted
  - issuers-chain-path
  - jwt.allow_none_alg
  - jwt.decrypt_alg_list
  - jwt.decrypt_enc_list
  - key-base
  - limited-quic
  - localpeer
  - log
  - log-send-hostname
  - log-tag
  - lua-load
  - lua-load-per-thread
  - lua-prepend-path
  - max-threads-per-group
  - mworker-max-reloads
  - nbthread
  - node
  - numa-cpu-mapping
  - ocsp-update.disable
  - ocsp-update.maxdelay
  - ocsp-update.mindelay
  - ocsp-update.httpproxy
  - ocsp-update.mode
  - pidfile
  - pp2-never-send-local
  - presetenv
  - prealloc-fd
  - resetenv
  - set-dumpable
  - set-var
  - setenv
  - ssl-default-bind-ciphers
  - ssl-default-bind-ciphersuites
  - ssl-default-bind-client-sigalgs
  - ssl-default-bind-curves
  - ssl-default-bind-options
  - ssl-default-bind-sigalgs
  - ssl-default-server-ciphers
  - ssl-default-server-ciphersuites
  - ssl-default-server-client-sigalgs
  - ssl-default-server-curves
  - ssl-default-server-options
  - ssl-default-server-sigalgs
  - ssl-dh-param-file
  - ssl-propquery
  - ssl-provider
  - ssl-provider-path
  - ssl-security-level
  - ssl-server-verify
  - ssl-skip-self-issued-ca
  - stats
  - stats-file
  - strict-limits
  - uid
  - ulimit-n
  - unix-bind
  - unsetenv
  - user
  - wurfl-cache-size
  - wurfl-data-file
  - wurfl-information-list
  - wurfl-information-list-separator

- Ajuste de rendimiento

  - busy-polling
  - max-spread-checks
  - maxcompcpuusage
  - maxcomprate
  - maxconn
  - maxconnrate
  - maxpipes
  - maxsessrate
  - maxsslconn
  - maxsslrate
  - maxzlibmem
  - no-memory-trimming
  - noepoll
  - noevports
  - nogetaddrinfo
  - nokqueue
  - noktls
  - nopoll
  - noreuseport
  - nosplice
  - profiling.memory
  - profiling.tasks
  - server-state-base
  - server-state-file
  - spread-checks
  - ssl-engine
  - ssl-mode-async
  - tune.applet.zero-copy-forwarding
  - tune.buffers.limit
  - tune.buffers.reserve
  - tune.bufsize
  - tune.bufsize.large
  - tune.bufsize.small
  - tune.cli.max-payload-size
  - tune.comp.maxlevel
  - tune.defaults.purge
  - tune.disable-fast-forward
  - tune.disable-zero-copy-forwarding
  - tune.epoll.mask-events
  - tune.events.max-events-at-once
  - tune.fail-alloc
  - tune.fd.edge-triggered
  - tune.h1.be.glitches-threshold
  - tune.h1.fe.glitches-threshold
  - tune.h1.zero-copy-fwd-recv
  - tune.h1.zero-copy-fwd-send
  - tune.h2.be.glitches-threshold
  - tune.h2.be.initial-window-size
  - tune.h2.be.max-concurrent-streams
  - tune.h2.be.max-frames-at-once
  - tune.h2.be.rxbuf
  - tune.h2.fe.glitches-threshold
  - tune.h2.fe.initial-window-size
  - tune.h2.fe.max-concurrent-streams
  - tune.h2.fe.max-frames-at-once
  - tune.h2.fe.max-rst-at-once
  - tune.h2.fe.max-total-streams
  - tune.h2.fe.rxbuf
  - tune.h2.header-table-size
  - tune.h2.initial-window-size
  - tune.h2.max-concurrent-streams
  - tune.h2.max-frame-size
  - tune.h2.zero-copy-fwd-send
  - tune.http.cookielen
  - tune.http.logurilen
  - tune.http.maxhdr
  - tune.idle-pool.shared
  - tune.idletimer
  - tune.lua.bool-sample-conversion
  - tune.lua.burst-timeout
  - tune.lua.forced-yield
  - tune.lua.log.loggers
  - tune.lua.log.stderr
  - tune.lua.maxmem
  - tune.lua.openlibs
  - tune.lua.service-timeout
  - tune.lua.session-timeout
  - tune.lua.task-timeout
  - tune.max-checks-per-thread
  - tune.maxaccept
  - tune.maxpollevents
  - tune.maxrewrite
  - tune.max-rules-at-once
  - tune.memory.hot-size
  - tune.pattern.cache-size
  - tune.peers.max-updates-at-once
  - tune.pipesize
  - tune.pool-high-fd-ratio
  - tune.pool-low-fd-ratio
  - tune.pt.zero-copy-forwarding
  - tune.quic.be.cc.cubic-min-losses
  - tune.quic.be.cc.hystart
  - tune.quic.be.cc.max-frame-loss
  - tune.quic.be.cc.max-win-size
  - tune.quic.be.cc.reorder-ratio
  - tune.quic.be.max-idle-timeout
  - tune.quic.be.sec.glitches-threshold
  - tune.quic.be.stream.data-ratio
  - tune.quic.be.stream.max-concurrent
  - tune.quic.be.stream.rxbuf
  - tune.quic.be.tx.pacing
  - tune.quic.be.tx.udp-gso
  - tune.quic.cc.cubic.min-losses (obsoleto)
  - tune.quic.cc-hystart (obsoleto)
  - tune.quic.disable-tx-pacing (obsoleto)
  - tune.quic.disable-udp-gso (obsoleto)
  - tune.quic.fe.cc.cubic-min-losses
  - tune.quic.fe.cc.hystart
  - tune.quic.fe.cc.max-frame-loss
  - tune.quic.fe.cc.max-win-size
  - tune.quic.fe.cc.reorder-ratio
  - tune.quic.fe.max-idle-timeout
  - tune.quic.fe.sec.glitches-threshold
  - tune.quic.fe.sec.retry-threshold
  - tune.quic.fe.sock-per-conn
  - tune.quic.fe.stream.data-ratio
  - tune.quic.fe.stream.max-concurrent
  - tune.quic.fe.stream.max-total
  - tune.quic.fe.stream.rxbuf
  - tune.quic.fe.tx.pacing
  - tune.quic.fe.tx.udp-gso
  - tune.quic.frontend.max-data-size (obsoleto)
  - tune.quic.frontend.max-idle-timeout (obsoleto)
  - tune.quic.frontend.max-streams-bidi (obsoleto)
  - tune.quic.frontend.max-tx-mem (obsoleto)
  - tune.quic.frontend.stream-data-ratio (obsoleto)
  - tune.quic.frontend.default-max-window-size (obsoleto)
  - tune.quic.listen
  - tune.quic.max-frame-loss (obsoleto)
  - tune.quic.mem.tx-max
  - tune.quic.reorder-ratio (obsoleto)
  - tune.quic.retry-threshold (obsoleto)
  - tune.quic.socket-owner (obsoleto)
  - tune.quic.zero-copy-fwd-send
  - tune.renice.runtime
  - tune.renice.startup
  - tune.rcvbuf.backend
  - tune.rcvbuf.client
  - tune.rcvbuf.frontend
  - tune.rcvbuf.server
  - tune.recv_enough
  - tune.ring.queues
  - tune.runqueue-depth
  - tune.sched.low-latency
  - tune.sndbuf.backend
  - tune.sndbuf.client
  - tune.sndbuf.frontend
  - tune.sndbuf.server
  - tune.streams-elasticity
  - tune.stick-counters
  - tune.ssl.cachesize
  - tune.ssl.capture-buffer-size
  - tune.ssl.capture-cipherlist-size (obsoleto)
  - tune.ssl.certificate-compression
  - tune.ssl.default-dh-param
  - tune.ssl.force-private-cache
  - tune.ssl.hard-maxrecord
  - tune.ssl.keylog
  - tune.ssl.keyupdate-rate-limit
  - tune.ssl.lifetime
  - tune.ssl.maxrecord
  - tune.ssl.ssl-ctx-cache-size
  - tune.ssl.ocsp-update.maxdelay (obsoleto)
  - tune.ssl.ocsp-update.mindelay (obsoleto)
  - tune.takeover-other-tg-connections
  - tune.vars.global-max-size
  - tune.vars.proc-max-size
  - tune.vars.reqres-max-size
  - tune.vars.sess-max-size
  - tune.vars.txn-max-size
  - tune.zlib.memlevel
  - tune.zlib.windowsize

- Depuración

  - anonkey
  - debug.counters
  - force-cfg-parser-pause
  - quiet
  - warn-blocked-traffic-after
  - zero-warning

- HTTPClient

  - httpclient.resolvers.disabled
  - httpclient.resolvers.id
  - httpclient.resolvers.prefer
  - httpclient.retries
  - httpclient.ssl.ca-file
  - httpclient.ssl.verify
  - httpclient.timeout.connect


## 3.1. Gestión de procesos y seguridad {#section-3-1}

<a id="entry-3-1-51degrees-data-file"></a>

**`51degrees-data-file <file path>`**

```haproxy
51degrees-data-file <file path>
```

La ruta del archivo de datos de 51Degrees para proporcionar servicios de detección de dispositivos.
El archivo debe estar descomprimido y ser accesible por HAProxy con los permisos pertinentes.

Ten en cuenta que esta opción solo está disponible cuando HAProxy ha sido compilado con
USE_51DEGREES.

<a id="entry-3-1-51degrees-property-name-list"></a>

**`51degrees-property-name-list [<string> ...]`**

```haproxy
51degrees-property-name-list [<string> ...]
```

Una lista de nombres de propiedades de 51Degrees que se cargarán del conjunto de datos. La lista
completa de nombres está disponible en el sitio web de 51Degrees:
<https://51degrees.com/resources/property-dictionary>

Ten en cuenta que esta opción solo está disponible cuando HAProxy ha sido compilado con
USE_51DEGREES.

<a id="entry-3-1-51degrees-property-separator"></a>

**`51degrees-property-separator <char>`**

```haproxy
51degrees-property-separator <char>
```

Un carácter que se añadirá a cada valor de propiedad en una cabecera de respuesta que contenga
resultados de 51Degrees. Si no se establece, se usará ','.

Ten en cuenta que esta opción solo está disponible cuando HAProxy ha sido compilado con
USE_51DEGREES.

<a id="entry-3-1-51degrees-cache-size"></a>

**`51degrees-cache-size <number>`**

```haproxy
51degrees-cache-size <number>
```

Establece el tamaño de la caché del conversor de 51Degrees a `<number>` entradas. Se trata de una
caché LRU que recuerda detecciones de dispositivos anteriores y sus resultados. Por defecto, esta
caché está desactivada.

Ten en cuenta que esta opción solo está disponible cuando HAProxy ha sido compilado con
USE_51DEGREES.

<a id="entry-3-1-51degrees-use-performance-graph"></a>

**`51degrees-use-performance-graph { on | off }`**

```haproxy
51degrees-use-performance-graph { on | off }
```

Activa ('on') o desactiva ('off') el uso del grafo de rendimiento en el proceso de detección. El
valor por defecto depende de la biblioteca de 51Degrees.

Ten en cuenta que esta opción solo está disponible cuando HAProxy ha sido compilado con
USE_51DEGREES y 51DEGREES_VER=4.

<a id="entry-3-1-51degrees-use-predictive-graph"></a>

**`51degrees-use-predictive-graph { on | off }`**

```haproxy
51degrees-use-predictive-graph { on | off }
```

Activa ('on') o desactiva ('off') el uso del grafo predictivo en el proceso de detección. El valor
por defecto depende de la biblioteca de 51Degrees.

Ten en cuenta que esta opción solo está disponible cuando HAProxy ha sido compilado con
USE_51DEGREES y 51DEGREES_VER=4.

<a id="entry-3-1-51degrees-drift"></a>

**`51degrees-drift <number>`**

```haproxy
51degrees-drift <number>
```

Establece el valor de deriva que una detección puede permitir.

Ten en cuenta que esta opción solo está disponible cuando HAProxy ha sido compilado con
USE_51DEGREES y 51DEGREES_VER=4.

<a id="entry-3-1-51degrees-difference"></a>

**`51degrees-difference <number>`**

```haproxy
51degrees-difference <number>
```

Establece el valor de diferencia que una detección puede permitir.

Ten en cuenta que esta opción solo está disponible cuando HAProxy ha sido compilado con
USE_51DEGREES y 51DEGREES_VER=4.

<a id="entry-3-1-51degrees-allow-unmatched"></a>

**`51degrees-allow-unmatched { on | off }`**

```haproxy
51degrees-allow-unmatched { on | off }
```

Activa ('on') o desactiva ('off') el uso de nodos sin coincidencia en el proceso de detección. El
valor por defecto depende de la biblioteca de 51Degrees.

Ten en cuenta que esta opción solo está disponible cuando HAProxy ha sido compilado con
USE_51DEGREES y 51DEGREES_VER=4.

<a id="entry-3-1-acme-scheduler"></a>

**`acme.scheduler { auto | off }`**

```haproxy
acme.scheduler { auto | off }
```

Activa o desactiva el planificador ACME.

El planificador ACME arranca con HAProxy; recorrerá los certificados e iniciará una tarea de
renovación ACME cuando el valor notAfter supere curtime + (notAfter - notBefore) / 12, o 7 días si
notBefore no está definido. A continuación, el planificador dormirá y despertará pasadas 12 horas.

El valor por defecto es "auto".

Ver también: acme

<a id="entry-3-1-ca-base"></a>

**`ca-base <dir>`**

```haproxy
ca-base <dir>
```

Asigna un directorio por defecto del que obtener certificados de CA SSL y CRL cuando se usa una ruta
relativa con las directivas "ca-file", "ca-verify-file" o "crl-file". Las ubicaciones absolutas
especificadas en "ca-file", "ca-verify-file" y "crl-file" prevalecen e ignoran "ca-base".

<a id="entry-3-1-chroot"></a>

**`chroot { <jail dir> | auto }`**

```haproxy
chroot { <jail dir> | auto }
```

Cambia el directorio actual a `<jail dir>` y realiza un chroot() allí antes de renunciar a los
privilegios. Esto aumenta el nivel de seguridad en caso de que se explote una vulnerabilidad
desconocida, ya que dificultaría mucho al atacante la explotación del sistema. Es importante
asegurarse de que `<jail dir>` esté tanto vacío como no escribible por nadie. Cuando el proceso se
inicia con privilegios de superusuario, el chroot() se realiza directamente. En Linux, cuando se
inicia sin privilegios, haproxy intenta realizarlo desde dentro de un nuevo espacio de nombres de
usuario creado con unshare(CLONE_NEWUSER); si ese mecanismo no está disponible, el chroot() fallará
con el error habitual.

Como caso especial, `<jail dir>` puede establecerse como "auto", en cuyo caso haproxy crea un
directorio temporal anónimo, lo desvincula y hace chroot en él. La jaula resultante no tiene nombre
en el sistema de archivos, está vacía y es de solo lectura, eliminando la necesidad de preparar un
directorio de jaula dedicado.

Al iniciar con privilegios de superusuario, se mostrará una advertencia si no se usa chroot, con el
fin de animar a los usuarios a usar siempre el mecanismo. Si por cualquier motivo existe una razón
de peso para no usar chroot (p. ej., acceso a un servidor mediante un socket UNIX con una ruta
incómoda), sigue siendo posible silenciar la advertencia añadiendo un "chroot /" explícito, lo que
tiene la ventaja de ser visible en la configuración.

<a id="entry-3-1-close-spread-time"></a>

**`close-spread-time <time>`**

```haproxy
close-spread-time <time>
```

Define una ventana de tiempo durante la cual se reparte el cierre de las conexiones inactivas y
activas en caso de parada suave. Tras recibirse un SIGUSR1 y terminar el periodo de gracia (si lo
hay), las conexiones inactivas se cerrarán todas a la vez si esta opción no está establecida, y las
conexiones HTTP o HTTP2 activas terminarán tras recibirse la siguiente solicitud, ya sea añadiendo
una línea "Connection: close" a la respuesta HTTP o enviando una trama GOAWAY en el caso de HTTP2.
Cuando esta opción está establecida, el cierre de conexiones se repartirá a lo largo de este
`<time>`. Si close-spread-time se establece como "infinite", se desactivará el cierre de conexiones
activas durante una parada suave. La cabecera "Connection: close" ya no se añadirá a las respuestas
HTTP (ni GOAWAY para HTTP2) y las conexiones inactivas solo se cerrarán cuando se alcance su tiempo
de espera (según los distintos timeouts establecidos en la configuración).

Argumentos:

```text
<time>  es una ventana de tiempo (por defecto en milisegundos) durante la
        cual se repartirá el cierre de las conexiones durante una operación
        de parada suave, o "infinite" si se debe desactivar el cierre de
        las conexiones activas.
```

Se recomienda establecer este ajuste a un valor menor que el usado en la opción "hard-stop-after" si
esta se usa, de modo que todas las conexiones tengan la oportunidad de cerrarse correctamente antes
de que el proceso se detenga.

Ver también: grace, hard-stop-after, idle-close-on-response

<a id="entry-3-1-cluster-secret"></a>

**`cluster-secret <secret>`**

```haproxy
cluster-secret <secret>
```

Define un secreto en forma de cadena ASCII compartido entre varios nodos que pertenecen al mismo
clúster. Podría usarse para distintos usos. Como mínimo, se usa para derivar los tokens de
reinicio sin estado para todas las conexiones QUIC instanciadas por este proceso. Este es también
el caso para derivar los secretos usados para cifrar los tokens Retry.

Si este parámetro no está establecido, se seleccionará un valor aleatorio en el arranque del
proceso. Esto permite usar funciones que dependen de él, aunque con algunas limitaciones.

<a id="entry-3-1-cpu-map"></a>

**`cpu-map [auto:]<thread-group>[/<thread-set>] <cpu-set>[,...] [...]`**

```haproxy
cpu-map [auto:]<thread-group>[/<thread-set>] <cpu-set>[,...] [...]
```

En algunos sistemas operativos, es posible vincular un grupo de hilos o un hilo a un conjunto de
CPU específico. Esto significa que los hilos designados nunca se ejecutarán en otras CPU. La
directiva "cpu-map" especifica conjuntos de CPU para hilos individuales o grupos de hilos. El
primer argumento es un rango de grupo de hilos, seguido opcionalmente de un conjunto de hilos.
Estos rangos tienen el siguiente formato:

```text
all | odd | even | number[-[number]]
```

`<number>` debe ser un número entre 1 y 32 o 64, dependiendo del tamaño de palabra de la máquina.
Cualquier ID de grupo por encima de 'thread-groups' y cualquier ID de hilo por encima del tamaño de
palabra de la máquina se ignoran. Todos los números de hilo son relativos al grupo al que
pertenecen. Es posible especificar un rango con dos de estos números delimitados por un guion
('-'). También es posible especificar todos los hilos a la vez usando "all", solo los números
impares usando "odd" o los números pares usando "even", igual que con la directiva de bind
"thread". El segundo argumento y los siguientes son conjuntos de CPU. Cada conjunto de CPU es un
número único que empieza en 0 para la primera CPU, o un rango con dos de estos números delimitado
por un guion ('-'). Estos números y rangos de CPU pueden repetirse delimitándolos con comas o
pasando más rangos como nuevos argumentos en la misma línea. Fuera de los sistemas operativos Linux
y BSD, puede haber una limitación del índice máximo de CPU a 31 o 63. Pueden especificarse
múltiples directivas "cpu-map", pero cada directiva "cpu-map" reemplazará las anteriores cuando se
solapen.

Los rangos pueden definirse parcialmente. El límite superior puede omitirse. En tal caso, se
sustituye por el valor máximo correspondiente, 32 o 64 dependiendo del tamaño de palabra de la
máquina.

El prefijo "auto:" puede añadirse antes del conjunto de hilos para que HAProxy vincule
automáticamente un conjunto de hilos a una CPU incrementando hilos y conjuntos de CPU. Para ser
válido, ambos conjuntos deben tener el mismo tamaño. No importa el orden de declaración de los
conjuntos de CPU, se vincularán del límite más bajo al más alto. No se admite tener a la vez un
rango de grupo y un rango de hilos con el prefijo "auto:". Solo se admite un rango; el otro debe ser
un número fijo.

Ten en cuenta que los rangos de grupo se mantienen por razones históricas. Hoy en día, un número
solitario designa un grupo de hilos y debe ser 1 si no se usan thread-groups, y especificar un
rango o número de hilos requiere anteponer "1/" si no se usan grupos de hilos. Finalmente, "1" es
estrictamente equivalente a "1/all" y designa todos los hilos del grupo.

Ejemplos:

```shell
cpu-map 1/all 0-3 # bind all threads of the first group on the
                  # first 4 CPUs

cpu-map 1/1- 0-   # will be replaced by "cpu-map 1/1-64 0-63"
                  # or "cpu-map 1/1-32 0-31" depending on the machine's
                  # word size.

# all these lines bind thread 1 to the cpu 0, the thread 2 to cpu 1
# and so on.
cpu-map auto:1/1-4   0-3
cpu-map auto:1/1-4   0-1 2-3
cpu-map auto:1/1-4   3 2 1 0
cpu-map auto:1/1-4   3,2,1,0

# bind each thread to exactly one CPU using all/odd/even keyword
cpu-map auto:1/all   0-63
cpu-map auto:1/even  0-31
cpu-map auto:1/odd   32-63

# invalid cpu-map because thread and CPU sets have different sizes.
cpu-map auto:1/1-4   0    # invalid
cpu-map auto:1/1     0-3  # invalid

# map 40 threads of those 4 groups to individual CPUs
cpu-map auto:1/1-10   0-9
cpu-map auto:2/1-10   10-19
cpu-map auto:3/1-10   20-29
cpu-map auto:4/1-10   30-39

# Map 80 threads to one physical socket and 80 others to another socket
# without forcing assignment. These are split into 4 groups since no
# group may have more than 64 threads.
cpu-map 1/1-40   0-39,80-119    # node0, siblings 0 & 1
cpu-map 2/1-40   0-39,80-119
cpu-map 3/1-40   40-79,120-159  # node1, siblings 0 & 1
cpu-map 4/1-40   40-79,120-159

```

<a id="entry-3-1-cpu-affinity"></a>

**`cpu-affinity <affinity>`**

```haproxy
cpu-affinity <affinity>
```

Define cómo quieres que los hilos se vinculen a las CPU. Actualmente acepta los siguientes valores:

- per-core: cada hilo se vinculará a todos los hilos de hardware de un núcleo.
- per-group: cada hilo se vinculará a todos los hilos de hardware del grupo. Este es el valor por
  defecto a menos que se use "threads-per-core 1" en "cpu-policy". "per-group" acepta un argumento
  opcional para especificar cómo deben asignarse las CPU. Cuando una lista de CPU es mayor que el
  número máximo permitido de CPU por grupo y debe dividirse entre varios grupos, una opción
  adicional permite elegir cómo se vincularán los grupos a esas CPU:
  - auto: a cada grupo de hilos solo se le asignará una parte equitativa de núcleos de CPU
    contiguos que estén dedicados a él y no compartidos con otros grupos. Este es el valor por
    defecto, ya que generalmente es más óptimo.
  - loose: cada grupo seguirá pudiendo usar cualquier CPU de la lista. Esto generalmente causa más
    contención, pero a veces puede ayudar a lidiar mejor con cargas parásitas que se ejecutan en
    las mismas CPU.
- auto: se usará "per-group", a menos que se use "threads-per-core 1" en "cpu-policy", en cuyo caso
  se usará "per-core". Este es el valor por defecto.
- per-thread: vincula un hilo a un solo hilo de hardware. Si se usa "threads-per-core 1" en
  "cpu-policy", cada hilo se vinculará a un hilo de hardware de un núcleo diferente.
- per-ccx: cada hilo se vinculará a todos los hilos de hardware de un CCX.

<a id="entry-3-1-cpu-policy"></a>

**`cpu-policy <policy> [threads-per-core 1 | auto]`**

```haproxy
cpu-policy <policy> [threads-per-core 1 | auto]
```

Selecciona la política de asignación de CPU que se usará.

En sistemas multi-CPU puede haber muchas razones para no usar todos los núcleos de CPU disponibles,
o para agruparlos en distintos grupos de hilos, ya sea por rendimiento, latencia, coste o gestión
de recursos a nivel de todo el sistema. La directiva "cpu-set" ya permite desalojar algunos de
ellos, pero una vez hecho, es necesario decidir cómo asignar los restantes a los hilos y grupos de
hilos.

Este mapeo normalmente se realiza con la directiva "cpu-map", aunque puede ser particularmente
difícil de mantener en sistemas heterogéneos.

La directiva "cpu-policy" elige, entre un pequeño número de políticas de asignación, cuál usar en
su lugar cuando no se usa "cpu-map". Actualmente se soportan las siguientes políticas, siendo
"performance" la predeterminada:

- none no se realiza ninguna post-selección particular. Todas las CPU habilitadas serán
  utilizables y, si el número de hilos no está establecido, se establecerá al número de CPU
  disponibles, pero no más de 32 en sistemas de 32 bits o 64 en sistemas de 64 bits, por
  thread-group. El número de thread-groups, si no está establecido, se establecerá a 1.

- efficiency exactamente igual que "group-by-ccx" más abajo, excepto que se desalojan los clústeres
  de CPU compuestos por núcleos cuyo rendimiento sea más de un 25% superior al del siguiente menos
  potente. Estos son típicamente núcleos "big" o "performance". Esto significa que si se detecta más
  de un tipo de núcleos de CPU, solo se usarán los eficientes. Esto puede tener sentido para usar
  con cargas moderadas cuando los núcleos más potentes deben quedar disponibles para la aplicación
  o para un componente de seguridad. Algunas CPU modernas tienen un gran número de estos núcleos de
  CPU eficientes que pueden ofrecer colectivamente un nivel decente de rendimiento consumiendo
  menos energía.

- first-usable-node si las CPU no fueron restringidas previamente en el arranque (por ejemplo
  usando la utilidad "taskset"), y si la directiva "nbthread" no fue establecida, se usará el
  primer nodo NUMA con CPU habilitadas, y este número de CPU se usará como número de hilos. Se
  habilitará un único grupo de hilos con todas ellas, dentro del límite de 32 o 64 dependiendo del
  sistema.

- group-by-2-ccx igual que "group-by-ccx" más abajo, pero crea un grupo cada dos CCX. Esto puede
  tener sentido en CPU con muchos CCX de pocos núcleos cada uno, para evitar crear muchos grupos, o
  para suavizar un poco la distribución cuando no todos los núcleos están en uso. Ten en cuenta que
  puede tener efectos muy negativos en el rendimiento cuando la comunicación entre CCX es lenta. En
  general se recomienda no usarlo.

- group-by-2-clusters igual que "group-by-cluster", pero crea un grupo cada dos clústeres. Esto
  puede tener sentido en CPU con muchos clústeres de pocos núcleos cada uno, para evitar crear
  muchos grupos, o para suavizar un poco la distribución cuando no todos los núcleos están en uso.
  Ten en cuenta que puede tener efectos muy negativos en el rendimiento cuando la comunicación
  entre clústeres es lenta. En general se recomienda no usarlo.

- group-by-3-ccx igual que "group-by-ccx" más abajo, pero crea un grupo cada tres CCX. Esto puede
  tener sentido en CPU con muchos CCX de pocos núcleos cada uno, para evitar crear muchos grupos, o
  para suavizar un poco la distribución cuando no todos los núcleos están en uso. Ten en cuenta que
  puede tener efectos muy negativos en el rendimiento cuando la comunicación entre CCX es lenta. En
  general se recomienda no usarlo.

- group-by-3-clusters igual que "group-by-cluster", pero crea un grupo cada tres clústeres. Esto
  puede tener sentido en CPU con muchos clústeres de pocos núcleos cada uno, para evitar crear
  muchos grupos, o para suavizar un poco la distribución cuando no todos los núcleos están en uso.
  Ten en cuenta que puede tener efectos muy negativos en el rendimiento cuando la comunicación
  entre clústeres es lenta. En general se recomienda no usarlo.

- group-by-4-ccx igual que "group-by-ccx" más abajo, pero crea un grupo cada cuatro CCX. Esto puede
  tener sentido en CPU con muchos CCX de pocos núcleos cada uno, para evitar crear muchos grupos, o
  para suavizar un poco la distribución cuando no todos los núcleos están en uso. Ten en cuenta que
  puede tener efectos muy negativos en el rendimiento cuando la comunicación entre CCX es lenta. En
  general se recomienda no usarlo.

- group-by-4-clusters igual que "group-by-cluster", pero crea un grupo cada cuatro clústeres. Esto
  puede tener sentido en CPU con muchos clústeres de pocos núcleos cada uno, para evitar crear
  muchos grupos, o para suavizar un poco la distribución cuando no todos los núcleos están en uso.
  Ten en cuenta que puede tener efectos muy negativos en el rendimiento cuando la comunicación
  entre clústeres es lenta. En general se recomienda no usarlo.

- group-by-ccx si no se estableció ni "nbthread" ni "nbtgroups", se crea un grupo de hilos por cada
  complejo de núcleos de CPU ("CCX") con CPU disponibles, cada uno con tantos hilos como CPU. Un
  CCX agrupa CPU con un acceso igualmente rápido a la caché de último nivel ("LLC"), típicamente la
  caché L3. En la mayoría de máquinas modernas es crítico para el rendimiento no mezclar CPU de CCX
  distantes en el mismo grupo de hilos. Todos los hilos de un grupo se vinculan entonces a todas
  las CPU del CCX, de modo que las comunicaciones intragrupo permanezcan locales al CCX sin imponer
  una vinculación demasiado fuerte. Se respetan los límites de hilos por grupo y los límites de
  grupos de hilos. Esto es recomendable en sistemas multi-socket y NUMA, así como en CPU con malas
  latencias inter-CCX.

- group-by-cluster si no se estableció ni "nbthread" ni "nbtgroups", se crea un grupo de hilos por
  cada clúster de CPU con CPU disponibles, cada uno con tantos hilos como CPU. Todos los hilos de
  un grupo se vinculan a todas las CPU del clúster, de modo que las comunicaciones intragrupo
  permanezcan locales al clúster sin imponer una vinculación demasiado fuerte. Se respetan los
  límites de hilos por grupo y los límites de grupos de hilos. Esto es recomendable en sistemas
  multi-socket y NUMA, así como en CPU con malas latencias inter-CCX. En la mayoría de servidores,
  los clústeres y los CCX son lo mismo, pero en máquinas heterogéneas ("performance" frente a
  "efficiency" o "big" frente a "little"), un clúster generalmente estará formado por solo una
  parte de un CCX compuesta únicamente de CPU muy similares (mismo tipo, +/-5% de diferencia de
  frecuencia como máximo). La diferencia es visible en los portátiles y máquinas de escritorio
  modernos que usan desarrolladores y administradores para validar configuraciones.

- performance exactamente igual que "group-by-ccx" más arriba, excepto que se desalojan los
  clústeres de CPU compuestos por núcleos cuyo rendimiento sea inferior al 80% del del siguiente
  más potente. Estos son típicamente núcleos "little" o "efficient", cuya adición generalmente no
  aporta beneficios significativos y puede resultar fácilmente contraproducente (p. ej.,
  handshakes TLS). A menudo, reservar dichos núcleos para otras tareas como el manejo de la red es
  mucho más eficaz. En sistemas de desarrollo también pueden usarse para ejecutar herramientas
  auxiliares como generadores de carga y herramientas de monitorización. Esta es la política por
  defecto.

- resource esto es como "group-by-cluster" más arriba, excepto que solo se usará el clúster de CPU
  más pequeño y eficiente, mientras que todos los demás se ignorarán. Esto puede usarse para
  limitar el uso de recursos al mínimo estricto que aún ofrece un rendimiento decente, por ejemplo
  para intentar reducir aún más el consumo de energía o minimizar el número de núcleos necesarios
  en algunos sistemas alquilados para una configuración sidecar, con el fin de reducir la escala
  del sistema más fácilmente. Ten en cuenta que si solo hay un clúster presente, se usará
  igualmente por completo.

Puede añadirse una palabra clave opcional, "threads-per-core". Acepta dos valores, "1" y "auto". Si
se establece a 1, solo se creará un hilo por núcleo, independientemente de cuántos hilos de
hardware tenga el núcleo. Si se establece a auto, se creará un hilo por cada hilo de hardware. Si
no se especifica ninguna afinidad y se usa threads-per-core 1, por defecto la afinidad será
per-core.

Ver también: "cpu-map", "cpu-set", "nbthread"

<a id="entry-3-1-cpu-set"></a>

**`cpu-set <directive>...`**

```haproxy
cpu-set <directive>...
```

Permite describir simbólicamente sobre qué conjuntos de CPU ejecutarse. La directiva admite las
siguientes palabras clave: - reset deshace cualquier limitación previa que pudiera haberse
heredado, por ejemplo, de un gestor de servicios o de un comando "taskset". - drop-cpu `<set>` no
vincularse a las CPU de este conjunto - only-cpu `<set>` no vincularse a las CPU que no estén en
este conjunto - drop-node `<set>` no vincularse a las CPU que pertenezcan a este nodo NUMA -
only-node `<set>` no vincularse a las CPU que no pertenezcan a este nodo NUMA - drop-cluster
`<set>` no vincularse a las CPU de este número de clúster de hardware - only-cluster `<set>` no
vincularse a las CPU de otros números de clúster de hardware - drop-core `<set>` no vincularse a
las CPU de este número de núcleo de hardware - only-core `<set>` no vincularse a las CPU de otros
números de núcleo de hardware - drop-thread `<set>` no vincularse a las CPU de este número de hilo
de hardware - only-thread `<set>` no vincularse a las CPU de otros números de hilo de hardware Ver
también: "cpu-policy"

<a id="entry-3-1-crt-base"></a>

**`crt-base <dir>`**

```haproxy
crt-base <dir>
```

Asigna un directorio por defecto del que obtener certificados SSL cuando se usa una ruta relativa
con las directivas "crtfile" o "crt". Las ubicaciones absolutas especificadas prevalecen e ignoran
"crt-base".

<a id="entry-3-1-daemon"></a>

**`daemon`**

```haproxy
daemon
```

Hace que el proceso se separe (fork) para ejecutarse en segundo plano. Este es el modo de operación
recomendado. Es equivalente al argumento "-D" de la línea de comandos. Puede desactivarse con el
argumento "-db" de la línea de comandos. Esta opción se ignora en modo systemd.

<a id="entry-3-1-default-path"></a>

**`default-path { current | config | parent | origin <path> }`**

```haproxy
default-path { current | config | parent | origin <path> }
```

Por defecto, HAProxy carga todos los archivos designados por una ruta relativa desde la ubicación
en la que se inicia el proceso. En algunas circunstancias puede ser deseable forzar que todas las
rutas relativas comiencen desde una ubicación diferente, como si el proceso se hubiera iniciado
desde dichas ubicaciones. Para eso sirve esta directiva. Técnicamente realizará un chdir() temporal
a la ubicación designada mientras procesa cada archivo de configuración y volverá al directorio
original tras procesar cada archivo. Toma un argumento que indica la política a usar al cargar
archivos cuya ruta no comienza con una barra ('/'): - "current" indica que todos los archivos
relativos se cargarán desde el directorio en el que se inicia el proceso; este es el valor por
defecto.

    - "config" indica que todos los archivos relativos deben cargarse desde el directorio que
      contiene el archivo de configuración. Más concretamente, si el archivo de configuración
      contiene una barra ('/'), se usa como directorio al que cambiar la parte más larga hasta la
      última barra; de lo contrario se usa el directorio actual. Este modo es práctico para
      empaquetar juntos maps, errorfiles, certificados y scripts Lua como paquetes reubicables.
      Cuando se cargan múltiples archivos de configuración, el directorio se actualiza para cada
      uno de ellos.

    - "parent" indica que todos los archivos relativos deben cargarse desde el padre del
      directorio que contiene el archivo de configuración. Más concretamente, si el archivo de
      configuración contiene una barra ('/'), se añade ".." a la parte más larga hasta la última
      barra y se usa como directorio al que cambiar; de lo contrario el directorio es "..". Este
      modo es práctico para empaquetar juntos maps, errorfiles, certificados y scripts Lua como
      paquetes reubicables, pero donde cada parte está ubicada en un subdirectorio diferente (p.
      ej. "config/", "certs/", "maps/", ...).

    - "origin" indica que todos los archivos relativos deben cargarse desde la ruta designada
      (obligatoria). Esto puede usarse para facilitar la gestión de diferentes instancias de HAProxy
      ejecutándose en paralelo en un sistema, donde cada instancia usa un prefijo diferente pero el
      resto de las secciones se hacen fácilmente reubicables.

Cada directiva "default-path" reemplaza instantáneamente cualquier anterior y posiblemente dará
lugar a un cambio a un directorio diferente. Aunque esto siempre debería producir el comportamiento
deseado, realmente no es una buena práctica usar múltiples directivas default-path y, si se usan,
la política debería mantenerse consistente en todos los archivos de configuración.

Advertencia: algunos elementos de configuración como los maps o los certificados se identifican de
forma única por su ruta configurada. Al usar una disposición reubicable, es posible que varios de
ellos acaben con el mismo nombre único, lo que dificulta su actualización en tiempo de ejecución,
especialmente cuando se cargan múltiples archivos de configuración desde diferentes directorios. Es
esencial observar un esquema estricto de nombres de archivo sin colisiones antes de adoptar rutas
relativas. Un enfoque robusto podría consistir en anteponer a todos los nombres de archivo su
respectivo nombre de sitio, o hacerlo a nivel de directorio.

<a id="entry-3-1-description"></a>

**`description <text>`**

```haproxy
description <text>
```

Añade un texto que describe la instancia.

Ten en cuenta que es necesario escapar ciertos caracteres (# por ejemplo) y que este texto se
inserta en una página html, por lo que deberías evitar el uso de los caracteres "\<" y "\>".

<a id="entry-3-1-deviceatlas-json-file"></a>

**`deviceatlas-json-file <path>`**

```haproxy
deviceatlas-json-file <path>
```

Establece la ruta del archivo de datos JSON de DeviceAtlas que cargará la API. La ruta debe ser un
archivo de datos JSON válido y accesible por el proceso de HAProxy.

<a id="entry-3-1-deviceatlas-log-level"></a>

**`deviceatlas-log-level <value>`**

```haproxy
deviceatlas-log-level <value>
```

Establece el nivel de información devuelta por la API. Esta directiva es opcional y está
establecida a 0 por defecto si no se establece.

<a id="entry-3-1-deviceatlas-properties-cookie"></a>

**`deviceatlas-properties-cookie <name>`**

```haproxy
deviceatlas-properties-cookie <name>
```

Establece el nombre de la cookie del cliente usado para la detección si el componente del lado del
cliente de DeviceAtlas fue usado durante la solicitud. Esta directiva es opcional y está
establecida a DAPROPS por defecto si no se establece.

<a id="entry-3-1-deviceatlas-separator"></a>

**`deviceatlas-separator <char>`**

```haproxy
deviceatlas-separator <char>
```

Establece el carácter separador para los resultados de las propiedades de la API. Esta directiva es
opcional y está establecida a \| por defecto si no se establece.

<a id="entry-3-1-dns-accept-family"></a>

**`dns-accept-family <family>[,...]`**

```haproxy
dns-accept-family <family>[,...]
```

Por defecto, los resolutores DNS aceptan tanto direcciones IPv4 como IPv6. Esto puede influirse con
las palabras clave "resolve-prefer" en las líneas de server, así como con el argumento de familia
de la acción "do-resolve", pero es solo una preferencia, que no impide que la otra familia se use
cuando está sola. En algunos entornos donde la doble pila no es utilizable, toparse con un registro
DNS solo IPv6 inalcanzable puede causar problemas significativos, ya que reemplazará a uno IPv4
anterior que posiblemente habría seguido funcionando hasta la siguiente solicitud. La opción global
"dns-accept-family" permite imponer el uso de solo una (o ambas) familias de direcciones. El
argumento es una lista separada por comas de las siguientes palabras: - "ipv4": consultar y aceptar
direcciones IPv4 (registros "A") - "ipv6": consultar y aceptar direcciones IPv6 (registros "AAAA") - "auto": usar IPv4, e IPv6 si el sistema tiene una pasarela por defecto para ello. El resultado de
la última comprobación se cachea durante 30 segundos.

Cuando se usa una sola familia, no se enviará ninguna solicitud a los resolutores por la otra
familia, y cualquier respuesta de la otra familia será ignorada. El valor por defecto desde la
versión 3.3 es "auto", lo que habilita efectivamente ambas familias solo una vez que se ha
comprobado que IPv6 es enrutable; de lo contrario, se ciñe a IPv4. Ver también:
"resolve-prefer", "do-resolve"

<a id="entry-3-1-expose-deprecated-directives"></a>

**`expose-deprecated-directives`**

```haproxy
expose-deprecated-directives
```

Esta declaración debe aparecer antes de usar ciertas directivas marcadas como obsoletas para
silenciar las advertencias y asegurarse de que el archivo de configuración no sea rechazado. No
todas las directivas obsoletas están afectadas, solo aquellas sin ninguna solución alternativa.

<a id="entry-3-1-expose-experimental-directives"></a>

**`expose-experimental-directives`**

```haproxy
expose-experimental-directives
```

Esta declaración debe aparecer antes de usar directivas marcadas como experimentales o el archivo
de configuración será rechazado. Ten en cuenta que no se garantiza que las funciones cubiertas por
esta opción funcionen bien y pueden romperse durante el ciclo de mantenimiento. Los desarrolladores
las mantendrán en modo de mejor esfuerzo mientras se trabaja en la próxima versión y harán cualquier
esfuerzo razonable por no romperlas, pero sin garantía. Por estas razones, no se espera que estas
funciones estén soportadas más allá del lanzamiento de la próxima versión LTS. Se espera que los
usuarios que quieran probar funciones experimentales actualicen rápidamente para beneficiarse de
las mejoras hechas a esa función. Para saber si esta directiva sigue siendo necesaria, es fácil: si
está habilitada sin que ninguna de esas funciones la use, se emitirá una advertencia sugiriendo
desactivarla. Así que si no hay ninguna advertencia, significa que sigue siendo necesaria.

<a id="entry-3-1-external-check"></a>

**`external-check [preserve-env]`**

```haproxy
external-check [preserve-env]
```

Permite el uso de un agente externo para realizar comprobaciones de salud. Esto está desactivado
por defecto como precaución de seguridad e, incluso habilitado, las comprobaciones pueden seguir
fallando a menos que "insecure-fork-wanted" también esté habilitado. Si el programa lanzado hace uso
de un ejecutable setuid (realmente no debería), puede que también necesites establecer
"insecure-setuid-wanted" en la sección global. Por defecto, las comprobaciones arrancan con un
entorno limpio que solo contiene variables definidas en el comando "external-check" de la sección
backend. Sin embargo, a veces puede ser deseable preservar el entorno, por ejemplo cuando scripts
complejos obtienen de él sus rutas o información adicionales. Esto puede hacerse añadiendo la
palabra clave "preserve-env". En este caso, sin embargo, se recomienda encarecidamente no ejecutar
un setuid ni hacerlo como usuario privilegiado, ya que esto expone el programa de comprobación a
posibles ataques. Ver "option external-check", "insecure-fork-wanted" e "insecure-setuid-wanted"
para más detalles.

<a id="entry-3-1-fd-hard-limit"></a>

**`fd-hard-limit <number>`**

```haproxy
fd-hard-limit <number>
```

Establece un límite superior al número máximo de descriptores de archivo que usará el proceso,
independientemente de los límites del sistema. Aunque "ulimit-n" y "maxconn" pueden usarse para
imponer un valor, cuando no están establecidos, el proceso estará limitado al límite duro del
ajuste RLIMIT_NOFILE tal como lo informa "ulimit -n -H". Pero algunos sistemas operativos modernos
permiten ahora aquí valores extremadamente grandes (del orden de mil millones), que consumirán
demasiada RAM para un uso normal. El ajuste fd-hard-limit se proporciona para imponer un límite
posiblemente inferior a este límite. Esto significa que siempre respetará los límites impuestos por
el sistema cuando estén por debajo de `<number>`, pero se usará el valor especificado si los límites
impuestos por el sistema son mayores. Por defecto, fd-hard-limit está establecido a 1048576. Este
valor por defecto podría cambiarse mediante la variable de compilación DEFAULT_MAXFD, que podría
servir como límite máximo del sistema (kernel) si el límite duro de RLIMIT_NOFILE es extremadamente
grande. Establecer fd-hard-limit en la sección global permite anular temporalmente el valor
proporcionado vía DEFAULT_MAXFD en tiempo de compilación. En el ejemplo siguiente no se especifica
ningún otro ajuste y el valor de maxconn se adaptará automáticamente al menor entre
"fd-hard-limit" y el límite RLIMIT_NOFILE:

```text
global
    # use as many FDs as possible but no more than 50000
    fd-hard-limit 50000
```

Ver también: ulimit-n, maxconn

<a id="entry-3-1-gid"></a>

**`gid <number>`**

```haproxy
gid <number>
```

Cambia el ID de grupo del proceso a `<number>`. Se recomienda que el ID de grupo esté dedicado a
HAProxy o a un pequeño conjunto de demonios similares. HAProxy debe iniciarse con un usuario
perteneciente a este grupo, o con privilegios de superusuario. Ten en cuenta que si HAProxy se
inicia desde un usuario con grupos suplementarios, solo podrá desprenderse de estos grupos si se
inicia con privilegios de superusuario. Ver también "group" y "uid".

<a id="entry-3-1-grace"></a>

**`grace <time>`**

```haproxy
grace <time>
```

Define un retraso entre el SIGUSR1 y la parada suave real.

Argumentos:

```text
<time>  es un retraso adicional (por defecto en milisegundos) tras la
        recepción de la señal SIGUSR1 que se esperará antes de proceder con
        la operación de parada suave.
```

Esto se usa por compatibilidad con entornos heredados donde el proceso haproxy debe detenerse pero
algunos componentes externos necesitan detectar el estado antes de que los listeners se desvinculen.
El principio es que la variable interna "stopping" (que informa la función de obtención de muestras
"stopping") pasará a verdadero, pero los listeners seguirán aceptando conexiones sin perturbación
hasta que expire el retraso, tras lo cual procederá la parada suave habitual. Esto no debe usarse
con procesos que se recargan, o impedirá que el proceso antiguo se desvincule y puede impedir que
el nuevo arranque, o simplemente causar problemas.

Ejemplo:

```shell
global
  grace 10s

# Returns 200 OK until stopping is set via SIGUSR1
frontend ext-check
  bind :9999
  monitor-uri /ext-check
  monitor fail if { stopping }
```

Ten en cuenta que un enfoque más flexible y duradero consistiría, en cambio, en que un sistema de
orquestación establezca una variable global desde la CLI, use esa variable para responder a
comprobaciones externas y luego, tras un retraso, envíe la señal SIGUSR1.

Ejemplo:

```shell
# Returns 200 OK until proc.stopping is set to non-zero. May be done
# from HTTP using set-var(proc.stopping) or from the CLI using:
# > set var proc.stopping int(1)
frontend ext-check
  bind :9999
  monitor-uri /ext-check
  monitor fail if { var(proc.stopping) -m int gt 0 }
```

Ver también: hard-stop-after, monitor

<a id="entry-3-1-group"></a>

**`group <group name>`**

```haproxy
group <group name>
```

Similar a "gid" pero usa el GID del nombre de grupo `<group name>` de /etc/group. Ver también "gid"
y "user".

<a id="entry-3-1-h1-accept-payload-with-any-method"></a>

**`h1-accept-payload-with-any-method`**

```haproxy
h1-accept-payload-with-any-method
```

No rechaza las solicitudes GET/HEAD/DELETE de HTTP/1.0 con carga útil mediante una respuesta HTTP
413 Payload Too Large.

Si bien está explícitamente permitido en HTTP/1.1, HTTP/1.0 no es claro en este punto y algunos
servidores antiguos no esperan ninguna carga útil y nunca buscan la longitud del cuerpo (mediante
las cabeceras Content-Length o Transfer-Encoding). Esto significa que algunos intermediarios
pueden manejar correctamente la carga útil de las solicitudes GET/HEAD/DELETE de HTTP/1.0, mientras
que otros pueden ignorarla totalmente. Eso puede provocar problemas de seguridad porque es posible
un ataque de request smuggling. Por ello, por defecto, HAProxy rechaza las solicitudes
GET/HEAD/DELETE de HTTP/1.0 con carga útil.

Sin embargo, puede ser un problema con algunos clientes antiguos. En este caso, puede establecerse
esta opción global.

<a id="entry-3-1-h1-do-not-close-on-insecure-transfer-encoding"></a>

**`h1-do-not-close-on-insecure-transfer-encoding`**

```haproxy
h1-do-not-close-on-insecure-transfer-encoding
```

Tal como exige la especificación HTTP/1.1 (RFC9112#6.1), la presencia a la vez de un campo de
cabecera Transfer-Encoding y de un campo de cabecera Content-Length en el mismo mensaje representa
un riesgo serio de transmitir un ataque de content smuggling si hay algún agente HTTP/1.0 en
cualquier punto de la cadena aguas arriba o aguas abajo, y ante esto, un agente debe cerrar
absolutamente la conexión tras la respuesta para evitar cualquier explotación. Pero esto puede
tener un impacto en el rendimiento en algunos clientes muy antiguos, especialmente si necesitan
renegociar una conexión TLS por cada solicitud. Esta opción está presente para pedir a HAProxy que
no imponga esta regla, y que simplemente sanee el mensaje pero mantenga la conexión viva tras la
respuesta. Esto solo puede hacerse cuando se esté absolutamente seguro de que no hay agentes
HTTP/1.0 presentes en la cadena y de que todas las implementaciones anteriores a HAProxy cumplen
plenamente HTTP/1.1 en cuanto a las reglas que se aplican a estos campos de cabecera. En cualquier
caso, HAProxy seguirá ignorando y descartando la cabecera Content-Length sobrante para no confundir
al siguiente salto.

Al habilitar esta opción para sortear un cliente o servidor antiguo y defectuoso, es importante
entender que, necesite o no esta opción, un agente que viole esta regla se expone al riesgo de que
sus mensajes queden truncados por agentes antiguos que consideren Content-Length e ignoren
Transfer-Encoding, ya que el tamaño acumulado de los tamaños de los chunks codificados no se tiene
en cuenta. Asimismo, la regla anterior no es solo cuestión de seguridad, sino también de ocuparse
de eliminar agentes que pueden sufrir problemas de comunicación debido a incompatibilidades con
otros más antiguos.

<a id="entry-3-1-h1-case-adjust"></a>

**`h1-case-adjust <from> <to>`**

```haproxy
h1-case-adjust <from> <to>
```

Define el ajuste de mayúsculas que se aplicará, cuando esté habilitado, al nombre de cabecera
`<from>`, para cambiarlo a `<to>` antes de enviarlo a clientes o servidores HTTP/1. `<from>` debe
estar en minúsculas, y `<from>` y `<to>` no deben diferir excepto en las mayúsculas. Puede
repetirse si varios nombres de cabecera necesitan ajustarse. No se permiten entradas duplicadas. Si
hay que ajustar muchos nombres de cabecera, puede ser más cómodo usar "h1-case-adjust-file". Ten en
cuenta que no se aplicará ninguna transformación a menos que se especifique "option
h1-case-adjust-bogus-client" o "option h1-case-adjust-bogus-server" en un proxy.

No existe un uso de mayúsculas estándar para los nombres de cabecera porque, como se indica en
RFC7230, son insensibles a mayúsculas y minúsculas. Por tanto, las aplicaciones deben manejarlos de
forma insensible a mayúsculas. Pero algunas aplicaciones defectuosas violan los estándares y
dependen erróneamente de los usos de mayúsculas más comunes de los navegadores. Este problema se
vuelve crítico con HTTP/2 porque todos los nombres de cabecera deben intercambiarse en minúsculas,
y HAProxy sigue la misma convención. Todos los nombres de cabecera se envían en minúsculas a
clientes y servidores, independientemente de la versión de HTTP.

Las aplicaciones que no procesan correctamente las solicitudes o respuestas pueden requerir el uso
temporal de estos rodeos para ajustar los nombres de cabecera que se les envían durante el tiempo
que tarda en corregirse la aplicación. Ten en cuenta que una aplicación que requiere tales rodeos
podría ser vulnerable a ataques de content smuggling y debe corregirse sin falta.

Ejemplo:

```text
global
  h1-case-adjust content-length Content-Length
```

Ver "h1-case-adjust-file", "option h1-case-adjust-bogus-client" y "option
h1-case-adjust-bogus-server".

<a id="entry-3-1-h1-case-adjust-file"></a>

**`h1-case-adjust-file <hdrs-file>`**

```haproxy
h1-case-adjust-file <hdrs-file>
```

Define un archivo que contiene una lista de pares clave/valor usados para ajustar las mayúsculas
de algunos nombres de cabecera antes de enviarlos a clientes o servidores HTTP/1. El archivo
`<hdrs-file>` debe contener 2 nombres de cabecera por línea. El primero debe estar en minúsculas y
ambos no deben diferir excepto en las mayúsculas. Las líneas que comienzan por '#' se ignoran, al
igual que las líneas vacías. Los tabuladores y espacios iniciales y finales se eliminan. No se
permiten entradas duplicadas. Ten en cuenta que no se aplicará ninguna transformación a menos que
se especifique "option h1-case-adjust-bogus-client" o "option h1-case-adjust-bogus-server" en un
proxy.

Si esta directiva se repite, solo se procesará la última. Es una alternativa a la directiva
"h1-case-adjust" si hay que ajustar muchos nombres de cabecera. Lee los riesgos asociados al uso
de esto.

Ver "h1-case-adjust", "option h1-case-adjust-bogus-client" y "option
h1-case-adjust-bogus-server".

<a id="entry-3-1-h2-workaround-bogus-websocket-clients"></a>

**`h2-workaround-bogus-websocket-clients`**

```haproxy
h2-workaround-bogus-websocket-clients
```

Esto desactiva el anuncio a los clientes del soporte de websockets h2. Puede usarse para sortear
clientes que tienen problemas al implementar la relativamente reciente RFC8441, como Firefox 88.
Para permitir que los clientes degraden automáticamente a http/1.1 para el túnel websocket,
especifica el soporte de h2 en la línea bind usando "alpn" sin una palabra clave "proto"
explícita. Si esta declaración fue activada previamente, puede desactivarse prefijando la palabra
clave con "no".

<a id="entry-3-1-hard-stop-after"></a>

**`hard-stop-after <time>`**

```haproxy
hard-stop-after <time>
```

Define el tiempo máximo permitido para realizar una parada suave limpia.

Argumentos:

```text
<time>  es el tiempo máximo (por defecto en milisegundos) durante el cual
        la instancia permanecerá viva cuando se reciba una parada suave a
        través de la señal SIGUSR1.
```

Esto puede usarse para asegurar que la instancia terminará incluso si quedan conexiones abiertas
durante una parada suave (por ejemplo, con timeouts largos para un proxy en modo tcp). Se aplica
tanto en modo TCP como HTTP.

Ejemplo:

```text
global
  hard-stop-after 30s
```

Ver también: grace

<a id="entry-3-1-harden-reject-privileged-ports-tcp"></a>

**`harden.reject-privileged-ports.tcp { on | off }`**

```haproxy
harden.reject-privileged-ports.tcp { on | off }
harden.reject-privileged-ports.quic { on | off }
```

Activa o desactiva por protocolo la protección que prohíbe la comunicación con clientes que usan
puertos privilegiados como puerto de origen. Este rango de puertos está definido según RFC 6335.
Por defecto, la protección está activa para el protocolo QUIC, ya que este comportamiento es
sospechoso y puede usarse como ataque de suplantación o de amplificación DNS/NTP.

<a id="entry-3-1-http-err-codes"></a>

**`http-err-codes [+-]<range>[,...] [...]`**

```haproxy
http-err-codes [+-]<range>[,...] [...]
```

Reemplaza, reduce o amplía la lista de códigos de estado que definen un error según lo considerado
por los códigos de terminación y el contador "http_err_cnt" en las stick tables. El rango por
defecto para los errores es de 400 a 499, pero en ciertos contextos algunos usuarios prefieren
excluir códigos específicos, especialmente al rastrear errores de cliente (p. ej., 404 en sistemas
con contenidos generados dinámicamente). Ver también "http-fail-codes" y "http_err_cnt".

Un rango especificado sin '+' ni '-' redefine el rango existente con el nuevo. Un rango que
comienza por '+' amplía el rango existente para incluir también el especificado, que puede
solaparse o no con el existente. Un rango que comienza por '-' elimina del existente el rango
especificado.
Un rango consiste en un número de 100 a 599, seguido opcionalmente de "-" y de otro número mayor o
igual que el primero para indicar el límite superior del rango. Pueden delimitarse múltiples rangos
por comas para una misma operación de añadir/eliminar/reemplazar.

Ejemplo:

```text
http-err-codes 400,402-444,446-480,490   # sets exactly these codes
http-err-codes 400-499 -450 +500         # sets 400 to 500 except 450
http-err-codes -450-459                  # removes 450 to 459 from range
http-err-codes +501,505                  # adds 501 and 505 to range
```

<a id="entry-3-1-http-fail-codes"></a>

**`http-fail-codes [+-]<range>[,...] [...]`**

```haproxy
http-fail-codes [+-]<range>[,...] [...]
```

Reemplaza, reduce o amplía la lista de códigos de estado que definen un fallo según lo considerado
por los códigos de terminación y el contador "http_fail_cnt" en las stick tables. El rango por defecto para los fallos es de 500 a 599, excepto 501 y 505, que pueden ser provocados por clientes. Los códigos de este rango normalmente indican un fallo del servidor al procesar la solicitud. Algunos usuarios prefieren
excluir ciertos códigos en ciertos contextos donde se sabe que no son relevantes, como el 500 en
ciertos entornos SOAP, ya que allí no refleja un fallo del servidor. La sintaxis es exactamente la
misma que la de http-err-codes más arriba. Ver también "http-err-codes" y "http_fail_cnt".

<a id="entry-3-1-insecure-fork-wanted"></a>

**`insecure-fork-wanted`**

```haproxy
insecure-fork-wanted
```

Por defecto, HAProxy se esfuerza por evitar cualquier creación de hilos y procesos después de
arrancar. Hacerlo es particularmente importante cuando se usan archivos Lua de origen incierto y al
experimentar con versiones de desarrollo que aún pueden contener errores cuya explotabilidad es incierta. Y, en términos generales, es una buena higiene asegurarse de que el tráfico no pueda
desencadenar actividad inesperada en segundo plano. Pero esto impide que funcionen las
comprobaciones externas y puede romper algunos scripts Lua muy específicos que dependen
activamente de la capacidad de hacer fork. Esta opción existe para desactivar esta protección. Ten
en cuenta que es una mala idea desactivarla, ya que una vulnerabilidad en una biblioteca o dentro
del propio HAProxy será más fácil de explotar una vez desactivada. Además, hacer fork desde Lua o
desde cualquier otro lugar no es fiable, ya que el proceso bifurcado puede contener aleatoriamente
un bloqueo establecido por otro hilo y no llegar nunca a terminar una operación. Por ello, es
altamente recomendable no usar nunca esta opción y reconsiderar cualquier carga de trabajo que
requiera dicho fork y moverla a una solución más segura (como agentes en lugar de comprobaciones
externas). Esta opción admite el prefijo "no" para desactivarla. También puede activarse con "-dI"
en la línea de comandos de haproxy.

<a id="entry-3-1-insecure-setuid-wanted"></a>

**`insecure-setuid-wanted`**

```haproxy
insecure-setuid-wanted
```

HAProxy no necesita llamar ejecutables en tiempo de ejecución (excepto cuando se usan
comprobaciones externas, algo fuertemente desaconsejado), y se espera incluso que se aísle en un
chroot vacío. Como tal, básicamente no hay ninguna razón válida para permitir que se llame a un
ejecutable setuid sin que el usuario sea plenamente consciente de los riesgos. En una situación
donde HAProxy necesitara llamar comprobaciones externas o desactivar el chroot, explotar una
vulnerabilidad en una biblioteca o en el propio HAProxy podría conducir a la ejecución de un
programa externo. En Linux es posible bloquear el proceso de modo que cualquier bit setuid
presente en dicho ejecutable se ignore. Esto reduce significativamente el riesgo de escalada de
privilegios en tal situación. Esto es lo que HAProxy hace por defecto. En caso de que esto cause un
problema a una comprobación externa (por ejemplo, una que necesitara el comando "ping"), es posible
desactivar esta protección añadiendo explícitamente esta directiva en la sección global. Si está
habilitada, es posible volver a desactivarla prefijándola con la palabra clave "no".

<a id="entry-3-1-issuers-chain-path"></a>

**`issuers-chain-path <dir>`**

```haproxy
issuers-chain-path <dir>
```

Asigna un directorio para cargar cadenas de certificados para completar el emisor. Todos los
archivos deben estar en formato PEM. Para los certificados cargados con "crt" o "crt-list", si la
cadena de certificación no está incluida en el PEM (también conocido comúnmente como certificado
intermedio), HAProxy completará la cadena si el emisor del certificado corresponde al primer
certificado de la cadena cargada con "issuers-chain-path". Un archivo "crt" con
PrivateKey+Certificate+IntermediateCA2+IntermediateCA1 podría sustituirse por
PrivateKey+Certificate. HAProxy completará la cadena si un archivo con
IntermediateCA2+IntermediateCA1 está presente en el directorio "issuers-chain-path". Todos los
demás certificados con el mismo emisor compartirán la cadena en memoria.

Las funciones OCSP pueden usar la cadena completada cuando no se usó ningún .issuer, o cuando no se
proporcionó ninguna cadena en el PEM.

<a id="entry-3-1-jwt-allow-none-alg"></a>

**`jwt.allow_none_alg`**

```haproxy
jwt.allow_none_alg
```

Permite tokens JWT firmados con el algoritmo "none" en el conversor 'jwt_verify'. Siempre se
considerarán válidos cuando esta opción esté establecida. Por defecto, los tokens sin firma se
rechazan ya que se consideran inseguros (ver RFC8725 [sección
3.1](https://www.rfc-editor.org/rfc/rfc8725#section-3.1)).

<a id="entry-3-1-jwt-decrypt-alg-list"></a>

**`jwt.decrypt_alg_list <list>`**

```haproxy
jwt.decrypt_alg_list <list>
```

Establece la lista de algoritmos permitidos en los conversores jwt_decrypt_XXX. Los tokens JWT que
usen un algoritmo no soportado o deshabilitado nunca se descifrarán. Los algoritmos especificados
deben tener el mismo formato que en la [sección 4.1](https://www.rfc-editor.org/rfc/rfc7518#section-4.1)
de RFC7518 y deben ir separados por dos puntos. El nombre especial "ALL" puede usarse para
habilitar todos los algoritmos soportados (ver el conversor "jwt_decrypt_jwk" para una lista
completa) y puede añadirse '!' a un nombre de algoritmo para deshabilitarlo explícitamente. Ten en
cuenta que, a menos que se especifique "ALL", el uso de esta opción deshabilitará cualquier
algoritmo que no se mencione explícitamente en la lista proporcionada.

Ejemplos:

```shell
# Enable all algorithms but the "ECDH-ES" one
jwt.decrypt_alg_list ALL:!ECDH-ES

# Only enable ECDH-ES algorithms
jwt.decrypt_alg_list ECDH-ES:ECDH-ES+A128KW:ECDH-ES+A192KW:ECDH-ES+A256KW
```

<a id="entry-3-1-jwt-decrypt-enc-list"></a>

**`jwt.decrypt_enc_list <list>`**

```haproxy
jwt.decrypt_enc_list <list>
```

Establece la lista de algoritmos de cifrado permitidos en los conversores jwt_decrypt_XXX. Los
tokens JWT que usen un algoritmo de cifrado no soportado o deshabilitado nunca se descifrarán. Los
algoritmos especificados deben tener el mismo formato que en la [sección 5.1](https://www.rfc-editor.org/rfc/rfc7518#section-5.1)
de RFC7518 y deben ir separados por dos puntos. El nombre especial "ALL" puede usarse para
habilitar todos los algoritmos soportados (ver el conversor "jwt_decrypt_jwk" para una lista
completa) y puede añadirse '!' a un nombre de algoritmo para deshabilitarlo explícitamente. Ten en
cuenta que, a menos que se especifique "ALL", el uso de esta opción deshabilitará cualquier
algoritmo que no se mencione explícitamente en la lista proporcionada.

Ejemplos:

```shell
# Enable only AES GCM encrypting algorithms
jwt.decrypt_enc_list A128GCM:A192GCM:A256GCM
```

<a id="entry-3-1-key-base"></a>

**`key-base <dir>`**

```haproxy
key-base <dir>
```

Asigna un directorio por defecto del que obtener claves privadas SSL cuando se usa una ruta
relativa con directivas "key". Las ubicaciones absolutas especificadas prevalecen e ignoran
"key-base". Esta opción solo funciona con una línea load de crt-store.

<a id="entry-3-1-limited-quic"></a>

**`limited-quic`**

```haproxy
limited-quic
```

Este ajuste debe usarse para habilitar explícitamente las vinculaciones del listener QUIC cuando
haproxy se compila con una versión de OpenSSL sin soporte QUIC. Activa una capa de compatibilidad
interna de haproxy que debe haberse seleccionado en tiempo de compilación con
USE_QUIC_OPENSSL_COMPAT=1. Esta capa de compatibilidad soporta la mayoría de las operaciones TLS
necesarias, aunque sin la capacidad QUIC 0-RTT.

Esta función está destinada principalmente a OpenSSL anterior a la versión 3.5.2, donde la API QUIC
no estaba implementada o lo estaba solo parcialmente. La capa de compatibilidad puede activarse
igualmente para la versión 3.5.2 y posteriores, pero probablemente sea innecesario.

Si limited-quic está establecido pero la capa de compatibilidad no fue seleccionada en tiempo de
compilación, la opción se ignora silenciosamente y las operaciones TLS de QUIC dependen de la
biblioteca TLS.

<a id="entry-3-1-localpeer"></a>

**`localpeer <name>`**

```haproxy
localpeer <name>
```

Establece el nombre de par (peer) de la instancia local. Se ignorará si se especifica el argumento
de línea de comandos "-L" o si se usa después de las definiciones de secciones "peers". En tales
casos, se emitirá un mensaje de advertencia durante el análisis de la configuración.

Esta opción también establecerá la variable de entorno HAPROXY_LOCALPEER. Ver también "-L" en la
guía de gestión y la sección "peers" más abajo.

<a id="entry-3-1-log"></a>

**`log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]`**

```haproxy
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    [profile <prof>] <facility> [max level [min level]]
```

Añade un servidor syslog global. Pueden definirse varios servidores globales. Recibirán los
registros de arranques y salidas, así como todos los registros de los proxies configurados con
"log global". Ver la opción "log" para proxies para más detalles.

<a id="entry-3-1-log-send-hostname"></a>

**`log-send-hostname [<string>]`**

```haproxy
log-send-hostname [<string>]
```

Establece el campo de nombre de host en la cabecera syslog. Si se establece el parámetro opcional
"string", la cabecera se establece al contenido de la cadena; de lo contrario, usa el nombre de
host del sistema. Generalmente se usa si no se retransmiten registros a través de un servidor syslog
intermedio o simplemente para personalizar el nombre de host impreso en los registros.

<a id="entry-3-1-log-tag"></a>

**`log-tag <string>`**

```haproxy
log-tag <string>
```

Establece el campo de etiqueta en la cabecera syslog a esta cadena. Por defecto es el nombre del
programa tal como se lanzó desde la línea de comandos, que normalmente es "haproxy". A veces puede
ser útil para diferenciar entre múltiples procesos ejecutándose en el mismo host. Ver también la
directiva "log-tag" por proxy.

<a id="entry-3-1-lua-load"></a>

**`lua-load <file> [ <arg1> [ <arg2> [ ... ] ] ]`**

```haproxy
lua-load <file> [ <arg1> [ <arg2> [ ... ] ] ]
```

Esta directiva global carga y ejecuta un archivo Lua en el contexto compartido que es visible para
todos los hilos. Cualquier variable establecida en dicho contexto es visible desde cualquier hilo.
Esta es la forma más sencilla y recomendada de cargar programas Lua, pero no escalará bien si se
realizan muchas llamadas Lua, ya que solo un hilo puede ejecutarse sobre el estado global a la vez.
Un programa cargado de esta forma siempre verá 0 en la variable "core.thread". Esta directiva puede
usarse múltiples veces.

Los args están disponibles en el archivo lua usando el código siguiente en el cuerpo del archivo.
No olvides que los arrays Lua comienzan en el índice 1. Una variable "local" declarada en un
archivo está disponible en todo el archivo y no está disponible en otros archivos.

     local args = table.pack(...)

<a id="entry-3-1-lua-load-per-thread"></a>

**`lua-load-per-thread <file> [ <arg1> [ <arg2> [ ... ] ] ]`**

```haproxy
lua-load-per-thread <file> [ <arg1> [ <arg2> [ ... ] ] ]
```

Esta directiva global carga y ejecuta un archivo Lua en cada hilo iniciado. Cualquier variable
global tiene una visibilidad local al hilo, de modo que cada hilo podría ver un valor diferente.
Por ello, es fuertemente recomendable no usar variables globales en programas cargados de esta
forma. Se carga e inicializa una copia independiente para cada hilo; todo se hace secuencialmente y
en el orden numérico de los hilos, de 1 a nbthread. Si algunas operaciones deben realizarse solo
una vez, el programa debería comprobar la variable "core.thread" para averiguar qué hilo se está
inicializando. Los programas cargados de esta forma se ejecutarán concurrentemente en todos los
hilos y serán altamente escalables. Esta es la forma recomendada de cargar funciones simples que
registran sample-fetches, conversores, acciones o servicios una vez que se tiene la certeza de que
el programa no depende de variables globales. Por simplicidad, la directiva está disponible incluso
si solo se usa un hilo e incluso si los hilos están deshabilitados (en cuyo caso será equivalente a
lua-load). Esta directiva puede usarse múltiples veces.

Ver lua-load para el uso de los args.

<a id="entry-3-1-lua-prepend-path"></a>

**`lua-prepend-path <string> [<type>]`**

```haproxy
lua-prepend-path <string> [<type>]
```

Antepone la cadena dada seguida de un punto y coma a la variable package.`<type>` de Lua. `<type>`
debe ser "path" o "cpath". Si no se da `<type>`, por defecto es "path".

Las rutas de Lua son listas de patrones delimitadas por punto y coma que especifican cómo intenta
la función `require` encontrar el archivo fuente de una biblioteca. Los signos de interrogación (?)
dentro de un patrón se sustituirán por el nombre del módulo. La ruta se evalúa de izquierda a
derecha. Esto implica que las rutas que se anteponen más tarde se comprobarán antes.

Como ejemplo, al especificar la siguiente ruta:

```text
lua-prepend-path /usr/share/haproxy-lua/?/init.lua
lua-prepend-path /usr/share/haproxy-lua/?.lua
```

Cuando se llama a `require "example"`, Lua intentará primero cargar el script
/usr/share/haproxy-lua/example.lua; si este no existe, se intentará /usr/share/haproxy-lua/example/init.lua
y, si tampoco existe, las rutas por defecto.

Ver <https://www.lua.org/pil/8.1.html> para los detalles en la documentación de Lua.

<a id="entry-3-1-master-worker"></a>

**`master-worker (deprecated)`**

```haproxy
master-worker (deprecated)
```

Modo master-worker. Es equivalente al argumento "-W" de la línea de comandos.

Esta palabra clave está obsoleta; inicia el modo master-worker usando "-W" o "-Ws".

Este modo lanzará un "master" que bifurcará un "worker" tras leer la configuración para procesar el
tráfico. El master se usa como gestor de procesos que monitorizará los "workers".

Usando este modo, puedes recargar HAProxy directamente enviando una señal SIGUSR2 al master. La
recarga pedirá al master que lea la configuración de nuevo y que bifurque un worker nuevo. El
worker anterior se mantendrá hasta el final de sus trabajos.

El modo master-worker es compatible tanto con el modo de primer plano como con el modo demonio.

Por defecto, si un worker termina con un código de retorno erróneo, en caso de un segfault por
ejemplo, todos los workers serán eliminados y el master se marchará. Es práctico combinar este
comportamiento con Restart=on-failure en un archivo de unidad systemd para relanzar todo el
proceso. Si no quieres este comportamiento, debes usar la palabra clave "no-exit-on-failure".

Ver también "-W" en la guía de gestión.

<a id="entry-3-1-master-worker-no-exit-on-failure"></a>

**`master-worker no-exit-on-failure`**

```haproxy
master-worker no-exit-on-failure
```

En modo master-worker, por defecto, si un worker termina con un código de retorno erróneo, en caso
de un segfault por ejemplo, todos los workers serán eliminados y el master se marchará. Es práctico
combinar este comportamiento con Restart=on-failure en un archivo de unidad systemd para relanzar
todo el proceso.

Esta palabra clave permite mantener vivos los procesos restantes cuando un worker ha fallado, en
lugar de eliminarlo todo. Debe usarse con precaución, ya que solo está pensada para depuración y
podría dejar el proceso master en un estado anormal.

<a id="entry-3-1-max-threads-per-group"></a>

**`max-threads-per-group <number>`**

```haproxy
max-threads-per-group <number>
```

Define el número máximo de hilos en un grupo de hilos. A menos que el número de grupos de hilos
esté fijado con la directiva "thread-groups", haproxy creará tantos grupos de hilos como sea
necesario para satisfacer el número de hilos solicitado. El valor mínimo es 1 y el máximo es 64 (en
sistemas de 64 bits, o 32 en sistemas de 32 bits). Los valores más bajos reducen la contención
causada por operaciones atómicas sobre estados compartidos, pero pueden aumentar el número de
sockets necesarios para crear todos los listeners y mantener conexiones backend inactivas. Los
valores más altos reducirán estos costes, a expensas de un mayor uso de CPU en situaciones de
contención y menores tasas de conexión. El valor por defecto es 16, que proporciona el mejor
equilibrio encontrado experimentalmente en varios sistemas probados, incluyendo procesadores
x86_64 de múltiples fabricantes y grandes sistemas Arm64, tanto en hardware físico como en hipervisores.

<a id="entry-3-1-mworker-max-reloads"></a>

**`mworker-max-reloads <number>`**

```haproxy
mworker-max-reloads <number>
```

En modo master-worker, esta opción limita el número de veces que un worker puede sobrevivir a una
recarga. Si el worker no se fue tras una recarga, una vez que su número de recargas sea mayor que
este número, el worker recibirá un SIGTERM. Esta opción ayuda a mantener bajo control el número de
workers. Ver también "show proc" en la guía de gestión.

Por defecto este valor está establecido a 50.

<a id="entry-3-1-nbthread"></a>

**`nbthread <number>`**

```haproxy
nbthread <number>
```

Este ajuste solo está disponible cuando se compiló con soporte de hilos. Hace que HAProxy se
ejecute en `<number>` hilos. "nbthread" también funciona cuando HAProxy se inicia en primer plano.
En algunas plataformas con soporte de afinidad de CPU, el valor por defecto de "nbthread" se
establece automáticamente al número de CPU a las que el proceso está vinculado al arrancar. Esto
significa que el número de hilos puede ajustarse fácilmente desde el proceso que lo llama usando
comandos como "taskset" o "cpuset". De lo contrario, este valor por defecto es 1. El valor por
defecto se informa en la salida de "haproxy -vv". Ten en cuenta que los valores establecidos aquí o
detectados automáticamente están sujetos al límite establecido por "thread-hard-limit" (si está
establecido).

<a id="entry-3-1-numa-cpu-mapping"></a>

**`numa-cpu-mapping`**

```haproxy
numa-cpu-mapping
```

Al ejecutarse en una plataforma con reconocimiento de NUMA, esto habilita que la directiva "cpu-policy"
inspeccione la topología y determine el mejor conjunto de CPU a usar y el número de hilos
correspondiente. Sin embargo, si la vinculación aplicada no es óptima en una arquitectura
particular, puede desactivarse con la declaración 'no numa-cpu-mapping'. Esta vinculación
automática tampoco se aplica si hay una declaración 'nbthread' en la configuración, si la afinidad
del proceso ya está especificada, por ejemplo mediante la directiva 'cpu-map' o la utilidad
taskset, o si cpu-policy está establecido a cualquier otro valor. Ver también "cpu-map",
"cpu-policy", "cpu-set".

<a id="entry-3-1-ocsp-update-disable"></a>

**`ocsp-update.disable [ on | off ]`**

```haproxy
ocsp-update.disable [ on | off ]
```

Desactiva completamente el ocsp-update en HAProxy. Cualquier configuración de ocsp-update será
ignorada. Por defecto es "off". Ver la opción "ocsp-update" para más información sobre el mecanismo
de actualización automática.

<a id="entry-3-1-ocsp-update-httpproxy"></a>

**`ocsp-update.httpproxy <address>[:port]`**

```haproxy
ocsp-update.httpproxy <address>[:port]
```

Permite usar un proxy HTTP para las actualizaciones OCSP. Esto solo funciona con HTTP; HTTPS no
está soportado. Esta opción permitirá al actualizador OCSP enviar URI absolutas en la solicitud al
proxy.

<a id="entry-3-1-ocsp-update-maxdelay"></a>

**`ocsp-update.maxdelay <number>`**

```haproxy
ocsp-update.maxdelay <number>
tune.ssl.ocsp-update.maxdelay <number> (deprecated)
```

Establece el intervalo máximo entre dos actualizaciones automáticas de la misma respuesta OCSP.
Este tiempo se expresa en segundos y por defecto es 3600 (1 hora). Debe establecerse a un valor
mayor que "ocsp-update.mindelay". Ver la opción "ocsp-update" para más información sobre el
mecanismo de actualización automática.

<a id="entry-3-1-ocsp-update-mindelay"></a>

**`ocsp-update.mindelay <number>`**

```haproxy
ocsp-update.mindelay <number>
tune.ssl.ocsp-update.mindelay <number> (deprecated)
```

Establece el intervalo mínimo entre dos actualizaciones automáticas de la misma respuesta OCSP.
Este tiempo se expresa en segundos y por defecto es 300 (5 minutos). Es particularmente útil para
respuestas OCSP que no tienen tiempos de expiración explícitos. Debe establecerse a un valor menor
que "ocsp-update.maxdelay". Ver la opción "ocsp-update" para más información sobre el mecanismo de
actualización automática.

<a id="entry-3-1-ocsp-update-mode"></a>

**`ocsp-update.mode [ on | off ]`**

```haproxy
ocsp-update.mode [ on | off ]
```

Establece el modo ocsp-update por defecto para todos los certificados usados en la configuración.
Esta opción global puede ser sustituida por la opción "ocsp-update" de crt-list. Esta opción está
establecida a "off" por defecto. Ver la opción "ocsp-update" para más información sobre el
mecanismo de actualización automática.

<a id="entry-3-1-pidfile"></a>

**`pidfile <pidfile>`**

```haproxy
pidfile <pidfile>
```

Escribe los PID de todos los demonios en el archivo `<pidfile>` en modo demonio, o escribe el PID
del proceso master en el archivo `<pidfile>` en modo master-worker. Esta opción es equivalente al
argumento de línea de comandos "-p". El archivo debe ser accesible para el usuario que inicia el
proceso. Ver también "daemon" y "master-worker".

<a id="entry-3-1-pp2-never-send-local"></a>

**`pp2-never-send-local`**

```haproxy
pp2-never-send-local
```

Un error en la implementación del protocolo PROXY v2 estuvo presente en HAProxy hasta la versión
2.1, haciendo que emitiera un comando PROXY en lugar de un comando LOCAL para las comprobaciones de
salud. Esto es particularmente menor, pero confunde los registros de algunos servidores.
Lamentablemente, el error se descubrió muy tarde y reveló que algunos servidores que posiblemente
solo probaron su implementación del protocolo PROXY contra HAProxy fallan al manejar correctamente
el comando LOCAL y permanecen permanentemente en estado "down" cuando HAProxy los comprueba.
Cuando esto ocurre, es posible habilitar esta opción global para revertir al comportamiento
anterior (defectuoso) durante el tiempo que toma contactar con los proveedores de los componentes
afectados y conseguir que lo corrijan. Esta opción está deshabilitada por defecto y actúa sobre
todos los servidores que tienen la declaración "send-proxy-v2".

<a id="entry-3-1-presetenv"></a>

**`presetenv <name> <value>`**

```haproxy
presetenv <name> <value>
```

Establece la variable de entorno `<name>` al valor `<value>`. Si la variable existe, NO se
sobrescribe. Los cambios surten efecto inmediatamente, de modo que la siguiente línea del archivo
de configuración ve el nuevo valor. Ver también "setenv", "resetenv" y "unsetenv".

<a id="entry-3-1-prealloc-fd"></a>

**`prealloc-fd`**

```haproxy
prealloc-fd
```

Realiza una apertura única del descriptor de archivo máximo, lo que resulta en una preasignación de
las estructuras de datos del kernel. Esto evita pausas cortas cuando nbthread\>1 y HAProxy abre un
descriptor de archivo que requiere que el kernel expanda sus estructuras de datos.

<a id="entry-3-1-resetenv"></a>

**`resetenv [<name> ...]`**

```haproxy
resetenv [<name> ...]
```

Elimina todas las variables de entorno excepto las especificadas en el argumento. Permite usar un
entorno limpio y controlado antes de establecer nuevos valores con setenv o unsetenv. Ten en cuenta
que algunas funciones internas pueden hacer uso de algunas variables de entorno, como las funciones
de manipulación de tiempo, pero también OpenSSL o incluso las comprobaciones externas. Debe usarse
con extremo cuidado y solo tras una validación completa. Los cambios surten efecto inmediatamente,
de modo que la siguiente línea del archivo de configuración ve el nuevo entorno. Ver también
"setenv", "presetenv" y "unsetenv".

<a id="entry-3-1-server-state-base"></a>

**`server-state-base <directory>`**

```haproxy
server-state-base <directory>
```

Especifica el prefijo de directorio que se antepondrá a todos los nombres de archivo de estado de
servidores que no comiencen por '/'. Ver también "server-state-file",
"load-server-state-from-file" y "server-state-file-name".

<a id="entry-3-1-server-state-file"></a>

**`server-state-file <file>`**

```haproxy
server-state-file <file>
```

Especifica la ruta al archivo que contiene el estado de los servidores. Si la ruta comienza con una
barra ('/'), se considera absoluta; de lo contrario, se considera relativa al directorio
especificado con "server-state-base" (si está establecido) o al directorio actual. Antes de
recargar HAProxy, es posible guardar el estado actual de los servidores usando el comando de
estadísticas "show servers state". La salida de este comando debe escribirse en el archivo señalado
por `<file>`. Al arrancar, antes de gestionar el tráfico, HAProxy leerá, cargará y aplicará el
estado de cada servidor encontrado en el archivo y disponible en su configuración en ejecución
actual. Ver también "server-state-base" y "show servers state", "load-server-state-from-file" y
"server-state-file-name"

<a id="entry-3-1-set-dumpable"></a>

**`set-dumpable [ on | off | libs ]`**

```haproxy
set-dumpable [ on | off | libs ]
```

Esta opción ayuda a elegir el comportamiento del volcado de núcleo (core dump) en caso de fallo del
proceso. Las opciones disponibles son:

- on habilita el volcado de núcleo a nivel de proceso si estaba previamente deshabilitado.

- off deshabilita un volcado de núcleo habilitado previamente.

- libs habilita el volcado de núcleo con una copia embebida de los binarios y bibliotecas que son
  necesarios para la depuración. Los desarrolladores pueden solicitarlo. En este caso, haproxy
  intentará cargar en memoria las bibliotecas de las que depende y conservarlas con celo. Si el
  proceso falla, se volcarán en el core, por lo que ya no hace falta recuperarlas del sistema de
  archivos y no hay riesgo de que no coincidan con el core. Esto ocupa desde unos pocos megabytes
  hasta unas decenas de megabytes de RAM adicional, así que es mejor no usarlo en sistemas
  pequeños.

Esta opción es mejor dejarla deshabilitada por defecto y habilitarla solo a petición de un
desarrollador. Por defecto está deshabilitada. Sin argumento, su valor por defecto es "on". Si se
ha habilitado, aún puede forzarse su deshabilitación prefijándola con la palabra clave "no" o
estableciéndola a "off". No tiene impacto en el rendimiento ni en la estabilidad, pero intentará
con empeño reactivar los volcados de núcleo que posiblemente fueron deshabilitados por limitaciones
de tamaño de archivo (ulimit -f), limitaciones de tamaño del core (ulimit -c) o por la
"volcabilidad" (dumpability) de un proceso tras cambiar su UID/GID (como
/proc/sys/fs/suid_dumpable en Linux). Los volcados de núcleo podrían seguir limitados por los
permisos del directorio actual (comprueba desde qué directorio se inicia el archivo), el permiso
del directorio chroot (puede ser necesario deshabilitar temporalmente la directiva chroot o
moverla a una ubicación dedicada escribible) o cualquier otra restricción específica del sistema.
Por ejemplo, algunas distribuciones de Linux son conocidas por sustituir el archivo core por
defecto por una ruta a un ejecutable que ni siquiera está instalado en el sistema (comprueba
/proc/sys/kernel/core_pattern). A menudo, basta con escribir "core", "core.%p" o
"/var/log/core/core.%p" para resolver el problema. Al intentar habilitar esta opción esperando que
reaparezca un problema raro, a menudo es buena idea intentar primero obtener dicho volcado
emitiendo, por ejemplo, un "kill -11" al proceso "haproxy" y comprobar que deja un core donde se
espera al morir.

<a id="entry-3-1-set-var"></a>

**`set-var <var-name> <expr>`**

```haproxy
set-var <var-name> <expr>
```

Establece la variable de proceso '`<var-name>`' al resultado de la evaluación de la expresión de
muestra `<expr>`. La variable '`<var-name>`' solo puede ser una variable de proceso (usando el
prefijo 'proc.'). Funciona exactamente como la acción 'set-var' en las reglas TCP o HTTP, excepto
en que la expresión se evalúa en el momento del análisis de la configuración y en que la variable
se establece al instante. Las funciones de obtención de muestras y conversores permitidos en la
expresión son solo los que usan datos internos, típicamente 'int(value)' o 'str(value)'. También es
posible referenciar variables previamente asignadas. Estas variables serán entonces legibles (y
modificables) desde los conjuntos de reglas habituales.

Ejemplo:

```text
global
    set-var proc.current_state str(primary)
    set-var proc.prio int(100)
    set-var proc.threshold int(200),sub(proc.prio)
```

<a id="entry-3-1-set-var-fmt"></a>

**`set-var-fmt <var-name> <fmt>`**

```haproxy
set-var-fmt <var-name> <fmt>
```

Establece la variable de proceso '`<var-name>`' a la cadena resultante de la evaluación del
log-format `<fmt>`. La variable '`<var-name>`' solo puede ser una variable de proceso (usando el
prefijo 'proc.'). Funciona exactamente como la acción 'set-var-fmt' en las reglas TCP o HTTP,
excepto en que la expresión se evalúa en el momento del análisis de la configuración y en que la
variable se establece al instante. Las funciones de obtención de muestras y conversores permitidos
en la expresión son solo los que usan datos internos, típicamente 'int(value)' o 'str(value)'.
También es posible referenciar variables previamente asignadas. Estas variables serán entonces
legibles (y modificables) desde los conjuntos de reglas habituales. Ver la [sección
8.2.6](/es/haproxy/configuration-logging/#section-8-2-6) para los detalles sobre la sintaxis del
formato de registro personalizado.

Ejemplo:

```text
global
    set-var-fmt proc.current_state "primary"
    set-var-fmt proc.bootid        "%pid|%t"
```

<a id="entry-3-1-setcap"></a>

**`setcap <name>[,<name>...]`**

```haproxy
setcap <name>[,<name>...]
```

Establece una lista de capacidades que deben conservarse al iniciar y ejecutar bien como usuario no
root (uid \> 0), o al iniciar con uid 0 (root) y cambiar después a un usuario no root. Por defecto,
todos los permisos se pierden con el cambio de uid, pero a menudo se necesitan algunos al intentar
conectarse a un servidor desde una dirección externa durante el proxy transparente, o al vincularse
a un puerto por debajo de 1024, p. ej. al usar "tune.quic.fe.sock-per-conn default-on", lo que da
lugar a configuraciones que se ejecutan enteramente bajo uid 0. Establecer capacidades
generalmente es una alternativa más segura, ya que solo se conservarán las capacidades requeridas.
La función es específica del sistema operativo y solo se habilita en Linux cuando
USE_LINUX_CAP=1 está establecido en tiempo de compilación. La lista de capacidades soportadas
también depende del sistema operativo y está enumerada en el mensaje de error que se muestra
cuando se pasa un nombre de capacidad no válido o vacío. Pueden pasarse múltiples capacidades,
delimitadas por comas. Entre las usadas comúnmente, "cap_net_raw" permite vincularse de forma
transparente a una dirección externa, y "cap_net_bind_service" permite vincularse a un puerto
privilegiado y puede ser usada por QUIC. Si el proceso se inicia y ejecuta bajo el mismo usuario
no root, las capacidades necesarias deben establecerse en el archivo binario de haproxy con setcap
junto con esta palabra clave. Para más detalles sobre el establecimiento de capacidades en el
binario de haproxy, ver el capítulo 13.1 Soporte de capacidades de Linux en la guía de gestión.

Ejemplo:

```text
global
    setcap cap_net_bind_service,cap_net_admin
```

<a id="entry-3-1-setenv"></a>

**`setenv <name> <value>`**

```haproxy
setenv <name> <value>
```

Establece la variable de entorno `<name>` al valor `<value>`. Si la variable existe, se
sobrescribe. Los cambios surten efecto inmediatamente, de modo que la siguiente línea del archivo
de configuración ve el nuevo valor. Ver también "presetenv", "resetenv" y "unsetenv".

<a id="entry-3-1-shm-stats-file"></a>

**`shm-stats-file <name>`**

```haproxy
shm-stats-file <name>
```

Cuando esta directiva está establecida, habilita el uso de memoria compartida para almacenar los
contadores de estadísticas. `<name>` se usa como argumento de shm_open() para abrir la memoria
compartida en una ubicación única. Esto también significa que la directiva solo está disponible en
sistemas que soportan shm_open(). Cuando se usa SHM para las estadísticas, todos los contadores que pueden compartirse de frontends, backends, listeners y servidores se almacenarán en la SHM,
siempre que tengan un GUID establecido. Al recargar haproxy, el nuevo proceso intentará escanear
la SHM en busca de objetos que puedan asociarse a objetos definidos en la configuración basándose
en el GUID y el tipo; el objetivo es poder conservar algunos valores de contadores tras la recarga.
Por otro lado, cuando haproxy se detiene correctamente, los objetos de la SHM se liberan, lo que
significa que los contadores se reinician efectivamente. También es posible eliminar manualmente el
archivo antes de iniciar un proceso nuevo para forzar el restablecimiento de los contadores.

Ver también "guid", "guid-prefix" y "shm-stats-file-max-objects"

<a id="entry-3-1-shm-stats-file-max-objects"></a>

**`shm-stats-file-max-objects <number>`**

```haproxy
shm-stats-file-max-objects <number>
```

Este ajuste define el número máximo de objetos que la memoria compartida usada para contadores
compartidos podrá almacenar por grupo de hilos. Está directamente relacionado con el tamaño máximo
de memoria del shm y se usa para "premapear" el shm a un tamaño dado para evitar el remapeo en
tiempo de ejecución. Por defecto es 2k, lo que debería bastar para la mayoría de configuraciones
sin arriesgar un uso de memoria inadecuado, pero puede cambiarse fácilmente si es necesario.
haproxy se quejará durante el arranque si este valor es demasiado bajo para registrar objetos que
se espera que se almacenen en la memoria compartida. Solo es relevante cuando se definió
"shm-stats-file".

Ver también "thread-groups"

<a id="entry-3-1-ssl-default-bind-ciphers"></a>

**`ssl-default-bind-ciphers <ciphers>`**

```haproxy
ssl-default-bind-ciphers <ciphers>
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL. Establece la cadena por
defecto que describe la lista de algoritmos de cifrado ("cipher suite") que se negocian durante el
handshake SSL/TLS hasta TLSv1.2 para todas las líneas "bind" que no definan explícitamente las
suyas. El formato de la cadena está definido en "man 1 ciphers" de las páginas de manual de
OpenSSL. Para información de contexto y recomendaciones, ver p. ej.
(<https://wiki.mozilla.org/Security/Server_Side_TLS>) y
(<https://mozilla.github.io/server-side-tls/ssl-config-generator/>). Para la configuración de
cifrados de TLSv1.3, comprueba la palabra clave "ssl-default-bind-ciphersuites". Comprueba la
palabra clave "bind" para más información.

<a id="entry-3-1-ssl-default-bind-ciphersuites"></a>

**`ssl-default-bind-ciphersuites <ciphersuites>`**

```haproxy
ssl-default-bind-ciphersuites <ciphersuites>
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL y se usó OpenSSL 1.1.1 o
posterior para compilar HAProxy. Establece la cadena por defecto que describe la lista de
algoritmos de cifrado ("cipher suite") que se negocian durante el handshake TLSv1.3 para todas las
líneas "bind" que no definan explícitamente las suyas. El formato de la cadena está definido en
"man 1 ciphers" de las páginas de manual de OpenSSL, en la sección "ciphersuites". Para la
configuración de cifrados de TLSv1.2 y anteriores, comprueba la palabra clave
"ssl-default-bind-ciphers". Este ajuste podría aceptar ciphersuites de TLSv1.2; sin embargo, este
es un comportamiento no documentado y no recomendado, ya que podría ser inconsistente o
defectuoso. Los ciphersuites TLSv1.3 por defecto de OpenSSL son:
"TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256"

TLSv1.3 solo soporta 5 ciphersuites:

- TLS_AES_128_GCM_SHA256
- TLS_AES_256_GCM_SHA384
- TLS_CHACHA20_POLY1305_SHA256
- TLS_AES_128_CCM_SHA256
- TLS_AES_128_CCM_8_SHA256

Comprueba la palabra clave "bind" para más información.

Ejemplo:

```text
global
    ssl-default-bind-ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-RSA-AES128-GCM-SHA256
    ssl-default-bind-ciphersuites TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256
```

<a id="entry-3-1-ssl-default-bind-client-sigalgs"></a>

**`ssl-default-bind-client-sigalgs <sigalgs>`**

```haproxy
ssl-default-bind-client-sigalgs <sigalgs>
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL. Establece la cadena por
defecto que describe la lista de algoritmos de firma relacionados con la autenticación de cliente
para todas las líneas "bind" que no definan explícitamente las suyas. El formato de la cadena es
una lista de algoritmos de firma delimitada por dos puntos. Cada algoritmo de firma puede usar una
de dos formas: nombres de esquemas de firma de TLS1.3 ("rsa_pss_rsae_sha256") o la forma
algoritmo de clave pública + resumen ("ECDSA+SHA256"). Una lista puede contener ambas formas. Para
más información sobre el formato, ver SSL_CTX_set1_client_sigalgs(3). Una lista de algoritmos de
firma también está disponible en RFC8446 [sección
4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3) y en OpenSSL en el archivo
ssl/t1_lib.c. Este ajuste no es aplicable a TLSv1.1 y versiones anteriores del protocolo, ya que
los algoritmos de firma no se negocian por separado en estas versiones. No se recomienda cambiar
este ajuste a menos que se requiera compatibilidad con un middlebox.

<a id="entry-3-1-ssl-default-bind-curves"></a>

**`ssl-default-bind-curves <curves>`**

```haproxy
ssl-default-bind-curves <curves>
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL. Establece la cadena por
defecto que describe la lista de algoritmos de curvas elípticas ("curve suite") que se negocian
durante el handshake SSL/TLS con ECDHE. El formato de la cadena es una lista de nombres de curvas
delimitada por dos puntos. Comprueba la palabra clave "bind" para más información.

<a id="entry-3-1-ssl-default-bind-options"></a>

**`ssl-default-bind-options [<option>]...`**

```haproxy
ssl-default-bind-options [<option>]...
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL. Establece las
ssl-options por defecto que imponer en todas las líneas "bind". Comprueba la palabra clave "bind"
para ver las opciones disponibles.

Ejemplo:

```text
global
   ssl-default-bind-options ssl-min-ver TLSv1.0 no-tls-tickets
```

<a id="entry-3-1-ssl-default-bind-sigalgs"></a>

**`ssl-default-bind-sigalgs <sigalgs>`**

```haproxy
ssl-default-bind-sigalgs <sigalgs>
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL. Establece la cadena por
defecto que describe la lista de algoritmos de firma que se negocian durante el handshake TLSv1.2 y
TLSv1.3 para todas las líneas "bind" que no definan explícitamente las suyas. El formato de la
cadena es una lista de algoritmos de firma delimitada por dos puntos. Cada algoritmo de firma
puede usar una de dos formas: nombres de esquemas de firma de TLS1.3 ("rsa_pss_rsae_sha256") o la
forma algoritmo de clave pública + resumen ("ECDSA+SHA256"). Una lista puede contener ambas
formas. Para más información sobre el formato, ver SSL_CTX_set1_sigalgs(3). Una lista de
algoritmos de firma también está disponible en RFC8446 [sección 4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3)
y en OpenSSL en el archivo ssl/t1_lib.c. Este ajuste no es aplicable a TLSv1.1 y versiones
anteriores del protocolo, ya que los algoritmos de firma no se negocian por separado en estas
versiones. No se recomienda cambiar este ajuste a menos que se requiera compatibilidad con un
middlebox.

<a id="entry-3-1-ssl-default-server-ciphers"></a>

**`ssl-default-server-ciphers <ciphers>`**

```haproxy
ssl-default-server-ciphers <ciphers>
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL. Establece la cadena por
defecto que describe la lista de algoritmos de cifrado que se negocian durante el handshake SSL/TLS
hasta TLSv1.2 con el servidor, para todas las líneas "server" que no definan explícitamente las
suyas. El formato de la cadena está definido en "man 1 ciphers" de las páginas de manual de
OpenSSL. Para información de contexto y recomendaciones, ver p. ej.
(<https://wiki.mozilla.org/Security/Server_Side_TLS>) y
(<https://mozilla.github.io/server-side-tls/ssl-config-generator/>). Para la configuración de
cifrados de TLSv1.3, comprueba la palabra clave "ssl-default-server-ciphersuites". Comprueba la
palabra clave "server" para más información.

<a id="entry-3-1-ssl-default-server-ciphersuites"></a>

**`ssl-default-server-ciphersuites <ciphersuites>`**

```haproxy
ssl-default-server-ciphersuites <ciphersuites>
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL y se usó OpenSSL 1.1.1 o
posterior para compilar HAProxy. Establece la cadena por defecto que describe la lista de
algoritmos de cifrado que se negocian durante el handshake TLSv1.3 con el servidor, para todas las
líneas "server" que no definan explícitamente las suyas. El formato de la cadena está definido en
"man 1 ciphers" de las páginas de manual de OpenSSL, en la sección "ciphersuites". Para la
configuración de cifrados de TLSv1.2 y anteriores, comprueba la palabra clave
"ssl-default-server-ciphers". Comprueba la palabra clave "server" para más información.

<a id="entry-3-1-ssl-default-server-client-sigalgs"></a>

**`ssl-default-server-client-sigalgs <sigalgs>`**

```haproxy
ssl-default-server-client-sigalgs <sigalgs>
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL. Establece la cadena por
defecto que describe la lista de algoritmos de firma relacionados con la autenticación de cliente
para todas las líneas "server" que no definan explícitamente las suyas. El formato de la cadena es
una lista de algoritmos de firma delimitada por dos puntos. Cada algoritmo de firma puede usar una
de dos formas: nombres de esquemas de firma de TLS1.3 ("rsa_pss_rsae_sha256") o la forma
algoritmo de clave pública + resumen ("ECDSA+SHA256"). Una lista puede contener ambas formas. Para
más información sobre el formato, ver SSL_CTX_set1_client_sigalgs(3). Una lista de algoritmos de
firma también está disponible en RFC8446 [sección
4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3) y en OpenSSL en el archivo
ssl/t1_lib.c. Este ajuste no es aplicable a TLSv1.1 y versiones anteriores del protocolo, ya que
los algoritmos de firma no se negocian por separado en estas versiones. No se recomienda cambiar
este ajuste a menos que se requiera compatibilidad con un middlebox.

<a id="entry-3-1-ssl-default-server-curves"></a>

**`ssl-default-server-curves <curves>`**

```haproxy
ssl-default-server-curves <curves>
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL. Establece la cadena por
defecto que describe la lista de algoritmos de curvas elípticas ("curve suite") que se negocian
durante el handshake SSL/TLS con ECDHE. El formato de la cadena es una lista de nombres de curvas
delimitada por dos puntos. Comprueba la palabra clave "server" para más información.

<a id="entry-3-1-ssl-default-server-options"></a>

**`ssl-default-server-options [<option>]...`**

```haproxy
ssl-default-server-options [<option>]...
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL. Establece las
ssl-options por defecto que imponer en todas las líneas "server". Comprueba la palabra clave
"server" para ver las opciones disponibles.

<a id="entry-3-1-ssl-default-server-sigalgs"></a>

**`ssl-default-server-sigalgs <sigalgs>`**

```haproxy
ssl-default-server-sigalgs <sigalgs>
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL. Establece la cadena por
defecto que describe la lista de algoritmos de firma que se negocian durante el handshake TLSv1.2 y
TLSv1.3 para todas las líneas "server" que no definan explícitamente las suyas. El formato de la
cadena es una lista de algoritmos de firma delimitada por dos puntos. Cada algoritmo de firma
puede usar una de dos formas: nombres de esquemas de firma de TLS1.3 ("rsa_pss_rsae_sha256") o la
forma algoritmo de clave pública + resumen ("ECDSA+SHA256"). Una lista puede contener ambas
formas. Para más información sobre el formato, ver SSL_CTX_set1_sigalgs(3). Una lista de
algoritmos de firma también está disponible en RFC8446 [sección 4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3)
y en OpenSSL en el archivo ssl/t1_lib.c. Este ajuste no es aplicable a TLSv1.1 y versiones
anteriores del protocolo, ya que los algoritmos de firma no se negocian por separado en estas
versiones. No se recomienda cambiar este ajuste a menos que se requiera compatibilidad con un
middlebox.

<a id="entry-3-1-ssl-dh-param-file"></a>

**`ssl-dh-param-file <file>`**

```haproxy
ssl-dh-param-file <file>
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL. Establece los parámetros
DH por defecto que se usan durante el handshake SSL/TLS cuando se usa el intercambio de claves
Diffie-Hellman efímero (DHE), para todas las líneas "bind" que no definan explícitamente los
suyos. Serán sustituidos por parámetros DH personalizados encontrados en un archivo de certificado
de bind, si los hay. Si no se especifican parámetros DH personalizados, ya sea usando
ssl-dh-param-file o estableciéndolos directamente en el archivo de certificado, no se usarán los
cifrados DHE, a menos que tune.ssl.default-dh-param esté establecido. En este último caso, se
usarán parámetros DH predefinidos del tamaño especificado. Se sabe que los parámetros
personalizados son más seguros y por tanto se recomienda su uso. Los parámetros DH personalizados
pueden generarse usando el comando de OpenSSL "openssl dhparam `<size>`", donde el tamaño debe ser
al menos 2048, ya que los parámetros DH de 1024 bits ya no deberían considerarse seguros.

Compatibilidad: OpenSSL >= 1.1.1. No compatible con AWS-LC.

<a id="entry-3-1-ssl-passphrase-cmd"></a>

**`ssl-passphrase-cmd <cmd> <args> ...`**

```haproxy
ssl-passphrase-cmd <cmd> <args> ...
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL. Permite definir una
línea de comandos completa que se llamará cuando se cargue un certificado cifrado durante el init.
El comando puede ser un script o cualquier otro programa. Se le proporcionará la ruta de la clave
privada cifrada como primer parámetro y después los parámetros "args" definidos por el usuario, y
debería volcar en la salida estándar la frase de contraseña que permite decodificar la clave
privada cifrada. Por cada nueva clave privada cifrada que se cargue durante el init, HAProxy
probará primero todas las demás frases de contraseña ya conocidas para decodificar la clave
privada y, en última instancia, llamará de nuevo al comando de frase de contraseña si ninguna
funciona.

<a id="entry-3-1-ssl-propquery"></a>

**`ssl-propquery <query>`**

```haproxy
ssl-propquery <query>
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL y cuando la versión de
OpenSSL es al menos 3.0. Permite definir una cadena de propiedades por defecto usada al obtener
algoritmos de los proveedores. Se comporta igual que la opción propquery de openssl y sigue la
misma sintaxis (descrita en
<https://www.openssl.org/docs/man3.0/man7/property.html>). Por ejemplo, si tienes dos proveedores
cargados, el foo y el predeterminado, el propquery "?provider=foo" permite elegir por defecto las
implementaciones de algoritmos proporcionadas por el proveedor foo, y recurrir a la del proveedor
predeterminado si no se encontró.

Compatibilidad: OpenSSL >= 3.0.0. No compatible con AWS-LC.

<a id="entry-3-1-ssl-provider"></a>

**`ssl-provider <name>`**

```haproxy
ssl-provider <name>
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL y cuando la versión de
OpenSSL es al menos 3.0. Permite cargar un proveedor durante el init. Si la carga tiene éxito,
cualquier capacidad proporcionada por el proveedor cargado podría ser usada por HAProxy. Pueden
especificarse múltiples opciones 'ssl-provider' en un archivo de configuración. Los proveedores se
cargarán en su orden de aparición.

Ten en cuenta que cargar un proveedor explícitamente impide que OpenSSL cargue automáticamente el
proveedor 'default'. OpenSSL también permite definir los proveedores que deben cargarse directamente
en su archivo de configuración (openssl.cnf por ejemplo), de modo que no es necesario usar esta
opción 'ssl-provider' para cargar proveedores. El comando de CLI "show ssl providers" puede usarse
para mostrar todos los proveedores que se cargaron con éxito.

La ruta de búsqueda por defecto de los proveedores de OpenSSL puede encontrarse en la salida del
comando "openssl version -a". Si el proveedor está en otro directorio, puedes establecer la
variable de entorno OPENSSL_MODULES, que toma el directorio donde puede encontrarse tu proveedor.

Ver también "ssl-propquery" y "ssl-provider-path".

Compatibilidad: OpenSSL >= 3.0.0. No compatible con AWS-LC.

<a id="entry-3-1-ssl-provider-path"></a>

**`ssl-provider-path <path>`**

```haproxy
ssl-provider-path <path>
```

Este ajuste solo está disponible cuando se compiló con soporte de OpenSSL y cuando la versión de
OpenSSL es al menos 3.0. Permite especificar la ruta de búsqueda que usará OpenSSL para buscar
proveedores. Se comporta igual que la variable de entorno OPENSSL_MODULES. Se usará para cualquier
opción 'ssl-provider' posterior o hasta que se defina un nuevo 'ssl-provider-path'. Ver también
"ssl-provider".

Compatibilidad: OpenSSL >= 3.0.0. No compatible con AWS-LC.

<a id="entry-3-1-ssl-load-extra-del-ext"></a>

**`ssl-load-extra-del-ext`**

```haproxy
ssl-load-extra-del-ext
```

Este ajuste permite configurar la forma en que HAProxy hace la búsqueda de los archivos SSL
adicionales. Por defecto, HAProxy añade una nueva extensión al nombre del archivo (p. ej.: con
"foobar.crt" carga "foobar.crt.key"). Con esta opción habilitada, HAProxy elimina la extensión
antes de añadir la nueva (p. ej.: con "foobar.crt" carga "foobar.key").

Tu archivo crt debe tener una extensión ".crt" para que esta opción funcione.

Esta opción no es compatible con las extensiones de bundle (.ecdsa, .rsa. .dsa) y no intentará
eliminarlas.

Esta opción está deshabilitada por defecto. Ver también "ssl-load-extra-files".

<a id="entry-3-1-ssl-load-extra-files"></a>

**`ssl-load-extra-files <none|all|bundle|sctl|ocsp|issuer|key>*`**

```haproxy
ssl-load-extra-files <none|all|bundle|sctl|ocsp|issuer|key>*
```

Este ajuste altera la forma en que HAProxy buscará los archivos no especificados durante la carga
de los certificados SSL. Esta opción se aplica a los certificados asociados a líneas "bind" así
como a líneas "server", pero algunos de los archivos adicionales no tendrán ningún impacto
funcional para los certificados de líneas "server".

Por defecto, HAProxy descubre automáticamente muchos archivos no especificados en la
configuración, y puedes querer desactivar este comportamiento si deseas optimizar el tiempo de
arranque.

"none": carga solo los archivos especificados en la configuración. No intenta cargar un bundle de
certificados si el archivo no existe. En el caso de un directorio, no intentará agrupar los
certificados si tienen el mismo nombre base.

"all": este es el comportamiento por defecto; intentará cargar todo: bundles, sctl, ocsp, issuer,
key.

"bundle": cuando un archivo especificado en la configuración no existe, HAProxy intentará cargar
un "cert bundle". Los bundles de certificados solo se gestionan en el lado del frontend y no
funcionarán para certificados de backend.

A partir de HAProxy 2.3, los bundles no se cargan en el mismo almacén de certificados de OpenSSL;
en su lugar, carga cada certificado en un almacén separado, lo que equivale a declarar múltiples
"crt". Se requiere OpenSSL 1.1.1 para lograrlo. Lo que significa que los bundles ahora se usan solo
por compatibilidad con versiones anteriores y ya no son obligatorios para hacer una configuración
bind híbrida RSA/ECC.

Para asociar estos archivos PEM en un "cert bundle" reconocido por HAProxy, deben nombrarse de la
siguiente manera: todos los archivos PEM que se van a agrupar deben tener el mismo nombre base,
con un sufijo que indique el tipo de clave. Actualmente se soportan tres sufijos: rsa, dsa y
ecdsa. Por ejemplo, si [www.example.com](http://www.example.com) tiene dos archivos PEM, uno RSA
y otro ECDSA, deben llamarse: "example.pem.rsa" y "example.pem.ecdsa". La primera parte del nombre
de archivo es arbitraria; solo importa el sufijo. Para cargar este bundle en HAProxy, especifica
únicamente el nombre base:

Ejemplo: bind :8443 ssl crt example.pem

Ten en cuenta que el sufijo no se da a HAProxy; esto le indica a HAProxy que busque un cert
bundle.

HAProxy cargará todos los archivos PEM del bundle como si estuvieran configurados por separado en
varios "crt".

La carga de bundles ya no tiene impacto en la carga de directorios, ya que los archivos se cargan
por separado.

En la CLI, los bundles se ven como archivos separados y se requiere la extensión del bundle para
confirmarlos.

Los archivos OCSP (.ocsp), los archivos de emisor (.issuer), la Transparencia de Certificados
(.sctl) así como las claves privadas (.key) están soportados con la agrupación multi-cert.

"sctl": intenta cargar "`<basename>`.sctl" por cada palabra clave crt. Si se proporciona para un
certificado de backend, se cargará pero no tendrá ningún impacto funcional.

"ocsp": intenta cargar "`<basename>`.ocsp" por cada palabra clave crt. Si se proporciona para un
certificado de backend, se cargará pero no tendrá ningún impacto funcional.

"issuer": intenta cargar "`<basename>`.issuer" si el emisor del archivo OCSP no está proporcionado
en el archivo PEM. Si se proporciona para un certificado de backend, se cargará pero no tendrá
ningún impacto funcional.

"key": si la clave privada no fue proporcionada por el archivo PEM, intenta cargar un archivo
"`<basename>`.key" que contenga una clave privada.

El comportamiento por defecto es "all".

Ejemplo:

```text
ssl-load-extra-files bundle sctl
ssl-load-extra-files sctl ocsp issuer
ssl-load-extra-files none
```

Ver también: "crt", la [sección 5.1](/es/haproxy/bind-and-server-options/#section-5-1) sobre las
opciones de bind y la [sección 5.2](/es/haproxy/bind-and-server-options/#section-5-2) sobre las
opciones de server.

<a id="entry-3-1-ssl-security-level"></a>

**`ssl-security-level <number>`**

```haproxy
ssl-security-level <number>
```

Esta directiva permite elegir el nivel de seguridad de OpenSSL como se describe en
<https://www.openssl.org/docs/man1.1.1/man3/SSL_CTX_set_security_level.html> El nivel de seguridad
se aplicará a todos los contextos SSL de HAProxy. Solo se soporta un valor entre 0 y 5.

El valor por defecto depende de tu versión de OpenSSL, de la distribución y de cómo fue compilada
la biblioteca.

Esta directiva requiere al menos OpenSSL 1.1.1.

Compatibilidad: OpenSSL >= 1.1.1. No compatible con AWS-LC.

<a id="entry-3-1-ssl-server-verify"></a>

**`ssl-server-verify [none|required]`**

```haproxy
ssl-server-verify [none|required]
```

El comportamiento por defecto de la verificación SSL en el lado de los servidores. Si se especifica
'none', los certificados de los servidores no se verifican. El valor por defecto es 'required'
salvo si se fuerza usando la opción de línea de comandos '-dV'.

<a id="entry-3-1-ssl-skip-self-issued-ca"></a>

**`ssl-skip-self-issued-ca`**

```haproxy
ssl-skip-self-issued-ca
```

Una CA autoemitida, también conocida como CA raíz x509, es el ancla de la validación de cadena:
dado que es inútil que un servidor la envíe, el cliente debe tenerla. La configuración estándar no
debe incluir dichas CA en el archivo PEM. Esta opción te permite mantener dichas CA en el archivo
PEM sin enviarlas al cliente. El caso de uso es proporcionar el emisor para ocsp sin necesidad del
archivo '.issuer' y poder compartirlo con 'issuers-chain-path'. Esto concierne a todos los
certificados sin certificados intermedios. Es inútil para BoringSSL; .issuer se ignora porque los
bits de ocsp no lo necesitan. Requiere al menos OpenSSL 1.0.2.

<a id="entry-3-1-stats-calculate-max-counters"></a>

**`stats calculate-max-counters [on|off]`**

```haproxy
stats calculate-max-counters [on|off]
```

Activa o desactiva el cálculo de los contadores máximos de estadísticas. Si no los necesitas,
desactivarlos puede aumentar un poco el rendimiento. El valor por defecto es on.

<a id="entry-3-1-stats-maxconn"></a>

**`stats maxconn <connections>`**

```haproxy
stats maxconn <connections>
```

Por defecto, el socket de estadísticas está limitado a 10 conexiones concurrentes. Es posible
cambiar este valor con "stats maxconn".

<a id="entry-3-1-stats-socket"></a>

**`stats socket [<address:port>|<path>] [param*]`**

```haproxy
stats socket [<address:port>|<path>] [param*]
```

Vincula un socket UNIX a `<path>` o una dirección TCPv4/v6 a `<address:port>`. Las conexiones a
este socket devolverán diversas salidas de estadísticas e incluso permitirán emitir algunos
comandos para cambiar algunos ajustes en tiempo de ejecución. Consulta la [sección
9.3](/es/haproxy/statistics-and-monitoring/#section-9-3) "Comandos de socket Unix" de la guía de
gestión para más detalles.

Se soportan todos los parámetros admitidos por las líneas "bind", por ejemplo para restringir el
acceso a ciertos usuarios o sus derechos de acceso. Consulta la [sección
5.1](/es/haproxy/bind-and-server-options/#section-5-1) para más información.

<a id="entry-3-1-stats-timeout"></a>

**`stats timeout <timeout, in milliseconds>`**

```haproxy
stats timeout <timeout, in milliseconds>
```

El tiempo de espera por defecto del socket de estadísticas está establecido a 10 segundos. Es
posible cambiar este valor con "stats timeout". El valor debe pasarse en milisegundos o llevar un
sufijo de unidad de tiempo entre { us, ms, s, m, h, d }.

<a id="entry-3-1-stats-file"></a>

**`stats-file <path>`**

```haproxy
stats-file <path>
```

Ruta a un stats-file de haproxy generado. En el arranque, haproxy precargará los valores en sus
contadores internos. Usa el comando de CLI "dump stats-file" para producir dicho stats-file. Ver el
manual de gestión para más detalles.

<a id="entry-3-1-stress-level"></a>

**`stress-level <level>`**

```haproxy
stress-level <level>
```

Activa código alternativo para estresar el binario de haproxy. El nivel es un entero de 0 a 9. El
valor por defecto 0 deshabilita cualquier ejecución de estrés. Los niveles de 1 a 9 aumentarán la
presión de estrés sobre el binario de haproxy. Ten en cuenta que usar cualquier nivel positivo
puede perjudicar significativamente el rendimiento. Por ello, nunca debería activarse salvo para
depuración y a petición de un desarrollador.

<a id="entry-3-1-strict-limits"></a>

**`strict-limits`**

```haproxy
strict-limits
```

Hace que el proceso falle en el arranque cuando un setrlimit falla. HAProxy intenta establecer el
mejor setrlimit según lo calculado. Si falla, emitirá una advertencia. Esta opción está para
garantizar un fallo explícito de HAProxy cuando esos límites fallan. Está habilitada por defecto.
Aún puede forzarse su deshabilitación prefijándola con la palabra clave "no".

<a id="entry-3-1-thread-group"></a>

**`thread-group <group> [<thread-range>...]`**

```haproxy
thread-group <group> [<thread-range>...]
```

Este ajuste solo está disponible cuando se compiló con soporte de hilos. Enumera la lista de hilos
que compondrán el grupo de hilos `<group>`. Los números de hilo y de grupo comienzan en 1. Los
rangos de hilos se definen usando un único número de hilo a la vez, o especificando los límites
inferior y superior delimitados por un guion '-' (p. ej. "1-16"). Los hilos no asignados se
asignarán automáticamente a grupos de hilos no asignados, y los grupos de hilos definidos con esta
directiva nunca recibirán más hilos que los definidos. Definir el mismo grupo varias veces anula
las definiciones anteriores con la nueva. Ver también "nbthread" y "thread-groups".

<a id="entry-3-1-thread-groups"></a>

**`thread-groups <number>`**

```haproxy
thread-groups <number>
```

Este ajuste solo está disponible cuando se compiló con soporte de hilos. Hace que HAProxy divida
sus hilos en `<number>` grupos independientes. En este momento, el valor por defecto es 1. Los
grupos de hilos permiten reducir el uso compartido entre hilos para limitar la contención, a costa
de algún esfuerzo adicional de configuración. También es la única forma de usar más de 64 hilos,
ya que pueden configurarse hasta 64 hilos por grupo. El número máximo de grupos se configura en
tiempo de compilación y por defecto es 16. Ver también "nbthread".

<a id="entry-3-1-thread-hard-limit"></a>

**`thread-hard-limit <number>`**

```haproxy
thread-hard-limit <number>
```

Este ajuste se usa para imponer un límite al número de hilos, ya sea detectado o configurado. Esto
es particularmente útil en sistemas operativos donde el número de hilos se detecta
automáticamente y se desea un número de hilos menor que el de CPU en configuraciones genéricas y
portables. En efecto, mientras que "nbthread" impone un número de hilos que dará lugar a una
advertencia y a un mal rendimiento si es mayor que las CPU disponibles, thread-hard-limit solo
limitará el valor máximo y limitará automáticamente el número de hilos a no más de este valor,
pero no elevará los valores más bajos. Si se fuerza "nbthread" a un valor mayor, thread-hard-limit
gana, y se emite una advertencia para que pueda corregirse la anomalía de la configuración. Por
defecto no hay límite. Ver también "nbthread".

<a id="entry-3-1-uid"></a>

**`uid <number>`**

```haproxy
uid <number>
```

Cambia el ID de usuario del proceso a `<number>`. Se recomienda que el ID de usuario esté dedicado
a HAProxy o a un pequeño conjunto de demonios similares. HAProxy debe iniciarse con privilegios de
superusuario para poder cambiar a otro. Ver también "gid" y "user".

<a id="entry-3-1-ulimit-n"></a>

**`ulimit-n <number>`**

```haproxy
ulimit-n <number>
```

Establece a `<number>` el número máximo de descriptores de archivo por proceso. Por defecto se
calcula automáticamente, por lo que se recomienda no usar esta opción. Si la intención es solo
limitar el número de descriptores de archivo, es mejor usar "fd-hard-limit" en su lugar.

Ten en cuenta que los servidores dinámicos no se tienen en cuenta en este cálculo automático de
recursos. Si se usa un gran número de ellos, puede ser necesario especificar manualmente este
valor.

Ver también: fd-hard-limit, maxconn

unix-bind [ prefix `<prefix>` ] [ mode `<mode>` ] [ user `<user>` ] [ uid `<uid>` ] [ group
`<group>` ] [ gid `<gid>` ]

Fija ajustes comunes a los sockets UNIX de escucha declarados en declaraciones "bind". Se usa
principalmente para simplificar la declaración de esos sockets UNIX y reducir el riesgo de
errores, ya que dichos ajustes son los más comúnmente requeridos pero también son específicos del
proceso. El ajuste `<prefix>` puede usarse para forzar que todas las rutas de socket sean relativas
a ese directorio. Esto puede ser necesario para acceder al chroot de otro componente. Ten en
cuenta que esas rutas se resuelven antes de que HAProxy haga chroot sobre sí mismo, de modo que
son absolutas. Los ajustes `<mode>`, `<user>`, `<uid>`, `<group>` y `<gid>` tienen todos el mismo
significado que sus homónimos usados por la declaración "bind". Si se especifican ambos, la
declaración "bind" tiene prioridad, lo que significa que los ajustes de "unix-bind" pueden verse
como ajustes por defecto de todo el proceso.

<a id="entry-3-1-unsetenv"></a>

**`unsetenv [<name> ...]`**

```haproxy
unsetenv [<name> ...]
```

Elimina las variables de entorno especificadas en los argumentos. Esto puede ser útil para
ocultar cierta información sensible que ocasionalmente se hereda del entorno del usuario durante
algunas operaciones. Las variables que no existían se ignoran silenciosamente, de modo que tras la
operación es seguro que no queda ninguna de estas variables. Los cambios surten efecto
inmediatamente, de modo que la siguiente línea del archivo de configuración no verá estas
variables. Ver también "setenv", "presetenv" y "resetenv".

<a id="entry-3-1-user"></a>

**`user <user name>`**

```haproxy
user <user name>
```

Similar a "uid" pero usa el UID del nombre de usuario `<user name>` de /etc/passwd. Ver también
"uid" y "group".

<a id="entry-3-1-node"></a>

**`node <name>`**

```haproxy
node <name>
```

Solo se permiten letras, dígitos, guion y guion bajo, como en los nombres DNS.

Esta declaración es útil en configuraciones HA donde dos o más procesos o servidores comparten la
misma dirección IP. Al establecer un node-name diferente en todos los nodos, resulta fácil
identificar de inmediato qué servidor está manejando el tráfico.

<a id="entry-3-1-wurfl-cache-size"></a>

**`wurfl-cache-size <size>`**

```haproxy
wurfl-cache-size <size>
```

Establece el tamaño de la caché del user agent WURFL. Para búsquedas más rápidas, los user agents
ya procesados se guardan en una caché LRU:

- "0" : no se usa caché.
- `<size>` : tamaño de la caché lru en elementos.

Ten en cuenta que esta opción solo está disponible cuando HAProxy ha sido compilado con
USE_WURFL=1.

<a id="entry-3-1-wurfl-data-file"></a>

**`wurfl-data-file <file path>`**

```haproxy
wurfl-data-file <file path>
```

La ruta del archivo de datos WURFL para proporcionar servicios de detección de dispositivos. El
archivo debe ser accesible por HAProxy con los permisos pertinentes.

Ten en cuenta que esta opción solo está disponible cuando HAProxy ha sido compilado con
USE_WURFL=1.

<a id="entry-3-1-wurfl-information-list"></a>

**`wurfl-information-list [<capability>]*`**

```haproxy
wurfl-information-list [<capability>]*
```

Una lista separada por espacios de capacidades WURFL, capacidades virtuales y nombres de
propiedades que planeamos usar en cabeceras inyectadas. La lista completa de nombres de
capacidades y capacidades virtuales está disponible en el sitio web de Scientiamobile:

```text
https://www.scientiamobile.com/wurflCapability
```

Las propiedades WURFL válidas son:

- wurfl_id Contiene el ID del dispositivo coincidente.

- wurfl_root_id Contiene el ID raíz del dispositivo coincidente.

- wurfl_isdevroot Indica si el dispositivo coincidente es un dispositivo raíz. Los valores
  posibles son "TRUE" o "FALSE".

- wurfl_useragent El user agent original que acompaña a esta solicitud web en particular.

- wurfl_api_version Contiene una cadena que representa la versión de la API Libwurfl usada
  actualmente.

- wurfl_info Una cadena que contiene información sobre el wurfl.xml analizado y su ruta completa.

- wurfl_last_load_time Contiene el timestamp UNIX de la última vez que WURFL se cargó con éxito.

- wurfl_normalized_useragent El user agent normalizado.

Ten en cuenta que esta opción solo está disponible cuando HAProxy ha sido compilado con
USE_WURFL=1.

<a id="entry-3-1-wurfl-information-list-separator"></a>

**`wurfl-information-list-separator <char>`**

```haproxy
wurfl-information-list-separator <char>
```

Un carácter que se usará para separar valores en una cabecera de respuesta que contenga resultados
WURFL. Si no se establece, se usará por defecto una coma (',').

Ten en cuenta que esta opción solo está disponible cuando HAProxy ha sido compilado con
USE_WURFL=1.

<a id="entry-3-1-wurfl-patch-file"></a>

**`wurfl-patch-file [<file path>]`**

```haproxy
wurfl-patch-file [<file path>]
```

Una lista de rutas de archivos de parche WURFL. Ten en cuenta que los parches se cargan durante el
arranque, es decir, antes del chroot.

Ten en cuenta que esta opción solo está disponible cuando HAProxy ha sido compilado con
USE_WURFL=1.

## 3.2. Ajuste de rendimiento {#section-3-2}

<a id="entry-3-2-busy-polling"></a>

**`busy-polling`**

```haproxy
busy-polling
```

En algunas situaciones, especialmente cuando se busca una baja latencia en procesadores que
admiten frecuencia variable o cuando se ejecuta dentro de máquinas virtuales, cada vez que el
proceso espera una E/S usando el poller, el procesador vuelve a dormirse o se ofrece a otra VM
durante mucho tiempo, lo que causa latencias excesivamente altas. Esta opción proporciona una
solución que evita que el procesador se duerma usando siempre un tiempo de espera nulo en los
pollers. Esto se traduce en una reducción significativa de la latencia (se observaron de 30 a 100
microsegundos) a costa del riesgo de sobrecalentar el procesador. Puede incluso usarse con hilos,
en cuyo caso los hilos mal vinculados pueden entrar fuertemente en conflicto, lo que resulta en un
peor rendimiento y valores altos de CPU robada en los campos "stolen" de la salida de "show info",
lo que indica qué hilos están mal configurados. Es importante no dejar que el proceso se ejecute en
el mismo procesador que las interrupciones de red cuando se usa esta opción. También es mejor
evitar usarla en varios hilos de CPU que comparten el mismo núcleo. Esta opción está desactivada
por defecto. Si se ha activado, todavía puede forzarse su desactivación prefijándola con la palabra
clave "no". Los pollers "select" y "poll" la ignoran.

Esta opción se desactiva automáticamente en los procesos antiguos en el contexto de una recarga sin
interrupción; evita demasiados conflictos de CPU cuando varios procesos permanecen cierto tiempo
esperando el final de sus conexiones actuales.

<a id="entry-3-2-max-spread-checks"></a>

**`max-spread-checks <delay in milliseconds>`**

```haproxy
max-spread-checks <delay in milliseconds>
```

Por defecto, HAProxy intenta repartir el inicio de las comprobaciones de salud a lo largo del menor
intervalo de comprobación de salud de todos los servidores de una granja. El principio es evitar
martillear servicios que se ejecutan en el mismo servidor. Pero cuando se usan intervalos de
comprobación grandes (10 segundos o más), los últimos servidores de la granja tardan cierto tiempo
en empezar a ser probados, lo que puede ser un problema. Este parámetro se usa para imponer un
límite superior al retraso entre la primera y la última comprobación, incluso si los intervalos de
comprobación de los servidores son mayores. Cuando los servidores se ejecutan con intervalos más
cortos, sus intervalos se respetarán de todos modos.

<a id="entry-3-2-maxcompcpuusage"></a>

**`maxcompcpuusage <number>`**

```haproxy
maxcompcpuusage <number>
```

Establece el uso máximo de CPU que HAProxy puede alcanzar antes de detener la compresión para
nuevas peticiones o de reducir el nivel de compresión de las peticiones actuales. Funciona como
'maxcomprate' pero mide el uso de CPU en lugar del ancho de banda de los datos entrantes. El valor
se expresa en porcentaje de la CPU usada por HAProxy. Un valor de 100 desactiva el límite. El valor
por defecto es 100. Establecer un valor más bajo evitará que el trabajo de compresión ralentice
todo el proceso e introduzca latencias altas.

<a id="entry-3-2-maxcomprate"></a>

**`maxcomprate <number>`**

```haproxy
maxcomprate <number>
```

Establece la tasa máxima por proceso de compresión de entrada en `<number>` kilobytes por segundo.
Para cada stream, si se alcanza el máximo, el nivel de compresión se reducirá durante el stream. Si
el máximo se alcanza al comienzo de un stream, el stream no se comprimirá en absoluto. Si el
máximo no se alcanza, el nivel de compresión se aumentará hasta tune.comp.maxlevel. Un valor de
cero significa que no hay límite; este es el valor por defecto.

<a id="entry-3-2-maxconn"></a>

**`maxconn <number>`**

```haproxy
maxconn <number>
```

Establece el número máximo por proceso de conexiones simultáneas en `<number>`. Es equivalente al
argumento de línea de comandos "-n". El valor proporcionado en el argumento de línea de comandos
vía "-n" tiene precedencia sobre el valor de maxconn establecido en la sección global. El proceso
de HAProxy también puede haberse compilado con la variable de compilación SYSTEM_MAXCONN, que en
ese caso sirve como máximo de maxconn del sistema. De nuevo, el argumento de línea de comandos
"-n" permite en tiempo de ejecución saltarse el límite SYSTEM_MAXCONN, si está establecido. Los
proxies dejarán de aceptar conexiones cuando se alcance maxconn. El límite flexible de
descriptores de archivo del proceso (puede obtenerse con el comando "ulimit -n") se ajusta
automáticamente según el maxconn proporcionado. Ver también "ulimit-n". Nota: el poller "select"
no puede usar de forma fiable más de 1024 descriptores de archivo en algunas plataformas. Si tu
plataforma solo admite select e informa "select FAILED" al arrancar, debes reducir maxconn hasta
que funcione (ligeramente por debajo de 500 en general). Si el valor de maxconn no se establece,
se calculará automáticamente basándose en los límites actuales de descriptores de archivo
informados por el comando "ulimit -nH" (tomamos el máximo entre los valores rígido y flexible);
luego el valor automático posiblemente se verá reducido por "fd-hard-limit" y por el límite de
memoria, si este último se impuso mediante la opción de línea de comandos "-m". El valor automático
también depende del tamaño del buffer, de la memoria asignada a la compresión, del tamaño de la
caché SSL y del uso o no de SSL y del maxsslconn asociado (que también puede ser automático).

Ver también: fd-hard-limit, ulimit-n

<a id="entry-3-2-maxconnrate"></a>

**`maxconnrate <number>`**

```haproxy
maxconnrate <number>
```

Establece el número máximo por proceso de conexiones por segundo en `<number>`. Los proxies
dejarán de aceptar conexiones cuando se alcance este límite. Puede usarse para limitar la capacidad
global independientemente de la capacidad de cada frontend. Es importante tener en cuenta que esto
solo puede usarse como medida de protección del servicio, ya que no necesariamente habrá un reparto
equitativo entre frontends cuando se alcance el límite, así que es buena idea limitar también cada
frontend a un valor cercano a su cuota esperada. Además, reducir tune.maxaccept puede mejorar la
equidad.

<a id="entry-3-2-maxpipes"></a>

**`maxpipes <number>`**

```haproxy
maxpipes <number>
```

Establece el número máximo por proceso de pipes en `<number>`. Actualmente, los pipes solo los usa
el splicing TCP basado en el kernel. Como un pipe contiene dos descriptores de archivo, el valor de
"ulimit-n" se incrementará en consecuencia. El valor por defecto es maxconn/4, lo que parece ser
más que suficiente para la mayoría de los usos intensivos. El código de splice asigna y libera
pipes dinámicamente y puede recurrir a la copia estándar, así que establecer este valor demasiado
bajo solo puede afectar al rendimiento.

<a id="entry-3-2-maxsessrate"></a>

**`maxsessrate <number>`**

```haproxy
maxsessrate <number>
```

Establece el número máximo por proceso de sesiones por segundo en `<number>`. Los proxies dejarán
de aceptar conexiones cuando se alcance este límite. Puede usarse para limitar la capacidad global
independientemente de la capacidad de cada frontend. Es importante tener en cuenta que esto solo
puede usarse como medida de protección del servicio, ya que no necesariamente habrá un reparto
equitativo entre frontends cuando se alcance el límite, así que es buena idea limitar también cada
frontend a un valor cercano a su cuota esperada. Además, reducir tune.maxaccept puede mejorar la
equidad.

<a id="entry-3-2-maxsslconn"></a>

**`maxsslconn <number>`**

```haproxy
maxsslconn <number>
```

Establece el número máximo por proceso de conexiones SSL simultáneas en `<number>`. Por defecto no
hay ningún límite específico de SSL, lo que significa que el ajuste maxconn global se aplicará a
todas las conexiones. Establecer este límite evita que openssl use demasiada memoria y caiga cuando
malloc devuelve NULL (ya que desafortunadamente no comprueba de forma fiable tales condiciones).
Ten en cuenta que el límite se aplica tanto a las conexiones entrantes como a las salientes, así
que una conexión que se descifra y luego se cifra cuenta como 2 conexiones SSL. Si este valor no se
establece, pero se impone un límite de memoria, este valor se calculará automáticamente basándose
en el límite de memoria, maxconn, el tamaño del buffer, la memoria asignada a la compresión, el
tamaño de la caché SSL y el uso de SSL en los frontends, los backends o ambos. Si no se especifica
ni maxconn ni maxsslconn cuando hay un límite de memoria, HAProxy ajustará automáticamente estos
valores para que el 100% de las conexiones puedan hacerse sobre SSL sin riesgo, y considerará los
lados donde está activado (frontend, backend o ambos).

<a id="entry-3-2-maxsslrate"></a>

**`maxsslrate <number>`**

```haproxy
maxsslrate <number>
```

Establece el número máximo por proceso de sesiones SSL por segundo en `<number>`. Los listeners
SSL dejarán de aceptar conexiones cuando se alcance este límite. Puede usarse para limitar el uso
global de CPU de SSL independientemente de la capacidad de cada frontend. Es importante tener en
cuenta que esto solo puede usarse como medida de protección del servicio, ya que no necesariamente
habrá un reparto equitativo entre frontends cuando se alcance el límite, así que es buena idea
limitar también cada frontend a un valor cercano a su cuota esperada. También es importante tener
en cuenta que las sesiones se contabilizan antes de entrar en la pila SSL y no después, lo que
además protege la pila contra handshakes defectuosos. Además, reducir tune.maxaccept puede mejorar
la equidad.

<a id="entry-3-2-maxzlibmem"></a>

**`maxzlibmem <number>`**

```haproxy
maxzlibmem <number>
```

Establece la cantidad máxima de RAM en megabytes por proceso utilizable por zlib. Cuando se alcanza
la cantidad máxima, los streams futuros no se comprimirán mientras no haya RAM disponible. Cuando
se establece a 0, no hay límite. El valor por defecto es 0. El valor está disponible en bytes en el
socket UNIX con "show info" en la línea "MaxZlibMemUsage"; la memoria usada por zlib es
"ZlibMemUsage" en bytes.

<a id="entry-3-2-no-memory-trimming"></a>

**`no-memory-trimming`**

```haproxy
no-memory-trimming
```

Desactiva el recorte de memoria ("malloc_trim") en unos pocos momentos en los que se intenta
reclamar mucha memoria (ante escasez de memoria o en una recarga). Recortar la memoria fuerza al
asignador del sistema a escanear todas las zonas no usadas y liberarlas. Generalmente esto se
considera una acción amable para dejar más memoria disponible a un proceso nuevo mientras que el
antiguo probablemente no le dará un uso significativo. Pero algunos sistemas que manejan decenas o
cientos de miles de conexiones simultáneas pueden experimentar mucha fragmentación de memoria, lo
que puede hacer que esta operación de liberación resulte extremadamente larga. Durante ese tiempo,
ya no pasa tráfico por el proceso, las conexiones nuevas no se aceptan, algunas comprobaciones de
salud pueden incluso fallar, y el watchdog puede incluso dispararse y matar el proceso que no
responde, dejando un volcado de núcleo enorme. Si esto llega a ocurrir, se sugiere usar esta opción
para desactivar el recorte y dejar de intentar ser amable con el proceso nuevo. Ten en cuenta que
los asignadores de memoria avanzados normalmente no sufren tal problema.

<a id="entry-3-2-noepoll"></a>

**`noepoll`**

```haproxy
noepoll
```

Desactiva el uso del sistema de sondeo de eventos "epoll" en Linux. Es equivalente al argumento de
línea de comandos "-de". El siguiente sistema de sondeo usado será generalmente "poll". Ver
también "nopoll".

<a id="entry-3-2-noevports"></a>

**`noevports`**

```haproxy
noevports
```

Desactiva el uso del sistema de sondeo de eventos event ports en sistemas SunOS derivados de
Solaris 10 y posteriores. Es equivalente al argumento de línea de comandos "-dv". El siguiente
sistema de sondeo usado será generalmente "poll". Ver también "nopoll".

<a id="entry-3-2-nogetaddrinfo"></a>

**`nogetaddrinfo`**

```haproxy
nogetaddrinfo
```

Desactiva el uso de getaddrinfo(3) para la resolución de nombres. Es equivalente al argumento de
línea de comandos "-dG". Se usará el obsoleto gethostbyname(3).

<a id="entry-3-2-nokqueue"></a>

**`nokqueue`**

```haproxy
nokqueue
```

Desactiva el uso del sistema de sondeo de eventos "kqueue" en BSD. Es equivalente al argumento de
línea de comandos "-dk". El siguiente sistema de sondeo usado será generalmente "poll". Ver
también "nopoll".

<a id="entry-3-2-noktls"></a>

**`noktls`**

```haproxy
noktls
```

Desactiva el uso de ktls. Es equivalente al argumento de línea de comandos "-dT".

<a id="entry-3-2-nopoll"></a>

**`nopoll`**

```haproxy
nopoll
```

Desactiva el uso del sistema de sondeo de eventos "poll". Es equivalente al argumento de línea de
comandos "-dp". El siguiente sistema de sondeo usado será "select". Nunca debería hacer falta
desactivar "poll" ya que está disponible en todas las plataformas soportadas por HAProxy. Ver
también "nokqueue", "noepoll" y "noevports".

<a id="entry-3-2-noreuseport"></a>

**`noreuseport`**

```haproxy
noreuseport
```

Desactiva el uso de SO_REUSEPORT; ver socket(7). Es equivalente al argumento de línea de comandos
"-dR".

<a id="entry-3-2-nosplice"></a>

**`nosplice`**

```haproxy
nosplice
```

Desactiva el uso del splicing TCP del kernel entre sockets en Linux. Es equivalente al argumento
de línea de comandos "-dS". Los datos se copiarán entonces usando llamadas recv/send convencionales
y más portables. El splicing TCP del kernel está limitado a algunas instancias muy recientes del
kernel 2.6. La mayoría de las versiones entre 2.6.25 y 2.6.28 tienen errores y reenviarán datos
corruptos, así que no deben usarse. Esta opción facilita desactivar globalmente el splicing del
kernel en caso de duda. Ver también "option splice-auto", "option splice-request" y "option
splice-response".

<a id="entry-3-2-profiling-memory"></a>

**`profiling.memory { on | off }`**

```haproxy
profiling.memory { on | off }
```

Activa ('on') o desactiva ('off') el perfilado de memoria por función. Esto mantendrá estadísticas
de uso de las llamadas malloc/calloc/realloc/free en cualquier parte del proceso (incluidas las
bibliotecas), que se informarán en la CLI usando el comando "show profiling". Esto está
esencialmente pensado para usarse cuando se observa un uso anormal de memoria que no puede
explicarse por los pools y se requiere información adicional. El impacto en el rendimiento será
típicamente de alrededor del 1%, quizá algo más en máquinas con muchos hilos, así que normalmente
es adecuado para su uso en producción. Lo mismo puede lograrse en tiempo de ejecución en la CLI
usando el comando "set profiling memory"; consulta el manual de gestión.

<a id="entry-3-2-profiling-tasks"></a>

**`profiling.tasks { auto | on | off | lock | no-lock | memory | no-memory }*`**

```haproxy
profiling.tasks { auto | on | off | lock | no-lock | memory | no-memory }*
```

Activa ('on') o desactiva ('off') el perfilado de CPU por tarea. Cuando se ajusta a 'auto', el
perfilado se activa automáticamente en un hilo cuando este empieza a sufrir una latencia media de
1000 microsegundos o más, tal como se informa en el campo de actividad "avg_loop_us", y se
desactiva automáticamente cuando la latencia vuelve a bajar de 990 microsegundos (este valor es
una media de los últimos 1024 bucles, así que no varía rápidamente y tiende a suavizar de forma
significativa los picos cortos). También puede activarse espontáneamente de vez en cuando en
sistemas sobrecargados, contenedores o máquinas virtuales, o cuando el sistema usa swap (algo que
no debe ocurrir absolutamente nunca en un balanceador de carga).

Cuando el perfilado de tareas está activado, HAProxy también puede recoger el tiempo que cada tarea
pasa manteniendo un lock o esperándolo, así como el tiempo transcurrido esperando que una asignación de
memoria tenga éxito en caso de fallo de caché de pool. Esto a veces puede ayudar a entender
ciertas causas de latencia. Para ello pueden pasarse adicionalmente las palabras clave extra
"lock" (para activar la recolección del tiempo de lock), "no-lock" (para desactivarla), "memory"
(para activar la recolección del tiempo de asignación de memoria) o "no-memory" (para
desactivarla). Por defecto no están activadas, ya que pueden tener un impacto de CPU no
despreciable en sistemas muy cargados (3-10%). Ten en cuenta que la sobrecarga solo se asume
cuando el perfilado está efectivamente en ejecución, de modo que cuando se ejecuta en modo "auto"
solo aparecerá cuando HAProxy decida activarlo.

El perfilado de CPU por tarea puede ser muy conveniente para informar de dónde se gasta el tiempo
y qué peticiones tienen qué efecto sobre qué otras peticiones. Activarlo afectará típicamente al
rendimiento global en menos del 1%, por lo que se recomienda dejarlo en el valor por defecto 'auto'
para que solo opere cuando se identifique un problema. Esta funcionalidad requiere un sistema que
admita la syscall clock_gettime(2) con los identificadores de reloj CLOCK_MONOTONIC y
CLOCK_THREAD_CPUTIME_ID; de lo contrario, el tiempo informado será cero. Esta opción puede
cambiarse en tiempo de ejecución usando "set profiling" en la CLI.

<a id="entry-3-2-spread-checks"></a>

**`spread-checks <0..50, in percent>`**

```haproxy
spread-checks <0..50, in percent>
```

A veces es deseable evitar enviar comprobaciones de agente y de salud a los servidores en
intervalos exactos, por ejemplo cuando muchos servidores lógicos están ubicados en el mismo
servidor físico. Con la ayuda de este parámetro es posible añadir algo de aleatoriedad al intervalo
de comprobación, entre 0 y +/- 50%. Un valor entre 2 y 5 parece mostrar buenos resultados. El
valor por defecto sigue siendo 0.

<a id="entry-3-2-ssl-engine"></a>

**`ssl-engine <name> [algo <comma-separated list of algorithms>]`**

```haproxy
ssl-engine <name> [algo <comma-separated list of algorithms>]
```

Establece el motor de OpenSSL en `<name>`. La lista de valores válidos para `<name>` puede
obtenerse con el comando "openssl engine". Esta instrucción puede usarse varias veces; simplemente
activará varios motores criptográficos. Referenciar un motor no soportado impedirá que HAProxy
arranque. Ten en cuenta que muchos motores darán un rendimiento HTTPS menor que el software puro
con procesadores recientes. El comando opcional "algo" establece los algoritmos por defecto que
suministrará un ENGINE usando la función de OPENSSL ENGINE_set_default_string(). El valor "ALL"
usa el motor para todas las operaciones criptográficas. Si no se especifica ninguna lista de
algos, se usa el valor "ALL". Puede especificarse una lista separada por comas de diferentes
algoritmos, incluyendo: RSA, DSA, DH, EC, RAND, CIPHERS, DIGESTS, PKEY, PKEY_CRYPTO, PKEY_ASN1.
Es el mismo formato que usa el archivo de configuración de openssl:
<https://www.openssl.org/docs/man1.0.2/apps/config.html>

La versión 2.6 de HAProxy desactivó el soporte de motores en la compilación por defecto. Esta
opción solo está disponible cuando HAProxy se ha compilado con soporte para ello. En caso de que
ssl-engine sea necesario, HAProxy puede recompilarse con el flag USE_ENGINE=1.

Compatibilidad: OpenSSL >= 1.1.1. No compatible con AWS-LC.

<a id="entry-3-2-ssl-mode-async"></a>

**`ssl-mode-async`**

```haproxy
ssl-mode-async
```

Añade el modo SSL_MODE_ASYNC al contexto SSL. Esto activa operaciones de E/S TLS asíncronas si se
usan motores SSL con capacidad asíncrona. La implementación actual admite un máximo de 32 motores.
La API ASYNC de Openssl no soporta mover buffers de lectura/escritura y no se ajusta a la gestión
de buffers de HAProxy. Por ello el modo asíncrono está desactivado en las operaciones de
lectura/escritura (solo se activa durante los handshakes iniciales y de renegociación).

Compatibilidad: OpenSSL >= 1.1.1. No compatible con AWS-LC.

<a id="entry-3-2-tune-applet-zero-copy-forwarding"></a>

**`tune.applet.zero-copy-forwarding { on | off }`**

```haproxy
tune.applet.zero-copy-forwarding { on | off }
```

Activa ('on') o desactiva ('off') el reenvío de copia cero de datos para los applets. Está
activado por defecto.

Ver también: tune.disable-zero-copy-forwarding.

<a id="entry-3-2-tune-buffers-limit"></a>

**`tune.buffers.limit <number>`**

```haproxy
tune.buffers.limit <number>
```

Establece un límite rígido sobre el número de buffers que pueden asignarse por proceso. El valor
por defecto es cero, lo que significa ilimitado. El límite se reajustará automáticamente para
satisfacer los buffers reservados para situaciones de emergencia, de modo que el usuario no tenga
que hacer cálculos complicados. Forzar este valor puede ser particularmente útil para limitar la
cantidad de memoria que un proceso puede tomar, conservando un comportamiento sensato. Cuando se
alcanza este límite, una tarea que solicita un buffer espera a que otro se libere primero. La
mayoría de las veces el tiempo de espera es muy corto y no perceptible, siempre que los límites
permanezcan razonables. Sin embargo, algunas limitaciones históricas han debilitado este mecanismo
a lo largo de las versiones y se sabe que, en ciertas situaciones de escasez sostenida, algunas
tareas pueden congelarse hasta que expire su tiempo de espera, así que es más seguro evitar su uso
cuando no sea estrictamente necesario.

<a id="entry-3-2-tune-buffers-reserve"></a>

**`tune.buffers.reserve <number>`**

```haproxy
tune.buffers.reserve <number>
```

Establece el número de buffers por hilo que se preasignan y reservan para usarse únicamente durante
condiciones de escasez de memoria que resulten en asignaciones fallidas. El valor mínimo es 0 y el
valor por defecto es 4. No hay razón para que un usuario quiera cambiar este valor, salvo que un
desarrollador del núcleo sugiera cambiarlo por una razón muy específica.

<a id="entry-3-2-tune-bufsize"></a>

**`tune.bufsize <size>`**

```haproxy
tune.bufsize <size>
```

Establece el tamaño del buffer a este tamaño (en bytes). Los valores más bajos permiten que
coexistan más streams en la misma cantidad de RAM, y los valores más altos permiten que funcionen
algunas aplicaciones con cookies muy grandes. El valor por defecto es 16384 y puede cambiarse en
tiempo de compilación. Se recomienda encarecidamente no cambiar este valor por defecto, ya que
valores muy bajos romperán algunos servicios como las estadísticas, y valores mayores que el
tamaño por defecto incrementarán el uso de memoria, posiblemente causando que el sistema se quede
sin memoria. Como mínimo, el parámetro global maxconn debería reducirse en el mismo factor en que
este se incremente. Además, el uso de HTTP/2 exige que este valor sea 16384 o más. El valor
también debe ser inferior a 256 MB (268435456 bytes). Si el bloque de cabeceras de una petición
HTTP es mayor que (tune.bufsize - tune.maxrewrite), HAProxy devolverá un error HTTP 400 (Bad
Request). De forma similar, si el bloque de cabeceras de una respuesta HTTP es mayor que este
tamaño, HAProxy devolverá un error HTTP 502 (Bad Gateway). Ten en cuenta que el valor establecido
con este parámetro se redondeará automáticamente hacia arriba al siguiente múltiplo de 8 en
máquinas de 32 bits y de 16 en máquinas de 64 bits. Ver también: tune.bufsize.large,
tune.bufsize.small.

<a id="entry-3-2-tune-bufsize-large"></a>

**`tune.bufsize.large <size>`**

```haproxy
tune.bufsize.large <size>
```

Establece el tamaño en bytes de los buffers grandes. Por defecto, el soporte de buffers grandes no
está activado; debe activarse explícitamente estableciendo este valor.

Estos buffers están pensados para usarse en algunos contextos específicos donde deben
almacenarse en buffer más datos sin cambiar el tamaño de los buffers regulares. Los buffers
grandes no se usan implícitamente. Ver también: tune.bufsize.

Ten en cuenta que cuando se configuran buffers grandes, se asignarán tres buffers grandes
especiales para cada hilo durante el arranque para uso interno.

<a id="entry-3-2-tune-bufsize-small"></a>

**`tune.bufsize.small <size>`**

```haproxy
tune.bufsize.small <size>
```

Establece el tamaño en bytes de los buffers pequeños. El valor por defecto es 1024.

Estos buffers están pensados para usarse en algunos contextos específicos donde el consumo de
memoria está restringido pero parece innecesario asignar un buffer completo. Sin embargo, si un
buffer pequeño no es suficiente, se realiza automáticamente una reasignación para pasar a un
buffer de tamaño estándar.

Por el momento, solo lo usa automáticamente el protocolo HTTP/3 para emitir las cabeceras de
respuesta. De lo contrario, el soporte de buffers pequeños puede activarse para proxies
específicos mediante la opción "use-small-buffers". Ver también: tune.bufsize.

Ver también: option use-small-buffers

<a id="entry-3-2-tune-cli-max-payload-size"></a>

**`tune.cli.max-payload-size <size>`**

```haproxy
tune.cli.max-payload-size <size>
```

Establece el tamaño máximo permitido para el payload pasado a un comando en la CLI.

En la CLI, una línea de comandos está limitada por el tamaño del buffer. Esto significa que todos
los comandos y sus argumentos deben caber en un buffer para poder procesarse, excluyendo el
payload que puede pasarse al último comando de la línea de comandos. Este payload puede asignarse
en un área dedicada si es necesario. Su tamaño está limitado por este parámetro. El valor por
defecto es 128KB.

Aunque debería ser lo bastante alto para la mayoría de los usos, si se cambia este valor debe
elegirse con cuidado. Un valor enorme puede repercutir en el rendimiento de HAProxy. Según el
comando, un payload enorme puede tardar bastante en procesarse y posiblemente activar el watchdog.

Consulta el manual de gestión para más detalles sobre la CLI.

<a id="entry-3-2-tune-comp-maxlevel"></a>

**`tune.comp.maxlevel <number>`**

```haproxy
tune.comp.maxlevel <number>
```

Establece el nivel máximo de compresión. El nivel de compresión afecta al uso de CPU durante la
compresión. Este valor afecta al uso de CPU durante la compresión. Cada stream que usa compresión
inicializa el algoritmo de compresión con este valor. El valor por defecto es 1.

<a id="entry-3-2-tune-defaults-purge"></a>

**`tune.defaults.purge`**

```haproxy
tune.defaults.purge
```

Para el soporte de backends dinámicos, ahora todas las secciones defaults con nombre se conservan
en memoria tras el análisis. Esto es necesario porque los backends añadidos en tiempo de ejecución
deben basarse en un defaults con nombre para su configuración.

Esto puede consumir una cantidad significativa de memoria si el número de instancias de defaults es
importante. En este caso, y si la funcionalidad de backends dinámicos es innecesaria, es posible
usar esta opción para forzar el borrado de las secciones defaults tras el análisis. Aun así, sigue
siendo obligatorio conservar las secciones defaults referenciadas que contengan ajustes que no
pueden copiar los proxies que las referencian. Por ejemplo, este es el caso si la sección defaults
define reglas TCP/HTTP o un conjunto de reglas tcpcheck.

<a id="entry-3-2-tune-disable-fast-forward"></a>

**`tune.disable-fast-forward`**

```haproxy
tune.disable-fast-forward
```

Desactiva el reenvío rápido de datos. Es un mecanismo para optimizar el reenvío de datos pasando
estos directamente de un lado al otro sin despertar el stream. Gracias a esta directiva es posible
desactivar esta optimización. Ten en cuenta que también desactiva cualquier splicing TCP del
kernel, así como el reenvío de copia cero. Este comando no está pensado para un uso regular;
generalmente solo lo sugerirán los desarrolladores durante sesiones de depuración complejas.

<a id="entry-3-2-tune-disable-zero-copy-forwarding"></a>

**`tune.disable-zero-copy-forwarding`**

```haproxy
tune.disable-zero-copy-forwarding
```

Desactiva globalmente el reenvío de copia cero de datos. Es un mecanismo para optimizar el reenvío
rápido de datos evitando el uso del buffer del canal. Gracias a esta directiva es posible
desactivar esta optimización. Ten en cuenta que también desactiva cualquier splicing TCP del
kernel.

Ver también: tune.pt.zero-copy-forwarding, tune.applet.zero-copy-forwarding,
tune.h1.zero-copy-fwd-recv, tune.h1.zero-copy-fwd-send, tune.h2.zero-copy-fwd-send,
tune.quic.zero-copy-fwd-send

<a id="entry-3-2-tune-epoll-mask-events"></a>

**`tune.epoll.mask-events <event[,...]>`**

```haproxy
tune.epoll.mask-events <event[,...]>
```

A lo largo de la historia de HAProxy se han encontrado algunos problemas complejos causados por
errores en el mecanismo epoll del kernel de Linux. Estos suelen ser muy raros y no reproducibles
fuera del entorno de quien los reporta, y generalmente solo pueden esquivarse desactivando epoll y
pasando a poll, lo cual no resulta muy satisfactorio para entornos de alto rendimiento. Cada vez,
los problemas afectan solo a tipos de eventos muy específicos (y raros), y ofrecer la posibilidad
de enmascararlos puede constituir una solución más aceptable. Esta opción ofrece esta posibilidad
al permitir ignorar silenciosamente algunos eventos poco comunes y reemplazarlos por una entrada
(que informa de un evento entrante no especificado). El efecto es evitar las rutas rápidas de
procesamiento de errores en ciertos lugares y usar únicamente las rutas comunes. Esto no debería
usarse nunca salvo que te invite a hacerlo un experto, para diagnosticar o esquivar un error del
kernel.

La opción toma un único argumento que es una lista de palabras separadas por comas, cada una
designando un evento a enmascarar. La lista de eventos soportados actualmente es: - "err":
enmascara el evento EPOLLERR - "hup": enmascara los eventos EPOLLHUP - "rdhup": enmascara los
eventos EPOLLRDHUP

Ejemplo:

```shell
# mask all non-traffic epoll events:
tune.epoll.mask-events err,hup,rdhup
```

<a id="entry-3-2-tune-events-max-events-at-once"></a>

**`tune.events.max-events-at-once <number>`**

```haproxy
tune.events.max-events-at-once <number>
```

Establece el número de eventos que puede procesar de una vez un gestor de tareas asíncrono (de la
API event_hdl). `<number>` debe estar entre 1 y 10000. Un número grande podría causar contención
de hilos como resultado de que la tarea haga trabajo pesado sin interrupción y, por otro lado, un
número pequeño podría provocar que la tarea se reprograme constantemente porque no puede consumir
suficientes eventos por ejecución y no es capaz de alcanzar al productor de eventos. El valor por
defecto puede forzarse en tiempo de compilación; de lo contrario, es 100.

<a id="entry-3-2-tune-fail-alloc"></a>

**`tune.fail-alloc`**

```haproxy
tune.fail-alloc
```

Si se compila con DEBUG_FAIL_ALLOC o se arranca con "-dMfail", indica el porcentaje de
probabilidades de que falle un intento de asignación. Debe estar entre 0 (sin fallos) y 100 (sin
éxitos). Esto es útil para depurar y asegurarse de que los fallos de memoria se manejan con
elegancia. Cuando no se establece, la tasa es 0. Sin embargo, la opción de línea de comandos
"-dMfail" la ajusta automáticamente a una tasa de fallo del 1% para que no sea necesario cambiar
la configuración para las pruebas.

<a id="entry-3-2-tune-fd-edge-triggered"></a>

**`tune.fd.edge-triggered { on | off }  [ EXPERIMENTAL ]`**

```haproxy
tune.fd.edge-triggered { on | off }  [ EXPERIMENTAL ]
```

Activa ('on') o desactiva ('off') el modo de sondeo disparado por flancos (edge-triggered) para
los FD que lo soporten. Actualmente solo está soportado con epoll. Puede reducir notablemente el
número de llamadas epoll_ctl() y mejorar ligeramente el rendimiento en ciertos escenarios. Sigue
siendo experimental; puede provocar conexiones congeladas si aún quedan errores, y está
desactivado por defecto.

<a id="entry-3-2-tune-glitches-kill-cpu-usage"></a>

**`tune.glitches.kill.cpu-usage <number>`**

```haproxy
tune.glitches.kill.cpu-usage <number>
```

Establece el uso mínimo de CPU, entre 0 y 100, al que se matarán las conexiones que muestren
demasiados glitches. Esto se aplica a las conexiones que han alcanzado su límite de
glitches-threshold. En entornos donde las conexiones muy largas a menudo se comportan mal sin
causar ningún impacto en el rendimiento, puede ser deseable conservarlas independientemente de su
mal comportamiento mientras no perjudiquen, y empezar a matar tales conexiones solo cuando la CPU
se vaya ocupando. Este parámetro permite especificar que una conexión que alcanza su umbral de
glitches se matará activamente cuando el uso de CPU esté en este nivel o por encima, pero nunca
por debajo. Ten en cuenta que el uso de CPU se mide por hilo, así que una única conexión que se
comporta mal podría ser matada. El valor por defecto es cero, lo que significa que una conexión
que alcanza su glitches-threshold se matará automáticamente. Una regla práctica sería establecer
este valor al doble del uso de CPU habitualmente observado, o al uso de CPU comúnmente observado
más la mitad del de inactividad (es decir, si la CPU suele llegar al 60%, establecer 80 aquí puede
tener sentido). Este parámetro no tiene efecto sin tune.h2.fe.glitches-threshold,
tune.quic.fe.sec.glitches-threshold o tune.h1.fe.glitches-threshold. Ver también los parámetros
globales "tune.h2.fe.glitches-threshold", "tune.h1.fe.glitches-threshold" y
"tune.quic.fe.sec.glitches-threshold".

<a id="entry-3-2-tune-h1-be-glitches-threshold"></a>

**`tune.h1.be.glitches-threshold <number>`**

```haproxy
tune.h1.be.glitches-threshold <number>
```

Establece el umbral para el número de glitches en una conexión de backend HTTP/1, a partir del cual
esa conexión se matará automáticamente. Esto permite matar automáticamente conexiones que se
comportan mal sin tener que escribir reglas explícitas para ellas. El valor por defecto es cero,
lo que indica que no se establece ningún umbral, de modo que ningún evento provocará el cierre de
una conexión. Los eventos típicos incluyen cabeceras mal formadas que, sin embargo, habían sido
aceptadas por "accept-unsafe-violations-in-http-response". Cualquier valor no nulo aquí
probablemente debería estar en los cientos o miles para ser efectivo sin afectar a servidores
ligeramente defectuosos. También es posible matar conexiones solo cuando el uso de CPU cruza
cierto nivel, usando "tune.glitches.kill.cpu-usage". Ten en cuenta que se intenta un cierre
graceful al 75% del umbral configurado anunciando "Connection: close" donde corresponda. Esto
asegura que una conexión ligeramente defectuosa deje de usarse al cabo de cierto tiempo sin
riesgo de interrumpir transferencias en curso.

Ver también: tune.h1.fe.glitches-threshold, bc_glitches y tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h1-fe-glitches-threshold"></a>

**`tune.h1.fe.glitches-threshold <number>`**

```haproxy
tune.h1.fe.glitches-threshold <number>
```

Establece el umbral para el número de glitches en una conexión de frontend HTTP/1, a partir del
cual esa conexión se matará automáticamente. Esto permite matar automáticamente conexiones que se
comportan mal sin tener que escribir reglas explícitas para ellas. El valor por defecto es cero,
lo que indica que no se establece ningún umbral, de modo que ningún evento provocará el cierre de
una conexión. Los eventos típicos incluyen cabeceras mal formadas que, sin embargo, habían sido
aceptadas por "accept-unsafe-violations-in-http-request". Cualquier valor no nulo aquí
probablemente debería estar en los cientos o miles para ser efectivo sin afectar a clientes
ligeramente defectuosos. También es posible matar conexiones solo cuando el uso de CPU cruza
cierto nivel, usando "tune.glitches.kill.cpu-usage". Ten en cuenta que se intenta un cierre
graceful al 75% del umbral configurado anunciando "Connection: close" donde corresponda. Esto
asegura que un cliente ligeramente no conforme tenga la oportunidad de crear una conexión nueva y
seguir funcionando sin afectarse, sin activar nunca el cierre abrupto que arriesgaría interrumpir
transferencias en curso.

Ver también: tune.h1.be.glitches-threshold, fc_glitches y tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h1-zero-copy-fwd-recv"></a>

**`tune.h1.zero-copy-fwd-recv { on | off }`**

```haproxy
tune.h1.zero-copy-fwd-recv { on | off }
```

Activa ('on') o desactiva ('off') las recepciones de copia cero de datos para el multiplexor H1.
Está activado por defecto.

Ver también: tune.disable-zero-copy-forwarding, tune.h1.zero-copy-fwd-send

<a id="entry-3-2-tune-h1-zero-copy-fwd-send"></a>

**`tune.h1.zero-copy-fwd-send { on | off }`**

```haproxy
tune.h1.zero-copy-fwd-send { on | off }
```

Activa ('on') o desactiva ('off') los envíos de copia cero de datos para el multiplexor H1. Está
activado por defecto.

Ver también: tune.disable-zero-copy-forwarding, tune.h1.zero-copy-fwd-recv

<a id="entry-3-2-tune-h2-be-glitches-threshold"></a>

**`tune.h2.be.glitches-threshold <number>`**

```haproxy
tune.h2.be.glitches-threshold <number>
```

Establece el umbral para el número de glitches en una conexión de backend, en el que esa conexión
se matará automáticamente. Esto permite matar automáticamente conexiones que se comportan mal sin
tener que escribir reglas explícitas para ellas. El valor por defecto es cero, lo que indica que
no se establece ningún umbral, de modo que ningún evento provocará el cierre de una conexión. Ten
en cuenta que algunos servidores H2 pueden ocasionalmente causar algunos glitches en conexiones de
larga duración, así que cualquier valor no nulo aquí probablemente debería estar en los cientos o
miles para ser efectivo sin afectar a servidores ligeramente defectuosos. También es posible matar
conexiones solo cuando el uso de CPU cruza cierto nivel, usando "tune.glitches.kill.cpu-usage".
Ten en cuenta que se intenta un cierre graceful al 75% del umbral configurado anunciando un GOAWAY
para un stream futuro. Esto asegura que una conexión ligeramente defectuosa deje de usarse al cabo
de cierto tiempo sin riesgo de interrumpir transferencias en curso.

Ver también: tune.h2.fe.glitches-threshold, bc_glitches y tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h2-be-initial-window-size"></a>

**`tune.h2.be.initial-window-size <number>`**

```haproxy
tune.h2.be.initial-window-size <number>
```

Establece el tamaño inicial de ventana HTTP/2 para las conexiones salientes, que es el número de
bytes que el servidor puede responder antes de esperar un reconocimiento de HAProxy. Este ajuste
solo afecta al contenido del payload, no a las cabeceras. Cuando no se establece, se aplica el
valor por defecto común definido por tune.h2.initial-window-size. Puede tener sentido aumentar
ligeramente este valor para permitir descargas más rápidas o reducir el uso de CPU en los
servidores, a costa de crear inequidad entre clientes. Es mejor usar tune.h2.be.rxbuf, que no
causa ninguna inequidad. No afecta al uso de recursos.

Ver también: tune.h2.initial-window-size.

<a id="entry-3-2-tune-h2-be-max-concurrent-streams"></a>

**`tune.h2.be.max-concurrent-streams <number>`**

```haproxy
tune.h2.be.max-concurrent-streams <number>
```

Establece el número máximo HTTP/2 de streams concurrentes por conexión saliente (es decir, el
número de peticiones pendientes en una sola conexión a un servidor). Cuando no se establece, se
aplica el valor por defecto definido por tune.h2.max-concurrent-streams. Un valor menor que el 100
por defecto puede mejorar la capacidad de respuesta de un sitio a costa de mantener más conexiones
establecidas con los servidores. Cuando el ajuste "http-reuse" está puesto a "always", se
recomienda reducir este valor para no mezclar demasiados clientes diferentes en la misma conexión,
porque si un cliente es más lento que otros, un mecanismo conocido como "head of line blocking"
tiende a causar un efecto en cascada sobre la velocidad de descarga de todos los clientes que
comparten una conexión (mantén bajo tune.h2.be.initial-window-size en este caso). Se recomienda
encarecidamente no aumentar este valor; algunos pueden encontrar óptimo funcionar con valores bajos
(típicamente 1..5).

<a id="entry-3-2-tune-h2-be-max-frames-at-once"></a>

**`tune.h2.be.max-frames-at-once <number>`**

```haproxy
tune.h2.be.max-frames-at-once <number>
```

Establece el número máximo de tramas HTTP/2 entrantes que se procesarán de una vez en una conexión
de backend. Puede ser útil establecerlo a un valor bajo (de unas decenas a unos cientos) cuando se
manejan buffers muy grandes, para mantener una latencia baja y una mejor equidad entre múltiples
conexiones. El valor por defecto es cero, lo que significa que no se impone ninguna limitación.

<a id="entry-3-2-tune-h2-be-rxbuf"></a>

**`tune.h2.be.rxbuf <size>`**

```haproxy
tune.h2.be.rxbuf <size>
```

Establece el tamaño del buffer de recepción HTTP/2 para las conexiones salientes, en bytes. Este
tamaño se redondeará hacia arriba al siguiente múltiplo de tune.bufsize y se compartirá entre
todos los streams que suben datos (tanto tramas HEADERS como DATA). En cualquier caso, siempre se
concederá un buffer a cada stream, y 7/8 de los buffers no usados se compartirán entre los streams
que descargan payload, lo que permite mejorar significativamente el rendimiento de subida y evitar
el bloqueo de cabeza de línea (HoL) en conexiones de backend compartidas entre múltiples clientes
cuando http-reuse está puesto a "always". La ventana por stream anunciada se ajusta automáticamente
para reflejar el espacio disponible, de modo que en la práctica no debería ser necesario tocar
tune.h2.be.initial-window-size. Si se establece menos que el tamaño necesario para atender todos
los streams, se usará este mínimo. El valor por defecto es unos 1600k (100 streams con buffers de
16kB cada uno).

Ver también: tune.h2.be.initial-window-size, tune.h2.fe.rxbuf, http-reuse.

<a id="entry-3-2-tune-h2-fe-glitches-threshold"></a>

**`tune.h2.fe.glitches-threshold <number>`**

```haproxy
tune.h2.fe.glitches-threshold <number>
```

Establece el umbral para el número de glitches en una conexión de frontend, en el que esa conexión
se matará automáticamente. Esto permite matar automáticamente conexiones que se comportan mal sin
tener que escribir reglas explícitas para ellas. El valor por defecto es cero, lo que indica que
no se establece ningún umbral, de modo que ningún evento provocará el cierre de una conexión. Ten
en cuenta que algunos clientes H2 pueden ocasionalmente causar algunos glitches en conexiones de
larga duración, así que cualquier valor no nulo aquí probablemente debería estar en los cientos o
miles para ser efectivo sin afectar a clientes ligeramente defectuosos. También es posible matar
conexiones solo cuando el uso de CPU cruza cierto nivel, usando "tune.glitches.kill.cpu-usage".
Ten en cuenta que se intenta un cierre graceful al 75% del umbral configurado anunciando un GOAWAY
para un stream futuro. Esto asegura que un cliente ligeramente no conforme tenga la oportunidad de
crear una conexión nueva y seguir funcionando sin afectarse, sin activar nunca el cierre abrupto
que arriesgaría interrumpir transferencias en curso.

Ver también: tune.h2.be.glitches-threshold, fc_glitches y tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h2-fe-initial-window-size"></a>

**`tune.h2.fe.initial-window-size <number>`**

```haproxy
tune.h2.fe.initial-window-size <number>
```

Establece el tamaño inicial de ventana HTTP/2 para las conexiones entrantes, que es el número de
bytes que el cliente puede subir antes de esperar un reconocimiento de HAProxy. Este ajuste solo
afecta al contenido del payload (es decir, el cuerpo de las peticiones POST), no a las cabeceras.
Cuando no se establece, se aplica el valor por defecto común definido por
tune.h2.initial-window-size. Puede tener sentido aumentar este valor para permitir subidas más
rápidas. El valor por defecto es igual a tune.bufsize (16384) y permite al menos 1.25 Mbps de
ancho de banda por stream con un ping de 100 ms, y 125 Mbps con un ping de 1 ms. No afecta al uso
de recursos. Usar valores demasiado grandes puede provocar que los clientes experimenten falta de
capacidad de respuesta si se accede a las páginas en paralelo a subidas grandes. Es mejor usar
tune.h2.fe.rxbuf, que no causa ninguna inequidad.

Ver también: tune.h2.initial-window-size.

<a id="entry-3-2-tune-h2-fe-max-concurrent-streams"></a>

**`tune.h2.fe.max-concurrent-streams <number> [args...]`**

```haproxy
tune.h2.fe.max-concurrent-streams <number> [args...]
```

Establece el número máximo HTTP/2 de streams concurrentes por conexión entrante (es decir, el
número de peticiones pendientes en una sola conexión desde un cliente). Cuando no se establece, se
aplica el valor por defecto definido por tune.h2.max-concurrent-streams. Un valor mayor que el 100
por defecto puede a veces mejorar ligeramente el tiempo de carga de página de sitios complejos con
muchos objetos pequeños sobre redes de alta latencia, pero también puede resultar en un mayor uso
de memoria al permitir que un cliente asigne más recursos de una vez. El valor por defecto de 100
generalmente es bueno y se recomienda no cambiarlo. Una concurrencia mayor también tiene un impacto
en la carga de procesamiento y la latencia cuando se manejan grandes números de conexiones que a
su vez usan muchos streams, y puede bajar la barrera frente a ataques de denegación de servicio.
El comando admite los siguientes argumentos opcionales tras el número:

- rq-load { `<number>` \| auto \| ignore }:

```text
El argumento opcional "rq-load" permite ajustar dinámicamente la
concurrencia anunciada en función de la carga de la cola de ejecución
del hilo: mientras la carga del hilo permanezca por debajo del umbral
indicado, se anunciará el límite de streams configurado. Cuando la
carga del hilo supera el límite configurado, el límite de streams
anunciado se reducirá proporcionalmente al cuadrado del cociente de
exceso. Niveles de carga objetivo entre 50 y 100 generalmente muestran
una muy buena moderación bajo cargas elevadas. Alternativamente, en
lugar de especificar un número explícito, la palabra clave acepta
"ignore", que es el valor por defecto y significa que la carga de la
cola de ejecución del hilo no se tendrá en cuenta para moderar el
límite de streams anunciado, y "auto", que fija el límite al valor de
"tune.runqueue-depth", que generalmente proporciona buenos resultados
sin tener que ajustar más la configuración.
```

- min `<number>`:

```text
Esto establece el nivel mínimo de concurrencia anunciada cuando se usa
rq-load, incluso si esto resulta en una carga mayor que el objetivo
configurado. Esto permite mantener un buen nivel de interactividad en
un sitio bajo una carga muy elevada. El valor mínimo y por defecto es
1, pero valores entre 5 y 15 pueden mejorar la experiencia de usuario.
```

Ejemplo:

```text
tune.h2.fe.max-concurrent-streams 100 rq-load auto min 15
```

<a id="entry-3-2-tune-h2-fe-max-frames-at-once"></a>

**`tune.h2.fe.max-frames-at-once <number>`**

```haproxy
tune.h2.fe.max-frames-at-once <number>
```

Establece el número máximo de tramas HTTP/2 entrantes que se procesarán de una vez en una conexión
de frontend. Puede ser útil establecerlo a un valor bajo (de unas decenas a unos cientos) cuando se
manejan buffers muy grandes, para mantener una latencia baja y una mejor equidad entre múltiples
conexiones. El valor por defecto es cero, lo que significa que no se impone ninguna limitación.

<a id="entry-3-2-tune-h2-fe-max-rst-at-once"></a>

**`tune.h2.fe.max-rst-at-once <number>`**

```haproxy
tune.h2.fe.max-rst-at-once <number>
```

Establece el número máximo de tramas RST_STREAM HTTP/2 entrantes que se procesarán de una vez en
una conexión de frontend. Una vez recibido el número especificado de tramas RST_STREAM, el gestor
de la conexión se colocará en una cola de baja prioridad y se procesará después de todas las
demás tareas. Puede ser útil establecerlo a un valor muy bajo (1 o unas pocas unidades) para
reducir significativamente el impacto de las inundaciones de RST_STREAM. Los RST_STREAM sí ocurren
cuando un usuario pulsa el botón de detener en su navegador, pero los pocos milisegundos extra
causados por esta reencolación generalmente pasan desapercibidos; sin embargo, suelen ser efectivos
para reducir significativamente la carga causada por tales inundaciones. El valor por defecto es
cero, lo que significa que no se impone ninguna limitación.

<a id="entry-3-2-tune-h2-fe-max-total-streams"></a>

**`tune.h2.fe.max-total-streams <number>`**

```haproxy
tune.h2.fe.max-total-streams <number>
```

Establece el número máximo HTTP/2 de streams totales procesados por conexión entrante. Una vez
alcanzado este límite, HAProxy enviará una trama GOAWAY graceful informando al cliente de que
cerrará la conexión después de que se hayan cerrado todos los streams pendientes. En la práctica,
los clientes tienden a cerrar tan rápido como pueden al recibirla y a establecer una conexión
nueva para las siguientes peticiones. Hacer esto a veces es útil y deseable en situaciones donde
los clientes permanecen conectados durante mucho tiempo y causan algún desequilibrio dentro de una
granja. Por ejemplo, en algunos entornos muy dinámicos es posible que se instancien nuevos
balanceadores de carga sobre la marcha para adaptarse a un aumento de carga, y que, cuando la
carga baje, deban detenerse sin romper las conexiones establecidas. Estableciendo un límite aquí,
las conexiones tendrán una vida limitada y se renovarán con frecuencia, con algunas posiblemente
establecidas hacia otros nodos, de modo que los recursos existentes se liberan rápidamente.

Es importante entender que hay una relación implícita entre este límite y
"tune.h2.fe.max-concurrent-streams" anterior. En efecto, HAProxy siempre aceptará procesar
cualquier stream pendiente que pudiera estar en vuelo entre el cliente y el frontend, así que el
límite anunciado siempre se elevará automáticamente por el valor configurado en
max-concurrent-streams, y este valor servirá como límite rígido por encima del cual una violación
por un cliente no conforme resultará en el cierre de la conexión. Así, al contar el número de
peticiones por conexión desde los registros, puede observarse cualquier número entre
max-total-streams y (max-total-streams + max-concurrent-streams) dependiendo de la rapidez con la
que el cliente cree los streams.

El valor por defecto es cero, lo que no impone ningún límite más allá de los implícitos en el
protocolo (2^30 ~= 1.07 mil millones). Valores alrededor de 1000 ya pueden provocar una renovación
frecuente de las conexiones sin causar ninguna latencia perceptible para la mayoría de los
clientes. Establecerlo demasiado bajo puede provocar un aumento del uso de CPU debido a
reconexiones TLS frecuentes, además de un mayor tiempo de carga de página. Ten en cuenta que
algunas herramientas de pruebas de carga no soportan las reconexiones y pueden informar de errores
con este ajuste; por ello puede ser necesario desactivarlo al ejecutar pruebas de rendimiento. Ver
también "tune.h2.fe.max-concurrent-streams".

<a id="entry-3-2-tune-h2-fe-rxbuf"></a>

**`tune.h2.fe.rxbuf <size>`**

```haproxy
tune.h2.fe.rxbuf <size>
```

Establece el tamaño del buffer de recepción HTTP/2 para las conexiones entrantes, en bytes. Este
tamaño se redondeará hacia arriba al siguiente múltiplo de tune.bufsize y se compartirá entre
todos los streams que suben datos (tanto tramas HEADERS como DATA). En cualquier caso, siempre se
concederá un buffer a cada stream, y 7/8 de los buffers no usados se compartirán entre los streams
que suben payload, lo que permite mejorar significativamente el rendimiento de subida. La ventana
por stream anunciada se ajusta automáticamente para reflejar el espacio disponible, de modo que en
la práctica no debería ser necesario tocar tune.h2.fe.initial-window-size. Si se establece menos
que el tamaño necesario para atender todos los streams, se usará este mínimo. El valor por defecto
de 1600k (100 streams con buffers de 16kB cada uno) permite aproximadamente 130 Mbps de velocidad
de subida para un cliente con un RTT de 100ms.

Ver también: tune.h2.fe.initial-window-size y tune.h2.be.rxbuf.

<a id="entry-3-2-tune-h2-header-table-size"></a>

**`tune.h2.header-table-size <number>`**

```haproxy
tune.h2.header-table-size <number>
```

Establece el tamaño de la tabla dinámica de cabeceras HTTP/2. Por defecto es de 4096 bytes y no
puede ser mayor de 65536 bytes. Un valor mayor puede ayudar a ciertos clientes a enviar peticiones
más compactas, dependiendo de sus capacidades. Esta cantidad de memoria se consume para cada
conexión HTTP/2. Se recomienda no cambiarla.

<a id="entry-3-2-tune-h2-initial-window-size"></a>

**`tune.h2.initial-window-size <number>`**

```haproxy
tune.h2.initial-window-size <number>
```

Establece el valor por defecto del tamaño inicial de ventana HTTP/2, tanto para las conexiones
entrantes como para las salientes. Este valor se usa para las conexiones entrantes cuando
tune.h2.fe.initial-window-size no está establecido, y por las salientes cuando
tune.h2.be.initial-window-size no está establecido. Este ajuste se usa tanto como valor inicial
como mínimo por stream. El valor por defecto es igual a 16384 (tune.bufsize), lo que para las
subidas permite aproximadamente al menos 1.25 Mbps de ancho de banda por stream sobre una red con
un ping de 100 ms, o 125 Mbps sobre una red local de 1 ms. Cuando se usan menos buffers de
recepción que el máximo, dentro de los límites definidos por tune.h2.be.rxbuf y tune.h2.fe.rxbuf,
los buffers no usados se compartirán entre los streams receptores. Como tal, normalmente no tiene
sentido cambiar este ajuste por defecto. Dado que cambiar este valor por defecto aumentará tanto
las velocidades de subida como la inequidad entre clientes en las descargas, se recomienda usar en
su lugar los ajustes específicos por lado tune.h2.fe.initial-window-size y
tune.h2.be.initial-window-size.

<a id="entry-3-2-tune-h2-log-errors"></a>

**`tune.h2.log-errors { none | connection | stream }`**

```haproxy
tune.h2.log-errors { none | connection | stream }
```

Establece el nivel de errores en el demultiplexor H2 que generarán un registro. El valor por
defecto es "stream", lo que significa que cualquier error de decodificación encontrado en el
demultiplexor provocará la emisión de un registro. El valor "connection" indica que solo los
errores que resultan en la invalidación de la conexión producirán un registro. Finalmente, "none"
indica que ningún error de decodificación producirá registro alguno. Se recomienda establecer al
menos "connection" para detectar anomalías del protocolo, incluso si ello significa pasar
temporalmente a "none" durante periodos difíciles.

<a id="entry-3-2-tune-h2-max-concurrent-streams"></a>

**`tune.h2.max-concurrent-streams <number>`**

```haproxy
tune.h2.max-concurrent-streams <number>
```

Establece el número máximo HTTP/2 por defecto de streams concurrentes por conexión (es decir, el
número de peticiones pendientes en una sola conexión). Este valor se usa para las conexiones
entrantes cuando tune.h2.fe.max-concurrent-streams no está establecido, y para las salientes
cuando tune.h2.be.max-concurrent-streams no está establecido. El valor por defecto es 100. El
impacto varía según el lado, así que consulta los dos ajustes anteriores para más detalles. Se
recomienda no usar este ajuste y pasar a los específicos por lado. Un valor de cero desactiva el
límite, de modo que un único cliente puede crear tantos streams como HAProxy pueda asignar. Se
recomienda encarecidamente no cambiar este valor.

<a id="entry-3-2-tune-h2-max-frame-size"></a>

**`tune.h2.max-frame-size <number>`**

```haproxy
tune.h2.max-frame-size <number>
```

Establece el tamaño máximo de trama HTTP/2 que HAProxy anuncia estar dispuesto a recibir de sus
pares. El valor por defecto es el mayor entre 16384 y el tamaño del buffer (tune.bufsize). En
cualquier caso, HAProxy no anunciará soporte para tamaños de trama mayores que los buffers. El
propósito principal de este ajuste es permitir limitar el tamaño máximo de trama cuando se usan
buffers grandes. Tamaños de trama demasiado grandes podrían repercutir en el rendimiento o
provocar que algunos pares se comporten mal. Se recomienda encarecidamente no cambiar este valor.

<a id="entry-3-2-tune-h2-zero-copy-fwd-send"></a>

**`tune.h2.zero-copy-fwd-send { on | off }`**

```haproxy
tune.h2.zero-copy-fwd-send { on | off }
```

Activa ('on') o desactiva ('off') los envíos de copia cero de datos para el multiplexor H2. Está
activado por defecto.

Ver también: tune.disable-zero-copy-forwarding

<a id="entry-3-2-tune-http-cookielen"></a>

**`tune.http.cookielen <number>`**

```haproxy
tune.http.cookielen <number>
```

Establece la longitud máxima de las cookies capturadas. Este es el valor máximo que se permitirá
tomar a "capture cookie xxx len yyy", y cualquier valor superior se truncará automáticamente a
este. Es importante no establecer un valor demasiado alto porque todas las capturas de cookies
siguen asignando este tamaño sea cual sea su valor configurado (comparten un mismo pool). Este
valor es por petición y por respuesta, así que la memoria asignada es el doble de este valor por
conexión. Cuando no se especifica, el límite se establece en 63 caracteres. Se recomienda no
cambiar este valor.

<a id="entry-3-2-tune-http-logurilen"></a>

**`tune.http.logurilen <number>`**

```haproxy
tune.http.logurilen <number>
```

Establece la longitud máxima del URI de petición en los registros. Esto evita truncar URIs de
petición largos con cadenas de consulta valiosas en las líneas de registro. No está relacionado
con los límites de syslog. Si aumentas este límite, puedes aumentar también el parámetro
'log ... len yyy'. Tu demonio syslog puede necesitar también directivas de configuración
específicas. El valor por defecto es 1024.

<a id="entry-3-2-tune-http-maxhdr"></a>

**`tune.http.maxhdr <number>`**

```haproxy
tune.http.maxhdr <number>
```

Establece el número máximo de cabeceras permitidas en los mensajes HTTP recibidos. Cuando un
mensaje llega con un número de cabeceras mayor que este valor (incluida la primera línea), se
rechaza con un código de estado "400 Bad Request" para una petición, o "502 Bad Gateway" para una
respuesta. El valor por defecto es 101, que es suficiente para todos los usos, considerando que el
ampliamente desplegado servidor Apache usa el mismo límite. Puede ser útil aumentar este límite
para permitir temporalmente que funcione una aplicación defectuosa mientras se corrige. El rango
aceptado es 1..32767. Ten en mente que cada cabecera nueva consume 32bits de memoria por cada
stream, así que no subas demasiado este límite.

Nota: HTTP/1.1 es un protocolo de texto, así que no hay un límite especial al enviar el mensaje.
El límite durante el análisis del mensaje es suficiente. HTTP/2 y HTTP/3 son protocolos binarios y
requieren un paso de codificación. También se establece un límite cuando se codifican las
cabeceras para cumplir las limitaciones impuestas por los protocolos. Este límite es lo bastante
grande pero no está documentado a propósito. Se aplica el mismo límite en los primeros pasos de la
decodificación por la misma razón.

<a id="entry-3-2-tune-idle-pool-shared"></a>

**`tune.idle-pool.shared { full | on | off }`**

```haproxy
tune.idle-pool.shared { full | on | off }
```

Controla el compartir pools de conexiones inactivas entre hilos para un mismo servidor. Puede
activarse para todos los hilos de un mismo grupo de hilos ('on'), activarse para todos los hilos
('full') o desactivarse ('off'). Por defecto se comparten entre los hilos del mismo grupo de hilos
('on'), para minimizar el número de conexiones persistentes a un servidor y optimizar la tasa de
reutilización de conexiones. Compartir con hilos de otros grupos de hilos puede repercutir en el
rendimiento y no está activado por defecto, pero puede ser útil si maximizar la reutilización de
conexiones es una prioridad. Para ayudar a depurar, o cuando se sospecha de un error de HAProxy en
torno a la reutilización de conexiones, puede ser conveniente desactivar forzosamente este uso
compartido del pool inactivo entre múltiples hilos, forzando esta opción a "off". Se recomienda
encarecidamente no desactivar esta opción sin establecer un valor conservador en "pool-low-conn"
para todos los servidores que dependan de la reutilización de conexiones para lograr un alto nivel
de rendimiento; de lo contrario, las conexiones podrían cerrarse muy a menudo a medida que aumenta
el número de hilos.

<a id="entry-3-2-tune-idletimer"></a>

**`tune.idletimer <timeout>`**

```haproxy
tune.idletimer <timeout>
```

Establece la duración tras la cual HAProxy considerará que un buffer vacío está probablemente
asociado a un stream inactivo. Esto se usa para ajustar óptimamente algunos tamaños de paquete al
reenviar alternativamente datos grandes y pequeños. La decisión de usar splice() o de enviar
buffers grandes en SSL está modulada por este parámetro. El valor está en milisegundos, entre 0 y
65535. Un valor de cero significa que HAProxy no intentará detectar streams inactivos. El valor
por defecto es 1000, lo que parece detectar correctamente las pausas del usuario final (por
ejemplo, leer una página antes de hacer clic). No debería haber razón para cambiar este valor.
Consulta tune.ssl.maxrecord más abajo.

<a id="entry-3-2-tune-listener-default-shards"></a>

**`tune.listener.default-shards { by-process | by-thread | by-group }`**

```haproxy
tune.listener.default-shards { by-process | by-thread | by-group }
```

Normalmente, todas las líneas "bind" crearán un único shard, es decir, un único socket al que
escucharán todos los hilos del proceso. Con muchos hilos esto no es muy eficiente, e incluso puede
inducir cierta sobrecarga importante en el kernel para actualizar el estado del sondeo o incluso
distribuir eventos a los distintos hilos. Los sistemas operativos modernos soportan el balanceo de
conexiones entrantes, un mecanismo que consiste en permitir que múltiples sockets se vinculen a la
misma dirección y puerto, y en repartir uniformemente todas las conexiones entrantes entre estos
sockets, de modo que cada hilo solo vea las conexiones que esperan en el socket al que está
vinculado. Esto reduce significativamente la sobrecarga del lado del kernel y aumenta el
rendimiento en la ruta de conexiones entrantes. En HAProxy esto normalmente se activa con el
ajuste "shards" en las líneas "bind", cuyo valor por defecto es 1, lo que significa que cada
listener será único en el proceso. En sistemas con muchos procesadores puede ser más cómodo
cambiar el ajuste por defecto a "by-thread" para crear siempre un socket de escucha por hilo, o
"by-group" para crear siempre un socket de escucha por grupo de hilos. Ten cuidado con el uso de
descriptores de archivo con "by-thread", ya que cada listener necesitará tantos sockets como hilos
haya. Además, algunos sistemas operativos (por ejemplo FreeBSD) están limitados a no más de 256
sockets en una misma dirección. Ten en cuenta que "by-group" seguirá siendo equivalente a
"by-process" para las configuraciones por defecto con un único grupo de hilos, y recurrirá a
compartir el mismo socket en sistemas que no soportan este mecanismo. El valor por defecto es
"by-group" con repliegue a "by-process" para sistemas o familias de sockets que no soportan
bindings múltiples.

<a id="entry-3-2-tune-listener-multi-queue"></a>

**`tune.listener.multi-queue { on | fair | off }`**

```haproxy
tune.listener.multi-queue { on | fair | off }
```

Activa ('on' / 'fair') o desactiva ('off') la aceptación multi-cola del listener, que reparte el
tráfico entrante entre todos los hilos en los que una línea "bind" puede ejecutarse, en lugar de
quedárselo para sí. Esto proporciona una distribución del tráfico más suave y escala mucho mejor,
especialmente en entornos donde los hilos pueden estar cargados de forma desigual por actividad
externa (interrupciones de red colisionando con un hilo, por ejemplo). El modo por defecto, "on",
optimiza la elección de un hilo escogiendo en una muestra el que menos conexiones tiene. A menudo
es la mejor elección cuando las conexiones son longevas, ya que consigue mantener todos los hilos
ocupados. Un segundo modo, "fair", en cambio recorre todos los hilos independientemente de su
nivel de carga instantáneo. Puede ajustarse mejor a conexiones cortas, o en máquinas con números
muy grandes de hilos donde la probabilidad de encontrar el hilo menos cargado con el primer modo
es baja. Finalmente, es posible desactivar forzosamente el mecanismo de redistribución usando
"off" para resolver problemas, o en situaciones donde las conexiones son cortas y se estima que el
sistema operativo ya proporciona una distribución suficientemente buena. El valor por defecto es
"on".

<a id="entry-3-2-tune-lua-bool-sample-conversion"></a>

**`tune.lua.bool-sample-conversion { normal | pre-3.1-bug }`**

```haproxy
tune.lua.bool-sample-conversion { normal | pre-3.1-bug }
```

Indica explícitamente a haproxy cómo deben manejarse los objetos sample de haproxy cuando se pasan
a Lua. En efecto, al usar convertidores nativos, sample fetches o variables desde un script Lua
(por citar algunos), haproxy convierte el tipo smp interno al tipo Lua equivalente. Debido a la
implementación histórica, hay una ambigüedad en torno al manejo de los booleanos: al hacer la
conversión Lua -\> haproxy smp, los booleanos se preservan correctamente, pero al hacer la
conversión haproxy smp -\> Lua, los booleanos se convertían por error en enteros. Esto significa
que un sample fetch o convertidor que devuelve un booleano devolvería un entero 0 o 1 cuando se
usa desde Lua. Desafortunadamente, en Lua los booleanos y los enteros no son intercambiables. Así,
para evitar ambigüedades, "tune.lua.bool-sample-conversion" debe establecerse explícitamente a
"normal" (lo que significa descartar el comportamiento histórico en favor de una mejor
consistencia) o "pre-3.1-bug" (imponer el comportamiento histórico para evitar que la lógica de
los scripts existentes se comporte mal). Si la opción no se establece explícitamente y se carga un
script Lua desde la configuración, haproxy emitirá una advertencia, y la opción tomará
implícitamente el valor por defecto "pre-3.1-bug" para coincidir con el comportamiento histórico.
Se recomienda establecer esta opción a "normal" tras asegurarse de que los scripts Lua en uso
manejan correctamente como booleanos los samples booleanos de haproxy.

Este ajuste debe establecerse antes que cualquier directiva "lua-load" o "lua-load-per-thread" para
que se tenga en cuenta; de lo contrario, se ignora.

<a id="entry-3-2-tune-lua-burst-timeout"></a>

**`tune.lua.burst-timeout <timeout>`**

```haproxy
tune.lua.burst-timeout <timeout>
```

El tiempo de espera de ejecución "burst" se aplica a cualquier handler Lua. Si el handler no
termina o no cede (yield) antes de que se alcance el tiempo de espera, se abortará para evitar la
contención de hilos, para evitar que el tráfico deje de atenderse durante demasiado tiempo y, en
última instancia, para evitar que el proceso caiga por la intervención del watchdog. A diferencia
de otros tiempos de espera de lua, que son acumulativos por yield, burst-timeout garantiza que el
tiempo pasado en una sola ventana de ejecución de lua no exceda el tiempo de espera configurado.

Ceder (yield) aquí significa que la ejecución de lua se interrumpe efectivamente, bien mediante
una llamada explícita a una función de lua que cede, como core.(m)sleep() o core.yield(), o tras
un forced-yield automático (ver tune.lua.forced-yield), y que se reanudará más tarde cuando la
tarea correspondiente quede programada para reejecución. No todos los handlers de lua pueden
ceder: hay que distinguir entre handlers aptos para yield y handlers no aptos para yield.

Para los handlers aptos para yield (tasks, actions...), alcanzar el tiempo de espera significa que
"tune.lua.forced-yield" podría ser demasiado alto para el sistema; reducirlo podría mejorar la
situación, pero también podría ser buena idea comprobar si añadir yields manuales en algunos
puntos clave dentro de la función lua ayuda o no. También podría indicar que el handler pasa
demasiado tiempo en una función de biblioteca lua concreta que no puede interrumpirse.

Para los handlers no aptos para yield (convertidores lua, sample fetches), podría simplemente
indicar que el handler hace demasiada computación, lo que podría deberse a un diseño inadecuado,
dado que se espera que tales handlers, que a menudo bloquean el flujo de ejecución de la petición,
terminen rápidamente para permitir que el procesamiento de la petición continúe. Un enfoque de
resolución común aquí sería intentar optimizar mejor la función lua para ganar velocidad, ya que
disminuir "tune.lua.forced-yield" no ayudará.

Este tiempo de espera solo cuenta el tiempo puro de ejecución de Lua. Si el Lua hace un core.sleep,
el tiempo de dormido no se tiene en cuenta. El tiempo de espera por defecto es 1000ms.

Nota: si un ciclo de GC de lua se inicia desde el handler (bien solicitado explícitamente o
activado automáticamente por lua tras cierto tiempo), el tiempo del ciclo de GC también se
contabilizará.

En efecto, no hay forma de deducir el tiempo del ciclo de GC, así que esto podría llevar a algunos
falsos positivos en sistemas saturados (donde el GC tiene dificultades para ponerse al día y
consume la mayor parte del tiempo de ejecución disponible). Si ese fuera el caso, he aquí algunas
pistas de resolución:

    - comprobar si el script podría optimizarse para reducir el uso de memoria de lua
    - ajustar los parámetros del GC de lua y/o solicitar ciclos de GC manuales
      (ver: https://www.lua.org/manual/5.4/manual.html#pdf-collectgarbage)
    - aumentar tune.lua.burst-timeout

Establecer el valor a 0 desactiva completamente esta protección.

<a id="entry-3-2-tune-lua-forced-yield"></a>

**`tune.lua.forced-yield <number>`**

```haproxy
tune.lua.forced-yield <number>
```

Esta directiva fuerza al motor Lua a ejecutar un yield cada `<number>` instrucciones ejecutadas.
Esto permite interrumpir un script largo y permite al planificador de HAProxy procesar otras
tareas, como aceptar conexiones o reenviar tráfico. El valor por defecto es 10000 instrucciones
para los scripts cargados con "lua-load-per-thread" y MAX(500, 10000 / nbthread) instrucciones
para los scripts cargados con "lua-load" (se encontró que era un valor óptimo para el rendimiento,
cuidando de no crear contención de hilos con múltiples hilos compitiendo por el lock global de
lua).

Si HAProxy ejecuta a menudo código Lua pero se requiere más capacidad de respuesta, este valor
puede reducirse. Si el código Lua es bastante largo y su resultado es absolutamente necesario para
procesar los datos, el `<number>` puede aumentarse, pero el valor debería establecerse con
criterio, ya que en un contexto multihilo podría aumentar la contención.

<a id="entry-3-2-tune-lua-log-loggers"></a>

**`tune.lua.log.loggers { on | off }`**

```haproxy
tune.lua.log.loggers { on | off }
```

Activa ('on') o desactiva ('off') el registro de la salida de los scripts LUA mediante los loggers
aplicables al proxy actual, si los hay.

Por defecto, 'on'.

<a id="entry-3-2-tune-lua-log-stderr"></a>

**`tune.lua.log.stderr { on | auto | off }`**

```haproxy
tune.lua.log.stderr { on | auto | off }
```

Activa ('on') o desactiva ('off') el registro de la salida de los scripts LUA mediante stderr.
Cuando se pone a 'auto', el registro vía stderr está condicionalmente 'on' si se cumple alguna de
estas condiciones:

    - tune.lua.log.loggers está puesto a 'off'
    - el script se ejecuta en un contexto ajeno al proxy sin ningún logger global
    - el script se ejecuta en un contexto de proxy sin ningún logger adjunto

Ten en cuenta que, cuando está activado, este registro se añade al registro configurado mediante
tune.lua.log.loggers.

Por defecto, 'auto'.

<a id="entry-3-2-tune-lua-maxmem"></a>

**`tune.lua.maxmem <number>`**

```haproxy
tune.lua.maxmem <number>
```

Establece la cantidad máxima de RAM en megabytes por proceso utilizable por Lua. Por defecto es
cero, lo que significa ilimitado. Es importante establecer un límite para asegurar que un error en
un script no provoque que el sistema se quede sin memoria.

<a id="entry-3-2-tune-lua-openlibs"></a>

**`tune.lua.openlibs [all | none | <lib>[,<lib>...]]`**

```haproxy
tune.lua.openlibs [all | none | <lib>[,<lib>...]]
```

Selecciona qué bibliotecas estándar de Lua se cargan al inicializar el estado de Lua. El argumento
es una lista de nombres de bibliotecas separados por comas tomada del siguiente conjunto: table,
io, os, string, math, utf8, package, debug. Pueden usarse los valores especiales "all" y "none" en
lugar de una lista. "none" no puede combinarse con nombres de bibliotecas. El valor por defecto es
"all".

Las bibliotecas base y coroutine siempre se cargan independientemente de este ajuste: base
proporciona las funciones núcleo de Lua de las que HAProxy depende, y coroutine es necesaria
porque HAProxy sobrescribe coroutine.create() con su propia implementación segura.

Ten en cuenta que fork() y la creación de hilos nuevos ya están bloqueados por defecto en HAProxy
independientemente de este ajuste, y solo pueden reactivarse mediante la directiva global
"insecure-fork-wanted". Restringir el conjunto de bibliotecas cargadas reduce aún más la superficie
de ataque expuesta a los scripts Lua. En particular: - omitir "os" impide os.execute() y os.exit() - omitir "io" impide io.open() y io.popen() - omitir "package" impide cargar módulos C nativos vía
require() - omitir "debug" impide la introspección de los internos de HAProxy vía
debug.getupvalue(), debug.getmetatable() o debug.sethook()

Ejemplos:

```text
tune.lua.openlibs none                    # only base + coroutine
tune.lua.openlibs string,math,table,utf8  # safe subset, no I/O or OS
tune.lua.openlibs all                     # default, load everything
```

Este ajuste debe establecerse antes que cualquier directiva "lua-load", "lua-load-per-thread" o
"lua-prepend-path"; de lo contrario, se devuelve un error de análisis.

<a id="entry-3-2-tune-lua-service-timeout"></a>

**`tune.lua.service-timeout <timeout>`**

```haproxy
tune.lua.service-timeout <timeout>
```

Este es el tiempo de espera de ejecución para los servicios Lua. Es útil para prevenir bucles
infinitos o un exceso de tiempo pasado en Lua. Este tiempo de espera cuenta solo el tiempo puro de
ejecución de Lua. Si el Lua hace un sleep, el tiempo de sleep no se tiene en cuenta. El tiempo de
espera por defecto es 4s.

<a id="entry-3-2-tune-lua-session-timeout"></a>

**`tune.lua.session-timeout <timeout>`**

```haproxy
tune.lua.session-timeout <timeout>
```

Este es el tiempo de espera de ejecución para las sesiones Lua. Es útil para prevenir bucles
infinitos o un exceso de tiempo pasado en Lua. Este tiempo de espera cuenta solo el tiempo puro de
ejecución de Lua. Si el Lua hace un sleep, el tiempo de sleep no se tiene en cuenta. El tiempo de
espera por defecto es 4s.

<a id="entry-3-2-tune-lua-task-timeout"></a>

**`tune.lua.task-timeout <timeout>`**

```haproxy
tune.lua.task-timeout <timeout>
```

El propósito es el mismo que "tune.lua.session-timeout", pero este tiempo de espera está dedicado
a las tareas. Por defecto, este tiempo de espera no está establecido porque una tarea puede
permanecer viva durante la vida de HAProxy. Por ejemplo, una tarea usada para comprobar
servidores.

<a id="entry-3-2-tune-max-checks-per-thread"></a>

**`tune.max-checks-per-thread <number>`**

```haproxy
tune.max-checks-per-thread <number>
```

Establece el número de comprobaciones activas por hilo por encima del cual un hilo intentará
activamente buscar un hilo menos cargado en el que ejecutar la comprobación de salud, o la
encolará hasta que disminuya el número de comprobaciones activas ejecutándose en él. El valor por
defecto es cero, lo que significa que no se establece tal límite. Puede ser necesario en ciertos
entornos que ejecutan un número extremadamente grande de comprobaciones costosas con muchos hilos,
cuando la carga aparece desigual y puede hacer que las comprobaciones de salud agoten el tiempo de
espera aleatoriamente al arrancar, típicamente al usar OpenSSL 3.0, que es unas 20 veces más
intensiva en CPU para las comprobaciones de salud que las versiones antiguas. El resultado será
intentar nivelar el trabajo de comprobación de salud entre todos los hilos. La gran mayoría de las
configuraciones no necesitan tocar este parámetro. Ten en cuenta que valores demasiado bajos
pueden ralentizar significativamente las comprobaciones de salud si estas son lentas de ejecutar.

<a id="entry-3-2-tune-maxaccept"></a>

**`tune.maxaccept <number>`**

```haproxy
tune.maxaccept <number>
```

Establece el número máximo de conexiones consecutivas que un proceso puede aceptar seguidas antes
de pasar a otro trabajo. En modo de proceso único, los números más altos solían dar mejor
rendimiento con tasas de conexión altas, aunque esto ya no es así con la multi-cola. Este valor se
aplica individualmente a cada listener, de modo que se tiene en cuenta el número de procesos a los
que está vinculado un listener. Este valor por defecto es 4, que mostró los mejores resultados. Si
un valor significativamente más alto se heredó de una configuración antigua, puede valer la pena
eliminarlo, ya que aumentará el rendimiento y reducirá el tiempo de respuesta. En modo
multiproceso se divide por el doble del número de procesos a los que está vinculado el listener.
Establecer este valor a -1 desactiva completamente la limitación. Normalmente no debería hacer
falta ajustar este valor.

<a id="entry-3-2-tune-maxpollevents"></a>

**`tune.maxpollevents <number>`**

```haproxy
tune.maxpollevents <number>
```

Establece la cantidad máxima de eventos que pueden procesarse de una vez en una llamada al sistema
de sondeo. El valor por defecto está adaptado al sistema operativo. Se ha notado que reducirlo por
debajo de 200 tiende a disminuir ligeramente la latencia a costa del ancho de banda de red, y
aumentarlo por encima de 200 tiende a cambiar latencia por un ancho de banda ligeramente mayor. El
valor configurado debe ser menor o igual que 1000000.

<a id="entry-3-2-tune-maxrewrite"></a>

**`tune.maxrewrite <number>`**

```haproxy
tune.maxrewrite <number>
```

Establece el espacio de buffer reservado a este tamaño en bytes. El espacio reservado se usa para
reescribir o añadir cabeceras. Las primeras lecturas en los sockets nunca llenarán más de
bufsize-maxrewrite. Históricamente su valor por defecto ha sido la mitad de bufsize, aunque eso no
tiene mucho sentido, ya que rara vez hay grandes números de cabeceras que añadir. Establecerlo
demasiado alto impide el procesamiento de peticiones o respuestas grandes. Establecerlo demasiado
bajo impide añadir cabeceras nuevas a peticiones ya grandes o a peticiones POST. Generalmente es
sensato establecerlo a unos 1024. Se reajusta automáticamente a la mitad de bufsize si es mayor
que eso. Esto significa que no tienes que preocuparte por ello al cambiar bufsize.

<a id="entry-3-2-tune-max-rules-at-once"></a>

**`tune.max-rules-at-once <number>`**

```haproxy
tune.max-rules-at-once <number>
```

Establece el número máximo de reglas que pueden evaluarse de una vez en las funciones de
evaluación de conjuntos de reglas, siempre que soporten yielding. En efecto, no es raro ver
configuraciones con un gran número de reglas "tcp-request content" o "http-request", por ejemplo.
Un gran número de reglas combinado con acciones exigentes de CPU (por ejemplo: acciones que
trabajan sobre contenido) puede crear contención de hilos, ya que todas las reglas de un conjunto
dado se evalúan bajo el mismo bucle de sondeo si la evaluación no se interrumpe. Esta opción
asegura que no se ejecuten más de `<number>` reglas bajo el mismo bucle de sondeo para los
conjuntos de reglas orientados a contenido (los que ya soportan yielding debido a la inspección de
contenido). Lo que hace es forzar que la función de evaluación ceda (yield), de modo que vuelve en
el siguiente bucle de sondeo para continuar la evaluación.

Los conjuntos de reglas afectados son:

- "tcp-request content"
- "tcp-response content"
- "http-request"
- "http-response"

El valor por defecto es 50.

<a id="entry-3-2-tune-memory-hot-size"></a>

**`tune.memory.hot-size <number>`**

```haproxy
tune.memory.hot-size <number>
```

Establece la cantidad de memoria por hilo que se mantendrá caliente (hot) en la caché local y que
nunca podrá ser recuperada por otros hilos. El acceso a esta memoria es muy rápido (sin locks), y
disponer de la suficiente es crítico para mantener un buen nivel de rendimiento bajo contención
extrema de hilos. El valor se expresa en bytes y el valor por defecto se configura en tiempo de
compilación vía CONFIG_HAP_POOL_CACHE_SIZE, cuyo valor por defecto es 524288 (512 kB). Un valor
mayor puede aumentar el rendimiento en algunos escenarios de uso, especialmente cuando los perfiles
de rendimiento muestran que la asignación de memoria está muy estresada. La experiencia muestra que
un buen valor se sitúa entre una y dos veces el tamaño de la caché L2 por núcleo de CPU. Valores
demasiado grandes tendrán un impacto negativo en el rendimiento al hacer un uso ineficiente de las
cachés L3 de las CPU, y consumirán mayores cantidades de memoria. Se recomienda no cambiar este
valor, o hacerlo en pequeños incrementos. Para desactivar completamente las cachés por hilo de CPU,
usar un valor muy pequeño podría funcionar, pero es mejor usar "-dMno-cache" en la línea de
comandos.

<a id="entry-3-2-tune-notsent-lowat-client"></a>

**`tune.notsent-lowat.client <size>`**

```haproxy
tune.notsent-lowat.client <size>
tune.notsent-lowat.server <size>
```

Ajusta el bufferizado por socket del kernel para informar de que el lado de envío de un socket está
lleno una vez que la cantidad de datos en buffer iguala este valor más el tamaño de ventana medido.
El principio es dejar en los buffers del socket el mínimo estricto de bytes necesarios, más un
pequeño margen correspondiente a lo que se enviaría para cuando haproxy intente enviar de nuevo.
Establecerlo a un valor bajo (típicamente alrededor de tune.bufsize) permite reducir
significativamente el consumo de memoria en los buffers del sistema y reducir la latencia a nivel
de aplicación incurrida al vaciar los datos bufferizados. Esto generalmente representa un ajuste
más efectivo y más preciso que tune.sndbuf.client y tune.sndbuf.client para los sistemas que lo
soportan. Se aplica por conexión (conexión desde un cliente o conexión a un servidor según el
ajuste) y solo lo usan las conexiones TCP. El valor por defecto es cero, lo que significa
ilimitado. Esto solo está disponible en Linux.

<a id="entry-3-2-tune-pattern-cache-size"></a>

**`tune.pattern.cache-size <number>`**

```haproxy
tune.pattern.cache-size <number>
```

Establece el tamaño de la caché de búsqueda de patrones en `<number>` entradas. Es una caché LRU
que recuerda búsquedas anteriores y sus resultados. La usan las ACL y los maps en búsquedas de
patrones lentas, concretamente las que usan los métodos de coincidencia "sub", "reg", "dir", "dom",
"end", "bin", así como las cadenas insensibles a mayúsculas. Se aplica a expresiones de patrones,
lo que significa que podrá memorizar el resultado de una búsqueda entre todos los patrones
especificados en una línea de configuración (incluidos todos los cargados desde archivos). Invalida
automáticamente las entradas que se actualizan mediante acciones HTTP o en la CLI. El tamaño de
caché por defecto se establece en 10000 entradas, lo que limita su huella a unos 5 MB por
proceso/hilo en sistemas de 32 bits y 8 MB por proceso/hilo en sistemas de 64 bits, ya que las
cachés son locales a cada hilo/proceso. Hay un riesgo de colisión muy bajo en esta caché, del orden
del tamaño de la caché dividido por 2^64. Típicamente, a 10000 peticiones por segundo con el tamaño
de caché por defecto de 10000 entradas, hay un 1% de probabilidad de que un ataque de fuerza bruta
pueda causar una sola colisión después de 60 años, o un 0.1% después de 6 años. Esto se considera
mucho más bajo que el riesgo de corrupción de memoria causada por componentes envejecidos. Si esto
no es aceptable, la caché puede desactivarse estableciendo este parámetro a 0.

<a id="entry-3-2-tune-peers-max-updates-at-once"></a>

**`tune.peers.max-updates-at-once <number>`**

```haproxy
tune.peers.max-updates-at-once <number>
```

Establece el número máximo de actualizaciones de stick-table que haproxy intentará procesar de una
vez al enviar mensajes. Recuperar los datos de estas actualizaciones requiere algunas operaciones de
bloqueo que pueden ser intensivas en CPU en máquinas con muchos hilos si no están limitadas, y
también puede aumentar la latencia del tráfico durante la transferencia inicial por lotes entre un
proceso más antiguo y uno más nuevo. A la inversa, valores bajos también pueden incurrir en mayor
sobrecarga de CPU y tardar más en completarse. El valor por defecto es 200 y se sugiere no
cambiarlo.

<a id="entry-3-2-tune-pipesize"></a>

**`tune.pipesize <size>`**

```haproxy
tune.pipesize <size>
```

Establece el tamaño del buffer de pipe del kernel a este tamaño (en bytes). Por defecto, los pipes
tienen el tamaño por defecto del sistema. Pero a veces, al usar splicing TCP, puede mejorar el
rendimiento aumentar los tamaños de pipe, especialmente si se sospecha que los pipes no se llenan y
que se realizan muchas llamadas a splice(). Esto repercute en la huella de memoria del kernel, así
que no debe cambiarse si no se entienden los impactos.

<a id="entry-3-2-tune-pool-high-fd-ratio"></a>

**`tune.pool-high-fd-ratio <number>`**

```haproxy
tune.pool-high-fd-ratio <number>
```

Este ajuste establece el número máximo de descriptores de archivo (en porcentaje) usados por HAProxy
globalmente respecto al número máximo de descriptores de archivo que HAProxy puede usar, antes de
que empecemos a matar conexiones inactivas cuando no podamos reutilizar una conexión y tengamos que
crear una nueva. El valor por defecto es 25 (un cuarto de los descriptores de archivo significará
que aproximadamente la mitad de las conexiones máximas del frontend pueden mantener detrás una
conexión inactiva; cualquier valor superior probablemente no tenga mucho sentido en el caso general
cuando se persigue la reutilización de conexiones).

<a id="entry-3-2-tune-pool-low-fd-ratio"></a>

**`tune.pool-low-fd-ratio <number>`**

```haproxy
tune.pool-low-fd-ratio <number>
```

Este ajuste establece el número máximo de descriptores de archivo (en porcentaje) usados por HAProxy
globalmente respecto al número máximo de descriptores de archivo que HAProxy puede usar, antes de
que dejemos de poner conexiones en el pool de inactivas para su reutilización. El valor por defecto
es 20.

<a id="entry-3-2-tune-pt-zero-copy-forwarding"></a>

**`tune.pt.zero-copy-forwarding { on | off }`**

```haproxy
tune.pt.zero-copy-forwarding { on | off }
```

Activa ('on') o desactiva ('off') el reenvío de copia cero de datos para el multiplexor de paso
(pass-through). Para poder usarse, el splicing del kernel también debe estar configurado. Está
activado por defecto.

Ver también: tune.disable-zero-copy-forwarding, option splice-auto, option splice-request y option
splice-response

<a id="entry-3-2-tune-quic-be-cc-cubic-min-losses"></a>

**`tune.quic.be.cc.cubic-min-losses <number>`**

```haproxy
tune.quic.be.cc.cubic-min-losses <number>
tune.quic.fe.cc.cubic-min-losses <number>
```

Define cuántos paquetes perdidos se necesitan para que el algoritmo de control de congestión Cubic
considere realmente un evento de pérdida. Normalmente, cualquier evento de pérdida se considera el
resultado de una congestión y es suficiente para que Cubic se reinicie con una ventana más pequeña.
Pero los experimentos muestran que puede haber una variedad de causas de pérdidas que no se deben en
absoluto a una congestión y que simplemente pueden calificarse de pérdidas espurias, y para las
cuales ajustar la ventana no tendrá ningún efecto, salvo ralentizar la comunicación. Una señal de
radio deficiente, la entrega fuera de orden, un uso alto de CPU en un cliente que causa retrasos
aleatorios, así como la imprecisión del temporizador del sistema, pueden estar entre las causas
comunes de esto. Este ajuste permite hacer a Cubic un poco más tolerante a las pérdidas espurias,
cambiando el número mínimo de pérdidas acumuladas entre dos ACK para considerarlas un evento de
pérdida, cuyo valor por defecto es 1. Se han observado experimentalmente algunas ganancias
significativas, pero siempre acompañadas de una agravación del ancho de banda desperdiciado en
retransmisiones y de un mayor riesgo de saturación de enlaces congestionados. El valor 2 puede
usarse durante periodos cortos para comparar algunas métricas. Nunca vayas más allá de 2 sin un
análisis previo de la situación por parte de un experto. El valor por defecto y mínimo es 1. Usa
siempre 1.

<a id="entry-3-2-tune-quic-cc-cubic-min-losses"></a>

**`tune.quic.cc.cubic.min-losses <number> (deprecated)`**

```haproxy
tune.quic.cc.cubic.min-losses <number> (deprecated)
```

Esta palabra clave quedó obsoleta en 3.3 y se eliminará en 3.5. Forma parte del proceso de
simplificación aplicado a la configuración QUIC. Si se usa, este ajuste solo se aplicará a las
conexiones del frontend.

<a id="entry-3-2-tune-quic-be-cc-hystart"></a>

**`tune.quic.be.cc.hystart { on | off }`**

```haproxy
tune.quic.be.cc.hystart { on | off }
tune.quic.fe.cc.hystart { on | off }
```

Activa ('on') o desactiva ('off') el algoritmo HyStart++ (RFC 9406) para las conexiones QUIC, usado
como reemplazo de la fase de arranque lento (slow start) de los algoritmos de control de congestión,
que puede causar una alta pérdida de paquetes. Está desactivado por defecto.

<a id="entry-3-2-tune-quic-cc-hystart"></a>

**`tune.quic.cc-hystart { on | off } (deprecated)`**

```haproxy
tune.quic.cc-hystart { on | off } (deprecated)
```

Esta palabra clave quedó obsoleta en 3.3 y se eliminará en 3.5. Forma parte del proceso de
simplificación aplicado a la configuración QUIC. Si se usa, este ajuste solo se aplicará a las
conexiones del frontend.

<a id="entry-3-2-tune-quic-be-cc-max-frame-loss"></a>

**`tune.quic.be.cc.max-frame-loss <number>`**

```haproxy
tune.quic.be.cc.max-frame-loss <number>
tune.quic.fe.cc.max-frame-loss <number>
```

Establece el límite del número de veces que una misma trama QUIC puede marcarse como perdida. Si se
excede, la conexión se considera fallida y se cierra inmediatamente.

El valor por defecto es 10.

<a id="entry-3-2-tune-quic-max-frame-loss"></a>

**`tune.quic.max-frame-loss <number> (deprecated)`**

```haproxy
tune.quic.max-frame-loss <number> (deprecated)
```

Esta palabra clave quedó obsoleta en 3.3 y se eliminará en 3.5. Forma parte del proceso de
simplificación aplicado a la configuración QUIC. Si se usa, este ajuste solo se aplicará a las
conexiones del frontend.

<a id="entry-3-2-tune-quic-be-cc-max-win-size"></a>

**`tune.quic.be.cc.max-win-size <size>`**

```haproxy
tune.quic.be.cc.max-win-size <size>
tune.quic.fe.cc.max-win-size <size>
```

Establece el tamaño máximo de ventana por defecto para el controlador de congestión de una única
conexión QUIC, tanto en el lado del frontend como en el del backend. El valor debe escribirse como
un entero con un sufijo opcional 'k', 'm' o 'g'. Debe estar entre 10k y 4g.

El multiplexor QUIC también usa el tamaño actual de la ventana de congestión para determinar si
puede asignar nuevos buffers de stream en la emisión de datos. Como tal, el tamaño máximo de la
ventana de congestión también sirve de límite para este asignador.

El valor por defecto es 480k.

Ver también las opciones de bind y server "quic-cc-algo".

<a id="entry-3-2-tune-quic-frontend-default-max-window-size"></a>

**`tune.quic.frontend.default-max-window-size <size> (deprecated)`**

```haproxy
tune.quic.frontend.default-max-window-size <size> (deprecated)
```

Esta palabra clave quedó obsoleta en 3.3 y se eliminará en 3.5. Forma parte del proceso de
simplificación aplicado a la configuración QUIC. Si se usa, este ajuste solo se aplicará a las
conexiones del frontend.

<a id="entry-3-2-tune-quic-be-cc-reorder-ratio"></a>

**`tune.quic.be.cc.reorder-ratio <0..100, in percent>`**

```haproxy
tune.quic.be.cc.reorder-ratio <0..100, in percent>
tune.quic.fe.cc.reorder-ratio <0..100, in percent>
```

El ratio aplicado al umbral de reordenación de paquetes calculado. Puede provocar una detección de
alta pérdida de paquetes cuando es demasiado pequeño.

El valor por defecto es 50.

<a id="entry-3-2-tune-quic-reorder-ratio"></a>

**`tune.quic.reorder-ratio <0..100, in percent> (deprecated)`**

```haproxy
tune.quic.reorder-ratio <0..100, in percent> (deprecated)
```

Esta palabra clave quedó obsoleta en 3.3 y se eliminará en 3.5. Forma parte del proceso de
simplificación aplicado a la configuración QUIC. Si se usa, este ajuste solo se aplicará a las
conexiones del frontend.

<a id="entry-3-2-tune-quic-be-max-idle-timeout"></a>

**`tune.quic.be.max-idle-timeout <timeout>`**

```haproxy
tune.quic.be.max-idle-timeout <timeout>
tune.quic.fe.max-idle-timeout <timeout>
```

Establece los parámetros de transporte QUIC max_idle_timeout, tanto en el lado del frontend como en
el del backend. Sigue el formato de tiempo de HAProxy y se expresa en milisegundos. Esto determina
el periodo tras el cual una conexión se cierra silenciosamente si ha permanecido inactiva durante
un periodo de tiempo efectivo. Ambos extremos dependen del mismo valor negociado: - el mínimo de
los dos parámetros si ninguno de los dos es nulo, - el máximo si solo uno de ellos no es nulo, - si
ambos parámetros son nulos, esta funcionalidad queda desactivada.

El valor por defecto es 30s.

<a id="entry-3-2-tune-quic-frontend-max-idle-timeout"></a>

**`tune.quic.frontend.max-idle-timeout <timeout> (deprecated)`**

```haproxy
tune.quic.frontend.max-idle-timeout <timeout> (deprecated)
```

Esta palabra clave quedó obsoleta en 3.3 y se eliminará en 3.5. Forma parte del proceso de
simplificación aplicado a la configuración QUIC. Si se usa, este ajuste solo se aplicará a las
conexiones del frontend.

<a id="entry-3-2-tune-quic-be-sec-glitches-threshold"></a>

**`tune.quic.be.sec.glitches-threshold <number>`**

```haproxy
tune.quic.be.sec.glitches-threshold <number>
tune.quic.fe.sec.glitches-threshold <number>
```

Establece el umbral para el número de glitches por conexión, tanto en el lado del frontend como en
el del backend, en el que esa conexión se matará automáticamente. Esto permite matar
automáticamente conexiones que se comportan mal sin tener que escribir reglas explícitas para
ellas. El valor por defecto es cero, lo que indica que no se establece ningún umbral, de modo que
ningún evento provocará el cierre de una conexión. Ten en cuenta que algunos clientes QUIC pueden
ocasionalmente causar algunos glitches en conexiones de larga duración, así que cualquier valor no
nulo aquí probablemente debería estar en los cientos o miles para ser efectivo sin afectar a
clientes ligeramente defectuosos. También es posible matar conexiones solo cuando el uso de CPU
cruza cierto nivel, usando "tune.glitches.kill.cpu-usage".

Ver también: fc_glitches, tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-quic-frontend-glitches-threshold"></a>

**`tune.quic.frontend.glitches-threshold <number> (deprecated)`**

```haproxy
tune.quic.frontend.glitches-threshold <number> (deprecated)
```

Esta palabra clave quedó obsoleta en 3.3 y se eliminará en 3.5. Forma parte del proceso de
simplificación aplicado a la configuración QUIC. Si se usa, este ajuste solo se aplicará a las
conexiones del frontend.

<a id="entry-3-2-tune-quic-fe-sec-retry-threshold"></a>

**`tune.quic.fe.sec.retry-threshold <number>`**

```haproxy
tune.quic.fe.sec.retry-threshold <number>
```

Activa dinámicamente la funcionalidad Retry para todos los listeners QUIC configurados en cuanto se
alcanza este número de conexiones semiabiertas. Una conexión semiabierta es una conexión cuyo
handshake aún no se ha completado con éxito ni ha fallado. Para ser funcional, este ajuste necesita
que se establezca un secreto de clúster; si no, se ignorará silenciosamente (ver el ajuste
"cluster-secret"). Este ajuste también se ignorará silenciosamente si el uso de QUIC Retry fue
forzado (ver "quic-force-retry").

El valor por defecto es 100.

Ver <https://www.rfc-editor.org/rfc/rfc9000.html#section-8.1.2> para más información sobre QUIC
retry.

<a id="entry-3-2-tune-quic-retry-threshold"></a>

**`tune.quic.retry-threshold <number> (deprecated)`**

```haproxy
tune.quic.retry-threshold <number> (deprecated)
```

Esta palabra clave quedó obsoleta en 3.3 y se eliminará en 3.5. Forma parte del proceso de
simplificación aplicado a la configuración QUIC. Si se usa, este ajuste solo se aplicará a las
conexiones del frontend.

<a id="entry-3-2-tune-quic-fe-sock-per-conn"></a>

**`tune.quic.fe.sock-per-conn { default-on | force-off }`**

```haproxy
tune.quic.fe.sock-per-conn { default-on | force-off }
```

Especifica globalmente cómo usarán socket las conexiones QUIC del frontend para las operaciones de
recepción/envío. Las conexiones pueden compartir el socket del listener o cada conexión puede
asignar su propio socket.

El valor por defecto es "default-on". Se usa para asignar un socket dedicado a cada conexión QUIC.
Esta opción es la preferida para lograr el mejor rendimiento con un tráfico QUIC grande. También es
la única forma de asegurar que el soft-stop se conduzca correctamente sin pérdida de datos para las
conexiones QUIC y que los casos de errores transitorios durante la operación sendto() se manejen
eficientemente. Sin embargo, esto depende de algunas funcionalidades avanzadas de la pila de red
UDP. Si tu plataforma se considera incompatible, haproxy pasará automáticamente al modo "force-off"
al arrancar. Ten en cuenta que los listeners QUIC que se ejecutan en puertos privilegiados pueden
requerir ejecutarse como uid 0, o alguna puesta a punto específica del sistema operativo que
permita al uid de destino vincular tales puertos, como las capacidades del sistema. Ver también la
directiva global "setcap".

El valor "force-off" indica que las transferencias QUIC ocurrirán en el socket del listener
compartido. Esta opción puede ser un buen compromiso para un tráfico pequeño, ya que permite
reducir el consumo de FD. Sin embargo, el rendimiento no será óptimo debido a un mayor uso de CPU
si los listeners se comparten entre muchos hilos o si puede usarse simultáneamente un gran número
de conexiones QUIC.

Este ajuste se aplica en conjunción con cada una de las opciones de bind "quic-socket". Si el modo
"default-on" se usa en el ajuste global, se activará para cada listener, excepto para aquellos con
"quic-socket listener". Sin embargo, si se usa "force-off" globalmente, se aplicará en cada
instancia de listener, independientemente de su configuración individual.

<a id="entry-3-2-tune-quic-socket-owner"></a>

**`tune.quic.socket-owner { connection | listener } (deprecated)`**

```haproxy
tune.quic.socket-owner { connection | listener } (deprecated)
```

Esta palabra clave quedó obsoleta en 3.3 y se eliminará en 3.5. Forma parte del proceso de
simplificación aplicado a la configuración QUIC. La opción más reciente se llama
"tune.quic.fe.sock-per-conn", con el valor heredado "connection" correspondiendo a "default-on" y
"listener" a "force-off".

<a id="entry-3-2-tune-quic-be-stream-data-ratio"></a>

**`tune.quic.be.stream.data-ratio <0..100, in percent>`**

```haproxy
tune.quic.be.stream.data-ratio <0..100, in percent>
tune.quic.fe.stream.data-ratio <0..100, in percent>
```

Este ajuste permite configurar el límite rígido del número de bytes de datos en vuelo sobre cada
stream. Se expresa como porcentaje relativo al ajuste de conexión rxbuf de stream QUIC, con el
resultado redondeado hacia arriba a bufsize.

El valor por defecto es 90. Esto es adecuado para el escenario web más frecuente, donde la subida
se realiza solo en uno o pocos streams, mientras que el resto se usan solo para descarga. Si el
límite de conexión rxbuf de stream permanece en un nivel razonable, asegura que solo una parte de
los streams abiertos pueda asignar hasta su capacidad máxima.

En el caso de una aplicación que use muchos streams de subida en paralelo y sufra inequidad entre
estos streams, puede tener sentido reducir este ratio, para aumentar la equidad y reducir el ancho
de banda por stream.

Ver también: "tune.quic.be.stream.rxbuf", "tune.quic.fe.stream.rxbuf",
"tune.quic.be.stream.max-concurrent", "tune.quic.fe.stream.max-concurrent"

<a id="entry-3-2-tune-quic-frontend-stream-data-ratio"></a>

**`tune.quic.frontend.stream-data-ratio  <0..100, in percent> (deprecated)`**

```haproxy
tune.quic.frontend.stream-data-ratio  <0..100, in percent> (deprecated)
```

Esta palabra clave quedó obsoleta en 3.3 y se eliminará en 3.5. Forma parte del proceso de
simplificación aplicado a la configuración QUIC. Si se usa, este ajuste solo se aplicará a las
conexiones del frontend.

<a id="entry-3-2-tune-quic-be-stream-max-concurrent"></a>

**`tune.quic.be.stream.max-concurrent <number>`**

```haproxy
tune.quic.be.stream.max-concurrent <number>
tune.quic.fe.stream.max-concurrent <number>
```

En el lado del frontend, esto se usa como valor para el parámetro de transporte
initial_max_streams_bidi anunciado. Se aplica como el número máximo de streams bidireccionales que
el par remoto estará autorizado a abrir concurrentemente durante la vida de la conexión. Esto
limita efectivamente el número de peticiones HTTP/3 concurrentes de los clientes.

El valor por defecto es 100. Ten en cuenta que si lo reduces, puedes restringir la capacidad de
bufferizado de los streams en recepción, lo que resultaría en un rendimiento de subida pobre.
Puede corregirse aumentando el ajuste de conexión rxbuf de stream QUIC.

En el lado del backend, esto lo aplica localmente haproxy para limitar el número de peticiones
concurrentes multiplexadas sobre una única conexión. Puede estar aún más restringido por el control
de flujo del par. Puede ser necesario reducir el valor por defecto de 100 para mejorar la
capacidad de respuesta de un sitio a costa de un número mayor de conexiones de backend abiertas. De
forma similar al lado del frontend, este ajuste también impacta directamente la capacidad de
bufferizado de Rx, aunque esta vez limitando la capacidad de descarga HTTP. El ajuste rxbuf de
stream QUIC puede aumentarse cuando se manejan mayoritariamente respuestas HTTP mayores que
"tune.bufsize".

Ver también: "tune.quic.be.stream.rxbuf", "tune.quic.fe.stream.rxbuf",
"tune.quic.be.stream.data-ratio", "tune.quic.fe.stream.data-ratio"

<a id="entry-3-2-tune-quic-fe-stream-max-total"></a>

**`tune.quic.fe.stream.max-total <number>`**

```haproxy
tune.quic.fe.stream.max-total <number>
```

Establece el número máximo de peticiones que puede manejar una única conexión QUIC. Una vez
alcanzado este total, la conexión se apagará de forma graceful. En HTTP/3, esto se traduce en una
trama GOAWAY. La conexión finalmente se cierra cuando se completan todas las transferencias
restantes.

Este ajuste se aplica como límite rígido sobre la conexión mediante el mecanismo de control de
flujo QUIC. Si un par lo viola, la conexión se cerrará inmediatamente.

Este ajuste puede usarse para forzar a los clientes a abrir conexiones nuevas de vez en cuando para
continuar la emisión de peticiones y evitar mantener conexiones durante demasiado tiempo. Sin
embargo, valores bajos aumentarán la latencia en el lado del cliente, así como el consumo de CPU en
ambos lados debido a los handshakes TLS.

El valor por defecto es 0, lo que implica ningún límite específico fuera de la limitación de
codificación del protocolo QUIC (2^60, más de mil millones de miles de millones).

<a id="entry-3-2-tune-quic-frontend-max-streams-bidi"></a>

**`tune.quic.frontend.max-streams-bidi <number> (deprecated)`**

```haproxy
tune.quic.frontend.max-streams-bidi <number> (deprecated)
```

Esta palabra clave quedó obsoleta en 3.3 y se eliminará en 3.5. Forma parte del proceso de
simplificación aplicado a la configuración QUIC. Si se usa, este ajuste solo se aplicará a las
conexiones del frontend.

<a id="entry-3-2-tune-quic-be-stream-rxbuf"></a>

**`tune.quic.be.stream.rxbuf <size>`**

```haproxy
tune.quic.be.stream.rxbuf <size>
tune.quic.fe.stream.rxbuf <size>
```

Este ajuste es el límite rígido del número de bytes de datos en vuelo sobre una conexión QUIC del
frontend. Se reutiliza como valor para el parámetro de transporte initial_max_data. Impacta directamente el ancho de banda de subida para el par, dependiendo de la latencia, y el consumo de
memoria por conexión en haproxy.

Por defecto, el valor se establece a 0, lo que indica que debe generarse automáticamente como el
producto entre max-concurrent y bufsize. Esto puede aumentarse, por ejemplo, si una aplicación de
backend depende de subidas masivas sobre redes de alta latencia.

Ver también: "tune.quic.be.stream.max-concurrent", "tune.quic.fe.stream.max-concurrent",
"tune.quic.be.stream.data-ratio", "tune.quic.fe.stream.data-ratio"

<a id="entry-3-2-tune-quic-frontend-max-data-size"></a>

**`tune.quic.frontend.max-data-size <size> (deprecated)`**

```haproxy
tune.quic.frontend.max-data-size <size> (deprecated)
```

Esta palabra clave quedó obsoleta en 3.3 y se eliminará en 3.5. Forma parte del proceso de
simplificación aplicado a la configuración QUIC. Si se usa, este ajuste solo se aplicará a las
conexiones del frontend.

<a id="entry-3-2-tune-quic-be-tx-pacing"></a>

**`tune.quic.be.tx.pacing { on | off }`**

```haproxy
tune.quic.be.tx.pacing { on | off }
tune.quic.fe.tx.pacing { on | off }
```

Activa ('on') o desactiva ('off') el soporte de pacing para la emisión QUIC. Por defecto está
activo. El propósito del pacing es suavizar la emisión de datos para reducir las pérdidas de red.
En la mayoría de los escenarios mejorará significativamente el rendimiento de la red al evitar
retransmisiones. Sin embargo, puede ser útil desactivarlo para redes con características de ancho
de banda muy alto y baja latencia, para prevenir retrasos no deseados y reducir el consumo de CPU.

Ver también las opciones de bind y server "quic-cc-algo".

<a id="entry-3-2-tune-quic-disable-tx-pacing"></a>

**`tune.quic.disable-tx-pacing (deprecated)`**

```haproxy
tune.quic.disable-tx-pacing (deprecated)
```

Esta palabra clave quedó obsoleta en 3.3 y se eliminará en 3.5. Forma parte del proceso de
simplificación aplicado a la configuración QUIC. Si se usa, este ajuste solo se aplicará a las
conexiones del frontend.

<a id="entry-3-2-tune-quic-be-tx-udp-gso"></a>

**`tune.quic.be.tx.udp-gso { on | off }`**

```haproxy
tune.quic.be.tx.udp-gso { on | off }
tune.quic.fe.tx.udp-gso { on | off }
```

Activa ('on') o desactiva ('off') el soporte de UDP GSO para la emisión QUIC. Por defecto está
activo. Esta funcionalidad del kernel permite emitir múltiples datagramas mediante una única llamada al sistema, lo cual es más eficiente para transferencias grandes. Puede ser útil desactivarlo por
sugerencia de los desarrolladores cuando se sospecha de un problema en la emisión.

<a id="entry-3-2-tune-quic-disable-udp-gso"></a>

**`tune.quic.disable-udp-gso (deprecated)`**

```haproxy
tune.quic.disable-udp-gso (deprecated)
```

Esta palabra clave quedó obsoleta en 3.3 y se eliminará en 3.5. Forma parte del proceso de
simplificación aplicado a la configuración QUIC. Si se usa, este ajuste solo se aplicará a las
conexiones del frontend.

<a id="entry-3-2-tune-quic-listen"></a>

**`tune.quic.listen { on | off }`**

```haproxy
tune.quic.listen { on | off }
```

Desactiva el protocolo de transporte QUIC en el lado del frontend. Todos los listeners QUIC
seguirán creándose, pero no escucharán datagramas entrantes. Por ello, haproxy no procesará tráfico
QUIC en el lado del frontend.

El valor por defecto es "on". Si se sospecha de un problema con el tráfico QUIC, esta opción puede
usarse para activar o desactivar fácilmente los listeners QUIC sin tocar cada línea de
configuración individual.

Ver también el sample fetch "quic_enabled".

<a id="entry-3-2-tune-quic-mem-tx-max"></a>

**`tune.quic.mem.tx-max <size>`**

```haproxy
tune.quic.mem.tx-max <size>
```

Establece la cantidad máxima de memoria utilizable por la pila QUIC en la capa de transporte para
la emisión. Sirve tanto de límite de bytes en vuelo como de buffers de salida del multiplexor. Ten
en cuenta que para evitar la contención de hilos este límite no se aplica estrictamente, así que
puede excederse en algunas ocasiones. Además, cada conexión siempre podrá usar una ventana de al
menos 2 datagramas, así que debería usarse un maxconn apropiado en conjunción.

<a id="entry-3-2-tune-quic-frontend-max-tx-mem"></a>

**`tune.quic.frontend.max-tx-mem <size> (deprecated)`**

```haproxy
tune.quic.frontend.max-tx-mem <size> (deprecated)
```

Esta palabra clave quedó obsoleta en 3.3 y se eliminará en 3.5. Forma parte del proceso de
simplificación aplicado a la configuración QUIC. Si se usa, este ajuste solo se aplicará a las
conexiones del frontend.

<a id="entry-3-2-tune-quic-zero-copy-fwd-send"></a>

**`tune.quic.zero-copy-fwd-send { on | off }`**

```haproxy
tune.quic.zero-copy-fwd-send { on | off }
```

Activa ('on') o desactiva ('off') los envíos de copia cero de datos para el multiplexor QUIC. Está
activado por defecto.

Ver también: tune.disable-zero-copy-forwarding

<a id="entry-3-2-tune-renice-runtime"></a>

**`tune.renice.runtime <number>`**

```haproxy
tune.renice.runtime <number>
```

Esta opción de configuración toma un valor entre -20 y 19. Aplica una prioridad de planificación
tal como se documenta en man 2 setpriority. Esta prioridad se aplica tras el análisis de la
configuración, lo que significa que solo el worker o el proceso independiente la aplicarán.
Normalmente se configura para establecer una prioridad más alta que la de un proceso que hace el
análisis de la configuración (tune.renice.startup).

Ver también: tune.renice.startup

<a id="entry-3-2-tune-renice-startup"></a>

**`tune.renice.startup <number>`**

```haproxy
tune.renice.startup <number>
```

Esta opción de configuración toma un valor entre -20 y 19. Aplica una prioridad de planificación
tal como se documenta en man 2 setpriority. Esta prioridad se aplica antes de aplicar el resto de
la configuración, lo que puede ser útil si quieres bajar la prioridad del análisis de la
configuración. Esto se aplica en el proceso independiente o en el worker antes del análisis de la
configuración. Una vez analizada la configuración, se restaura la prioridad anterior salvo que se
use tune.renice.runtime.

Ver también: tune.renice.runtime

<a id="entry-3-2-tune-rcvbuf-backend"></a>

**`tune.rcvbuf.backend  <size>`**

```haproxy
tune.rcvbuf.backend  <size>
tune.rcvbuf.frontend <size>
```

Establece a este tamaño el buffer de recepción del socket del kernel en sockets no conectados.
Esto puede usarse para QUIC en modo listener y log-forward en el frontend. Los buffers del sistema
por defecto podrían a veces ser demasiado pequeños para sockets que reciben mucho tráfico agregado,
causando algunas pérdidas y posiblemente retransmisiones (en el caso de QUIC), y posiblemente
ralentizando el establecimiento de conexiones bajo tráfico intenso. El valor se expresa en bytes y
se aplica a cada socket. En modo listener, los sockets se comparten entre todas las conexiones y el
número total de sockets depende del valor "shards" de la línea "bind". No hay un valor bueno; uno
bueno corresponde a un tamaño esperado por conexión multiplicado por el número esperado de
conexiones. El kernel puede recortar valores grandes. Ver también "tune.rcvbuf.client" y
"tune.rcvbuf.server" para sus contrapartes de socket conectado, así como "tune.sndbuf.backend" y
"tune.sndbuf.frontend" para el ajuste de envío.

<a id="entry-3-2-tune-rcvbuf-client"></a>

**`tune.rcvbuf.client <size>`**

```haproxy
tune.rcvbuf.client <size>
tune.rcvbuf.server <size>
```

Fuerza el tamaño del buffer de recepción del socket del kernel en el lado del cliente o del
servidor al valor especificado en bytes. Este valor se aplica a todos los frontends y backends
TCP/HTTP. Normalmente no debería establecerse nunca, y el tamaño por defecto (0) deja que el kernel
autoajuste este valor dependiendo de la cantidad de memoria disponible. Sin embargo, a veces puede
ayudar establecerlo a valores muy bajos (p. ej. 4096) para ahorrar memoria del kernel evitando que
bufferice cantidades demasiado grandes de datos recibidos. Los valores más bajos aumentarán
significativamente el uso de CPU, sin embargo.

<a id="entry-3-2-tune-recv-enough"></a>

**`tune.recv_enough <size>`**

```haproxy
tune.recv_enough <size>
```

HAProxy usa algunas pistas para detectar que una lectura corta indica el final de los buffers del
socket. Una de ellas es que una lectura devuelve más de `<recv_enough>` bytes, cuyo valor por
defecto es 10136 (7 segmentos de 1448 cada uno). Este valor por defecto puede cambiarse con este
ajuste para manejar mejor cargas de trabajo con muchos mensajes cortos, como sesiones telnet o
SSH.

<a id="entry-3-2-tune-ring-queues"></a>

**`tune.ring.queues <number>`**

```haproxy
tune.ring.queues <number>
```

Establece el número de colas de escritura delante de los buffers en anillo (ring buffers). Esto
puede repercutir en el uso de CPU de las trazas durante sesiones de depuración, y tanto un valor
demasiado bajo como demasiado grande puede tener un efecto importante. El valor bueno fue
determinado experimentalmente por los desarrolladores y no debería haber razón para intentar
cambiarlo, salvo que se indique hacerlo para intentar abordar problemas específicos. Tal ajuste no
debería dejarse en la configuración entre actualizaciones de versión, porque su valor óptimo puede
evolucionar con el tiempo.

<a id="entry-3-2-tune-runqueue-depth"></a>

**`tune.runqueue-depth <number>`**

```haproxy
tune.runqueue-depth <number>
```

Establece la cantidad máxima de tareas que pueden procesarse de una vez al ejecutar tareas. El
valor por defecto depende del número de hilos, pero se sitúa entre 35 y 280, lo que tiende a mostrar
las tasas de peticiones más altas y las latencias más bajas. Aumentarlo puede incurrir en latencia
al manejar E/S, y hacerlo demasiado pequeño puede incurrir en sobrecarga extra. Los números de
hilos más altos se benefician de valores más bajos. Al experimentar con valores mucho más grandes,
puede ser útil activar también tune.sched.low-latency y posiblemente tune.fd.edge-triggered para
limitar la latencia máxima al mínimo posible.

<a id="entry-3-2-tune-sched-low-latency"></a>

**`tune.sched.low-latency { on | off }`**

```haproxy
tune.sched.low-latency { on | off }
```

Activa ('on') o desactiva ('off') el planificador de tareas de baja latencia. Por defecto HAProxy
procesa tareas de varias clases, una clase cada vez, ya que es lo más eficiente. Pero al ejecutarse
con valores grandes de tune.runqueue-depth esto puede tener un efecto medible en la latencia de
peticiones o conexiones. Cuando este ajuste de baja latencia está activado, las tareas de clases
de menor prioridad siempre se ejecutarán antes que las demás si existen. Esto permitirá bajar la
latencia máxima experimentada por las peticiones o conexiones nuevas en medio de un tráfico
masivo, a costa de un mayor impacto sobre ese tráfico grande. Para el uso regular es mejor
dejarlo desactivado. El valor por defecto es off.

<a id="entry-3-2-tune-sndbuf-backend"></a>

**`tune.sndbuf.backend  <size>`**

```haproxy
tune.sndbuf.backend  <size>
tune.sndbuf.frontend <size>
```

Establece a este tamaño el buffer de envío del socket del kernel en sockets no conectados. Esto
puede usarse para el registro por socket UNIX y UDP en el lado del backend, y para QUIC en modo
listener en el frontend. Los buffers del sistema por defecto podrían a veces ser demasiado
pequeños para sockets compartidos entre muchas conexiones (o emisores de registros), causando
algunas pérdidas y posiblemente retransmisiones, y ralentizando el establecimiento de conexiones
nuevas bajo tráfico intenso. El valor se expresa en bytes y se aplica a cada socket. En modo
listener, los sockets se comparten entre todas las conexiones y el número total de sockets depende
del valor "shards" de la línea "bind". No hay un valor bueno; uno bueno corresponde a un tamaño
esperado por conexión multiplicado por el número esperado de conexiones. El kernel puede recortar
valores grandes. Ver también "tune.sndbuf.client" y "tune.sndbuf.server" para sus contrapartes de
socket conectado, así como "tune.rcvbuf.backend" y "tune.rcvbuf.frontend" para el ajuste de
recepción.

<a id="entry-3-2-tune-sndbuf-client"></a>

**`tune.sndbuf.client <size>`**

```haproxy
tune.sndbuf.client <size>
tune.sndbuf.server <size>
```

Fuerza el tamaño del buffer de envío del socket del kernel en el lado del cliente o del servidor
al valor especificado en bytes. Este valor se aplica a todos los frontends y backends TCP/HTTP.
Normalmente no debería establecerse nunca, y el tamaño por defecto (0) deja que el kernel autoajuste
este valor dependiendo de la cantidad de memoria disponible. Sin embargo, a veces puede ayudar
establecerlo a valores muy bajos (p. ej. 4096) para ahorrar memoria del kernel evitando que
bufferice cantidades demasiado grandes de datos recibidos. Los valores más bajos aumentarán
significativamente el uso de CPU, sin embargo. Otro caso de uso es evitar que se agoten los tiempos de espera de escritura con clientes extremadamente lentos, debido a que el kernel espera que se lea una gran
parte del buffer antes de notificar de nuevo a HAProxy. Ver también tune.notsent-lowat.client y
tune.notsent-lowat.server para ajustes más efectivos que controlan más finamente el uso de memoria
y la capacidad de respuesta en Linux sin dañar el rendimiento.

<a id="entry-3-2-tune-ssl-cachesize"></a>

**`tune.ssl.cachesize <number>`**

```haproxy
tune.ssl.cachesize <number>
```

Establece el tamaño de la caché global de sesiones SSL, en número de bloques. Un bloque es lo
bastante grande para contener una sesión codificada sin certificado del par. Una sesión codificada
con certificado del par se almacena en múltiples bloques dependiendo del tamaño del certificado del
par. Un bloque usa aproximadamente 200 bytes de memoria (basado en el cálculo `sizeof(struct
sh_ssl_sess_hdr) + SHSESS_BLOCK_MIN_SIZE` usado para la función `shctx_init`). El valor por defecto
puede forzarse en tiempo de compilación; de lo contrario, es 20000. Cuando la caché está llena,
las entradas más inactivas se purgan y se reasignan. Valores más altos reducen la ocurrencia de tal
purga y, por ende, el número de handshakes SSL intensivos en CPU, al asegurar que todos los
usuarios conserven su sesión el mayor tiempo posible. Todas las entradas se preasignan al arrancar.
Establecer este valor a 0 desactiva la caché de sesiones SSL.

<a id="entry-3-2-tune-ssl-capture-buffer-size"></a>

**`tune.ssl.capture-buffer-size <number>`**

```haproxy
tune.ssl.capture-buffer-size <number>
tune.ssl.capture-cipherlist-size <number> (deprecated)
```

Establece el tamaño máximo del buffer usado para capturar la lista de cifrados del client hello,
la lista de extensiones, la lista de curvas elípticas y los formatos de punto de curva elíptica.
Si el valor es 0 (valor por defecto), la captura está desactivada; de lo contrario, se asigna un
buffer para cada conexión SSL/TLS.

<a id="entry-3-2-tune-ssl-certificate-compression"></a>

**`tune.ssl.certificate-compression { auto | off }`**

```haproxy
tune.ssl.certificate-compression { auto | off }
```

Este ajuste permite configurar el soporte de compresión de certificados, que es una extensión (RFC
8879) de TLS 1.3.

Cuando se pone a "auto" usa el valor por defecto de la biblioteca TLS.

Con "off" intenta desactivar explícitamente el soporte de la funcionalidad. HAProxy ya no
intentará enviar certificados comprimidos ni aceptará certificados comprimidos.

Configura tanto el lado del backend como el del frontend.

Esta palabra clave está soportada por OpenSSL \>= 3.2.0.

El valor por defecto es auto.

<a id="entry-3-2-tune-ssl-default-dh-param"></a>

**`tune.ssl.default-dh-param <number>`**

```haproxy
tune.ssl.default-dh-param <number>
```

Establece el tamaño máximo de los parámetros Diffie-Hellman usados para generar la clave
Diffie-Hellman efímera/temporal en caso de intercambio de claves DHE. El tamaño final intentará
coincidir con el tamaño de la clave RSA (o DSA) del servidor (p. ej., una clave DH temporal de 2048
bits para una clave RSA de 2048 bits), pero no excederá este valor máximo. Solo se permiten valores
de 1024 o superiores. Los valores más altos aumentarán la carga de CPU, y los valores mayores de
1024 bits no están soportados por los clientes de Java 7 y anteriores. Este valor no se usa si se
suministran parámetros Diffie-Hellman estáticos, bien directamente en el archivo de certificado o
usando el parámetro ssl-dh-param-file. Si no hay definido ni un default-dh-param ni un
ssl-dh-param-file, y si el archivo PEM del servidor de un frontend dado no especifica sus propios
parámetros DH, entonces los cifrados DHE no estarán disponibles para ese frontend.

Compatibilidad: OpenSSL >= 1.1.1. No compatible con AWS-LC.

<a id="entry-3-2-tune-ssl-force-private-cache"></a>

**`tune.ssl.force-private-cache`**

```haproxy
tune.ssl.force-private-cache
```

Esta opción desactiva el compartir la caché de sesiones SSL entre todos los procesos. Normalmente
no debería usarse, ya que forzará muchas renegociaciones debido a clientes que alcanzan un proceso
aleatorio. Pero puede ser necesaria en algunos sistemas operativos donde no pueda usarse ninguno
de los métodos de sincronización de caché SSL. En este caso, añadir una primera capa de balanceo
de carga basado en hash antes de la capa SSL podría limitar el impacto de la falta de compartición
de sesiones.

<a id="entry-3-2-tune-ssl-hard-maxrecord"></a>

**`tune.ssl.hard-maxrecord <number>`**

```haproxy
tune.ssl.hard-maxrecord <number>
```

Establece la cantidad máxima de bytes pasados a SSL_write() en cualquier momento. El valor por
defecto 0 significa que no hay límite. En contraste con tune.ssl.maxrecord, este ajuste no se
ajustará dinámicamente. Los registros más pequeños pueden disminuir el rendimiento, pero pueden ser
necesarios cuando se manejan clientes con poca huella de recursos.

<a id="entry-3-2-tune-ssl-keylog"></a>

**`tune.ssl.keylog { on | off }`**

```haproxy
tune.ssl.keylog { on | off }
```

Esta opción activa el registro de las claves TLS. Debe usarse con cuidado, ya que consumirá más
memoria por sesión SSL y podría reducir el rendimiento. Está desactivada por defecto.

Estos sample fetches deberían usarse para generar el SSLKEYLOGFILE necesario para descifrar
tráfico con wireshark.

<https://tlswg.org/sslkeylogfile/draft-ietf-tls-keylogfile.html>

El SSLKEYLOG es una serie de líneas con este formato:

```text
<Label> <space> <ClientRandom> <space> <Secret>
```

El ClientRandom lo proporciona el sample fetch %[ssl_fc_client_random,hex]; el secreto y la Label
pueden encontrarse en la tabla de abajo. Necesitas generar un SSLKEYLOGFILE con todas las etiquetas de esta tabla.

Los siguientes sample fetches son cadenas hexadecimales y no necesitan convertirse.

```text
  Etiqueta SSLKEYLOGFILE          |  Sample fetches de los Secretos
  --------------------------------|-----------------------------------------
  CLIENT_EARLY_TRAFFIC_SECRET     |  %[ssl_xx_client_early_traffic_secret]
  CLIENT_HANDSHAKE_TRAFFIC_SECRET |  %[ssl_xx_client_handshake_traffic_secret]
  SERVER_HANDSHAKE_TRAFFIC_SECRET |  %[ssl_xx_server_handshake_traffic_secret]
  CLIENT_TRAFFIC_SECRET_0         |  %[ssl_xx_client_traffic_secret_0]
  SERVER_TRAFFIC_SECRET_0         |  %[ssl_xx_server_traffic_secret_0]
  EXPORTER_SECRET                 |  %[ssl_xx_exporter_secret]
  EARLY_EXPORTER_SECRET           |  %[ssl_xx_early_exporter_secret]
```

Estos fetches existen para los lados del frontend (fc) o del backend (bc); sustituye "xx" por "fc"
o "bc" para usar el lado correcto.

Esto solo está disponible con OpenSSL 1.1.1, y es útil con sesiones TLS1.3.

Si quieres generar el contenido de un SSLKEYLOGFILE con TLS \< 1.3, solo necesitas esta línea:

"CLIENT_RANDOM %[ssl_fc_client_random,hex] %[ssl_fc_session_key,hex]"

Un keylog completo podría generarse con un log-format de esta manera, aunque esto no es ideal para
syslog:

```text
log-format "CLIENT_EARLY_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_client_early_traffic_secret]\n
            CLIENT_HANDSHAKE_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_client_handshake_traffic_secret]\n
            SERVER_HANDSHAKE_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_server_handshake_traffic_secret]\n
            CLIENT_TRAFFIC_SECRET_0 %[ssl_bc_client_random,hex] %[ssl_bc_client_traffic_secret_0]\n
            SERVER_TRAFFIC_SECRET_0 %[ssl_bc_client_random,hex] %[ssl_bc_server_traffic_secret_0]\n
            EXPORTER_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_exporter_secret]\n
            EARLY_EXPORTER_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_early_exporter_secret]"
```

HAProxy también proporciona los formatos anteriores como variables de entorno predefinidas que
pueden usarse directamente en una directiva "log-format":

```shell
$HAPROXY_KEYLOG_FC_LOG_FMT   claves de conexión del frontend (lado cliente)
$HAPROXY_KEYLOG_BC_LOG_FMT   claves de conexión del backend (lado servidor)
```

<a id="entry-3-2-tune-ssl-keyupdate-rate-limit"></a>

**`tune.ssl.keyupdate-rate-limit <limit>`**

```haproxy
tune.ssl.keyupdate-rate-limit <limit>
```

Limita la cantidad de KeyUpdate por segundo que estamos dispuestos a aceptar a `<limit>` antes de
considerarlo una inundación y matar la conexión. Manejar KeyUpdate es costoso de CPU, y hay poca
razón para recibir muchos. Usar un valor de "0" desactiva la limitación de tasa. El valor por
defecto es 100. <a id="entry-3-2-tune-ssl-lifetime"></a>

**`tune.ssl.lifetime <timeout>`**

```haproxy
tune.ssl.lifetime <timeout>
```

Establece cuánto tiempo puede seguir siendo válida una sesión SSL en caché. Este tiempo se expresa
en segundos y por defecto es 300 (5 min). Es importante entender que no garantiza que las sesiones
duren tanto, porque si la caché está llena, las sesiones que lleven más tiempo inactivas se purgarán a pesar
de su vida configurada. La verdadera utilidad de este ajuste es evitar que las sesiones se usen
durante demasiado tiempo.

<a id="entry-3-2-tune-ssl-maxrecord"></a>

**`tune.ssl.maxrecord <number>`**

```haproxy
tune.ssl.maxrecord <number>
```

Establece la cantidad máxima de bytes pasados a SSL_write() al comienzo de la transferencia de
datos. El valor por defecto 0 significa que no hay límite. Sobre SSL/TLS, el cliente solo puede
descifrar los datos una vez que ha recibido un registro completo. Con registros grandes, esto
significa que los clientes podrían tener que descargar hasta 16kB de datos antes de empezar a
procesarlos. Limitar el valor puede mejorar los tiempos de carga de página en navegadores situados
sobre redes de alta latencia o bajo ancho de banda. Se sugiere encontrar valores óptimos que
quepan en 1 o 2 segmentos TCP (generalmente 1448 bytes sobre Ethernet con timestamps TCP
activados, o 1460 cuando las timestamps están desactivadas), teniendo en mente que SSL/TLS añade
cierta sobrecarga. Valores típicos de 1419 y 2859 dieron buenos resultados durante las pruebas.
Usa "strace -e trace=write" para encontrar el mejor valor. HAProxy cambiará automáticamente a este
ajuste después de que se haya detectado un stream inactivo (ver tune.idletimer más arriba). Ver
también tune.ssl.hard-maxrecord.

<a id="entry-3-2-tune-ssl-ssl-ctx-cache-size"></a>

**`tune.ssl.ssl-ctx-cache-size <number>`**

```haproxy
tune.ssl.ssl-ctx-cache-size <number>
```

Establece el tamaño de la caché usada para almacenar los certificados generados en `<number>`
entradas. Es una caché LRU. Como generar un certificado SSL dinámicamente es costoso, estos se
guardan en caché. El tamaño de caché por defecto se establece en 1000 entradas.

<a id="entry-3-2-tune-streams-elasticity"></a>

**`tune.streams-elasticity <number>`**

```haproxy
tune.streams-elasticity <number>
```

Define un porcentaje objetivo de streams por conexión de frontend relativo al número máximo de
conexiones concurrentes (maxconn) cuando todas las conexiones están establecidas. Esta métrica se
aplica a protocolos multiplexados como HTTP/2 o QUIC, donde cada conexión puede recibir múltiples
streams. Siempre se garantiza al menos uno, así que el porcentaje debe ser de al menos el 100%.
Durante el establecimiento de la conexión, HAProxy anuncia dinámicamente streams adicionales hasta
el límite configurado, manteniendo el ratio objetivo. Al establecerse la conexión, cada conexión de
frontend recibe al menos un stream; los streams extra se asignan según el porcentaje objetivo y
los límites de streams configurados. Esto asegura una asignación eficiente de streams bajo
condiciones de carga variables (más streams con cargas bajas, menos con cargas altas).

Los sitios muy dinámicos con muchos objetos por página se benefician de ratios altos, que permiten
muchos streams por conexión. Los sitios que usan de media menos streams (WebSocket, código de
aplicación) pueden preferir ratios pequeños cercanos a 120 o 150 (un 20 a 50% más de streams que
conexiones), lo que previene recuentos excesivos de streams bajo cargas sostenidas.

El valor por defecto es 0, lo que significa que no se impone a este nivel, de modo que solo
aplican las configuraciones de H2 y QUIC (con el ajuste por defecto de 100 streams por conexión,
esto corresponde a 10000%). Este sigue siendo el ajuste recomendado para despliegues pequeños
(maxconn de alrededor de un millar). Los despliegues de tamaño moderado (de unos pocos miles a
decenas de miles de conexiones) típicamente establecen el ratio entre 1000 y 5000, lo que permite
de 10 a 50 streams por conexión a plena carga. Los despliegues a gran escala (de cientos de miles
a millones de conexiones) podrían usar valores más bajos (120 a 200) para soportar de media de 1.2
a 2 streams por conexión a plena carga.

Al contrario que HTTP/2, QUIC es capaz de ajustar dinámicamente el número de streams concurrentes
durante la vida de la conexión. Sin embargo, el control de flujo de QUIC es más estricto que el de
HTTP/2, por lo que al usarlo es preferible especificar valores lo bastante grandes para prevenir
latencia extra en la conexión. También hay una limitación para los listeners QUIC con 0-RTT
activado. En este caso, el valor inicial anunciado al par ignorará la elasticidad de streams y en
su lugar dependerá únicamente del ajuste "tune.quic.fe.stream.max-concurrent". Sin embargo, el
principio de elasticidad de streams seguirá siendo efectivo más allá de este anuncio inicial
durante la vida de la conexión.

Monitorizar el número total de streams activos en los backends, colas incluidas, proporciona un
indicador práctico de una carga objetivo sostenible y ayuda a evitar el sobreaprovisionamiento.

<a id="entry-3-2-tune-stick-counters"></a>

**`tune.stick-counters <number>`**

```haproxy
tune.stick-counters <number>
```

Establece el número de stick-counters que pueden rastrearse al mismo tiempo por una conexión o una
petición mediante acciones "track-sc\*" en reglas "tcp-request" o "http-request". El valor por
defecto se establece en tiempo de compilación mediante la macro MAX_SESS_STK_CTR, y por defecto es
3. Con este ajuste es posible cambiar el valor e ignorar el pasado en tiempo de compilación, pero
no puede establecerse a un valor mayor que 100. Aumentar este valor puede ser necesario al portar
configuraciones complejas a haproxy, pero se advierte a los usuarios de los costes: cada entrada
toma 16 bytes por conexión y 16 bytes por petición, todos los cuales deben asignarse y ponerse a
cero para todas las peticiones incluso cuando no se usan. Como tal, un valor de 10 inflará el
consumo de memoria por petición en 320 bytes y hará que esta memoria se borre para cada petición,
lo que sí tiene impactos medibles en la CPU. A la inversa, cuando no se usan reglas "track-sc", el
valor puede reducirse (siendo 0 válido para desactivar completamente los stick-counters).

<a id="entry-3-2-tune-takeover-other-tg-connections"></a>

**`tune.takeover-other-tg-connections <value>`**

```haproxy
tune.takeover-other-tg-connections <value>
```

Por defecto, no intentaremos usar conexiones inactivas de otros grupos de hilos. Esto puede
cambiarse, sin embargo. Los valores válidos para `<value>` son: "none", el valor por defecto; si
se usa, no se hará ningún intento de usar conexiones inactivas de otros grupos de hilos;
"restricted", donde solo intentaremos obtener una conexión inactiva de otro hilo si estamos usando
protocolos que no pueden crear conexiones nuevas, como reverse http, así como al usar
strict-maxconn; y "full", donde siempre buscaremos conexiones inactivas en otros grupos de hilos.
Ten en cuenta que usar conexiones de otros grupos de hilos puede acarrear penalizaciones de
rendimiento, así que no debería usarse salvo que sea realmente necesario. Ten en cuenta que este
comportamiento ahora está controlado por tune.idle-pool.shared, y esta palabra clave está ahí solo
por compatibilidad con configuraciones más antiguas, y quedará obsoleta.

<a id="entry-3-2-tune-vars-global-max-size"></a>

**`tune.vars.global-max-size <size>`**

```haproxy
tune.vars.global-max-size <size>
tune.vars.proc-max-size <size>
tune.vars.reqres-max-size <size>
tune.vars.sess-max-size <size>
tune.vars.txn-max-size <size>
```

Estos cinco ajustes ayudan a gestionar la cantidad máxima de memoria usada por el sistema de
variables. "global" limita la cantidad total de memoria disponible para todos los ámbitos. "proc"
limita la memoria del ámbito de proceso, "sess" la del ámbito de sesión, "txn" la del ámbito de
transacción, y "reqres" limita la memoria para el procesamiento de cada petición o respuesta. La
contabilidad de la memoria es jerárquica, lo que significa que los límites más gruesos incluyen a
los más finos: "proc" incluye "sess", "sess" incluye "txn", y "txn" incluye "reqres".

Por ejemplo, cuando "tune.vars.sess-max-size" está limitado a 100, "tune.vars.txn-max-size" y
"tune.vars.reqres-max-size" tampoco pueden exceder 100. Si creamos una variable "txn.var" que
contiene 100 bytes, todo el espacio disponible queda consumido. Ten en cuenta que exceder los
límites en tiempo de ejecución no resultará en un mensaje de error, pero los valores podrían quedar
cortados o corromperse. Así que asegúrate de planificar con precisión el espacio necesario para
almacenar todas tus variables.

<a id="entry-3-2-tune-zlib-memlevel"></a>

**`tune.zlib.memlevel <number>`**

```haproxy
tune.zlib.memlevel <number>
```

Establece el parámetro memLevel en la inicialización de zlib para cada stream. Define cuánta
memoria debe asignarse para el estado interno de compresión. Un valor de 1 usa la memoria mínima
pero es lento y reduce el ratio de compresión; un valor de 9 usa la memoria máxima para una
velocidad óptima. Puede ser un valor entre 1 y 9. El valor por defecto es 8.

<a id="entry-3-2-tune-zlib-windowsize"></a>

**`tune.zlib.windowsize <number>`**

```haproxy
tune.zlib.windowsize <number>
```

Establece el tamaño de ventana (el tamaño del buffer de historial) como parámetro de la
inicialización de zlib para cada stream. Los valores mayores de este parámetro dan como resultado
una mejor compresión a costa del uso de memoria. Puede ser un valor entre 8 y 15. El valor por
defecto es 15.

## 3.3. Depuración {#section-3-3}

<a id="entry-3-3-anonkey"></a>

**`anonkey <key>`**

```haproxy
anonkey <key>
```

Esto establece la clave global de anonimización en `<key>`, que debe ser un número de 32 bits entre
0 y 4294967295. Esta es la clave que usarán por defecto los comandos de la CLI cuando el modo
anonimizado esté activado. Esta clave también puede establecerse en tiempo de ejecución desde el
comando de la CLI "set anon global-key". Ver también el argumento de línea de comandos "-dC" en el
manual de gestión.

<a id="entry-3-3-debug-counters"></a>

**`debug.counters { on | off }`**

```haproxy
debug.counters { on | off }
```

Activa ('on') o desactiva ('off') la actualización de los contadores de eventos en el código.
Estos son los contadores informados bajo el tipo "CNT" en el comando de la CLI "debug counters".
Estos contadores solo están disponibles cuando el código se compiló con DEBUG_COUNTERS puesto a un
valor 1 o superior. Con el valor 1, los contadores no se actualizan por defecto ("debug.counters
off"), y con el valor 2 sí se actualizan por defecto ("debug.counters on"). Normalmente no hay
razón para cambiar este ajuste salvo que un desarrollador lo solicite, o salvo que se sospeche que
consume cantidades anormales de CPU (en cuyo caso es necesario un reporte a los desarrolladores con
un volcado de los contadores). También es posible cambiar este estado en tiempo de ejecución
usando el comando de la CLI "debug counters". Consulta el manual de gestión.

<a id="entry-3-3-force-cfg-parser-pause"></a>

**`force-cfg-parser-pause <timeout>`**

```haproxy
force-cfg-parser-pause <timeout>
```

Este comando pausa el analizador de configuración durante `<timeout>` milisegundos. Esto es útil
para desarrollo o para probar los tiempos de espera de los scripts de init, en particular para
simular una recarga muy larga. Requiere que expose-experimental-directives esté establecido.

`<timeout>` es el valor de tiempo de espera especificado en milisegundos por defecto, pero puede
estar en cualquier otra unidad si el número lleva como sufijo la unidad, tal como se explica al
principio de este documento.

Ejemplo:

```text
global
    expose-experimental-directives
    force-cfg-parser-pause 10s
```

<a id="entry-3-3-quick-exit"></a>

**`quick-exit`**

```haproxy
quick-exit
```

Esto acelera la salida del proceso antiguo en una recarga al saltarse la liberación de los objetos
de memoria y de los listeners, ya que todos ellos los reclama el sistema operativo a la muerte del
proceso. Las ganancias son solo marginales (del orden de unos cientos de milisegundos para
configuraciones enormes, como mucho). El uso principal, de hecho, es cuando se detecta un error en
el código de deinit(), ya que esto permite esquivarlo. Es mejor no usarlo salvo que lo indiquen los
desarrolladores.

<a id="entry-3-3-quiet"></a>

**`quiet`**

```haproxy
quiet
```

No muestra ningún mensaje durante el arranque. Es equivalente al argumento de línea de comandos
"-q".

<a id="entry-3-3-warn-blocked-traffic-after"></a>

**`warn-blocked-traffic-after <time>`**

```haproxy
warn-blocked-traffic-after <time>
```

Esto permite ajustar el retraso tras el cual una tarea atascada que bloquea el tráfico provocará la
emisión de una advertencia en la salida de error estándar. El retraso se expresa en milisegundos y
por defecto es 100 ms. Los valores permitidos deben estar comprendidos entre 1 ms y 1000 ms
inclusive. Los valores más bajos provocarán advertencias con frecuencia, y los más altos rara vez.
El watchdog matará de todos modos una tarea desbocada que no responda en dos intervalos de un segundo, así que un retraso de advertencia de 1000 ms normalmente no provocará ninguna advertencia.
Se recomienda mantenerse con valores entre 10 y 100ms para detectar anomalías de configuración que
pueden degradar la experiencia del usuario, causando tiempos de respuesta largos o tirones en
sesiones interactivas. Por ejemplo, una función sample-fetch de Lua mal diseñada que haga cálculos
pesados, o un archivo de map map_reg o map_regm muy grande con un coste de evaluación muy alto
pueden causar tales problemas. Como comparación, un handshake TLS puede consumir entre uno y dos
milisegundos, y comprimir un buffer de respuesta HTTP de 16kB lleva alrededor de un milisegundo.
La salida contiene un volcado de hilos de la tarea responsable del bloqueo con un backtrace y algo de contexto
que ayuda a averiguar dónde se está gastando el tiempo.

<a id="entry-3-3-zero-warning"></a>

**`zero-warning`**

```haproxy
zero-warning
```

Cuando esta opción está establecida, HAProxy se negará a arrancar si se emitió alguna advertencia
al procesar la configuración y aplicarla. Esto significa que las advertencias sobre malas
combinaciones de parámetros, las advertencias sobre límites muy altos que no pudieron establecerse,
etc., hacen que el proceso salga con un error durante el arranque. Algunas advertencias tardías de
arranque no pueden ser capturadas por esta opción, como el fallo al eliminar los grupos
suplementarios al cambiar el ID de grupo en los modos "daemon" o "master-worker", o el fallo al
marcar el proceso como volcable (dumpable) tras el fork(). Esta opción no captura las advertencias
emitidas en tiempo de ejecución. Se recomienda encarecidamente establecer esta opción en
configuraciones que no cambian a menudo, ya que ayuda a detectar errores sutiles y mantener la
configuración limpia y compatible hacia adelante. Ten en cuenta que "haproxy -c" también informará
de errores en tal caso. Esta opción es equivalente al argumento de línea de comandos "-dW".

## 3.4. Ajuste de HTTPClient {#section-3-4}

HTTPClient es una biblioteca HTTP interna; puede ser usada por varios subsistemas, por ejemplo en
scripts LUA. HTTPClient no se usa en la ruta de datos; en otras palabras, no tiene nada que ver con
el tráfico HTTP que pasa por HAProxy.

<a id="entry-3-4-httpclient-resolvers-disabled"></a>

**`httpclient.resolvers.disabled <on|off>`**

```haproxy
httpclient.resolvers.disabled <on|off>
```

Desactiva la resolución DNS del httpclient. Evita la creación de la sección de resolvers "default".

El valor por defecto es off.

<a id="entry-3-4-httpclient-resolvers-id"></a>

**`httpclient.resolvers.id <resolvers id>`**

```haproxy
httpclient.resolvers.id <resolvers id>
```

Esta opción define la sección de resolvers con la que el httpclient intentará resolver.

La opción por defecto es el ID de resolvers "default". Por defecto, si esta opción no se usa,
simplemente se desactivará la resolución si no se encuentra la sección.

Sin embargo, cuando esta opción se activa explícitamente, provocará un error de configuración si
falla al cargar.

<a id="entry-3-4-httpclient-resolvers-prefer"></a>

**`httpclient.resolvers.prefer <ipv4|ipv6>`**

```haproxy
httpclient.resolvers.prefer <ipv4|ipv6>
```

Esta opción permite elegir qué familia de IP quieres al resolver, lo cual es conveniente cuando
IPv6 no está disponible en tu red. La opción por defecto es "ipv6".

<a id="entry-3-4-httpclient-retries"></a>

**`httpclient.retries <number>`**

```haproxy
httpclient.retries <number>
```

Esta opción permite configurar el número de intentos de reintento del httpclient cuando una
petición falla. Hace lo mismo que la palabra clave "retries" en un backend.

El valor por defecto es 3.

<a id="entry-3-4-httpclient-ssl-ca-file"></a>

**`httpclient.ssl.ca-file <cafile>`**

```haproxy
httpclient.ssl.ca-file <cafile>
```

Esta opción define el ca-file que debería usarse para verificar el certificado del servidor. Toma
los mismos parámetros que la opción "ca-file" en la línea de server.

Por defecto, y cuando esta opción no se usa, el valor es "@system-ca", que intenta cargar las CA
del sistema. Si falla, el SSL quedará desactivado para el httpclient.

Sin embargo, cuando esta opción se activa explícitamente, provocará un error de configuración si
falla.

<a id="entry-3-4-httpclient-ssl-verify"></a>

**`httpclient.ssl.verify [none|required]`**

```haproxy
httpclient.ssl.verify [none|required]
```

Funciona igual que la opción verify en las líneas de server. Si se especifica 'none', los
certificados de los servidores no se verifican. La opción por defecto es "required".

Por defecto, y cuando esta opción no se usa, el valor es "required". Si falla, el SSL quedará
desactivado para el httpclient.

Sin embargo, cuando esta opción se activa explícitamente, provocará un error de configuración si
falla.

<a id="entry-3-4-httpclient-timeout-connect"></a>

**`httpclient.timeout.connect <timeout>`**

```haproxy
httpclient.timeout.connect <timeout>
```

Establece el tiempo máximo de espera por defecto para un intento de conexión del httpclient.

Argumentos:

```text
<timeout> es el valor del tiempo de espera, especificado por defecto en
          milisegundos, pero puede estar en cualquier otra unidad si el
          número lleva sufijada la unidad, como se explica al principio
          de este documento.
```

El valor por defecto es 5000ms.
