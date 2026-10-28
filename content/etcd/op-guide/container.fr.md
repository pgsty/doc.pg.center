---
title: Exécuter des clusters etcd dans des conteneurs
weight: 4200
description: "Exécution d'etcd avec Docker en utilisant le bootstrap statique"
categories: [Tâche]
search_keywords: [v3.7.3]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/container.md"
---

Le guide suivant explique comment exécuter etcd avec Docker en utilisant le [processus de bootstrap statique](/fr/etcd/op-guide/clustering/#static).

## Docker {#docker}

Afin d’exposer l’API etcd aux clients situés en dehors de l’hôte Docker, utilisez l’adresse IP hôte du conteneur. Voir [`docker inspect`](https://docs.docker.com/engine/reference/commandline/inspect) pour plus de détails sur la manière d’obtenir l’adresse IP. En alternative, spécifiez le drapeau `--net=host` à la commande `docker run` afin d’éviter de placer le conteneur dans une pile réseau distincte.

### Exécution d’un nœud unique etcd {#running-a-single-node-etcd}

Utilisez l'adresse IP hôte lors de la configuration d'etcd :

```
export NODE1=192.168.1.21
```

Configurez un volume Docker pour stocker les données etcd :

```
docker volume create --name etcd-data
export DATA_DIR="etcd-data"
```

Exécutez la dernière version d’etcd (`v3.7.3` au moment de la rédaction) :

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

Lister le membre du cluster :

```
etcdctl --endpoints=http://${NODE1}:2379 member list
```

### Exécution d'un cluster etcd à 3 nœuds {#running-a-3-node-etcd-cluster}

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

Pour exécuter `etcdctl` en utilisant la version 3 de l'API :

```
docker exec etcd /usr/local/bin/etcdctl put foo bar
```

## Infrastructure physique {#bare-metal}

Pour provisionner un cluster etcd à 3 nœuds sur du matériel physique, les exemples présents dans le répertoire [baremetal](https://github.com/coreos/coreos-baremetal/tree/master/examples) peuvent être utiles.

## Montage d'un volume de certificat {#mounting-a-certificate-volume}

L’image de conteneur distribuée avec etcd ne contient pas de certificats racines par défaut. Pour utiliser HTTPS avec des certificats approuvés par une autorité racine (par exemple, pour la découverte), montez un répertoire de certificats dans le conteneur etcd :

La commande `rkt` suivante est un exemple historique. Sa configuration de découverte v2 est incompatible avec etcd 3.7 ; pour les déploiements actuels, utilisez les exemples de bootstrap statique ci-dessus.

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

L’exemple Docker ci-dessous réutilise `NODE1` défini plus haut et utilise le bootstrap statique pour montrer le montage d’un volume de certificat.

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
