---
title: Proxy gRPC
weight: 4350
description: Un proxy inverso de etcd sin estado que opera en la capa gRPC
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/grpc_proxy.md"
---

El proxy gRPC es un proxy inverso de etcd sin estado que opera en la capa gRPC (L7). El proxy está diseñado para reducir la carga total de procesamiento sobre el clúster de etcd principal. Para conseguir escalabilidad horizontal, agrupa las solicitudes de watch y de concesiones de la API. Para proteger al clúster contra clientes abusivos, almacena en caché las solicitudes de rangos de claves.

El proxy gRPC admite varios puntos de acceso del servidor de etcd. Cuando el proxy se inicia, elige aleatoriamente un punto de acceso del servidor de etcd para usarlo. Ese punto de acceso atiende todas las solicitudes hasta que el proxy detecta un fallo del punto de acceso. Si el proxy gRPC detecta un fallo de un punto de acceso, conmuta a un punto de acceso diferente, si hay alguno disponible, para ocultar los fallos a sus clientes. Otras políticas de reintento, como el turno rotativo ponderado, podrían admitirse en el futuro.

## API de watch escalable {#scalable-watch-api}

El proxy gRPC agrupa múltiples watchers de clientes (`c-watchers`) sobre la misma clave o rango en un único watcher (`s-watcher`) conectado a un servidor de etcd. El proxy difunde todos los eventos del `s-watcher` a sus `c-watchers`.

Suponiendo que N clientes hacen watch sobre la misma clave, un proxy gRPC puede reducir la carga de watch sobre el servidor de etcd de N a 1. Los usuarios pueden desplegar varios proxies gRPC para distribuir aún más la carga del servidor.

En el siguiente ejemplo, tres clientes hacen watch sobre la clave A. El proxy gRPC agrupa los tres watchers, creando un único watcher adjunto al servidor de etcd.

```
            +-------------+
            | etcd server |
            +------+------+
                   ^ watch key A (s-watcher)
                   |
           +-------+-----+
           | gRPC proxy  | <-------+
           |             |         |
           ++-----+------+         |watch key A (c-watcher)
watch key A ^     ^ watch key A    |
(c-watcher) |     | (c-watcher)    |
    +-------+-+  ++--------+  +----+----+
    |  client |  |  client |  |  client |
    |         |  |         |  |         |
    +---------+  +---------+  +---------+
```

### Limitaciones {#limitations}

Para agrupar de forma eficaz múltiples watchers de clientes en un único watcher, el proxy gRPC agrega los nuevos `c-watchers` a un `s-watcher` existente cuando es posible. Este `s-watcher` agrupado puede estar desincronizado del servidor de etcd debido a retrasos de red o eventos almacenados en búfer sin entregar. Cuando no se especifica la revisión del watch, el proxy gRPC no garantizará que el `c-watcher` comience a observar desde la revisión más reciente del almacén. Por ejemplo, si un cliente hace watch desde un servidor de etcd con la revisión 1000, ese watcher comenzará en la revisión 1000. Si un cliente hace watch desde el proxy gRPC, puede comenzar a observar desde la revisión 990.

Limitaciones similares se aplican a la cancelación. Cuando se cancela un watcher, la revisión del servidor de etcd puede ser mayor que la revisión de la respuesta de cancelación.

Estas dos limitaciones no deberían causar problemas en la mayoría de los casos de uso. En el futuro, puede que existan opciones adicionales para forzar que el watcher omita el proxy gRPC y obtener respuestas de revisión más precisas.

## API de concesiones escalable {#scalable-lease-api}

Para mantener vivas sus concesiones, un cliente debe establecer al menos un flujo gRPC hacia un servidor de etcd para enviar latidos periódicos. Si una carga de trabajo de etcd implica una actividad intensa de concesiones repartida entre muchos clientes, estos flujos pueden contribuir a un uso excesivo de CPU. Para reducir el número total de flujos sobre el clúster principal, el proxy admite la agrupación de flujos de concesiones.

Suponiendo que N clientes actualizan concesiones, un único proxy gRPC reduce la carga de flujos sobre el servidor de etcd de N a 1. Los despliegues pueden tener proxies gRPC adicionales para distribuir aún más los flujos entre varios proxies.

