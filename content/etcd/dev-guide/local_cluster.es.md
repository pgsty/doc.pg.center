---
title: Configurar un clúster local
weight: 3125
description: Configuración de clústeres locales para pruebas y desarrollo
categories: [Tutorial]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/local_cluster.md"
---

Para despliegues de prueba y desarrollo, la forma más rápida y sencilla es configurar un clúster local. Para un despliegue en producción, consulta la sección sobre [clústeres][clustering].

## Clúster local autónomo {#local-standalone-cluster}

### Inicio de un clúster {#starting-a-cluster}

Ejecuta lo siguiente para desplegar un clúster de etcd como clúster autónomo:

```
$ ./etcd
...
```

Si el binario `etcd` no está presente en el directorio de trabajo actual, puede estar en `$GOPATH/bin/etcd` o en `/usr/local/bin/etcd`. Ejecuta el comando según corresponda.

El miembro de etcd en ejecución escucha en `localhost:2379` las solicitudes de los clientes.

### Interacción con el clúster {#interacting-with-the-cluster}

Usa `etcdctl` para interactuar con el clúster en ejecución:

1. Almacena un par clave-valor de ejemplo en el clúster:

    ```
      $ ./etcdctl put foo bar
      OK
    ```

    Si se muestra OK, el almacenamiento del par clave-valor fue correcto.

2. Recupera el valor de `foo`:

    ```
    $ ./etcdctl get foo
    bar
    ```

    Si se devuelve `bar`, la interacción con el clúster de etcd funciona como se espera.

## Clúster local de varios miembros {#local-multi-member-cluster}

### Inicio de un clúster {#starting-a-cluster-1}

En la raíz del repositorio git de etcd se proporciona un `Procfile` para configurar fácilmente un clúster local de varios miembros. Para iniciar un clúster de varios miembros, ve a la raíz del árbol de código fuente de etcd y haz lo siguiente:

1. Instala `goreman` para controlar aplicaciones basadas en Procfile:

    ```
    $ go install github.com/mattn/goreman@latest
    ```

2. Inicia un clúster con `goreman` usando el Procfile estándar de etcd:

    ```
    $ goreman -f Procfile start
    ```

    Los miembros comienzan a ejecutarse. Escuchan en `localhost:2379`, `localhost:22379` y `localhost:32379` respectivamente las solicitudes de los clientes.

### Interacción con el clúster {#interacting-with-the-cluster-1}

Usa `etcdctl` para interactuar con el clúster en ejecución:

1. Muestra la lista de miembros:

    ```
    $ etcdctl --write-out=table --endpoints=localhost:2379 member list
    ```
    La lista de miembros de etcd se muestra de la siguiente manera:

    ```
    +------------------+---------+--------+------------------------+------------------------+
    |        ID        | STATUS  |  NAME  |       PEER ADDRS       |      CLIENT ADDRS      |
    +------------------+---------+--------+------------------------+------------------------+
    | 8211f1d0f64f3269 | started | infra1 | http://127.0.0.1:2380  | http://127.0.0.1:2379  |
    | 91bc3c398fb3c146 | started | infra2 | http://127.0.0.1:22380 | http://127.0.0.1:22379 |
    | fd422379fda50e48 | started | infra3 | http://127.0.0.1:32380 | http://127.0.0.1:32379 |
    +------------------+---------+--------+------------------------+------------------------+
    ```

2. Almacena un par clave-valor de ejemplo en el clúster:

    ```
    $ etcdctl put foo bar
    OK
    ```

    Si se muestra OK, el almacenamiento del par clave-valor fue correcto.

### Prueba de tolerancia a fallos {#testing-fault-tolerance}

Para poner a prueba la tolerancia a fallos de etcd, detén un miembro e intenta recuperar la clave.

1. Identifica el nombre del proceso del miembro que se va a detener.

    El `Procfile` enumera las propiedades del clúster de varios miembros. Por ejemplo, considera el miembro con el nombre de proceso `etcd2`.

2. Detén el miembro:

    ```
    # kill etcd2
    $ goreman run stop etcd2
    ```

3. Almacena una clave:

    ```
    $ etcdctl put key hello
    OK
    ```

4.  Recupera la clave almacenada en el paso anterior:

    ```
    $ etcdctl get key
    hello
    ```

5. Recupera una clave del miembro detenido:

    ```
    $ etcdctl --endpoints=localhost:22379 get key
    ```

    El comando debería mostrar un error causado por un fallo de conexión:

    ```
    2017/06/18 23:07:35 grpc: Conn.resetTransport failed to create client transport: connection error: desc = "transport: dial tcp 127.0.0.1:22379: getsockopt: connection refused"; Reconnecting to "localhost:22379"
    Error:  grpc: timed out trying to connect
    ```
6. Reinicia el miembro detenido:

    ```
    $ goreman run restart etcd2
    ```

7. Obtén la clave del miembro reiniciado:

    ```
    $ etcdctl --endpoints=localhost:22379 get key
    hello
    ```

    Reiniciar el miembro restablece la conexión. `etcdctl` ahora podrá recuperar la clave con éxito. Para saber más sobre la interacción con etcd, lee la sección de [interacción con etcd][interacting].

[clustering]: /es/etcd/op-guide/clustering/
[interacting]: /es/etcd/dev-guide/interacting_v3/
