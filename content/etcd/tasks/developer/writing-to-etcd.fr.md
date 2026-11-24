---
title: Écriture dans etcd
description: "Ajout d'une paire clé-valeur à un cluster etcd"
weight: 250
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7/tasks/developer/writing-to-etcd.md"
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
