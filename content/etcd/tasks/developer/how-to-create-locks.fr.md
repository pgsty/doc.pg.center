---
title: Comment créer des verrous
description: Guide de création de verrous distribués dans etcd
weight: 800
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-create-locks.md"
---

LOCK acquiert un verrou distribué portant un nom donné. Une fois le verrou acquis, il reste détenu jusqu'à la terminaison d'etcdctl.

## Prérequis {#prerequisites}

* Installer [`etcd` et `etcdctl`](/fr/etcd/install/)

## Création d’un verrou {#creating-a-lock}

`lock` pour verrouillage distribué :

![08_etcdctl_lock_2016050501](/etcd/tasks/img/create-lock.gif)

```shell
etcdctl --endpoints=$ENDPOINTS lock mutex1
```

### Options {#options}
- endpoints - définit une liste séparée par des virgules d'adresses machine du cluster.
- ttl - durée d'expiration en secondes de la session de verrouillage.
