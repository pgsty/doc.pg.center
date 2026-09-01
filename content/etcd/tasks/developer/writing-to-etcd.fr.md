---
title: Écriture dans etcd
description: "Ajout d'une paire clé-valeur à un cluster etcd"
weight: 250
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/writing-to-etcd.md"
---

## Prérequis {#prerequisites}

- Installer `etcdctl`

## Procédure {#procedure}

Utilisez la sous-commande `put` pour écrire une paire clé-valeur :

```shell
etcdctl --endpoints=$ENDPOINTS put foo "Hello World!"
```
où :
- `foo` est le nom de la clé
- `"Hello World!"` est la valeur délimitée par des guillemets
