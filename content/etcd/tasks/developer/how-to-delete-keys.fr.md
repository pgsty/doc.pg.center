---
title: Comment supprimer des clés
description: Décris une méthode pour supprimer des clés etcd
weight: 400
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/how-to-delete-keys.md"
---

## Prérequis {#prerequisites}

* Installer [`etcd` et `etcdctl`](/fr/etcd/install/)

## Ajouter ou supprimer des clés {#add-or-delete-keys}

`del` pour supprimer la clé spécifiée ou la plage de clés :

```bash
etcdctl del $KEY [$END_KEY]
```

### Options {#options}

```bash
--prefix[=false]: delete keys with matching prefix
--prev-kv[=false]: return deleted key-value pairs
--from-key[=false]: delete keys that are greater than or equal to the given key using byte compare
--range[=false]: delete range of keys without delay
```

### Options héritées des commandes parentes {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
```

### Exemples {#examples}

![04_etcdctl_delete_2016050601](/etcd/tasks/img/delete-keys.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put key myvalue
etcdctl --endpoints=$ENDPOINTS del key

etcdctl --endpoints=$ENDPOINTS put k1 value1
etcdctl --endpoints=$ENDPOINTS put k2 value2
etcdctl --endpoints=$ENDPOINTS del k --prefix
```
