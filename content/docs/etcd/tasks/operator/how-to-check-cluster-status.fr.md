---
title: "Comment vérifier l'état du cluster"
description: "Guide de vérification de l'état du cluster etcd"
weight: 1000
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/operator/how-to-check-cluster-status.md"
aliases: [/etcd/tasks/operator/how-to-check-cluster-status/]
---

## Prérequis {#prerequisites}

* Installer [`etcd` et `etcdctl`](/fr/docs/etcd/install/)

## Vérifier l'état global {#check-overall-status}

`endpoint status` pour vérifier l'état global de chaque point de terminaison spécifié dans le drapeau `--endpoints` :

```bash
etcdctl endpoint status (--endpoints=$ENDPOINTS|--cluster)
```

### Options {#options}

```bash
--cluster[=false]: use all endpoints from the cluster member list
```

## Vérifier l'état de santé {#check-health}

`endpoint health` pour vérifier l'état de santé de chaque point de terminaison spécifié dans le drapeau `--endpoints` :

```bash
etcdctl endpoint health (--endpoints=$ENDPOINTS|--cluster)
```

### Options {#options-1}

```bash
--cluster[=false]: use all endpoints from the cluster member list
```

## Vérifier le hachage KV {#check-kv-hash}

`endpoint hashkv` pour vérifier le hachage de l'historique des paires clé-valeur de chaque point de terminaison spécifié dans le drapeau `--endpoints` :

```bash
etcdctl endpoint hashkv (--endpoints=$ENDPOINTS|--cluster) [rev=$REV]
```

### Options {#options-2}

```bash
--cluster[=false]: use all endpoints from the cluster member list
--rev=0: maximum revision to hash (default: latest revision)
```

## Options héritées des commandes parentes {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
-w, --write-out="simple": set the output format (fields, json, protobuf, simple, table)
```

### Exemples {#examples}

```shell
etcdctl --write-out=table --endpoints=$ENDPOINTS endpoint status

+------------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|    ENDPOINT      |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
+------------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
| 10.240.0.17:2379 | 4917a7ab173fabe7 |  3.5.0  |   45 kB |      true |      false |         4 |      16726 |              16726 |        |
| 10.240.0.18:2379 | 59796ba9cd1bcd72 |  3.5.0  |   45 kB |     false |      false |         4 |      16726 |              16726 |        |
| 10.240.0.19:2379 | 94df724b66343e6c |  3.5.0  |   45 kB |     false |      false |         4 |      16726 |              16726 |        |
+------------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------|
```

```shell
etcdctl --endpoints=$ENDPOINTS endpoint health

10.240.0.17:2379 is healthy: successfully committed proposal: took = 3.345431ms
10.240.0.19:2379 is healthy: successfully committed proposal: took = 3.767967ms
10.240.0.18:2379 is healthy: successfully committed proposal: took = 4.025451ms
```

```shell
etcdctl --cluster endpoint hashkv  --write-out=table

+------------------+------------+---------------+
|     ENDPOINT     |    HASH    | HASH REVISION |
+------------------+------------+---------------+
| 10.240.0.17:2379 | 3892279174 |             3 |
| 10.240.0.18:2379 | 3892279174 |             3 |
| 10.240.0.19:2379 | 3892279174 |             3 |
+------------------+------------+---------------+
```
