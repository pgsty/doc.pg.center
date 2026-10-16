---
title: Ejecutar clústeres de etcd en contenedores
weight: 4200
description: Ejecución de etcd con Docker mediante el arranque estático
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/container.md"
---

La siguiente guía muestra cómo ejecutar etcd con Docker usando el [proceso de arranque estático](/es/etcd/op-guide/clustering/#static).

## Docker {#docker}

Para exponer la API de etcd a clientes fuera del host de Docker, usa la dirección IP del host del contenedor. Consulta [`docker inspect`](https://docs.docker.com/engine/reference/commandline/inspect) para más detalles sobre cómo obtener la dirección IP. Como alternativa, especifica la opción `--net=host` en el comando `docker run` para evitar colocar el contenedor dentro de una pila de red separada.

### Ejecución de un etcd de un solo nodo {#running-a-single-node-etcd}

Usa la dirección IP del host al configurar etcd:

```
export NODE1=192.168.1.21
```

Configura un volumen de Docker para almacenar los datos de etcd:

```
docker volume create --name etcd-data
export DATA_DIR="etcd-data"
```

Ejecuta la última versión de etcd (`v3.7.2` en el momento de
escribir esto):

```
ETCD_VERSION=v3.7.2
REGISTRY=quay.io/coreos/etcd
# available from v3.2.5
REGISTRY=gcr.io/etcd-development/etcd

docker run \
  -p 2379:2379 \
  -p 2380:2380 \
  --volume=${DATA_DIR}:/etcd-data \
  --name etcd ${REGISTRY}:${ETCD_VERSION} \
  /usr/local/bin/etcd \
  --data-dir=/etcd-data --name node1 \
  --initial-advertise-peer-urls http://${NODE1}:2380 --listen-peer-urls http://0.0.0.0:2380 \
  --advertise-client-urls http://${NODE1}:2379 --listen-client-urls http://0.0.0.0:2379 \
  --initial-cluster node1=http://${NODE1}:2380
```

Lista el miembro del clúster:

```
etcdctl --endpoints=http://${NODE1}:2379 member list
```

### Ejecución de un clúster etcd de 3 nodos {#running-a-3-node-etcd-cluster}

```
REGISTRY=quay.io/coreos/etcd
# available from v3.2.5
REGISTRY=gcr.io/etcd-development/etcd

# For each machine
ETCD_VERSION=v3.7.2
TOKEN=my-etcd-token
CLUSTER_STATE=new
NAME_1=etcd-node-0
NAME_2=etcd-node-1
NAME_3=etcd-node-2
HOST_1=10.20.30.1
HOST_2=10.20.30.2
HOST_3=10.20.30.3
CLUSTER=${NAME_1}=http://${HOST_1}:2380,${NAME_2}=http://${HOST_2}:2380,${NAME_3}=http://${HOST_3}:2380
DATA_DIR=/var/lib/etcd

# For node 1
THIS_NAME=${NAME_1}
THIS_IP=${HOST_1}
docker run \
  -p 2379:2379 \
  -p 2380:2380 \
  --volume=${DATA_DIR}:/etcd-data \
  --name etcd ${REGISTRY}:${ETCD_VERSION} \
  /usr/local/bin/etcd \
  --data-dir=/etcd-data --name ${THIS_NAME} \
  --initial-advertise-peer-urls http://${THIS_IP}:2380 --listen-peer-urls http://0.0.0.0:2380 \
  --advertise-client-urls http://${THIS_IP}:2379 --listen-client-urls http://0.0.0.0:2379 \
  --initial-cluster ${CLUSTER} \
  --initial-cluster-state ${CLUSTER_STATE} --initial-cluster-token ${TOKEN}

# For node 2
THIS_NAME=${NAME_2}
THIS_IP=${HOST_2}
docker run \
  -p 2379:2379 \
  -p 2380:2380 \
  --volume=${DATA_DIR}:/etcd-data \
  --name etcd ${REGISTRY}:${ETCD_VERSION} \
  /usr/local/bin/etcd \
  --data-dir=/etcd-data --name ${THIS_NAME} \
  --initial-advertise-peer-urls http://${THIS_IP}:2380 --listen-peer-urls http://0.0.0.0:2380 \
  --advertise-client-urls http://${THIS_IP}:2379 --listen-client-urls http://0.0.0.0:2379 \
  --initial-cluster ${CLUSTER} \
  --initial-cluster-state ${CLUSTER_STATE} --initial-cluster-token ${TOKEN}

# For node 3
THIS_NAME=${NAME_3}
THIS_IP=${HOST_3}
docker run \
  -p 2379:2379 \
  -p 2380:2380 \
  --volume=${DATA_DIR}:/etcd-data \
  --name etcd ${REGISTRY}:${ETCD_VERSION} \
  /usr/local/bin/etcd \
  --data-dir=/etcd-data --name ${THIS_NAME} \
  --initial-advertise-peer-urls http://${THIS_IP}:2380 --listen-peer-urls http://0.0.0.0:2380 \
  --advertise-client-urls http://${THIS_IP}:2379 --listen-client-urls http://0.0.0.0:2379 \
  --initial-cluster ${CLUSTER} \
  --initial-cluster-state ${CLUSTER_STATE} --initial-cluster-token ${TOKEN}
```

Para ejecutar `etcdctl` usando la versión 3 de la API:

```
docker exec etcd /usr/local/bin/etcdctl put foo bar
```

## Servidor físico {#bare-metal}

Para aprovisionar un clúster etcd de 3 nodos en servidores físicos, los ejemplos del [repositorio baremetal](https://github.com/coreos/coreos-baremetal/tree/master/examples) pueden ser útiles.

## Montaje de un volumen de certificados {#mounting-a-certificate-volume}

El contenedor de la distribución de etcd no incluye certificados raíz por defecto. Para usar HTTPS con certificados respaldados por una autoridad raíz de confianza (por ejemplo, para el descubrimiento), monta un directorio de certificados en el contenedor de etcd:

El siguiente comando `rkt` es un ejemplo histórico. Su configuración de descubrimiento v2 es incompatible con etcd 3.7; usa los ejemplos de arranque estático anteriores para los despliegues actuales.

```
ETCD_VERSION=v3.7.2
REGISTRY=quay.io/coreos/etcd
# available from v3.2.5
REGISTRY=docker://gcr.io/etcd-development/etcd

rkt run \
  --insecure-options=image \
  --volume etcd-ssl-certs-bundle,kind=host,source=/etc/ssl/certs/ca-certificates.crt \
  --mount volume=etcd-ssl-certs-bundle,target=/etc/ssl/certs/ca-certificates.crt \
  ${REGISTRY}:${ETCD_VERSION} -- --name my-name \
  --initial-advertise-peer-urls http://localhost:2380 --listen-peer-urls http://localhost:2380 \
  --advertise-client-urls http://localhost:2379 --listen-client-urls http://localhost:2379 \
  --discovery https://discovery.etcd.io/c11fbcdc16972e45253491a24fcf45e1
```

El ejemplo de Docker siguiente reutiliza el `NODE1` definido anteriormente y usa el arranque estático para demostrar el montaje de un volumen de certificados.

```
ETCD_VERSION=v3.7.2
REGISTRY=quay.io/coreos/etcd
# available from v3.2.5
REGISTRY=gcr.io/etcd-development/etcd

docker run \
  -p 2379:2379 \
  -p 2380:2380 \
  --volume=/etc/ssl/certs/ca-certificates.crt:/etc/ssl/certs/ca-certificates.crt \
  ${REGISTRY}:${ETCD_VERSION} \
  /usr/local/bin/etcd --name my-name \
  --initial-advertise-peer-urls http://${NODE1}:2380 --listen-peer-urls http://0.0.0.0:2380 \
  --advertise-client-urls http://${NODE1}:2379 --listen-client-urls http://0.0.0.0:2379 \
  --initial-cluster my-name=http://${NODE1}:2380
```
