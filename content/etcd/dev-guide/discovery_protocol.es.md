---
title: Protocolo del servicio de descubrimiento
weight: 1500
description: Descubrir otros miembros de etcd en la fase de arranque de un clúster
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/discovery_protocol.md"
---

> [!NOTE]
> Esta página documenta el antiguo protocolo de descubrimiento v2, que se eliminó en etcd 3.7. Para un despliegue nuevo con v3.7, usa el [protocolo de descubrimiento v3](/es/etcd/dev-internal/discovery_protocol/).

El protocolo del servicio de descubrimiento ayuda a un nuevo miembro de etcd a descubrir a todos los demás miembros durante la fase de arranque del clúster mediante una URL de descubrimiento compartida.

El protocolo del servicio de descubrimiento se usa _únicamente_ en la fase de arranque del clúster y no puede usarse para la reconfiguración en tiempo de ejecución ni para la monitorización del clúster.

El protocolo usa un token de descubrimiento nuevo para arrancar un clúster de etcd _único_. Recuerda que un token de descubrimiento solo puede representar un clúster de etcd. En cuanto el protocolo de descubrimiento comienza con ese token, aunque falle a mitad de camino, no debe usarse para arrancar otro clúster de etcd.

El resto de este artículo recorre el proceso de descubrimiento con ejemplos que corresponden a un clúster de descubrimiento autoalojado. El servicio público de descubrimiento, discovery.etcd.io, funciona de la misma manera, pero con una capa de acabado que oculta las URL poco estéticas, genera UUID automáticamente y ofrece ciertas protecciones contra solicitudes excesivas. En esencia, el servicio público de descubrimiento sigue usando un clúster de etcd como almacén de datos, tal como se describe en este documento.

## Flujo de trabajo del protocolo {#protocol-workflow}

La idea del protocolo de descubrimiento es usar un clúster de etcd interno para coordinar el arranque de un clúster nuevo. Primero, todos los miembros nuevos interactúan con el servicio de descubrimiento y ayudan a generar la lista de miembros esperada. Luego, cada miembro nuevo arranca su servidor usando esa lista, lo que ofrece la misma funcionalidad que la opción -initial-cluster.

En el siguiente flujo de trabajo de ejemplo, enumeraremos cada paso del protocolo en formato curl para facilitar su comprensión.

Por convención, el protocolo de descubrimiento de etcd usa el prefijo de clave `_etcd/registry`. Si `http://example.com` aloja un clúster de etcd para el servicio de descubrimiento, la URL completa del espacio de claves de descubrimiento será `http://example.com/v2/keys/_etcd/registry`. Usaremos esta URL como prefijo en el ejemplo.

### Creación de un token de descubrimiento nuevo {#creating-a-new-discovery-token}

Genera un token único que identificará el clúster nuevo. Este token se usará como prefijo único en el espacio de claves de descubrimiento en los pasos siguientes. Una forma sencilla de hacerlo es usar `uuidgen`:

```
UUID=$(uuidgen)
```

### Especificación del tamaño esperado del clúster {#specifying-the-expected-cluster-size}

El token de descubrimiento espera un tamaño de clúster que debe especificarse. El servicio de descubrimiento usa este tamaño para saber cuándo ha encontrado todos los miembros que formarán inicialmente el clúster.

```
curl -X PUT http://example.com/v2/keys/_etcd/registry/${UUID}/_config/size -d value=${cluster_size}
```

Normalmente el tamaño del clúster es 3, 5 o 7. Consulta [tamaño óptimo del clúster][cluster-size] para más detalles.

### Inicio de los procesos de etcd {#bringing-up-etcd-processes}

Dada la URL de descubrimiento, úsala como opción `-discovery` e inicia los procesos de etcd. Cada proceso de etcd seguirá internamente los pasos siguientes si se le proporciona una opción `-discovery`.

### Registro del propio miembro {#registering-itself}

Lo primero que hace el proceso de etcd es registrarse en la URL de descubrimiento como miembro. Esto se hace creando el ID del miembro como clave en la URL de descubrimiento.

```
curl -X PUT http://example.com/v2/keys/_etcd/registry/${UUID}/${member_id}?prevExist=false -d value="${member_name}=${member_peer_url_1}&${member_name}=${member_peer_url_2}"
```

### Comprobación del estado {#checking-the-status}

Comprueba el tamaño esperado del clúster y el estado del registro en la URL de descubrimiento, y decide cuál es la siguiente acción.

```
curl -X GET http://example.com/v2/keys/_etcd/registry/${UUID}/_config/size
curl -X GET http://example.com/v2/keys/_etcd/registry/${UUID}
```

Si todavía no hay suficientes miembros registrados, esperará a que aparezcan los miembros restantes.

Si el número de miembros registrados es mayor que el tamaño esperado N, trata los primeros N miembros registrados como la lista de miembros del clúster. Si el propio miembro está en la lista de miembros, el procedimiento de descubrimiento tiene éxito y obtiene todos los pares a través de la lista de miembros. Si no está en la lista de miembros, el procedimiento de descubrimiento termina con el fallo de que el clúster ya está completo.

En la implementación de etcd, el miembro puede comprobar el estado del clúster incluso antes de registrarse. Por eso puede fallar rápidamente si el clúster ya está completo.

### Espera de todos los miembros {#waiting-for-all-members}

El proceso de espera se describe en detalle en la [documentación de la API de etcd][api].

```
curl -X GET http://example.com/v2/keys/_etcd/registry/${UUID}?wait=true&waitIndex=${current_etcd_index}
```

Sigue esperando hasta encontrar todos los miembros.

## Servicio de descubrimiento público {#public-discovery-service}

CoreOS Inc. aloja un servicio público de descubrimiento en https://discovery.etcd.io/ , que ofrece algunas características útiles para facilitar su uso.

### Enmascaramiento del prefijo de clave {#mask-key-prefix}

El servicio público de descubrimiento redirigirá `https://discovery.etcd.io/${UUID}` al clúster de etcd subyacente, hacia la clave en `/v2/keys/_etcd/registry`. Enmascara el prefijo de clave de registro para obtener una URL de descubrimiento corta y legible.

### Obtención de un token nuevo {#get-new-token}

```
GET /new

Sent query:
	size=${cluster_size}
Possible status codes:
	200 OK
	400 Bad Request
200 Body:
	generated discovery url
```

El proceso de generación del servicio sigue los pasos desde [Creación de un token de descubrimiento nuevo][new-discovery-token] hasta [Especificación del tamaño esperado del clúster][expected-cluster-size].

### Comprobación del estado de descubrimiento {#check-discovery-status}

```
GET /${UUID}
```

El estado de este token de descubrimiento, incluidas las máquinas que se han registrado, puede comprobarse solicitando el valor del UUID.

### Repositorio de código abierto {#open-source-repository}

El repositorio está ubicado en https://github.com/coreos/discovery.etcd.io. Puede usarse para construir un servicio de descubrimiento personalizado.

[api]: https://etcd.io/docs/v2.3/api#waiting-for-a-change
[cluster-size]: https://etcd.io/docs/v2.3/admin_guide#optimal-cluster-size
[expected-cluster-size]: #specifying-the-expected-cluster-size
[new-discovery-token]: #creating-a-new-discovery-token