En el siguiente ejemplo, tres clientes actualizan tres concesiones independientes (`L1`, `L2` y `L3`). El proxy gRPC agrupa los tres flujos de concesiones de los clientes (`c-streams`) en un único flujo de mantenimiento de concesión (`s-stream`) adjunto a un servidor de etcd. El proxy reenvía los latidos de concesión del lado del cliente desde los c-streams al s-stream, y luego devuelve las respuestas a los c-streams correspondientes.

```
          +-------------+
          | etcd server |
          +------+------+
                 ^
                 | heartbeat L1, L2, L3
                 | (s-stream)
                 v
         +-------+-----+
         | gRPC proxy  +<-----------+
         +---+------+--+            | heartbeat L3
             ^      ^               | (c-stream)
heartbeat L1 |      | heartbeat L2  |
(c-stream)   v      v (c-stream)    v
      +------+-+  +-+------+  +-----+--+
      | client |  | client |  | client |
      +--------+  +--------+  +--------+
```

## Protección contra clientes abusivos {#abusive-clients-protection}

El proxy gRPC almacena en caché las respuestas de las solicitudes cuando ello no rompe los requisitos de consistencia. Esto puede proteger al servidor de etcd de clientes abusivos en bucles for muy ajustados.

## Iniciar el proxy gRPC de etcd {#start-etcd-grpc-proxy}

Considera un clúster de etcd con los siguientes puntos de acceso estáticos:

|Nombre|Dirección|Nombre de host|
|------|---------|------------------|
|infra0|10.0.1.10|infra0.example.com|
|infra1|10.0.1.11|infra1.example.com|
|infra2|10.0.1.12|infra2.example.com|

Inicia el proxy gRPC de etcd para usar estos puntos de acceso estáticos con el comando:

```bash
$ etcd grpc-proxy start --endpoints=infra0.example.com,infra1.example.com,infra2.example.com --listen-addr=127.0.0.1:2379
```

El proxy gRPC de etcd se inicia y escucha en el puerto 2379. Reenvía las solicitudes de los clientes a uno de los tres puntos de acceso indicados arriba.

Envío de solicitudes a través del proxy:

```bash
$ ETCDCTL_API=3 etcdctl --endpoints=127.0.0.1:2379 put foo bar
OK
$ ETCDCTL_API=3 etcdctl --endpoints=127.0.0.1:2379 get foo
foo
bar
```

## Sincronización de puntos de acceso de clientes y resolución de nombres {#client-endpoint-synchronization-and-name-resolution}

El proxy admite el registro de sus puntos de acceso para su descubrimiento escribiendo en un punto de acceso definido por el usuario. Esto cumple dos propósitos. Primero, permite a los clientes sincronizar sus puntos de acceso con un conjunto de puntos de acceso del proxy para lograr alta disponibilidad. Segundo, actúa como proveedor de puntos de acceso para la [resolución de nombres gRPC](/es/etcd/dev-guide/grpc_naming/) de etcd.

Registra uno o más proxies proporcionando un prefijo definido por el usuario:

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23790 \
  --advertise-client-url=127.0.0.1:23790 \
  --resolver-prefix="___grpc_proxy_endpoint" \
  --resolver-ttl=60

$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23791 \
  --advertise-client-url=127.0.0.1:23791 \
  --resolver-prefix="___grpc_proxy_endpoint" \
  --resolver-ttl=60
```

El proxy listará todos sus miembros en member list:

```bash
ETCDCTL_API=3 etcdctl --endpoints=http://localhost:23790 member list --write-out table

+----+---------+--------------------------------+------------+-----------------+
| ID | STATUS  |              NAME              | PEER ADDRS |  CLIENT ADDRS   |
+----+---------+--------------------------------+------------+-----------------+
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23791 |
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23790 |
+----+---------+--------------------------------+------------+-----------------+
```

Esto permite a los clientes descubrir automáticamente los puntos de acceso del proxy mediante Sync:

```go
cli, err := clientv3.New(clientv3.Config{
    Endpoints: []string{"http://localhost:23790"},
})
if err != nil {
    log.Fatal(err)
}
defer cli.Close()

// fetch registered grpc-proxy endpoints
if err := cli.Sync(context.Background()); err != nil {
    log.Fatal(err)
}
```

Ten en cuenta que si se configura un proxy sin un prefijo de resolutor,

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23792 \
  --advertise-client-url=127.0.0.1:23792
```

