---
title: "Ajustes de configuración YAML"
linkTitle: "Configuración YAML"
weight: 20
icon: fa-solid fa-code
description: "Referencia completa de las opciones y secciones de configuración YAML de Patroni."
module: [PATRONI]
categories: [Referencia]
upstream_link: "https://patroni.readthedocs.io/en/latest/yaml_configuration.html"
---

<a id="yaml"></a>

--------

## Global/Universal {#globaluniversal}

- **thread_pool_size**: tamaño del pool de hilos utilizado por Patroni para ejecutar tareas asíncronas y comunicarse vía REST API con otros miembros durante la carrera por el liderazgo o las comprobaciones failsafe. El valor mínimo es `5`, el valor predeterminado es `5`.
- **thread_stack_size**: especifica el tamaño de pila que se utilizará para los hilos iniciados por Patroni. El valor debe estar alineado por `64kB`. El valor mínimo es `64kB`, el valor predeterminado (establecido por Patroni) es `512kB`.
- **name**: el nombre del host. Debe ser único para el clúster.
- **namespace**: ruta dentro del almacén de configuración donde Patroni guardará la información sobre el clúster. Valor predeterminado: "/service"
- **scope**: nombre del clúster

<a id="log_settings"></a>

--------

## Registro {#log}

- **type**: establece el formato de los registros. Puede ser **plain** o **json**. Para usar el formato **json**, debes tener instalado el [jsonlogger](/es/patroni/installation#extras). El valor predeterminado es **plain**.
- **level**: establece el nivel general de registro. El valor predeterminado es **INFO** (ver [la documentación del registro de Python](https://docs.python.org/3.6/library/logging.html#levels))
- **traceback_level**: establece el nivel en el que los tracebacks serán visibles. El valor predeterminado es **ERROR**. Establécelo en **DEBUG** si quieres ver los tracebacks solo cuando habilites **log.level=DEBUG**.
- **format**: establece la cadena de formato del registro. Si el tipo de registro es **plain**, el formato del registro debe ser una cadena. Consulta [los atributos de LogRecord](https://docs.python.org/3.6/library/logging.html#logrecord-attributes) para ver los atributos disponibles. Si el tipo de registro es **json**, el formato del registro puede ser una lista además de una cadena. Cada elemento de la lista debe corresponder a atributos de LogRecord. Ten cuidado: solo se requiere el nombre del campo, y **%(** y **)** deben omitirse. Si deseas imprimir un campo del registro con un nombre de clave diferente, usa un diccionario donde la clave del diccionario sea el campo del registro y el valor sea el nombre del campo que quieres que se imprima en el registro. El valor predeterminado es **%(asctime)s %(levelname)s: %(message)s**
- **dateformat**: establece la cadena de formato de fecha y hora. (ver la [documentación de formatTime()](https://docs.python.org/3.6/library/logging.html#logging.Formatter.formatTime))
- **static_fields**: añade campos adicionales al registro. Esta opción solo está disponible cuando el tipo de registro está establecido en **json**.
- **max_queue_size**: Patroni utiliza un registro en dos pasos. Los registros se escriben en la cola en memoria y hay un hilo separado que los extrae de la cola y los escribe en stderr o en un archivo. El tamaño máximo de la cola interna está limitado por defecto a **1000** registros, lo que basta para conservar los registros de las últimas 1h20m.
- **dir**: Directorio donde escribir los registros de la aplicación. El directorio debe existir y ser escribible por el usuario que ejecuta Patroni. Si estableces este valor, la aplicación conservará 4 registros de 25MB por defecto. Puedes ajustar esos valores de retención con `file_num` y `file_size` (ver abajo).
- **mode**: Permisos para los archivos de registro (por ejemplo, `0644`). Si no se especifica, los permisos se establecerán en función del valor umask actual.
- **file_num**: El número de registros de la aplicación que se conservan.
- **file_size**: Tamaño del archivo patroni.log (en bytes) que dispara una rotación de registro.
- **loggers**: Esta sección permite redefinir el nivel de registro por módulo de python
  - **patroni.postmaster: WARNING**
  - **urllib3: DEBUG**
- **deduplicate_heartbeat_logs**: Si se establece en `true`, los registros de latido sucesivos que sean idénticos no se emitirán. El valor predeterminado es `false`.

> [!WARNING]
> La hora a la que se ejecuta el bucle de HA puede ser información muy valiosa para diagnosticar conmutaciones por error debidas al agotamiento de recursos y problemas similares. Cuando `deduplicate_heartbeat_logs` está establecido en `true` no se generará ningún registro para la ejecución del bucle de HA (a menos que cambie el líder) y, por lo tanto, esta información potencialmente útil no estará disponible en los registros.

Aquí hay un ejemplo de cómo configurar patroni para registrar en formato json.

```yaml
log:
   type: json
   format:
      - message
      - module
      - asctime: '@timestamp'
      - levelname: level
   static_fields:
      app: patroni
```

<a id="bootstrap_settings"></a>

--------

## Configuración de arranque (bootstrap) {#bootstrap-configuration}

> [!NOTE]
> Una vez que Patroni haya inicializado el clúster por primera vez y los ajustes se hayan almacenado en el DCS, ¡todos los cambios futuros en la sección `bootstrap.dcs` de la configuración YAML no tendrán ningún efecto! Si quieres cambiarlos, usa [patronictl_edit_config](/es/patroni/patronictl#patronictl_edit_config) o la [REST API](/es/patroni/rest_api#rest_api) de Patroni.

- **bootstrap**:
  - **dcs**: Esta sección se escribirá en `/<namespace>/<scope>/config` del almacén de configuración dado después de inicializar el nuevo clúster. La configuración dinámica global del clúster. Puedes poner cualquiera de los parámetros descritos en los [ajustes de configuración dinámica](/es/patroni/config/dynamic#dynamic) bajo `bootstrap.dcs` y, después de que Patroni haya inicializado (arrancado) el nuevo clúster, escribirá esta sección en `/<namespace>/<scope>/config` del almacén de configuración.

  - **method**: script personalizado que se utilizará para arrancar este clúster.

    Ver la [documentación de los métodos de arranque personalizados](/es/patroni/replica_bootstrap#custom_bootstrap) para más detalles. Cuando se especifica `initdb` se revierte al comando `initdb` predeterminado. `initdb` también se desencadena cuando no hay parámetro `method` en el archivo de configuración.

  - **initdb**: (opcional) lista de opciones que se pasarán a initdb.

    - **- data-checksums**: Debe habilitarse cuando se necesita pg_rewind en 9.3.
    - **- encoding: UTF8**: codificación predeterminada para las nuevas bases de datos.
    - **- locale: UTF8**: configuración regional predeterminada para las nuevas bases de datos.

  - **post_bootstrap** o **post_init**: Un script adicional que se ejecutará después de inicializar el clúster. El script recibe una URL de cadena de conexión (con el superusuario del clúster como nombre de usuario). La variable PGPASSFILE se establece en la ubicación del archivo pgpass.

<a id="citus_settings"></a>

--------

## Citus {#citus}

Habilita la integración de Patroni con [Citus](https://docs.citusdata.com). Si está configurado, Patroni se encargará de registrar los nodos workers de Citus en el coordinador. Puedes encontrar más información sobre el soporte de Citus [aquí](/es/patroni/citus#citus).

- **group**: el id del grupo de Citus, entero. Usa `0` para el coordinador y `1`, `2`, etc... para los workers
- **database**: la base de datos donde debe crearse la extensión [citus](/es/patroni/citus#citus). Debe ser la misma en el coordinador y en todos los workers. Actualmente solo se soporta una base de datos.

<a id="consul_settings"></a>

--------

## Consul {#consul}

La mayoría de los parámetros son opcionales, pero tienes que especificar uno de **host** o **url**

- **host**: el host:puerto para el agente local de Consul.
- **url**: url para el agente local de Consul, en formato: http(s)://host:port.
- **port**: (opcional) puerto de Consul.
- **scheme**: (opcional) **http** o **https**, el valor predeterminado es **http**.
- **token**: (opcional) token de ACL.
- **verify**: (opcional) si verificar el certificado SSL para las solicitudes HTTPS.
- **cacert**: (opcional) El certificado de la CA. Si está presente habilitará la validación.
- **cert**: (opcional) archivo con el certificado de cliente.
- **key**: (opcional) archivo con la clave de cliente. Puede estar vacío si la clave forma parte de **cert**.
- **dc**: (opcional) Centro de datos con el que comunicarse. Por defecto se utiliza el centro de datos del host.
- **consistency**: (opcional) Selecciona el modo de consistencia de consul. Los valores posibles son `default`, `consistent` o `stale` (más detalles en la [referencia de la API de consul](https://www.consul.io/api/features/consistency.html/))
- **checks**: (opcional) lista de comprobaciones de estado de Consul utilizadas para la sesión. Por defecto se utiliza una lista vacía.
- **register_service**: (opcional) si registrar o no un servicio con el nombre definido por el parámetro scope y la etiqueta master, primary, replica o standby-leader según el rol del nodo. El valor predeterminado es **false**.
- **service_tags**: (opcional) etiquetas estáticas adicionales que añadir al servicio de Consul además del rol (`primary`/`replica`/`standby-leader`). Por defecto se utiliza una lista vacía.
- **service_check_interval**: (opcional) con qué frecuencia realizar la comprobación de estado contra la url registrada. El valor predeterminado es '5s'.
- **service_check_tls_server_name**: (opcional) sobrescribe el host SNI al conectarse vía TLS; ver también la [referencia de la API de comprobación del agente consul](https://www.consul.io/api-docs/agent/check#tlsservername).

El `token` necesita tener los siguientes permisos de ACL:

    service_prefix "${scope}" {
        policy = "write"
    }
    key_prefix "${namespace}/${scope}" {
        policy = "write"
    }
    session_prefix "" {
        policy = "write"
    }

--------

## Etcd {#etcd}

La mayoría de los parámetros son opcionales, pero tienes que especificar uno de **host**, **hosts**, **url**, **proxy** o **srv**

- **host**: el host:puerto para el endpoint de etcd.
- **hosts**: lista de endpoints de etcd en formato host1:port1,host2:port2,etc... Puede ser una cadena separada por comas o una lista yaml real.
- **use_proxies**: Si este parámetro se establece en true, Patroni considerará **hosts** como una lista de proxies y no realizará un descubrimiento de la topología del clúster de etcd.
- **url**: url para el etcd.
- **proxy**: url del proxy para el etcd. Si te conectas al etcd mediante un proxy, usa este parámetro en lugar de **url**.
- **srv**: Dominio en el que buscar los registros SRV para el autodescubrimiento del clúster. Patroni intentará consultar estos nombres de servicio SRV para el dominio especificado (en ese orden hasta el primer éxito): `_etcd-client-ssl`, `_etcd-client`, `_etcd-ssl`, `_etcd`, `_etcd-server-ssl`, `_etcd-server`. Si se recuperan registros SRV para `_etcd-server-ssl` o `_etcd-server`, se utiliza el protocolo de pares de ETCD para consultar a ETCD por los miembros disponibles. De lo contrario, se utilizarán los hosts de los registros SRV.
- **srv_suffix**: Configura un sufijo para el nombre SRV que se consulta durante el descubrimiento. Usa este flag para diferenciar entre múltiples clústeres de etcd bajo el mismo dominio. Funciona solo en conjunción con **srv**. Por ejemplo, si se establecen `srv_suffix: foo` y `srv: example.org`, se realiza la siguiente consulta DNS SRV:`_etcd-client-ssl-foo._tcp.example.org` (y así sucesivamente para cada nombre de servicio SRV posible de ETCD).
- **protocol**: (opcional) http o https; si no se especifica, se usa http. Si se especifica **url** o **proxy**, tomará el protocolo de ellos.
- **username**: (opcional) usuario para la autenticación de etcd.
- **password**: (opcional) contraseña para la autenticación de etcd.
- **cacert**: (opcional) El certificado de la CA. Si está presente habilitará la validación.
- **cert**: (opcional) archivo con el certificado de cliente.
- **key**: (opcional) archivo con la clave de cliente. Puede estar vacío si la clave forma parte de **cert**.

--------

## Etcdv3 {#etcdv3}

Si quieres que Patroni funcione con un clúster de Etcd mediante la versión 3 del protocolo, necesitas usar la sección `etcd3` en el archivo de configuración de Patroni. Todos los parámetros de configuración son los mismos que para `etcd`.

> [!WARNING]
> Las claves creadas con la versión 2 del protocolo no son visibles con la versión 3 del protocolo y viceversa; por lo tanto, no es posible cambiar de `etcd` a `etcd3` solo actualizando el archivo de configuración de Patroni. Además, Patroni utiliza el gRPC-gateway (proxy) de Etcd para comunicarse con la API V3, lo que significa que la autenticación por nombre común de TLS no es posible.

--------

## ZooKeeper {#zookeeper}

- **hosts**: Lista de los miembros del clúster de ZooKeeper en formato: \['host1:port1', 'host2:port2', 'etc...'\].
- **use_ssl**: (opcional) Si se usa SSL o no. El valor predeterminado es `false`. Si se establece en `false`, se ignoran todos los parámetros específicos de SSL.
- **cacert**: (opcional) El certificado de la CA. Si está presente habilitará la validación.
- **cert**: (opcional) Archivo con el certificado de cliente.
- **key**: (opcional) Archivo con la clave de cliente.
- **key_password**: (opcional) La contraseña de la clave de cliente.
- **verify**: (opcional) Si verificar el certificado o no. El valor predeterminado es `true`.
- **set_acls**: (opcional) Si se establece, configura Kazoo para aplicar una ACL predeterminada a cada ZNode que cree. Las ACL pueden usar el esquema `x509` (predeterminado) u otros esquemas soportados de ZooKeeper como `digest`. Deben especificarse como un diccionario donde la clave es el principal completo (opcionalmente precedido del esquema) y el valor es una lista de permisos. Los permisos pueden ser uno o más de `CREATE`, `READ`, `WRITE`, `DELETE`, `ADMIN` o `ALL`. Por ejemplo, `set_acls: {CN=principal1: [CREATE, READ], digest:principal2:+pjROuBuuwNNSujKyH8dGcEnFPQ=: [ALL]}`.
- **auth_data**: (opcional) Credenciales de autenticación para usar en la conexión. Debe ser un diccionario de la forma en que `scheme` es la clave y `credential` es el valor. El valor predeterminado es un diccionario vacío.

> [!NOTE]
> Se requiere instalar `kazoo>=2.6.0` para soportar SSL.

--------

## Exhibitor {#exhibitor}

- **hosts**: lista inicial de nodos de Exhibitor (ZooKeeper) en formato: 'host1,host2,etc...'. Esta lista se actualiza automáticamente cada vez que cambia la topología del clúster de Exhibitor (ZooKeeper).
- **poll_interval**: con qué frecuencia se debe actualizar la lista de nodos de ZooKeeper y Exhibitor desde Exhibitor.
- **port**: Puerto de Exhibitor.

<a id="kubernetes_settings"></a>

--------

## Kubernetes {#kubernetes}

- **bypass_api_service**: (opcional) Al comunicarse con la API de Kubernetes, Patroni normalmente depende del servicio [kubernetes](/es/patroni/kubernetes#kubernetes), cuya dirección se expone en los pods mediante la variable de entorno `KUBERNETES_SERVICE_HOST`. Si `bypass_api_service` está establecido en `true`, Patroni resolverá la lista de nodos de la API detrás del servicio y se conectará directamente a ellos.
- **namespace**: (opcional) Espacio de nombres de Kubernetes donde se ejecuta el pod de Patroni. El valor predeterminado es `default`.
- **labels**: Etiquetas en formato `{label1: value1, label2: value2}`. Estas etiquetas se utilizarán para encontrar objetos existentes (Pods y Endpoints o ConfigMaps) asociados con el clúster actual. Además, Patroni las establecerá en cada objeto (Endpoint o ConfigMap) que cree.
- **scope_label**: (opcional) nombre de la etiqueta que contiene el nombre del clúster. El valor predeterminado es `cluster-name`.
- **bootstrap_labels**: (opcional) Etiquetas en formato `{label1: value1, label2: value2}`. Estas etiquetas se asignarán a un pod de Patroni cuando su estado sea `initializing new cluster`, `running custom bootstrap script`, `starting after custom bootstrap` o `creating replica`.
- **role_label**: (opcional) nombre de la etiqueta que contiene el rol (`primary`, `replica` u otro valor personalizado). Patroni establecerá esta etiqueta en el pod en el que se ejecuta. El valor predeterminado es `role`.
- **leader_label_value**: (opcional) valor de la etiqueta del pod cuando el rol de Postgres es `primary`. El valor predeterminado es `primary`.
- **follower_label_value**: (opcional) valor de la etiqueta del pod cuando el rol de Postgres es `replica`. El valor predeterminado es `replica`.
- **standby_leader_label_value**: (opcional) valor de la etiqueta del pod cuando el rol de Postgres es `standby_leader`. El valor predeterminado es `primary`.
- **tmp_role_label**: (opcional) nombre de la etiqueta temporal que contiene el rol (`primary` o `replica`). El valor de esta etiqueta siempre utilizará el predeterminado del rol correspondiente. Establece solo cuando sea necesario.
- **use_endpoints**: (opcional) si se establece en true, Patroni utilizará Endpoints en lugar de ConfigMaps para ejecutar las elecciones de líder y mantener el estado del clúster.
- **pod_ip**: (opcional) Dirección IP del pod en el que se ejecuta Patroni. Este valor es necesario cuando `use_endpoints` está habilitado y se utiliza para poblar los subconjuntos del endpoint del líder cuando el PostgreSQL del pod es promovido.
- **ports**: (opcional) si el objeto Service tiene el nombre para el puerto, el mismo nombre debe aparecer en el objeto Endpoint; de lo contrario, el servicio no funcionará. Por ejemplo, si tu servicio está definido como `{Kind: Service, spec: {ports: [{name: postgresql, port: 5432, targetPort: 5432}]}}`, entonces tienes que establecer `kubernetes.ports: [{"name": "postgresql", "port": 5432}]` y Patroni lo utilizará para actualizar los subconjuntos del Endpoint del líder. Este parámetro se usa solo si `kubernetes.use_endpoints` está establecido.
- **cacert**: (opcional) Especifica el archivo con el CA_BUNDLE con certificados de CAs de confianza para usar al verificar los certificados SSL de la API de Kubernetes. Si no se proporciona, patroni utilizará el valor proporcionado por el secreto del ServiceAccount.
- **retriable_http_codes**: (opcional) lista de códigos de estado HTTP de la API de K8s sobre los que reintentar. Por defecto Patroni reintenta en `500`, `503` y `504`, o si la respuesta de la API de K8s tiene la cabecera HTTP `retry-after`.

<a id="raft_settings"></a>

--------

## Raft (en desuso) {#raft-deprecated}

- **self_addr**: `ip:port` en el que escuchar conexiones Raft. El `self_addr` debe ser accesible desde los demás nodos del clúster. Si no se establece, el nodo no participará en el consenso.

- **bind_addr**: (opcional) `ip:port` en el que escuchar conexiones Raft. Si no se especifica, se utilizará el `self_addr`.

- **partner_addrs**: lista de otros nodos de Patroni en el clúster en formato: \['ip1:port', 'ip2:port', 'etc...'\]

- **data_dir**: directorio donde almacenar el registro y la instantánea de Raft. Si no se especifica, se utiliza el directorio de trabajo actual.

- **password**: (opcional) Cifra el tráfico Raft con una contraseña especificada; requiere el módulo de python `cryptography`.
- **min_timeout**: (opcional) tiempo de espera mínimo de elección en segundos para la implementación Raft subyacente de pysyncobj. Debe ser mayor que 3 * `append_entries_period`. Predeterminado: `0.4`.
- **max_timeout**: (opcional) tiempo de espera máximo de elección en segundos para la implementación Raft subyacente de pysyncobj. Debe ser mayor que `min_timeout`. Predeterminado: `1.4`.
- **connection_timeout**: (opcional) tiempo en segundos tras el cual una conexión sin datos recibidos se considera muerta. Debe ser mayor o igual que `max_timeout`. Predeterminado: `3.5`.
- **append_entries_period**: (opcional) intervalo en segundos para enviar comandos de latido (append_entries). Debe ser menor que un tercio de `min_timeout`. Predeterminado: `0.1`.
- **connection_retry_time**: (opcional) intervalo en segundos entre intentos de reconexión a nodos desconectados. Predeterminado: `5.0`.
- **leader_fallback_timeout**: (opcional) tiempo en segundos tras el cual un líder sin respuesta de la mayoría vuelve al estado de réplica. Debe ser mayor que `append_entries_period`. Predeterminado: `30.0`.

> [!NOTE]
> Estos parámetros de tiempo de espera son útiles para redes de alta latencia donde los tiempos de espera predeterminados de pysyncobj son demasiado agresivos. Deben satisfacerse las siguientes restricciones: `min_timeout` > 3 * `append_entries_period`, `max_timeout` > `min_timeout`, `connection_timeout` >= `max_timeout`, y `leader_fallback_timeout` > `append_entries_period`. Patroni los valida al arrancar y se negará a iniciar si se violan. Estos valores no pueden cambiarse en tiempo de ejecución y requieren un reinicio.
>
> [!WARNING]
> Estos controles solo relajan los tiempos de espera de elección y conexión de pysyncobj; no extienden el plazo por comando que Patroni aplica a las operaciones Raft. Cada comando Raft (actualización del bloqueo de líder, escritura del estado del clúster) aún debe completarse dentro de `retry_timeout` (predeterminado `10`). En enlaces de latencia muy alta - aproximadamente por encima de unos pocos segundos de tiempo de ida y vuelta - un solo comando puede exceder `retry_timeout` incluso cuando `connection_timeout` se eleva muy por encima del RTT, por lo que el DCS parecerá inalcanzable y el primario podría degradarse. En dichos enlaces también debes elevar `retry_timeout` y `ttl` en consecuencia, manteniendo `loop_wait + 2 * retry_timeout <= ttl`.

  Breve FAQ sobre la implementación de Raft

  - P: ¿Cómo listar todos los nodos que proporcionan consenso?

    R: `syncobj_admin -conn host:port -status` donde el host:port es la dirección de uno de los nodos del clúster

  - P: Un nodo que formaba parte del consenso ha desaparecido y no puedo reutilizar la misma IP para otro nodo. ¿Cómo eliminar este nodo del consenso?

    R: `syncobj_admin -conn host:port -remove host2:port2` donde `host2:port2` es la dirección del nodo que quieres eliminar del consenso.

  - P: ¿Dónde obtener la utilidad `syncobj_admin`?

    R: Se instala junto con el módulo `pysyncobj` (implementación RAFT de python), que es una dependencia de Patroni.

  - P: ¿es posible ejecutar un nodo de Patroni sin añadirlo al consenso?

    R: Sí, simplemente comenta o elimina `raft.self_addr` de la configuración de Patroni.

  - P: ¿Es posible ejecutar Patroni y PostgreSQL solo en dos nodos?

    R: Sí, en el tercer nodo puedes ejecutar `patroni_raft_controller` (sin Patroni ni PostgreSQL). En tal configuración, se puede perder temporalmente un nodo sin afectar al primario.

<a id="postgresql_settings"></a>

--------

## PostgreSQL {#postgresql}

- **postgresql**:
  - **authentication**:

    - **superuser**:
      - **username**: nombre del superusuario, establecido durante la inicialización (initdb) y utilizado posteriormente por Patroni para conectarse a postgres.
      - **password**: contraseña del superusuario, establecida durante la inicialización (initdb).
      - **sslmode**: (opcional) se corresponde con el parámetro de conexión [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), que permite a un cliente especificar el tipo de modo de negociación TLS con el servidor. Para más información sobre cómo funciona cada modo, visita la [documentación de PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). El modo predeterminado es `prefer`.
      - **sslkey**: (opcional) se corresponde con el parámetro de conexión [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), que especifica la ubicación de la clave secreta utilizada con el certificado del cliente.
      - **sslpassword**: (opcional) se corresponde con el parámetro de conexión [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), que especifica la contraseña para la clave secreta especificada en `sslkey`.
      - **sslcert**: (opcional) se corresponde con el parámetro de conexión [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), que especifica la ubicación del certificado de cliente.
      - **sslrootcert**: (opcional) se corresponde con el parámetro de conexión [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), que especifica la ubicación de un archivo que contiene uno o más certificados de autoridades certificadoras (CA) que el cliente utilizará para verificar el certificado de un servidor.
      - **sslcrl**: (opcional) se corresponde con el parámetro de conexión [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), que especifica la ubicación de un archivo que contiene una lista de revocación de certificados. Un cliente rechazará conectarse a cualquier servidor que tenga un certificado presente en esta lista.
      - **sslcrldir**: (opcional) se corresponde con el parámetro de conexión [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), que especifica la ubicación de un directorio con archivos que contienen una lista de revocación de certificados. Un cliente rechazará conectarse a cualquier servidor que tenga un certificado presente en esta lista.
      - **sslnegotiation**: (opcional) se corresponde con el parámetro de conexión [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), que controla cómo se negocia el cifrado SSL con el servidor, si se usa SSL.
      - **gssencmode**: (opcional) se corresponde con el parámetro de conexión [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), que determina si se negociará una conexión GSS TCP/IP segura con el servidor o con qué prioridad
      - **channel_binding**: (opcional) se corresponde con el parámetro de conexión [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), que controla el uso de channel binding por parte del cliente.
    - **replication**:
      - **username**: usuario de replicación; el usuario se creará durante la inicialización. Las réplicas utilizarán este usuario para acceder al origen de replicación mediante replicación por streaming
      - **password**: contraseña de replicación; el usuario se creará durante la inicialización.
      - **sslmode**: (opcional) se corresponde con el parámetro de conexión [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), que permite a un cliente especificar el tipo de modo de negociación TLS con el servidor. Para más información sobre cómo funciona cada modo, visita la [documentación de PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). El modo predeterminado es `prefer`.
      - **sslkey**: (opcional) se corresponde con el parámetro de conexión [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), que especifica la ubicación de la clave secreta utilizada con el certificado del cliente.
      - **sslpassword**: (opcional) se corresponde con el parámetro de conexión [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), que especifica la contraseña para la clave secreta especificada en `sslkey`.
      - **sslcert**: (opcional) se corresponde con el parámetro de conexión [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), que especifica la ubicación del certificado de cliente.
      - **sslrootcert**: (opcional) se corresponde con el parámetro de conexión [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), que especifica la ubicación de un archivo que contiene uno o más certificados de autoridades certificadoras (CA) que el cliente utilizará para verificar el certificado de un servidor.
      - **sslcrl**: (opcional) se corresponde con el parámetro de conexión [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), que especifica la ubicación de un archivo que contiene una lista de revocación de certificados. Un cliente rechazará conectarse a cualquier servidor que tenga un certificado presente en esta lista.
      - **sslcrldir**: (opcional) se corresponde con el parámetro de conexión [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), que especifica la ubicación de un directorio con archivos que contienen una lista de revocación de certificados. Un cliente rechazará conectarse a cualquier servidor que tenga un certificado presente en esta lista.
      - **sslnegotiation**: (opcional) se corresponde con el parámetro de conexión [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), que controla cómo se negocia el cifrado SSL con el servidor, si se usa SSL.
      - **gssencmode**: (opcional) se corresponde con el parámetro de conexión [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), que determina si se negociará una conexión GSS TCP/IP segura con el servidor o con qué prioridad
      - **channel_binding**: (opcional) se corresponde con el parámetro de conexión [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), que controla el uso de channel binding por parte del cliente.
    - **rewind**:
      - **username**: (opcional) nombre del usuario para `pg_rewind`; el usuario se creará durante la inicialización de postgres 11+ y se le concederán todos los [permisos](https://www.postgresql.org/docs/11/app-pgrewind.html#id-1.9.5.8.8) necesarios.
      - **password**: (opcional) contraseña del usuario para `pg_rewind`; el usuario se creará durante la inicialización.
      - **sslmode**: (opcional) se corresponde con el parámetro de conexión [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), que permite a un cliente especificar el tipo de modo de negociación TLS con el servidor. Para más información sobre cómo funciona cada modo, visita la [documentación de PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). El modo predeterminado es `prefer`.
      - **sslkey**: (opcional) se corresponde con el parámetro de conexión [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), que especifica la ubicación de la clave secreta utilizada con el certificado del cliente.
      - **sslpassword**: (opcional) se corresponde con el parámetro de conexión [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), que especifica la contraseña para la clave secreta especificada en `sslkey`.
      - **sslcert**: (opcional) se corresponde con el parámetro de conexión [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), que especifica la ubicación del certificado de cliente.
      - **sslrootcert**: (opcional) se corresponde con el parámetro de conexión [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), que especifica la ubicación de un archivo que contiene uno o más certificados de autoridades certificadoras (CA) que el cliente utilizará para verificar el certificado de un servidor.
      - **sslcrl**: (opcional) se corresponde con el parámetro de conexión [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), que especifica la ubicación de un archivo que contiene una lista de revocación de certificados. Un cliente rechazará conectarse a cualquier servidor que tenga un certificado presente en esta lista.
      - **sslcrldir**: (opcional) se corresponde con el parámetro de conexión [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), que especifica la ubicación de un directorio con archivos que contienen una lista de revocación de certificados. Un cliente rechazará conectarse a cualquier servidor que tenga un certificado presente en esta lista.
      - **sslnegotiation**: (opcional) se corresponde con el parámetro de conexión [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), que controla cómo se negocia el cifrado SSL con el servidor, si se usa SSL.
      - **gssencmode**: (opcional) se corresponde con el parámetro de conexión [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), que determina si se negociará una conexión GSS TCP/IP segura con el servidor o con qué prioridad
      - **channel_binding**: (opcional) se corresponde con el parámetro de conexión [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), que controla el uso de channel binding por parte del cliente.

  - **callbacks**: scripts de callback que se ejecutan en determinadas acciones. Patroni pasará la acción, el rol y el nombre del clúster. (Ver scripts/aws.py como ejemplo de cómo escribirlos.)

    - **on_reload**: ejecuta este script cuando se desencadena una recarga de la configuración.
    - **on_restart**: ejecuta este script cuando postgres se reinicia (sin cambiar de rol).
    - **on_role_change**: ejecuta este script cuando a postgres se le promueve o degrada.
    - **on_start**: ejecuta este script cuando postgres arranca.
    - **on_stop**: ejecuta este script cuando postgres se detiene.

  - **connect_address**: Dirección IP + puerto a través del cual Postgres es accesible desde otros nodos y aplicaciones.

  - **proxy_address**: Dirección IP + puerto a través del cual es accesible un pool de conexiones (por ejemplo, pgbouncer) que se ejecuta junto a Postgres. El valor se escribe en la clave del miembro en el DCS como `proxy_url` y podría usarse/ser útil para el descubrimiento de servicios.

  - **create_replica_methods**: una lista ordenada de los métodos de creación para convertir un nodo de Patroni en una nueva réplica. «basebackup» es el método predeterminado; se asume que otros métodos se refieren a scripts, cada uno de los cuales se configura como su propio elemento de configuración. Ver la [documentación de los métodos personalizados de creación de réplicas](/es/patroni/replica_bootstrap#custom_replica_creation) para más explicación.

  - **data_dir**: La ubicación del directorio de datos de Postgres, ya sea [existente](/es/patroni/existing_data#existing_data) o para ser inicializado por Patroni.

  - **config_dir**: La ubicación del directorio de configuración de Postgres; el valor predeterminado es el directorio de datos. Debe ser escribible por Patroni.

  - **bin_dir**: (opcional) Ruta a los binarios de PostgreSQL (pg_ctl, initdb, pg_controldata, pg_basebackup, postgres, pg_isready, pg_rewind). Si no se proporciona o es una cadena vacía, se utilizará la variable de entorno PATH para encontrar los ejecutables.

  - **bin_name**: (opcional) Permite sobrescribir los nombres de los binarios de Postgres, si estás utilizando una distribución personalizada de Postgres:

    - **pg_ctl**: (opcional) Nombre personalizado para el binario `pg_ctl`.
    - **initdb**: (opcional) Nombre personalizado para el binario `initdb`.
    - **pg_controldata**: (opcional) Nombre personalizado para el binario `pg_controldata`.
    - **pg_basebackup**: (opcional) Nombre personalizado para el binario `pg_basebackup`.
    - **postgres**: (opcional) Nombre personalizado para el binario `postgres`.
    - **pg_isready**: (opcional) Nombre personalizado para el binario `pg_isready`.
    - **pg_rewind**: (opcional) Nombre personalizado para el binario `pg_rewind`.

  - **listen**: Dirección IP + puerto al que escucha Postgres; debe ser accesible desde otros nodos del clúster si estás usando replicación por streaming. Se permiten múltiples direcciones separadas por comas, siempre que el componente del puerto se añada al final de la última con dos puntos, es decir, `listen: 127.0.0.1,127.0.0.2:5432`. Patroni utilizará la primera dirección de esta lista para establecer conexiones locales al nodo de PostgreSQL.

  - **use_unix_socket**: especifica que Patroni debería preferir el uso de sockets unix para conectarse al clúster. El valor predeterminado es `false`. Si `unix_socket_directories` está definido, Patroni utilizará el primer valor adecuado de él para conectarse al clúster y recurrirá a tcp si no hay nada adecuado. Si `unix_socket_directories` no se especifica en `postgresql.parameters`, Patroni asumirá que se debe usar el valor predeterminado y omitirá `host` de los parámetros de conexión.

  - **use_unix_socket_repl**: especifica que Patroni debería preferir el uso de sockets unix para la conexión al clúster con el usuario de replicación. El valor predeterminado es `false`. Si `unix_socket_directories` está definido, Patroni utilizará el primer valor adecuado de él para conectarse al clúster y recurrirá a tcp si no hay nada adecuado. Si `unix_socket_directories` no se especifica en `postgresql.parameters`, Patroni asumirá que se debe usar el valor predeterminado y omitirá `host` de los parámetros de conexión.

  - **pgpass**: ruta al archivo de contraseñas [.pgpass](https://www.postgresql.org/docs/current/static/libpq-pgpass.html). Patroni crea este archivo antes de ejecutar pg_basebackup, el script post_init y en algunas otras circunstancias. La ubicación debe ser escribible por Patroni.

  - **recovery_conf**: ajustes de configuración adicionales escritos en recovery.conf al configurar la réplica.

  - **custom_conf** : ruta a un archivo `postgresql.conf` personalizado opcional, que se utilizará en lugar de `postgresql.base.conf`. El archivo debe existir en todos los nodos del clúster, ser legible por PostgreSQL y se incluirá desde su ubicación en el `postgresql.conf` real. Ten en cuenta que Patroni no monitorizará este archivo en busca de cambios, ni hará copia de seguridad de él. Sin embargo, sus ajustes aún pueden sobrescribirse mediante los mecanismos de configuración propios de Patroni; ver la [configuración dinámica](/es/patroni/config#config) para más detalles.

  - **parameters**: parámetros de configuración (GUC) para Postgres en formato `{ssl: "on", ssl_cert_file: "cert_file"}`.
  - **parameters_primary**: (opcional) sobrescrituras de parámetros específicas del rol para el primario. Estos valores se combinan con **parameters** y lo sobrescriben.
  - **parameters_replica**: (opcional) sobrescrituras de parámetros específicas del rol para la réplica. Estos valores se combinan con **parameters** y lo sobrescriben.
  - **parameters_standby_leader**: (opcional) sobrescrituras de parámetros específicas del rol para standby_leader. Estos valores se combinan con **parameters** y lo sobrescriben.

  - **pg_hba**: lista de líneas que Patroni utilizará para generar `pg_hba.conf`. Patroni ignora este parámetro si el parámetro de PostgreSQL `hba_file` está establecido en un valor no predeterminado. Junto con la [configuración dinámica](/es/patroni/config/dynamic#dynamic), este parámetro simplifica la gestión de `pg_hba.conf`.

    - **- host all all 0.0.0.0/0 md5**
    - **- host replication replicator 127.0.0.1/32 md5**: se requiere una línea como esta para la replicación.
  - **pg_hba_primary**: (opcional) entradas pg_hba específicas del rol para el primario. Estas reemplazan completamente a **pg_hba** (sin combinación). Si no se definen, se utiliza **pg_hba**.
  - **pg_hba_replica**: (opcional) entradas pg_hba específicas del rol para la réplica. Estas reemplazan completamente a **pg_hba** (sin combinación). Si no se definen, se utiliza **pg_hba**.
  - **pg_hba_standby_leader**: (opcional) entradas pg_hba específicas del rol para standby_leader. Estas reemplazan completamente a **pg_hba** (sin combinación). Si no se definen, se utiliza **pg_hba**.

  - **pg_ident**: lista de líneas que Patroni utilizará para generar `pg_ident.conf`. Patroni ignora este parámetro si el parámetro de PostgreSQL `ident_file` está establecido en un valor no predeterminado. Junto con la [configuración dinámica](/es/patroni/config/dynamic#dynamic), este parámetro simplifica la gestión de `pg_ident.conf`.

    - **- mapname1 systemname1 pguser1**
    - **- mapname1 systemname2 pguser2**
  - **pg_ident_primary**: (opcional) entradas pg_ident específicas del rol para el primario. Estas reemplazan completamente a **pg_ident** (sin combinación). Si no se definen, se utiliza **pg_ident**.
  - **pg_ident_replica**: (opcional) entradas pg_ident específicas del rol para la réplica. Estas reemplazan completamente a **pg_ident** (sin combinación). Si no se definen, se utiliza **pg_ident**.
  - **pg_ident_standby_leader**: (opcional) entradas pg_ident específicas del rol para standby_leader. Estas reemplazan completamente a **pg_ident** (sin combinación). Si no se definen, se utiliza **pg_ident**.

  - **pg_ctl_timeout**: Cuánto debería esperar pg_ctl al hacer `start`, `stop` o `restart`. El valor predeterminado es 60 segundos.

  - **use_pg_rewind**: intenta usar pg_rewind en el antiguo líder cuando se une al clúster como réplica. El clúster debe inicializarse con `data page checksums` (opción `--data-checksums` para `initdb`) y/o `wal_log_hints` debe establecerse en `on`, o de lo contrario `pg_rewind` no funcionará.

  - **rewind**: (opcional) opciones personalizadas que pasar al comando `pg_rewind`. Puede especificarse como una lista de cadenas y/o diccionarios con un único par clave-valor. Las opciones no permitidas incluyen: `target-pgdata`, `source-pgdata`, `source-server`, `write-recovery-conf`, `dry-run`, `restore-target-wal`, `config-file`, `no-ensure-shutdown`, `version` y `help`. Ejemplo de uso:

    ```yaml
    postgresql:
      rewind:
        - debug
        - progress
        - sync-method: fsync
    ```

  - **remove_data_directory_on_rewind_failure**: Si esta opción está habilitada, Patroni eliminará el directorio de datos de PostgreSQL y recreará la réplica. De lo contrario, intentará seguir al nuevo líder. El valor predeterminado es **false**.

  - **remove_data_directory_on_diverged_timelines**: Patroni eliminará el directorio de datos de PostgreSQL y recreará la réplica si nota que las líneas de tiempo están divergiendo y el antiguo primario no puede iniciar el streaming desde el nuevo primario. Esta opción es útil cuando no se puede usar `pg_rewind`. Al realizar la comprobación de divergencia de líneas de tiempo en PostgreSQL v10 y anteriores, Patroni intentará conectarse con la credencial de replicación a la base de datos "postgres". Por lo tanto, dicho acceso debería estar permitido en el pg_hba.conf. El valor predeterminado es **false**.

  - **replica_method**: para cada create_replica_methods distinto de basebackup, añadirías una sección de configuración con el mismo nombre. Como mínimo, esta debería incluir "command" con una ruta completa al script real que se va a ejecutar. Otros parámetros de configuración se pasarán al script en la forma "parameter=value".

  - **pre_promote**: un script de aislamiento (fencing) que se ejecuta durante una conmutación por error después de adquirir el bloqueo de líder pero antes de promover la réplica. Si el script termina con un código distinto de cero, Patroni no promueve la réplica y elimina la clave de líder del DCS.

  - **before_stop**: un script que se ejecuta inmediatamente antes de detener postgres. A diferencia de un callback, este script se ejecuta de forma síncrona, bloqueando el apagado hasta que haya completado. El código de retorno de este script no afecta a si el apagado continúa después.

<a id="restapi_settings"></a>

--------

## REST API {#rest-api}

- **restapi**:
  - **thread_pool_size**: tamaño del pool de hilos utilizado por Patroni para procesar solicitudes de la REST API. El valor mínimo es `5`, el valor predeterminado es `5`.
  - **connect_address**: Dirección IP (o nombre de host) y puerto para acceder a la [REST API](/es/patroni/rest_api#rest_api) de Patroni. Todos los miembros del clúster deben poder alcanzar esta dirección. A menos que Patroni se use solo para una demostración local, usa una dirección de red en lugar de "localhost" o una dirección de bucle invertido como "127.0.0.1". Puede servir como endpoint para comprobaciones de estado HTTP (lee más abajo sobre el parámetro "listen" de la REST API), y también para consultas de usuario (ya sea directamente o mediante la REST API), así como para las comprobaciones de estado realizadas por los miembros del clúster durante las elecciones de líder (por ejemplo, para determinar si el líder sigue en ejecución, o si hay un nodo que tiene una posición WAL más avanzada que la del nodo que hace la consulta; etc.). La connect_address se pone en la clave del miembro en el DCS, lo que permite traducir el nombre del miembro a la dirección para conectarse a su REST API.
  - **listen**: Dirección IP (o nombre de host) y puerto en los que escuchará Patroni para la REST API - para proporcionar también las mismas comprobaciones de estado y la mensajería de clúster entre los nodos participantes, como se describió anteriormente. para proporcionar información de comprobación de estado para HAProxy (o cualquier otro balanceador de carga capaz de hacer comprobaciones HTTP "OPTIONS" o "GET").
  - **authentication**: (opcional)
    - **username**: Usuario de autenticación básica para proteger los endpoints no seguros de la REST API.
    - **password**: Contraseña de autenticación básica para proteger los endpoints no seguros de la REST API.
  - **certfile**: (opcional): Especifica el archivo con el certificado en formato PEM. Si el certfile no se especifica o se deja vacío, el servidor de la API funcionará sin SSL.
  - **keyfile**: (opcional): Especifica el archivo con la clave secreta en formato PEM.
  - **keyfile_password**: (opcional): Especifica una contraseña para descifrar el keyfile.
  - **cafile**: (opcional): Especifica el archivo con el CA_BUNDLE con certificados de CAs de confianza para usar al verificar certificados de cliente.
  - **ciphers**: (opcional): Especifica los conjuntos de cifrado permitidos (p. ej. "ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:!SSLv1:!SSLv2:!SSLv3:!TLSv1:!TLSv1.1")
  - **verify_client**: (opcional): `none` (predeterminado), `optional` o `required`. Con `none` la REST API no comprobará certificados de cliente. Con `required` se requieren certificados de cliente para todas las llamadas a la REST API. Con `optional` se requieren certificados de cliente para todos los endpoints no seguros de la REST API. Cuando se usa `required`, la autenticación del cliente tiene éxito si la verificación de la firma del certificado tiene éxito. Para `optional`, el certificado del cliente solo se comprobará para las solicitudes `PUT`, `POST`, `PATCH` y `DELETE`.
  - **allowlist**: (opcional): Especifica el conjunto de hosts a los que se permite llamar a los endpoints no seguros de la REST API. El elemento único puede ser un nombre de host, una dirección IP o una dirección de red en notación CIDR. Por defecto se usa `allow all`. En caso de que `allowlist` o `allowlist_include_members` estén establecidos, cualquier cosa que no esté incluida se rechaza.
  - **allowlist_include_members**: (opcional): Si se establece en `true`, permite acceder a los endpoints no seguros de la REST API desde otros miembros del clúster registrados en el DCS (la dirección IP o el nombre de host se toma del `api_url` de los miembros). Ten cuidado: podría ocurrir que el SO use una IP diferente para las conexiones salientes.
  - **http_extra_headers**: (opcional): Las cabeceras HTTP permiten al servidor de la REST API pasar información adicional con una respuesta HTTP.
  - **https_extra_headers**: (opcional): Las cabeceras HTTPS permiten al servidor de la REST API pasar información adicional con una respuesta HTTP cuando TLS está habilitado. Esto también pasará la información adicional establecida en `http_extra_headers`.
  - **request_queue_size**: (opcional): Establece el tamaño de la cola de solicitudes para el socket TCP utilizado por la REST API de Patroni. Una vez que la cola está llena, las solicitudes posteriores reciben un error "Connection denied". El valor predeterminado es 5.
  - **server_tokens**: (opcional): Configura el valor de la cabecera HTTP `Server`.
    - `Minimal`: La cabecera contendrá solo la versión de Patroni, p. ej. `Patroni/4.0.0`.
    - `ProductOnly`: La cabecera contendrá solo el nombre del producto, p. ej. `Patroni`.
    - `Original` (predeterminado): La cabecera expondrá el comportamiento original y mostrará las versiones de BaseHTTP y Python, p. ej. `BaseHTTP/0.6 Python/3.12.3`.

Aquí hay un ejemplo de **http_extra_headers** y **https_extra_headers**:

```yaml
restapi:
  listen: <listen>
  connect_address: <connect_address>
  authentication:
    username: <username>
    password: <password>
  http_extra_headers:
    'X-Frame-Options': 'SAMEORIGIN'
    'X-XSS-Protection': '1; mode=block'
    'X-Content-Type-Options': 'nosniff'
  cafile: <ca file>
  certfile: <cert>
  keyfile: <key>
  https_extra_headers:
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
```

<div class="warning">

<div class="title">

Advertencia

</div>

- El `restapi.connect_address` debe ser accesible desde todos los nodos de un clúster de Patroni dado. Internamente Patroni lo utiliza durante la carrera por el liderazgo para encontrar los nodos con el mínimo retraso de replicación.
- Si habilitaste la validación de certificados de cliente (`restapi.verify_client` está establecido en `required`), también **debes** proporcionar **certificados de cliente válidos** en `ctl.certfile`, `ctl.keyfile`, `ctl.keyfile_password`. Si no se proporcionan, Patroni no funcionará correctamente.

</div>

<a id="patronictl_settings"></a>

--------

## CTL {#ctl}

- **ctl**: (opcional)
  - **authentication**:
    - **username**: Usuario de autenticación básica para acceder a los endpoints protegidos de la REST API. Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) utilizará el valor proporcionado para el parámetro "username" de la REST API.
    - **password**: Contraseña de autenticación básica para acceder a los endpoints protegidos de la REST API. Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) utilizará el valor proporcionado para el parámetro "password" de la REST API.
  - **insecure**: Permite conexiones a la REST API sin verificar los certificados SSL.
  - **cacert**: Especifica el archivo con el CA_BUNDLE o el directorio con certificados de CAs de confianza para usar al verificar los certificados SSL de la REST API. Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) utilizará el valor proporcionado para el parámetro "cafile" de la REST API.
  - **certfile**: Especifica el archivo con el certificado de cliente en formato PEM.
  - **keyfile**: Especifica el archivo con la clave secreta de cliente en formato PEM.
  - **keyfile_password**: Especifica una contraseña para descifrar el keyfile del cliente.

--------

## Watchdog {#watchdog}

- **mode**: `off`, `automatic` o `required`. Con `off` el watchdog está desactivado. Con `automatic` se usará el watchdog si está disponible, pero se ignorará si no lo está. Con `required` el nodo no se convertirá en líder a menos que el watchdog pueda habilitarse con éxito.
- **device**: Ruta al dispositivo watchdog. El valor predeterminado es `/dev/watchdog`.
- **safety_margin**: Número de segundos de margen de seguridad entre el disparo del watchdog y la expiración de la clave de líder.

<a id="tags_settings"></a>

--------

## Etiquetas {#tags}

- **clonefrom**: `true` o `false`. Si se establece en `true`, otros nodos podrían preferir usar este nodo para el arranque (tomar `pg_basebackup` de él). Si hay varios nodos con la etiqueta `clonefrom` establecida en `true`, el nodo desde el que arrancar se elegirá aleatoriamente. El valor predeterminado es `false`.
- **noloadbalance**: `true` o `false`. Si se establece en `true`, el nodo devolverá el código de estado HTTP 503 para la comprobación de estado `GET /replica` de la REST API y, por lo tanto, será excluido del balanceo de carga. El valor predeterminado es `false`.
- **replicatefrom**: El nombre de otra réplica de la cual replicar. Se utiliza para soportar la replicación en cascada.
- **nosync**: `true` o `false`. Si se establece en `true`, el nodo nunca será seleccionado como réplica síncrona.
- **sync_priority**: entero, controla la prioridad que este nodo debería tener durante la selección de réplica síncrona cuando [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) está establecido en `on`. Los nodos con mayor prioridad serán preferidos sobre los nodos de menor prioridad. Si el `sync_priority` es 0 o negativo, dicho nodo no puede escribirse en el parámetro de PostgreSQL `synchronous_standby_names` (similar a `nosync: true`). Este parámetro ordena las prioridades en dirección inversa a la columna `sync_priority` de la vista `pg_stat_replication`.
- **nofailover**: `true` o `false`, controla si este nodo puede participar en la carrera por el liderazgo y convertirse en líder. El valor predeterminado es `false`, lo que significa que este nodo <span id="can">puede</span>\_ participar en las carreras por el liderazgo.
- **failover_priority**: entero, controla la prioridad que este nodo debería tener durante una conmutación por error. Los nodos con mayor prioridad serán preferidos sobre los nodos de menor prioridad si recibieron/reprodujeron la misma cantidad de WAL. Sin embargo, los nodos con valores más altos de LSN de recepción/reproducción son preferidos independientemente de su prioridad. Si el `failover_priority` es 0 o negativo, dicho nodo no puede participar en la carrera por el liderazgo ni convertirse en líder (similar a `nofailover: true`). Limitación conocida: `failover_priority` actualmente no funciona con la [replicación síncrona basada en cuórum](/es/patroni/replication_modes#quorum_mode).
- **nostream**: `true` o `false`. Si se establece en `true`, el nodo no utilizará el protocolo de replicación para transmitir WAL. En su lugar dependerá de la recuperación desde el archivado (si `restore_command` está configurado) y del sondeo de `pg_wal`/`pg_xlog`. También desactiva la copia y sincronización de los slots de replicación lógicos permanentes en el propio nodo y en todas sus réplicas en cascada. Establecer esta etiqueta en el nodo primario no tiene efecto.

> [!WARNING]
> Proporciona solo uno de `nofailover` o `failover_priority`. Proporcionar `nofailover: true` es lo mismo que `failover_priority: 0`, y proporcionar `nofailover: false` dará al nodo prioridad 1.

Además de estas etiquetas predefinidas, también puedes añadir las tuyas propias:

- **key1**: `true`
- **key2**: `false`
- **key3**: `1.4`
- **key4**: `"RandomString"`

Las etiquetas son visibles en la [REST API](/es/patroni/rest_api#rest_api) y en [patronictl_list](/es/patroni/patronictl#patronictl_list). También puedes comprobar la salud de una instancia utilizando estas etiquetas. Si la etiqueta no está definida para una instancia, o si el valor respectivo no coincide con el valor consultado, devolverá el código de estado HTTP 503.
