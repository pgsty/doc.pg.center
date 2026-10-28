---
title: "etcd-Cluster in Containern ausführen"
weight: 4200
description: "etcd mit Docker durch statische Initialisierung ausführen"
categories: [Aufgabe]
search_keywords: [v3.7.3]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/container.md"
---

Die folgende Anleitung zeigt, wie etcd mit Docker über die [statische Initialisierung](/de/etcd/op-guide/clustering/#static) ausgeführt wird.

## Docker {#docker}

Um die etcd-API für Clients außerhalb des Docker-Hosts bereitzustellen, die IP-Adresse des Container-Hosts verwenden. Weitere Informationen zum Ermitteln der IP-Adresse bietet [`docker inspect`](https://docs.docker.com/engine/reference/commandline/inspect). Alternativ dem Befehl `docker run` die Option `--net=host` übergeben, damit der Container keinen separaten Netzwerkstack erhält.

### etcd mit einem einzelnen Knoten ausführen {#running-a-single-node-etcd}

Bei der Konfiguration von etcd die IP-Adresse des Hosts verwenden:

```
export NODE1=192.168.1.21
```

Ein Docker-Volume zur Speicherung der etcd-Daten konfigurieren:

```
docker volume create --name etcd-data
export DATA_DIR="etcd-data"
```

Die neueste Version von etcd ausführen (zum Zeitpunkt der Erstellung dieses Dokuments `v3.7.3`):

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

Das Clustermitglied auflisten:

```
etcdctl --endpoints=http://${NODE1}:2379 member list
```

### Einen etcd-Cluster mit 3 Knoten ausführen {#running-a-3-node-etcd-cluster}

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

`etcdctl` mit API-Version 3 ausführen:

```
docker exec etcd /usr/local/bin/etcdctl put foo bar
```

## Physische Hardware {#bare-metal}

Für die Bereitstellung eines etcd-Clusters mit 3 Knoten auf physischer Hardware können die Beispiele im [baremetal-Repository](https://github.com/coreos/coreos-baremetal/tree/master/examples) hilfreich sein.

## Ein Zertifikatsvolume einhängen {#mounting-a-certificate-volume}

Der veröffentlichte etcd-Container enthält keine standardmäßigen Stammzertifikate. Um HTTPS mit Zertifikaten zu verwenden, denen eine Stammzertifizierungsstelle vertraut (z. B. für die Diensterkennung), ein Zertifikatsverzeichnis in den etcd-Container einhängen:

Der folgende `rkt`-Befehl ist ein historisches Beispiel. Seine v2-Discovery-Konfiguration ist mit etcd 3.7 nicht kompatibel; für aktuelle Bereitstellungen die Beispiele zur statischen Initialisierung oben verwenden.

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

Das folgende Docker-Beispiel verwendet das oben gesetzte `NODE1` und zeigt das Einhängen eines Zertifikatsvolumes mit statischer Initialisierung.

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
