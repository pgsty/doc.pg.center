---
title: "Preguntas frecuentes"
linkTitle: "FAQ"
weight: 90
description: "Preguntas frecuentes sobre PgBouncer"
icon: fa-solid fa-circle-question
module: [PGBOUNCER]
categories: [Referencia]
upstream_link: "https://www.pgbouncer.org/faq.html"
---

--------

## ¿Cómo conectarse a PgBouncer? {#how-to-connect-to-pgbouncer}

PgBouncer actúa como un servidor de Postgres, así que simplemente apunta tu
cliente al puerto de PgBouncer.

--------

## ¿Cómo realizar el balanceo de carga de las consultas entre varios servidores? {#how-to-load-balance-queries-between-several-servers}

PgBouncer admite una lista de hosts separados por comas en una cadena de
conexión de base de datos. Con
[`load_balance_hosts=round-robin`](/es/pgbouncer/config/#load_balance_hosts),
las nuevas conexiones de servidor rotan a través de esa lista. Por ejemplo:

```ini
[databases]
app = host=pg1,pg2 port=5432 dbname=app load_balance_hosts=round-robin
```

También puedes usar herramientas externas:

1.  DNS round-robin. Usa varias IP detrás de un mismo nombre DNS. PgBouncer
    no consulta el DNS cada vez que se lanza una nueva conexión. En su lugar,
    almacena en caché todas las IP y hace round-robin internamente. Nota: si
    hay más de 8 IP detrás de un nombre, el backend de DNS debe ser
    compatible con el protocolo EDNS0. Consulta
    [Soporte de resolución DNS](/es/pgbouncer/install/#dns-lookup-support) para más detalles.

2.  Usa un balanceador de carga de conexiones TCP. Tanto
    [LVS](http://www.linuxvirtualserver.org/) como
    [HAProxy](https://www.haproxy.org/) parecen ser buenas opciones. Por el
    lado de PgBouncer puede ser buena idea reducir `server_lifetime` y
    también activar `server_round_robin`: de forma predeterminada, las
    conexiones inactivas se reutilizan mediante un algoritmo LIFO, que puede
    no funcionar tan bien cuando se necesita balanceo de carga.

--------

## Cómo realizar una conmutación por error {#how-to-failover}

Con una lista de hosts separados por comas y
[`load_balance_hosts=disable`](/es/pgbouncer/config/#load_balance_hosts),
PgBouncer sigue usando el mismo host hasta que falla un intento de conexión;
entonces prueba el siguiente host. Esto no realiza la detección de rol
primario/réplica. Para una conmutación por error que siga los cambios en la
topología de la base de datos, usa herramientas externas:

1. Reconfiguración de DNS: cuando la dirección IP detrás de un nombre DNS se
   reconfigura, PgBouncer se reconectará al nuevo servidor. Este
   comportamiento puede ajustarse con dos parámetros de configuración:
   `dns_max_ttl` ajusta el tiempo de vida de un nombre de host, y
   `dns_zone_check_period` ajusta la frecuencia con la que se consultará el
   SOA de una zona para detectar cambios. Si un registro SOA de zona ha
   cambiado, PgBouncer volverá a consultar todos los nombres de host de esa
   zona.

2. Escribe un nuevo host en la configuración y deja que PgBouncer la
   recargue: envía SIGHUP o usa el comando `RELOAD` en la consola. PgBouncer
   detectará una configuración de host modificada y se reconectará al nuevo
   servidor.

3. Usa el comando `RECONNECT`. Está pensado para situaciones en las que
   ninguna de las dos opciones anteriores es aplicable, por ejemplo cuando
   usas el HAProxy mencionado anteriormente para enrutar conexiones aguas
   abajo de PgBouncer. `RECONNECT` simplemente provoca que se reabran todas
   las conexiones de servidor. Por tanto, ejecútalo después de que ese otro
   componente haya cambiado su información de enrutamiento de conexiones.

--------

## ¿Cómo usar instrucciones preparadas con la agrupación de sesiones? {#how-to-use-prepared-statements-with-session-pooling}

En el modo de agrupación de sesiones, la consulta de restablecimiento debe
limpiar las instrucciones preparadas antiguas. Esto puede lograrse con
`server_reset_query = DISCARD ALL;` o al menos `DEALLOCATE ALL;`.

--------

## ¿Cómo usar instrucciones preparadas con la agrupación de transacciones? {#how-to-use-prepared-statements-with-transaction-pooling}

Desde la versión 1.21.0, PgBouncer puede rastrear las instrucciones preparadas
en el modo de agrupación de transacciones y asegurarse de que se preparen
sobre la marcha en la conexión de servidor vinculada. Para activar esta
característica, `max_prepared_statements` debe establecerse en un valor
distinto de cero (el valor predeterminado es 200). Consulta la [documentación
de `max_prepared_statements`](/es/pgbouncer/config/#max_prepared_statements)
para más detalles.

Si usas PHP/PDO, según su versión podría ser incompatible con el soporte de
instrucciones preparadas de PgBouncer ([#991]). PHP/PDO solo es compatible
cuando se usan [PHP 8.4+ **y** libpq 17][php-fix]. Por ello, para
configuraciones con versiones más antiguas se recomienda actualizar, o
desactivar las instrucciones preparadas en el lado del cliente.

[php-fix]: https://github.com/php/php-src/commit/f35ad560b468e3e0a6c289949ba9b19af4fa3e7b

[#991]: https://github.com/pgbouncer/pgbouncer/issues/991

### Desactivación de las instrucciones preparadas en JDBC {#disabling-prepared-statements-in-jdbc}

La forma correcta de hacerlo para JDBC es añadir el parámetro
`prepareThreshold=0` a la cadena de conexión.

### Desactivación de las instrucciones preparadas en PHP/PDO {#disabling-prepared-statements-in-phppdo}

Para desactivar el uso de instrucciones preparadas del lado del servidor, el
atributo de PDO `PDO::ATTR_EMULATE_PREPARES` debe establecerse en `true`. Ya
sea en el momento de la conexión:

    $db = new PDO("dsn", "user", "pass", array(PDO::ATTR_EMULATE_PREPARES => true));

o más tarde:

    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, true);

--------

## ¿Cómo actualizar PgBouncer sin cortar las conexiones? {#how-to-upgrade-pgbouncer-without-dropping-connections}

Puedes usar un reinicio progresivo siguiendo el procedimiento descrito en la
[sección de la documentación de `SHUTDOWN WAIT_FOR_CLIENTS`](/es/pgbouncer/usage/#shutdown-wait_for_clients).

--------

## ¿Cómo saber qué cliente está en qué conexión de servidor? {#how-to-know-which-client-is-on-which-server-connection}

Usa los comandos `SHOW CLIENTS` y `SHOW SERVERS` en la consola.

1.  Usa `ptr` y `link` para mapear la conexión local del cliente con la
    conexión de servidor.

2.  Usa `addr` y `port` de la conexión del cliente para identificar la
    conexión TCP procedente del cliente.

3.  Usa `local_addr` y `local_port` para identificar la conexión TCP con el
    servidor.

--------

## ¿Se debería instalar PgBouncer en el servidor web o en el servidor de bases de datos? {#should-pgbouncer-be-installed-on-the-web-server-or-database-server}

Depende.

Instalar PgBouncer en el servidor web es adecuado cuando se usan conexiones
de corta duración. Así se minimiza la latencia de establecimiento de la
conexión. (TCP requiere un par de recorridos de ida y vuelta de paquetes
antes de que una conexión sea utilizable.) Instalar PgBouncer en el servidor
de bases de datos es adecuado cuando hay muchos hosts diferentes (p. ej.,
servidores web) conectándose a él. Así, sus conexiones pueden optimizarse
conjuntamente.

También es posible instalar PgBouncer tanto en el servidor web como en el
servidor de bases de datos. Un aspecto negativo de ello es que cada salto de
PgBouncer añade una pequeña cantidad de latencia a cada consulta.

Al final, tendrás que probar qué modelo funciona mejor para tus necesidades
de rendimiento. También debes considerar cómo afectará la instalación de
PgBouncer a la conmutación por error de tus aplicaciones en caso de que un
servidor web o un servidor de bases de datos deje de estar disponible.
