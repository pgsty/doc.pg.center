---
title: Gestion des versions
weight: 4900
description: Prise en charge de la gestion des versions par etcd
categories: [Concept]
upstream_link: "https://github.com/etcd-io/website/blob/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7/op-guide/versioning.md"
---

Ce document décrit les versions prises en charge par le projet etcd.

## Gestion des versions des services et versions prises en charge {#service-versioning-and-supported-versions}

Les versions d'etcd sont exprimées sous la forme **x.y.z**, où **x** représente la version majeure, **y** la version mineure et **z** la version de correctif, conformément à la terminologie [Semantic Versioning](https://semver.org/).
Les nouvelles versions mineures peuvent ajouter des fonctionnalités supplémentaires à l'API.

Le projet etcd maintient des branches de publication pour la version actuelle et les deux versions précédentes. Par exemple, lorsque v3.7 est la version actuelle, v3.6 et v3.5 sont prises en charge. Lorsque v3.8 sera publiée, v3.5 ne le sera plus.

Les correctifs applicables, y compris les correctifs de sécurité, peuvent être appliqués en retour à ces trois branches de version, selon leur gravité et leur faisabilité.
Les versions correctives sont créées à partir de ces branches lorsque nécessaire.

Les [mainteneurs](https://github.com/etcd-io/etcd/blob/main/OWNERS) du projet prennent cette décision.

Vous pouvez vérifier la version du cluster etcd en cours d'exécution avec `etcdctl` :

```sh
etcdctl --endpoints=127.0.0.1:2379 endpoint status
```

## Gestion des versions de l'API {#api-versioning}

Les réponses de l'API `v3` ne doivent pas changer après la version 3.0.0, mais de nouvelles fonctionnalités seront ajoutées au fil du temps.