La API member list del grpc-proxy devuelve su propio `advertise-client-url`:

```bash
ETCDCTL_API=3 etcdctl --endpoints=http://localhost:23792 member list --write-out table

+----+---------+--------------------------------+------------+-----------------+
| ID | STATUS  |              NAME              | PEER ADDRS |  CLIENT ADDRS   |
+----+---------+--------------------------------+------------+-----------------+
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23792 |
+----+---------+--------------------------------+------------+-----------------+
```

## Espacio de nombres {#namespacing}

Supón que una aplicación espera tener control total sobre todo el espacio de claves, pero que el clúster de etcd está compartido con otras aplicaciones. Para permitir que todas las aplicaciones se ejecuten sin interferir entre sí, el proxy puede particionar el espacio de claves de etcd de modo que los clientes parezcan tener acceso al espacio de claves completo. Cuando el proxy recibe la opción `--namespace`, todas las solicitudes de clientes que entran al proxy se traducen para añadir un prefijo definido por el usuario a las claves. Los accesos al clúster de etcd se harán bajo ese prefijo y las respuestas del proxy lo eliminarán; para el cliente, parecerá que no existe ningún prefijo.

Para asignar un espacio de nombres a un proxy, inícialo con `--namespace`:

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23790 \
  --namespace=my-prefix/
```

Los accesos al proxy ahora llevan de forma transparente el prefijo en el clúster de etcd:

```bash
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:23790 put my-key abc
# OK
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:23790 get my-key
# my-key
# abc
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:2379 get my-prefix/my-key
# my-prefix/my-key
# abc
```

## Terminación TLS {#tls-termination}

Termina el TLS proveniente de un clúster de etcd seguro con el proxy gRPC sirviendo un punto de acceso local sin cifrar.

Para probarlo, inicia un clúster de etcd de un solo miembro con cliente https:

```sh
$ etcd --listen-client-urls https://localhost:2379 --advertise-client-urls https://localhost:2379 --cert-file=peer.crt --key-file=peer.key --trusted-ca-file=ca.crt --client-cert-auth
```

Confirma que el puerto de cliente está sirviendo https:

```sh
# fails
$ ETCDCTL_API=3 etcdctl --endpoints=http://localhost:2379 endpoint status
# works
$ ETCDCTL_API=3 etcdctl --endpoints=https://localhost:2379 --cert=client.crt --key=client.key --cacert=ca.crt endpoint status
```

A continuación, inicia un proxy gRPC en `localhost:12379` conectándote al punto de acceso de etcd `https://localhost:2379` usando los certificados de cliente:

```sh
$ etcd grpc-proxy start --endpoints=https://localhost:2379 --listen-addr localhost:12379 --cert client.crt --key client.key --cacert=ca.crt --insecure-skip-tls-verify &
```

Finalmente, prueba la terminación TLS escribiendo una clave en el proxy por http:

```sh
$ ETCDCTL_API=3 etcdctl --endpoints=http://localhost:12379 put abc def
# OK
```

## Métricas y estado de salud {#metrics-and-health}

El proxy gRPC expone los puntos de acceso `/health` y `/metrics` de Prometheus para los miembros de etcd definidos por `--endpoints`. Como alternativa, se puede definir una URL adicional que responderá tanto a `/metrics` como a `/health` con la opción `--metrics-addr`.

```bash
$ etcd grpc-proxy start \
  --endpoints https://localhost:2379 \
  --metrics-addr https://0.0.0.0:4443 \
  --listen-addr 127.0.0.1:23790 \
  --key client.key \
  --key-file proxy-server.key \
  --cert client.crt \
  --cert-file proxy-server.crt \
  --cacert ca.pem \
  --trusted-ca-file proxy-ca.pem
 ```

### Problema conocido {#known-issue}

La interfaz principal del proxy sirve tanto HTTP2 como HTTP/1.1. Si el proxy se configura con TLS como se muestra en el ejemplo anterior, al usar un cliente como cURL contra la interfaz de escucha será necesario establecer explícitamente el protocolo HTTP/1.1 en la solicitud para que devuelva `/metrics` o `/health`. Usando la opción `--metrics-addr`, la interfaz secundaria no tendrá este requisito.

```bash
 $ curl --cacert proxy-ca.pem --key proxy-client.key --cert proxy-client.crt https://127.0.0.1:23790/metrics --http1.1
```
