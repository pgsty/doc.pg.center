---
title: Comment créer des verrous
description: Guide de création de verrous distribués avec etcd
weight: 800
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/how-to-create-locks.md"
aliases: [/etcd/tasks/developer/how-to-create-locks/]
---

LOCK acquiert un verrou distribué portant un nom donné. Une fois le verrou acquis, il reste détenu jusqu'à la terminaison d'etcdctl.

## Prérequis {#prerequisites}

* Installer [`etcd` et `etcdctl`](/fr/docs/etcd/install/)

## Création d’un verrou {#creating-a-lock}

`lock` pour verrouillage distribué :

![08_etcdctl_lock_2016050501](/docs/etcd/tasks/img/create-lock.gif)

```shell
etcdctl --endpoints=$ENDPOINTS lock mutex1
```

### Options {#options}
- endpoints - définit une liste séparée par des virgules d'adresses machine du cluster.
- ttl - durée d'expiration en secondes de la session de verrouillage.
