---
title: "コンテナ内でのetcdクラスターの実行"
weight: 4200
description: "静的ブートストラップを使ってDockerでetcdを実行する"
categories: [タスク]
search_keywords: [v3.7.3]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/container.md"
---

このガイドでは、[静的ブートストラップ手順](/ja/etcd/op-guide/clustering/#static)を使ってDockerでetcdを実行する方法を説明します。

## Docker {#docker}

Dockerホストの外部のクライアントにetcd APIを公開するには、コンテナのホストIPアドレスを使用します。IPアドレスの取得方法については、[`docker inspect`](https://docs.docker.com/engine/reference/commandline/inspect)を参照してください。または、`docker run`コマンドに`--net=host`フラグを指定し、コンテナを独立したネットワークスタックに配置しない方法もあります。

### 単一ノードのetcdの実行 {#running-a-single-node-etcd}

etcdを構成する際は、ホストのIPアドレスを使用します。

```
export NODE1=192.168.1.21
```

etcdデータを保存するDockerボリュームを構成します。

```
docker volume create --name etcd-data
export DATA_DIR="etcd-data"
```

etcdの最新バージョン（執筆時点では`v3.7.3`）を実行します。

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

クラスターメンバーを一覧表示します。

```
etcdctl --endpoints=http://${NODE1}:2379 member list
```

### 3ノードのetcdクラスターの実行 {#running-a-3-node-etcd-cluster}

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

APIバージョン3を使って`etcdctl`を実行するには、次のようにします。

```
docker exec etcd /usr/local/bin/etcdctl put foo bar
```

## ベアメタル {#bare-metal}

ベアメタル上に3ノードのetcdクラスターを構築するには、[baremetalリポジトリ](https://github.com/coreos/coreos-baremetal/tree/master/examples)の例が参考になります。

## 証明書ボリュームのマウント {#mounting-a-certificate-volume}

etcdのリリースコンテナには、デフォルトのルート証明書が含まれていません。ルート認証局によって信頼された証明書でHTTPSを使う場合（ディスカバリーなど）は、etcdコンテナに証明書ディレクトリをマウントしてください。

以下の`rkt`コマンドは過去の使用例です。このv2ディスカバリー設定はetcd 3.7では使用できません。現在の環境にデプロイする場合は、上の静的ブートストラップの例を参照してください。

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

以下のDockerの例は上で設定した`NODE1`を使い、静的ブートストラップによる証明書ボリュームのマウントを示します。

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
