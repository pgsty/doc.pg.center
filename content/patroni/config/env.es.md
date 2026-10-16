---
title: "Ajustes de configuración por entorno"
linkTitle: "Configuración por entorno"
weight: 30
icon: fa-solid fa-sliders
description: "Variables de entorno para sobrescribir parámetros de configuración de Patroni."
module: [PATRONI]
categories: [Referencia]
upstream_link: "https://patroni.readthedocs.io/en/latest/ENVIRONMENT.html"
---

<a id="env"></a>
Es posible sobrescribir algunos de los parámetros de configuración definidos en el archivo de configuración de Patroni utilizando las variables de entorno del sistema. Este documento lista todas las variables de entorno gestionadas por Patroni. Los valores establecidos mediante esas variables siempre tienen precedencia sobre los establecidos en el archivo de configuración de Patroni.

--------

## Global/Universal {#globaluniversal}

- **PATRONI_CONFIGURATION**: es posible establecer toda la configuración de Patroni mediante la variable de entorno [PATRONI_CONFIGURATION](/es/patroni/config#config). En este caso, ¡no se considerará ninguna otra variable de entorno!
- **PATRONI_THREAD_POOL_SIZE**: tamaño del pool de hilos utilizado por Patroni para ejecutar tareas asíncronas y comunicarse vía REST API con otros miembros durante la carrera por el liderazgo o las comprobaciones failsafe. El valor mínimo es `5`, el valor predeterminado es `5`.
- **PATRONI_THREAD_STACK_SIZE**: especifica el tamaño de pila que se utilizará para los hilos iniciados por Patroni. El valor debe estar alineado por `64kB`. El valor mínimo es `64kB`, el valor predeterminado (establecido por Patroni) es `512kB`.
- **PATRONI_NAME**: nombre del nodo donde se ejecuta la instancia actual de Patroni. Debe ser único para el clúster.
- **PATRONI_NAMESPACE**: ruta dentro del almacén de configuración donde Patroni guardará la información sobre el clúster. Valor predeterminado: "/service"
- **PATRONI_SCOPE**: nombre del clúster
- **PG_MALLOC_ARENA_MAX**: valor personalizado para la variable de entorno `MALLOC_ARENA_MAX` para el proceso `postmaster`. Si no está establecido, `postmaster` heredará el valor de `MALLOC_ARENA_MAX`.

--------

## Registro {#log}

- **PATRONI_LOG_TYPE**: establece el formato de los registros. Puede ser **plain** o **json**. Para usar el formato **json**, debes tener instalado el [jsonlogger](/es/patroni/installation#extras). El valor predeterminado es **plain**.
- **PATRONI_LOG_LEVEL**: establece el nivel general de registro. El valor predeterminado es **INFO** (ver [la documentación del registro de Python](https://docs.python.org/3.6/library/logging.html#levels))
- **PATRONI_LOG_TRACEBACK_LEVEL**: establece el nivel en el que los tracebacks serán visibles. El valor predeterminado es **ERROR**. Establécelo en **DEBUG** si quieres ver los tracebacks solo cuando habilites **PATRONI_LOG_LEVEL=DEBUG**.
- **PATRONI_LOG_FORMAT**: establece la cadena de formato del registro. Si el tipo de registro es **plain**, el formato del registro debe ser una cadena. Consulta [los atributos de LogRecord](https://docs.python.org/3.6/library/logging.html#logrecord-attributes) para ver los atributos disponibles. Si el tipo de registro es **json**, el formato del registro puede ser una lista además de una cadena. Cada elemento de la lista debe corresponder a atributos de LogRecord. Ten cuidado: solo se requiere el nombre del campo, y **%(** y **)** deben omitirse. Si deseas imprimir un campo del registro con un nombre de clave diferente, usa un diccionario donde la clave del diccionario sea el campo del registro y el valor sea el nombre del campo que quieres que se imprima en el registro. El valor predeterminado es **%(asctime)s %(levelname)s: %(message)s**
- **PATRONI_LOG_DATEFORMAT**: establece la cadena de formato de fecha y hora. (ver la [documentación de formatTime()](https://docs.python.org/3.6/library/logging.html#logging.Formatter.formatTime))
- **PATRONI_LOG_STATIC_FIELDS**: añade campos adicionales al registro. Esta opción solo está disponible cuando el tipo de registro está establecido en **json**. Ejemplo `PATRONI_LOG_STATIC_FIELDS="{app: patroni}"`
- **PATRONI_LOG_MAX_QUEUE_SIZE**: Patroni utiliza un registro en dos pasos. Los registros se escriben en la cola en memoria y hay un hilo separado que los extrae de la cola y los escribe en stderr o en un archivo. El tamaño máximo de la cola interna está limitado por defecto a **1000** registros, lo que basta para conservar los registros de las últimas 1h20m.
- **PATRONI_LOG_DIR**: Directorio donde escribir los registros de la aplicación. El directorio debe existir y ser escribible por el usuario que ejecuta Patroni. Si estableces esta variable de entorno, la aplicación conservará 4 registros de 25MB por defecto. Puedes ajustar esos valores de retención con `PATRONI_LOG_FILE_NUM` y `PATRONI_LOG_FILE_SIZE` (ver abajo).
- **PATRONI_LOG_MODE**: Permisos para los archivos de registro (por ejemplo, `0644`). Si no se especifica, los permisos se establecerán en función del valor umask actual.
- **PATRONI_LOG_FILE_NUM**: El número de registros de la aplicación que se conservan.
- **PATRONI_LOG_FILE_SIZE**: Tamaño del archivo patroni.log (en bytes) que dispara una rotación de registro.
- **PATRONI_LOG_LOGGERS**: Redefine el nivel de registro por módulo de python. Ejemplo `PATRONI_LOG_LOGGERS="{patroni.postmaster: WARNING, urllib3: DEBUG}"`
- **PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS**: Si se establece en `true`, los registros de latido sucesivos que sean idénticos no se emitirán. El valor predeterminado es `false`.

> [!WARNING]
> La hora a la que se ejecuta el bucle de HA puede ser información muy valiosa para diagnosticar conmutaciones por error debidas al agotamiento de recursos y problemas similares. Cuando `PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS` está establecido en `true` no se generará ningún registro para la ejecución del bucle de HA (a menos que cambie el líder) y, por lo tanto, esta información potencialmente útil no estará disponible en los registros.

--------

## Citus {#citus}

Habilita la integración de Patroni con [Citus](https://docs.citusdata.com). Si está configurado, Patroni se encargará de registrar los nodos workers de Citus en el coordinador. Puedes encontrar más información sobre el soporte de Citus [aquí](/es/patroni/citus#citus).

- **PATRONI_CITUS_GROUP**: el id del grupo de Citus, entero. Usa `0` para el coordinador y `1`, `2`, etc... para los workers
- **PATRONI_CITUS_DATABASE**: la base de datos donde debe crearse la extensión [citus](/es/patroni/citus#citus). Debe ser la misma en el coordinador y en todos los workers. Actualmente solo se soporta una base de datos.

--------

## Consul {#consul}

- **PATRONI_CONSUL_HOST**: el host:puerto para el agente local de Consul.
- **PATRONI_CONSUL_URL**: url para el agente local de Consul, en formato: http(s)://host:port
- **PATRONI_CONSUL_PORT**: (opcional) puerto de Consul
- **PATRONI_CONSUL_SCHEME**: (opcional) **http** o **https**, el valor predeterminado es **http**
- **PATRONI_CONSUL_TOKEN**: (opcional) token de ACL
- **PATRONI_CONSUL_VERIFY**: (opcional) si verificar el certificado SSL para las solicitudes HTTPS
- **PATRONI_CONSUL_CACERT**: (opcional) El certificado de la CA. Si está presente habilitará la validación.
- **PATRONI_CONSUL_CERT**: (opcional) Archivo con el certificado de cliente
- **PATRONI_CONSUL_KEY**: (opcional) Archivo con la clave de cliente. Puede estar vacío si la clave forma parte del certificado.
- **PATRONI_CONSUL_DC**: (opcional) Centro de datos con el que comunicarse. Por defecto se utiliza el centro de datos del host.
- **PATRONI_CONSUL_CONSISTENCY**: (opcional) Selecciona el modo de consistencia de consul. Los valores posibles son `default`, `consistent` o `stale` (más detalles en la [referencia de la API de consul](https://www.consul.io/api/features/consistency.html/))
- **PATRONI_CONSUL_CHECKS**: (opcional) lista de comprobaciones de estado de Consul utilizadas para la sesión. Por defecto se utiliza una lista vacía.
- **PATRONI_CONSUL_REGISTER_SERVICE**: (opcional) si registrar o no un servicio con el nombre definido por el parámetro scope y la etiqueta master, primary, replica o standby-leader según el rol del nodo. El valor predeterminado es **false**
- **PATRONI_CONSUL_SERVICE_TAGS**: (opcional) etiquetas estáticas adicionales que añadir al servicio de Consul además del rol (`primary`/`replica`/`standby-leader`). Por defecto se utiliza una lista vacía.
- **PATRONI_CONSUL_SERVICE_CHECK_INTERVAL**: (opcional) con qué frecuencia realizar la comprobación de estado contra la url registrada
- **PATRONI_CONSUL_SERVICE_CHECK_TLS_SERVER_NAME**: (opcional) sobrescribe el host SNI al conectarse vía TLS; ver también la [referencia de la API de comprobación del agente consul](https://www.consul.io/api-docs/agent/check#tlsservername).

--------

## Etcd {#etcd}

- **PATRONI_ETCD_PROXY**: url del proxy para el etcd. Si te conectas al etcd mediante un proxy, usa este parámetro en lugar de **PATRONI_ETCD_URL**
- **PATRONI_ETCD_URL**: url para el etcd, en formato: http(s)://(username:password@)host:port
- **PATRONI_ETCD_HOSTS**: lista de endpoints de etcd en formato 'host1:port1','host2:port2',etc...
- **PATRONI_ETCD_USE_PROXIES**: Si este parámetro se establece en true, Patroni considerará **hosts** como una lista de proxies y no realizará un descubrimiento de la topología del clúster de etcd, sino que se ceñirá a una lista fija de **hosts**.
- **PATRONI_ETCD_PROTOCOL**: http o https; si no se especifica, se usa http. Si se especifica **url** o **proxy**, tomará el protocolo de ellos.
- **PATRONI_ETCD_HOST**: el host:puerto para el endpoint de etcd.
- **PATRONI_ETCD_SRV**: Dominio en el que buscar los registros SRV para el autodescubrimiento del clúster. Patroni intentará consultar estos nombres de servicio SRV para el dominio especificado (en ese orden hasta el primer éxito): `_etcd-client-ssl`, `_etcd-client`, `_etcd-ssl`, `_etcd`, `_etcd-server-ssl`, `_etcd-server`. Si se recuperan registros SRV para `_etcd-server-ssl` o `_etcd-server`, se utiliza el protocolo de pares de ETCD para consultar a ETCD por los miembros disponibles. De lo contrario, se utilizarán los hosts de los registros SRV.
- **PATRONI_ETCD_SRV_SUFFIX**: Configura un sufijo para el nombre SRV que se consulta durante el descubrimiento. Usa este flag para diferenciar entre múltiples clústeres de etcd bajo el mismo dominio. Funciona solo en conjunción con **PATRONI_ETCD_SRV**. Por ejemplo, si se establecen `PATRONI_ETCD_SRV_SUFFIX=foo` y `PATRONI_ETCD_SRV=example.org`, se realiza la siguiente consulta DNS SRV:`_etcd-client-ssl-foo._tcp.example.org` (y así sucesivamente para cada nombre de servicio SRV posible de ETCD).
- **PATRONI_ETCD_USERNAME**: usuario para la autenticación de etcd.
- **PATRONI_ETCD_PASSWORD**: contraseña para la autenticación de etcd.
- **PATRONI_ETCD_CACERT**: El certificado de la CA. Si está presente habilitará la validación.
- **PATRONI_ETCD_CERT**: Archivo con el certificado de cliente.
- **PATRONI_ETCD_KEY**: Archivo con la clave de cliente. Puede estar vacío si la clave forma parte del certificado.

--------

## Etcdv3 {#etcdv3}

Los nombres de las variables de entorno para Etcdv3 son similares a los de Etcd; solo necesitas usar `ETCD3` en lugar de `ETCD` en el nombre de la variable. Ejemplo: `PATRONI_ETCD3_HOST`, `PATRONI_ETCD3_CACERT`, y así sucesivamente.

> [!WARNING]
> Las claves creadas con la versión 2 del protocolo no son visibles con la versión 3 del protocolo y viceversa; por lo tanto, no es posible cambiar de Etcd a Etcdv3 solo actualizando la configuración de Patroni. Además, Patroni utiliza el gRPC-gateway (proxy) de Etcd para comunicarse con la API V3, lo que significa que la autenticación por nombre común de TLS no es posible.

--------

## ZooKeeper {#zookeeper}

- **PATRONI_ZOOKEEPER_HOSTS**: Lista separada por comas de los miembros del clúster de ZooKeeper: "'host1:port1','host2:port2','etc...'". ¡Es importante entrecomillar cada entidad!
- **PATRONI_ZOOKEEPER_USE_SSL**: (opcional) Si se usa SSL o no. El valor predeterminado es `false`. Si se establece en `false`, se ignoran todos los parámetros específicos de SSL.
- **PATRONI_ZOOKEEPER_CACERT**: (opcional) El certificado de la CA. Si está presente habilitará la validación.
- **PATRONI_ZOOKEEPER_CERT**: (opcional) Archivo con el certificado de cliente.
- **PATRONI_ZOOKEEPER_KEY**: (opcional) Archivo con la clave de cliente.
- **PATRONI_ZOOKEEPER_KEY_PASSWORD**: (opcional) La contraseña de la clave de cliente.
- **PATRONI_ZOOKEEPER_VERIFY**: (opcional) Si verificar el certificado o no. El valor predeterminado es `true`.
- **PATRONI_ZOOKEEPER_SET_ACLS**: (opcional) Si se establece, configura Kazoo para aplicar una ACL predeterminada a cada ZNode que cree. Las ACL pueden usar el esquema `x509` (predeterminado) u otros esquemas soportados de ZooKeeper como `digest`. Deben especificarse como un diccionario donde la clave es el principal completo (opcionalmente precedido del esquema) y el valor es una lista de permisos. Los permisos pueden ser uno o más de `CREATE`, `READ`, `WRITE`, `DELETE`, `ADMIN` o `ALL`. Por ejemplo, `set_acls: {CN=principal1: [CREATE, READ], digest:principal2:+pjROuBuuwNNSujKyH8dGcEnFPQ=: [ALL]}`.
- **PATRONI_ZOOKEEPER_AUTH_DATA**: (opcional) Credenciales de autenticación para usar en la conexión. Debe ser un diccionario de la forma en que `scheme` es la clave y `credential` es el valor. El valor predeterminado es un diccionario vacío.

> [!NOTE]
> Se requiere instalar `kazoo>=2.6.0` para soportar SSL.

--------

## Exhibitor {#exhibitor}

- **PATRONI_EXHIBITOR_HOSTS**: lista inicial de nodos de Exhibitor (ZooKeeper) en formato: 'host1,host2,etc...'. Esta lista se actualiza automáticamente cada vez que cambia la topología del clúster de Exhibitor (ZooKeeper).
- **PATRONI_EXHIBITOR_PORT**: Puerto de Exhibitor.

<a id="kubernetes_environment"></a>

--------

## Kubernetes {#kubernetes}

- **PATRONI_KUBERNETES_BYPASS_API_SERVICE**: (opcional) Al comunicarse con la API de Kubernetes, Patroni normalmente depende del servicio [kubernetes](/es/patroni/kubernetes#kubernetes), cuya dirección se expone en los pods mediante la variable de entorno `KUBERNETES_SERVICE_HOST`. Si `PATRONI_KUBERNETES_BYPASS_API_SERVICE` está establecido en `true`, Patroni resolverá la lista de nodos de la API detrás del servicio y se conectará directamente a ellos.
- **PATRONI_KUBERNETES_NAMESPACE**: (opcional) Espacio de nombres de Kubernetes donde se ejecuta el pod de Patroni. El valor predeterminado es `default`.
- **PATRONI_KUBERNETES_LABELS**: Etiquetas en formato `{label1: value1, label2: value2}`. Estas etiquetas se utilizarán para encontrar objetos existentes (Pods y Endpoints o ConfigMaps) asociados con el clúster actual. Además, Patroni las establecerá en cada objeto (Endpoint o ConfigMap) que cree.
- **PATRONI_KUBERNETES_SCOPE_LABEL**: (opcional) nombre de la etiqueta que contiene el nombre del clúster. El valor predeterminado es `cluster-name`.
- **PATRONI_KUBERNETES_BOOTSTRAP_LABELS**: (opcional) Etiquetas en formato `{label1: value1, label2: value2}`. Estas etiquetas se asignarán a un pod de Patroni cuando su estado sea `initializing new cluster`, `running custom bootstrap script`, `starting after custom bootstrap` o `creating replica`.
- **PATRONI_KUBERNETES_ROLE_LABEL**: (opcional) nombre de la etiqueta que contiene el rol (`primary`, `replica` u otro valor personalizado). Patroni establecerá esta etiqueta en el pod en el que se ejecuta. El valor predeterminado es `role`.
- **PATRONI_KUBERNETES_LEADER_LABEL_VALUE**: (opcional) valor de la etiqueta del pod cuando el rol de Postgres es `primary`. El valor predeterminado es `primary`.
- **PATRONI_KUBERNETES_FOLLOWER_LABEL_VALUE**: (opcional) valor de la etiqueta del pod cuando el rol de Postgres es `replica`. El valor predeterminado es `replica`.
- **PATRONI_KUBERNETES_STANDBY_LEADER_LABEL_VALUE**: (opcional) valor de la etiqueta del pod cuando el rol de Postgres es `standby_leader`. El valor predeterminado es `primary`.
- **PATRONI_KUBERNETES_TMP_ROLE_LABEL**: (opcional) nombre de la etiqueta temporal que contiene el rol (`primary` o `replica`). El valor de esta etiqueta siempre utilizará el predeterminado del rol correspondiente. Establece solo cuando sea necesario.
- **PATRONI_KUBERNETES_USE_ENDPOINTS**: (opcional) si se establece en true, Patroni utilizará Endpoints en lugar de ConfigMaps para ejecutar las elecciones de líder y mantener el estado del clúster.
- **PATRONI_KUBERNETES_POD_IP**: (opcional) Dirección IP del pod en el que se ejecuta Patroni. Este valor es necesario cuando `PATRONI_KUBERNETES_USE_ENDPOINTS` está habilitado y se utiliza para poblar los subconjuntos del endpoint del líder cuando el PostgreSQL del pod es promovido.
- **PATRONI_KUBERNETES_PORTS**: (opcional) si el objeto Service tiene el nombre para el puerto, el mismo nombre debe aparecer en el objeto Endpoint; de lo contrario, el servicio no funcionará. Por ejemplo, si tu servicio está definido como `{Kind: Service, spec: {ports: [{name: postgresql, port: 5432, targetPort: 5432}]}}`, entonces tienes que establecer `PATRONI_KUBERNETES_PORTS='[{"name": "postgresql", "port": 5432}]'` y Patroni lo utilizará para actualizar los subconjuntos del Endpoint del líder. Este parámetro se usa solo si `PATRONI_KUBERNETES_USE_ENDPOINTS` está establecido.
- **PATRONI_KUBERNETES_CACERT**: (opcional) Especifica el archivo con el CA_BUNDLE con certificados de CAs de confianza para usar al verificar los certificados SSL de la API de Kubernetes. Si no se proporciona, patroni utilizará el valor proporcionado por el secreto del ServiceAccount.
- **PATRONI_RETRIABLE_HTTP_CODES**: (opcional) lista de códigos de estado HTTP de la API de K8s sobre los que reintentar. Por defecto Patroni reintenta en `500`, `503` y `504`, o si la respuesta de la API de K8s tiene la cabecera HTTP `retry-after`.

--------

## Raft (en desuso) {#raft-deprecated}

- **PATRONI_RAFT_SELF_ADDR**: `ip:port` en el que escuchar conexiones Raft. El `self_addr` debe ser accesible desde los demás nodos del clúster. Si no se establece, el nodo no participará en el consenso.
- **PATRONI_RAFT_BIND_ADDR**: (opcional) `ip:port` en el que escuchar conexiones Raft. Si no se especifica, se utilizará el `self_addr`.
- **PATRONI_RAFT_PARTNER_ADDRS**: lista de otros nodos de Patroni en el clúster en formato `"'ip1:port1','ip2:port2'"`. ¡Es importante entrecomillar cada entidad!
- **PATRONI_RAFT_DATA_DIR**: directorio donde almacenar el registro y la instantánea de Raft. Si no se especifica, se utiliza el directorio de trabajo actual.
- **PATRONI_RAFT_PASSWORD**: (opcional) Cifra el tráfico Raft con una contraseña especificada; requiere el módulo de python `cryptography`.
- **PATRONI_RAFT_MIN_TIMEOUT**: (opcional) tiempo de espera mínimo de elección en segundos para la implementación Raft subyacente de pysyncobj. Debe ser mayor que 3 * `PATRONI_RAFT_APPEND_ENTRIES_PERIOD`. Predeterminado: `0.4`.
- **PATRONI_RAFT_MAX_TIMEOUT**: (opcional) tiempo de espera máximo de elección en segundos para la implementación Raft subyacente de pysyncobj. Debe ser mayor que `PATRONI_RAFT_MIN_TIMEOUT`. Predeterminado: `1.4`.
- **PATRONI_RAFT_CONNECTION_TIMEOUT**: (opcional) tiempo en segundos tras el cual una conexión sin datos recibidos se considera muerta. Debe ser mayor o igual que `PATRONI_RAFT_MAX_TIMEOUT`. Predeterminado: `3.5`.
- **PATRONI_RAFT_APPEND_ENTRIES_PERIOD**: (opcional) intervalo en segundos para enviar comandos de latido. Debe ser menor que un tercio de `PATRONI_RAFT_MIN_TIMEOUT`. Predeterminado: `0.1`.
- **PATRONI_RAFT_CONNECTION_RETRY_TIME**: (opcional) intervalo en segundos entre intentos de reconexión a nodos desconectados. Predeterminado: `5.0`.
- **PATRONI_RAFT_LEADER_FALLBACK_TIMEOUT**: (opcional) tiempo en segundos tras el cual un líder sin respuesta de la mayoría vuelve al estado de réplica. Debe ser mayor que `PATRONI_RAFT_APPEND_ENTRIES_PERIOD`. Predeterminado: `30.0`.

> [!NOTE]
> Patroni valida estas restricciones al arrancar y se negará a iniciar si se violan. Estos valores no pueden cambiarse en tiempo de ejecución y requieren un reinicio. Ver [ajustes de Raft](/es/patroni/config/yaml#raft_settings) para más detalles, incluida la limitación de latencia alta.

--------

## PostgreSQL {#postgresql}

- **PATRONI_POSTGRESQL_LISTEN**: Dirección IP + puerto al que escucha Postgres. Se permiten múltiples direcciones separadas por comas, siempre que el componente del puerto se añada al final de la última con dos puntos, es decir, `listen: 127.0.0.1,127.0.0.2:5432`. Patroni utilizará la primera dirección de esta lista para establecer conexiones locales al nodo de PostgreSQL.
- **PATRONI_POSTGRESQL_CONNECT_ADDRESS**: Dirección IP + puerto a través del cual Postgres es accesible desde otros nodos y aplicaciones.
- **PATRONI_POSTGRESQL_PROXY_ADDRESS**: Dirección IP + puerto a través del cual es accesible un pool de conexiones (por ejemplo, pgbouncer) que se ejecuta junto a Postgres. El valor se escribe en la clave del miembro en el DCS como `proxy_url` y podría usarse/ser útil para el descubrimiento de servicios.
- **PATRONI_POSTGRESQL_DATA_DIR**: La ubicación del directorio de datos de Postgres, ya sea existente o que será inicializado por Patroni.
- **PATRONI_POSTGRESQL_CONFIG_DIR**: La ubicación del directorio de configuración de Postgres; el valor predeterminado es el directorio de datos. Debe ser escribible por Patroni.
- **PATRONI_POSTGRESQL_BIN_DIR**: Ruta a los binarios de PostgreSQL. (pg_ctl, initdb, pg_controldata, pg_basebackup, postgres, pg_isready, pg_rewind) El valor predeterminado es una cadena vacía, lo que significa que se utilizará la variable de entorno PATH para encontrar los ejecutables.
- **PATRONI_POSTGRESQL_BIN_PG_CTL**: (opcional) Nombre personalizado para el binario `pg_ctl`.
- **PATRONI_POSTGRESQL_BIN_INITDB**: (opcional) Nombre personalizado para el binario `initdb`.
- **PATRONI_POSTGRESQL_BIN_PG_CONTROLDATA**: (opcional) Nombre personalizado para el binario `pg_controldata`.
- **PATRONI_POSTGRESQL_BIN_PG_BASEBACKUP**: (opcional) Nombre personalizado para el binario `pg_basebackup`.
- **PATRONI_POSTGRESQL_BIN_POSTGRES**: (opcional) Nombre personalizado para el binario `postgres`.
- **PATRONI_POSTGRESQL_BIN_IS_READY**: (opcional) Nombre personalizado para el binario `pg_isready`.
- **PATRONI_POSTGRESQL_BIN_PG_REWIND**: (opcional) Nombre personalizado para el binario `pg_rewind`.
- **PATRONI_POSTGRESQL_PGPASS**: ruta al archivo de contraseñas [.pgpass](https://www.postgresql.org/docs/current/static/libpq-pgpass.html). Patroni crea este archivo antes de ejecutar pg_basebackup y en algunas otras circunstancias. La ubicación debe ser escribible por Patroni.
- **PATRONI_REPLICATION_USERNAME**: usuario de replicación; el usuario se creará durante la inicialización. Las réplicas utilizarán este usuario para acceder al origen de replicación mediante replicación por streaming
- **PATRONI_REPLICATION_PASSWORD**: contraseña de replicación; el usuario se creará durante la inicialización.
- **PATRONI_REPLICATION_SSLMODE**: (opcional) se corresponde con el parámetro de conexión [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), que permite a un cliente especificar el tipo de modo de negociación TLS con el servidor. Para más información sobre cómo funciona cada modo, visita la [documentación de PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). El modo predeterminado es `prefer`.
- **PATRONI_REPLICATION_SSLKEY**: (opcional) se corresponde con el parámetro de conexión [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), que especifica la ubicación de la clave secreta utilizada con el certificado del cliente.
- **PATRONI_REPLICATION_SSLPASSWORD**: (opcional) se corresponde con el parámetro de conexión [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), que especifica la contraseña para la clave secreta especificada en `PATRONI_REPLICATION_SSLKEY`.
- **PATRONI_REPLICATION_SSLCERT**: (opcional) se corresponde con el parámetro de conexión [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), que especifica la ubicación del certificado de cliente.
- **PATRONI_REPLICATION_SSLROOTCERT**: (opcional) se corresponde con el parámetro de conexión [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), que especifica la ubicación de un archivo que contiene uno o más certificados de autoridades certificadoras (CA) que el cliente utilizará para verificar el certificado de un servidor.
- **PATRONI_REPLICATION_SSLCRL**: (opcional) se corresponde con el parámetro de conexión [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), que especifica la ubicación de un archivo que contiene una lista de revocación de certificados. Un cliente rechazará conectarse a cualquier servidor que tenga un certificado presente en esta lista.
- **PATRONI_REPLICATION_SSLCRLDIR**: (opcional) se corresponde con el parámetro de conexión [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), que especifica la ubicación de un directorio con archivos que contienen una lista de revocación de certificados. Un cliente rechazará conectarse a cualquier servidor que tenga un certificado presente en esta lista.
- **PATRONI_REPLICATION_SSLNEGOTIATION**: (opcional) se corresponde con el parámetro de conexión [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), que controla cómo se negocia el cifrado SSL con el servidor, si se usa SSL.
- **PATRONI_REPLICATION_GSSENCMODE**: (opcional) se corresponde con el parámetro de conexión [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), que determina si se negociará una conexión GSS TCP/IP segura con el servidor o con qué prioridad
- **PATRONI_REPLICATION_CHANNEL_BINDING**: (opcional) se corresponde con el parámetro de conexión [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), que controla el uso de channel binding por parte del cliente.
- **PATRONI_SUPERUSER_USERNAME**: nombre del superusuario, establecido durante la inicialización (initdb) y utilizado posteriormente por Patroni para conectarse a postgres. Este usuario también es utilizado por pg_rewind.
- **PATRONI_SUPERUSER_PASSWORD**: contraseña del superusuario, establecida durante la inicialización (initdb).
- **PATRONI_SUPERUSER_SSLMODE**: (opcional) se corresponde con el parámetro de conexión [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), que permite a un cliente especificar el tipo de modo de negociación TLS con el servidor. Para más información sobre cómo funciona cada modo, visita la [documentación de PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). El modo predeterminado es `prefer`.
- **PATRONI_SUPERUSER_SSLKEY**: (opcional) se corresponde con el parámetro de conexión [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), que especifica la ubicación de la clave secreta utilizada con el certificado del cliente.
- **PATRONI_SUPERUSER_SSLPASSWORD**: (opcional) se corresponde con el parámetro de conexión [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), que especifica la contraseña para la clave secreta especificada en `PATRONI_SUPERUSER_SSLKEY`.
- **PATRONI_SUPERUSER_SSLCERT**: (opcional) se corresponde con el parámetro de conexión [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), que especifica la ubicación del certificado de cliente.
- **PATRONI_SUPERUSER_SSLROOTCERT**: (opcional) se corresponde con el parámetro de conexión [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), que especifica la ubicación de un archivo que contiene uno o más certificados de autoridades certificadoras (CA) que el cliente utilizará para verificar el certificado de un servidor.
- **PATRONI_SUPERUSER_SSLCRL**: (opcional) se corresponde con el parámetro de conexión [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), que especifica la ubicación de un archivo que contiene una lista de revocación de certificados. Un cliente rechazará conectarse a cualquier servidor que tenga un certificado presente en esta lista.
- **PATRONI_SUPERUSER_SSLCRLDIR**: (opcional) se corresponde con el parámetro de conexión [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), que especifica la ubicación de un directorio con archivos que contienen una lista de revocación de certificados. Un cliente rechazará conectarse a cualquier servidor que tenga un certificado presente en esta lista.
- **PATRONI_SUPERUSER_SSLNEGOTIATION**: (opcional) se corresponde con el parámetro de conexión [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), que controla cómo se negocia el cifrado SSL con el servidor, si se usa SSL.
- **PATRONI_SUPERUSER_GSSENCMODE**: (opcional) se corresponde con el parámetro de conexión [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), que determina si se negociará una conexión GSS TCP/IP segura con el servidor o con qué prioridad
- **PATRONI_SUPERUSER_CHANNEL_BINDING**: (opcional) se corresponde con el parámetro de conexión [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), que controla el uso de channel binding por parte del cliente.
- **PATRONI_REWIND_USERNAME**: (opcional) nombre del usuario para `pg_rewind`; el usuario se creará durante la inicialización de postgres 11+ y se le concederán todos los [permisos](https://www.postgresql.org/docs/11/app-pgrewind.html#id-1.9.5.8.8) necesarios.
- **PATRONI_REWIND_PASSWORD**: (opcional) contraseña del usuario para `pg_rewind`; el usuario se creará durante la inicialización.
- **PATRONI_REWIND_SSLMODE**: (opcional) se corresponde con el parámetro de conexión [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), que permite a un cliente especificar el tipo de modo de negociación TLS con el servidor. Para más información sobre cómo funciona cada modo, visita la [documentación de PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). El modo predeterminado es `prefer`.
- **PATRONI_REWIND_SSLKEY**: (opcional) se corresponde con el parámetro de conexión [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), que especifica la ubicación de la clave secreta utilizada con el certificado del cliente.
- **PATRONI_REWIND_SSLPASSWORD**: (opcional) se corresponde con el parámetro de conexión [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), que especifica la contraseña para la clave secreta especificada en `PATRONI_REWIND_SSLKEY`.
- **PATRONI_REWIND_SSLCERT**: (opcional) se corresponde con el parámetro de conexión [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), que especifica la ubicación del certificado de cliente.
- **PATRONI_REWIND_SSLROOTCERT**: (opcional) se corresponde con el parámetro de conexión [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), que especifica la ubicación de un archivo que contiene uno o más certificados de autoridades certificadoras (CA) que el cliente utilizará para verificar el certificado de un servidor.
- **PATRONI_REWIND_SSLCRL**: (opcional) se corresponde con el parámetro de conexión [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), que especifica la ubicación de un archivo que contiene una lista de revocación de certificados. Un cliente rechazará conectarse a cualquier servidor que tenga un certificado presente en esta lista.
- **PATRONI_REWIND_SSLCRLDIR**: (opcional) se corresponde con el parámetro de conexión [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), que especifica la ubicación de un directorio con archivos que contienen una lista de revocación de certificados. Un cliente rechazará conectarse a cualquier servidor que tenga un certificado presente en esta lista.
- **PATRONI_REWIND_SSLNEGOTIATION**: (opcional) se corresponde con el parámetro de conexión [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), que controla cómo se negocia el cifrado SSL con el servidor, si se usa SSL.
- **PATRONI_REWIND_GSSENCMODE**: (opcional) se corresponde con el parámetro de conexión [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), que determina si se negociará una conexión GSS TCP/IP segura con el servidor o con qué prioridad
- **PATRONI_REWIND_CHANNEL_BINDING**: (opcional) se corresponde con el parámetro de conexión [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), que controla el uso de channel binding por parte del cliente.

--------

## REST API {#rest-api}

- **PATRONI_RESTAPI_THREAD_POOL_SIZE**: tamaño del pool de hilos utilizado por Patroni para procesar solicitudes de la REST API. El valor mínimo es `5`, el valor predeterminado es `5`.
- **PATRONI_RESTAPI_CONNECT_ADDRESS**: Dirección IP y puerto para acceder a la REST API.
- **PATRONI_RESTAPI_LISTEN**: Dirección IP y puerto en los que escuchará Patroni para proporcionar información de comprobación de estado para HAProxy.
- **PATRONI_RESTAPI_USERNAME**: Usuario de autenticación básica para proteger los endpoints no seguros de la REST API.
- **PATRONI_RESTAPI_PASSWORD**: Contraseña de autenticación básica para proteger los endpoints no seguros de la REST API.
- **PATRONI_RESTAPI_CERTFILE**: Especifica el archivo con el certificado en formato PEM. Si el certfile no se especifica o se deja vacío, el servidor de la API funcionará sin SSL.
- **PATRONI_RESTAPI_KEYFILE**: Especifica el archivo con la clave secreta en formato PEM.
- **PATRONI_RESTAPI_KEYFILE_PASSWORD**: Especifica una contraseña para descifrar el keyfile.
- **PATRONI_RESTAPI_CAFILE**: Especifica el archivo con el CA_BUNDLE con certificados de CAs de confianza para usar al verificar certificados de cliente.
- **PATRONI_RESTAPI_CIPHERS**: (opcional) Especifica los conjuntos de cifrado permitidos (p. ej. "ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:!SSLv1:!SSLv2:!SSLv3:!TLSv1:!TLSv1.1")
- **PATRONI_RESTAPI_VERIFY_CLIENT**: `none` (predeterminado), `optional` o `required`. Con `none` la REST API no comprobará certificados de cliente. Con `required` se requieren certificados de cliente para todas las llamadas a la REST API. Con `optional` se requieren certificados de cliente para todos los endpoints no seguros de la REST API. Cuando se usa `required`, la autenticación del cliente tiene éxito si la verificación de la firma del certificado tiene éxito. Para `optional`, el certificado del cliente solo se comprobará para las solicitudes `PUT`, `POST`, `PATCH` y `DELETE`.
- **PATRONI_RESTAPI_ALLOWLIST**: (opcional): Especifica el conjunto de hosts a los que se permite llamar a los endpoints no seguros de la REST API. El elemento único puede ser un nombre de host, una dirección IP o una dirección de red en notación CIDR. Por defecto se usa `allow all`. En caso de que `allowlist` o `allowlist_include_members` estén establecidos, cualquier cosa que no esté incluida se rechaza.
- **PATRONI_RESTAPI_ALLOWLIST_INCLUDE_MEMBERS**: (opcional): Si se establece en `true`, permite acceder a los endpoints no seguros de la REST API desde otros miembros del clúster registrados en el DCS (la dirección IP o el nombre de host se toma del `api_url` de los miembros). Ten cuidado: podría ocurrir que el SO use una IP diferente para las conexiones salientes.
- **PATRONI_RESTAPI_HTTP_EXTRA_HEADERS**: (opcional) Las cabeceras HTTP permiten al servidor de la REST API pasar información adicional con una respuesta HTTP.
- **PATRONI_RESTAPI_HTTPS_EXTRA_HEADERS**: (opcional) Las cabeceras HTTPS permiten al servidor de la REST API pasar información adicional con una respuesta HTTP cuando TLS está habilitado. Esto también pasará la información adicional establecida en `http_extra_headers`.
- **PATRONI_RESTAPI_REQUEST_QUEUE_SIZE**: (opcional): Establece el tamaño de la cola de solicitudes para el socket TCP utilizado por la REST API de Patroni. Una vez que la cola está llena, las solicitudes posteriores reciben un error "Connection denied". El valor predeterminado es 5.
- **PATRONI_RESTAPI_SERVER_TOKENS**: (opcional) Configura el valor de la cabecera HTTP `Server`. `Original` (predeterminado) expondrá el comportamiento original y mostrará las versiones de BaseHTTP y Python, p. ej. `BaseHTTP/0.6 Python/3.12.3`. `Minimal`: La cabecera contendrá solo la versión de Patroni, p. ej. `Patroni/4.0.0`. `ProductOnly`: La cabecera contendrá solo el nombre del producto, p. ej. `Patroni`.

<div class="warning">

<div class="title">

Advertencia

</div>

- El `PATRONI_RESTAPI_CONNECT_ADDRESS` debe ser accesible desde todos los nodos de un clúster de Patroni dado. Internamente Patroni lo utiliza durante la carrera por el liderazgo para encontrar los nodos con el mínimo retraso de replicación.
- Si habilitaste la validación de certificados de cliente (`PATRONI_RESTAPI_VERIFY_CLIENT` está establecido en `required`), también **debes** proporcionar **certificados de cliente válidos** en `PATRONI_CTL_CERTFILE`, `PATRONI_CTL_KEYFILE`, `PATRONI_CTL_KEYFILE_PASSWORD`. Si no se proporcionan, Patroni no funcionará correctamente.

</div>

--------

## CTL {#ctl}

- **PATRONICTL_CONFIG_FILE**: (opcional) ubicación del archivo de configuración.
- **PATRONI_CTL_USERNAME**: (opcional) Usuario de autenticación básica para acceder a los endpoints protegidos de la REST API. Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) utilizará el valor proporcionado para el parámetro "username" de la REST API.
- **PATRONI_CTL_PASSWORD**: (opcional) Contraseña de autenticación básica para acceder a los endpoints protegidos de la REST API. Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) utilizará el valor proporcionado para el parámetro "password" de la REST API.
- **PATRONI_CTL_INSECURE**: (opcional) Permite conexiones a la REST API sin verificar los certificados SSL.
- **PATRONI_CTL_CACERT**: (opcional) Especifica el archivo con el CA_BUNDLE o el directorio con certificados de CAs de confianza para usar al verificar los certificados SSL de la REST API. Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) utilizará el valor proporcionado para el parámetro "cafile" de la REST API.
- **PATRONI_CTL_CERTFILE**: (opcional) Especifica el archivo con el certificado de cliente en formato PEM.
- **PATRONI_CTL_KEYFILE**: (opcional) Especifica el archivo con la clave secreta de cliente en formato PEM.
- **PATRONI_CTL_KEYFILE_PASSWORD**: (opcional) Especifica una contraseña para descifrar el keyfile del cliente.
