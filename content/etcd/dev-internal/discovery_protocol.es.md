---
title: Protocolo del servicio de descubrimiento
weight: 1500
description: Descubrir a los demás miembros de etcd durante la fase de arranque de un clúster
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-internal/discovery_protocol.md"
---

El protocolo del servicio de descubrimiento ayuda a un nuevo miembro de etcd a descubrir a todos los demás miembros durante la fase de arranque del clúster, usando un token de descubrimiento compartido y una lista de endpoints.

El protocolo del servicio de descubrimiento se usa _únicamente_ en la fase de arranque del clúster, y no puede usarse para la reconfiguración en tiempo de ejecución ni para la supervisión del clúster.

El protocolo usa un nuevo token de descubrimiento para arrancar un clúster de etcd _único_. Recuerda que un token de descubrimiento solo puede representar un clúster de etcd. En cuanto el protocolo de descubrimiento sobre este token comienza, aunque falle a mitad de camino, no debe usarse para arrancar otro clúster de etcd.

El resto de este artículo recorrerá el proceso de descubrimiento con ejemplos que corresponden a un clúster de descubrimiento autoalojado.

Ten en cuenta que este documento solo trata del descubrimiento v3. Consulta el documento anterior para obtener más detalles sobre el [descubrimiento v2][v2-discovery].

## Flujo de trabajo del protocolo {#protocol-workflow}

La idea del protocolo de descubrimiento es usar un clúster interno de etcd para coordinar el arranque de un clúster nuevo. Primero, todos los miembros nuevos interactúan con el servicio de descubrimiento y ayudan a generar la lista de miembros esperada. Luego, cada miembro nuevo arranca su servidor usando esta lista, lo que proporciona la misma funcionalidad que la opción -initial-cluster.

En el siguiente flujo de trabajo de ejemplo, listaremos cada paso del protocolo usando el comando `etcdctl` para facilitar la comprensión, y suponemos que `http://example.com:2379` aloja un clúster de etcd para el servicio de descubrimiento.

Por convención, el protocolo de descubrimiento de etcd usa el prefijo de clave `/_etcd/registry`.


### Creación de un nuevo token de descubrimiento {#creating-a-new-discovery-token}

Genera un token único que identificará el clúster nuevo. Este se usará como prefijo único en el espacio de claves de descubrimiento en los pasos siguientes. Una forma sencilla de hacerlo es usar `uuidgen`:

```
UUID=$(uuidgen)
```

### Especificación del tamaño esperado del clúster {#specifying-the-expected-cluster-size}

El token de descubrimiento espera un tamaño de clúster que debe especificarse. El servicio de descubrimiento usa este tamaño para saber cuándo ha encontrado todos los miembros que formarán inicialmente el clúster.

```
etcdctl --endpoints=http://example.com:2379 put /_etcd/registry/${UUID}/_config/size ${cluster_size}
```

Normalmente, el tamaño del clúster es 3, 5 o 7. Consulta el [tamaño óptimo del clúster][cluster-size] para obtener más detalles.

### Inicio de los procesos de etcd {#bringing-up-etcd-processes}

Establece el token de descubrimiento `${UUID}` en la opción `--discovery-token`, y establece los endpoints del clúster de etcd que respalda el servicio de descubrimiento en la opción `--discovery-endpoints`. Esto habilitará el descubrimiento v3 para arrancar el clúster de etcd.

Cada proceso de etcd seguirá internamente los pasos siguientes si se proporcionan las opciones `--discovery-token` y `--discovery-endpoints`.

Si el servicio de descubrimiento habilita la autenticación mediante certificado de cliente, configura las siguientes opciones. Su uso sigue exactamente el mismo patrón que el uso de `etcdctl` para comunicarse con un clúster de etcd.
```
--discovery-insecure-transport
--discovery-insecure-skip-tls-verify
--discovery-cert
--discovery-key
--discovery-cacert
```

Si el servicio de descubrimiento habilita la autenticación basada en roles, configura las siguientes opciones. Su uso sigue exactamente el mismo patrón que el uso de `etcdctl` para comunicarse con un clúster de etcd.
```
--discovery-user
--discovery-password
```

Los valores de tiempo o de tiempo de espera predeterminados también se pueden cambiar con las siguientes opciones, que se usan exactamente igual que `etcdctl` para comunicarse con un clúster de etcd.
```
--discovery-dial-timeout
--discovery-request-timeout
--discovery-keepalive-time
--discovery-keepalive-timeout
```

### Autorregistro {#registering-itself}

Lo primero que hace cada proceso de etcd es registrarse como miembro en el clúster nuevo dado. Esto se hace creando el ID de miembro como clave en la clave completa del registro.

```
etcdctl --endpoints=http://example.com:2379 put /_etcd/registry/${UUID}/members/${member_id} ${member_name}=${member_peer_url_1}&${member_name}=${member_peer_url_2}
```

### Comprobación del estado {#checking-the-status}

Comprueba el tamaño esperado del clúster y el estado del registro, y decide cuál es la siguiente acción.

```
etcdctl --endpoints=http://example.com:2379 get /_etcd/registry/${UUID}/_config/size
etcdctl --endpoints=http://example.com:2379 get /_etcd/registry/${UUID}/members
```

Si todavía no hay suficientes miembros registrados, esperará a que aparezcan otros miembros.

Si el número de miembros registrados es mayor que el tamaño esperado N, trata los primeros N miembros registrados como la lista de miembros del clúster. Si el propio miembro está en la lista de miembros, el procedimiento de descubrimiento tiene éxito y obtiene todos los pares a través de la lista de miembros. Si no está en la lista de miembros, el procedimiento de descubrimiento termina con el fallo de que el clúster está completo.

El miembro puede comprobar el estado del clúster incluso antes de registrarse. Por lo tanto, puede fallar rápidamente si el clúster está completo.

### Espera de todos los miembros {#waiting-for-all-members}

El proceso de espera sigue observando el prefijo de clave `/_etcd/registry/${UUID}/members` hasta encontrar todos los miembros.

```
etcdctl --endpoints=http://example.com:2379 watch /_etcd/registry/${UUID}/members --prefix
```

[v2-discovery]: https://etcd.io/docs/v3.5/dev-internal/discovery_protocol
[cluster-size]: https://etcd.io/docs/v2.3/admin_guide#optimal-cluster-size
[expected-cluster-size]: #specifying-the-expected-cluster-size
[new-discovery-token]: #creating-a-new-discovery-token
