---
title: Запуск кластеров etcd в контейнерах
weight: 4200
description: Запуск etcd в Docker со статической начальной инициализацией
categories: [Задача]
search_keywords: [v3.7.3]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/container.md"
---

В этом руководстве показано, как запустить etcd в Docker с помощью [процесса статической начальной инициализации](/ru/etcd/op-guide/clustering/#static).

## Docker {#docker}

Чтобы предоставить клиентам вне узла Docker доступ к API etcd, используйте IP-адрес узла контейнера. Способ получения IP-адреса подробно описан в документации [`docker inspect`](https://docs.docker.com/engine/reference/commandline/inspect). Также можно передать команде `docker run` флаг `--net=host`, чтобы не помещать контейнер в отдельный сетевой стек.

### Запуск одного узла etcd {#running-a-single-node-etcd}

При настройке etcd используйте IP-адрес узла:

```
export NODE1=192.168.1.21
```

Настройте том Docker для хранения данных etcd:

```
docker volume create --name etcd-data
export DATA_DIR="etcd-data"
```

Запустите последнюю версию etcd (на момент написания — `v3.7.3`):

```
ETCD_VERSION=v3.7.3
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

Выведите список участников кластера:

```
etcdctl --endpoints=http://${NODE1}:2379 member list
```

### Запуск кластера etcd из 3 узлов {#running-a-3-node-etcd-cluster}

```
REGISTRY=quay.io/coreos/etcd
# available from v3.2.5
REGISTRY=gcr.io/etcd-development/etcd

# For each machine
ETCD_VERSION=v3.7.3
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

Чтобы использовать `etcdctl` с API версии 3:

```
docker exec etcd /usr/local/bin/etcdctl put foo bar
```

## Физические серверы {#bare-metal}

При развёртывании кластера etcd из 3 узлов на физических серверах могут быть полезны примеры из [репозитория baremetal](https://github.com/coreos/coreos-baremetal/tree/master/examples).

## Подключение тома с сертификатами {#mounting-a-certificate-volume}

Контейнер выпуска etcd не содержит корневых сертификатов по умолчанию. Чтобы использовать HTTPS с сертификатами, которым доверяет корневой центр, например для обнаружения, подключите каталог сертификатов к контейнеру etcd:

Следующая команда `rkt` приведена как исторический пример. Её конфигурация обнаружения v2 несовместима с etcd 3.7; для современных развёртываний используйте примеры статической начальной инициализации выше.

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

Пример Docker ниже использует заданную выше переменную `NODE1` и показывает подключение тома с сертификатами при статической начальной инициализации.

```
ETCD_VERSION=v3.7.3
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
