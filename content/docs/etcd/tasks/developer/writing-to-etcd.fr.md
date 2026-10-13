---
title: Écriture dans etcd
description: "Ajout d'une paire clé-valeur à un cluster etcd"
weight: 250
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/writing-to-etcd.md"
aliases: [/etcd/tasks/developer/writing-to-etcd/]
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
