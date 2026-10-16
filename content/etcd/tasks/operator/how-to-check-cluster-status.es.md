---
title: "Cómo comprobar el estado del clúster"
description: "Guía para comprobar el estado del clúster etcd"
weight: 1000
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/operator/how-to-check-cluster-status.md"
---

## Prerrequisitos {#prerequisites}

* Instala [`etcd` y `etcdctl`](/es/etcd/install/)

## Comprobar el estado general {#check-overall-status}

`endpoint status` para comprobar el estado general de cada endpoint especificado en el parámetro `--endpoints`:

```bash
etcdctl endpoint status (--endpoints=$ENDPOINTS|--cluster)
```

### Opciones {#options}

```bash
--cluster[=false]: use all endpoints from the cluster member list
```

## Comprobar el estado de salud {#check-health}

`endpoint health` para comprobar el estado de salud de cada endpoint especificado en el parámetro `--endpoints`:

```bash
etcdctl endpoint health (--endpoints=$ENDPOINTS|--cluster)
```

### Opciones {#options-1}

```bash
--cluster[=false]: use all endpoints from the cluster member list
```

## Comprobar el hash de KV {#check-kv-hash}

`endpoint hashkv` para comprobar el hash del historial de pares clave-valor de cada endpoint especificado en el parámetro `--endpoints`:

```bash
etcdctl endpoint hashkv (--endpoints=$ENDPOINTS|--cluster) [rev=$REV]
```

### Opciones {#options-2}

```bash
--cluster[=false]: use all endpoints from the cluster member list
--rev=0: maximum revision to hash (default: latest revision)
```

## Opciones heredadas de los comandos padre {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
-w, --write-out="simple": set the output format (fields, json, protobuf, simple, table)
```

### Ejemplos {#examples}

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
