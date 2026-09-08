---
title: "Comment effectuer l'élection du leader dans un cluster etcd"
description: Étapes pour effectuer une élection de leader via le client etcdctl
weight: 900
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/operator/how-to-conduct-elections.md"
aliases: [/etcd/tasks/operator/how-to-conduct-elections/]
---

## Prérequis {#prerequisites}

- Vérifiez que [`etcd`](/fr/docs/etcd/install/) et [`etcdctl`](/fr/docs/etcd/install/) sont installés.
- Vérifiez l'état du cluster etcd actif.

## Conduire l'élection du leader {#conduct-leader-election}

La commande `etcdctl` est utilisée pour effectuer des élections de leader dans un cluster etcd. Elle garantit qu'un seul client peut devenir leader à la fois.

`etcdctl --endpoints=$ENDPOINTS elect <election-name> [proposal]`

```shell
etcdctl --endpoints=$ENDPOINTS elect election-name p1
```

### Options {#options}

-  `--endpoints : $ENDPOINTS`

Adresse de chaque membre du cluster etcd.

- `election-name` chaîne de caractères

Identifiant sous forme de chaîne pour l'élection. Tous les participants en compétition pour la direction doivent utiliser le même nom d'élection.

- `leader-name` chaîne de caractères

Valeur de proposition du nouveau leader.

### Exemple {#example}

```shell
./etcdctl elect my-election proposal1
my-election/694d99fafea88404
proposal1

another election:
./etcdctl elect new-election proposal1
new-election/694d99fafea8840f
proposal1
```
