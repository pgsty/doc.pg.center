---
title: Gestion des versions
weight: 4900
description: Prise en charge de la versionning par etcd
categories: [Concept]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/versioning.md"
---

Ce document décrit les versions prises en charge par le projet etcd.

## Versioning des services et versions prises en charge {#service-versioning-and-supported-versions}

Les versions d'etcd sont exprimées sous la forme **x.y.z**, où **x** représente la version majeure, **y** la version mineure et **z** la version de correctif, conformément à la terminologie [Semantic Versioning](https://semver.org/).
Les nouvelles versions mineures peuvent ajouter des fonctionnalités supplémentaires à l'API.

Le projet etcd maintient des branches de version pour la version actuelle et les versions précédentes. Par exemple, lorsque v3.5 est la version actuelle, v3.4 est prise en charge. Lorsque v3.6 est publiée, v3.4 n'est plus pris en charge.

Les correctifs applicables, y compris les correctifs de sécurité, peuvent être appliqués en retour à ces deux branches de version, selon leur gravité et leur faisabilité.
Les versions correctives sont créées à partir de ces branches lorsque nécessaire.

Les responsables du projet [Maintainers](https://github.com/etcd-io/etcd/blob/main/OWNERS) détiennent cette décision.

Vous pouvez vérifier la version du cluster etcd en cours d'exécution avec `etcdctl` :

```sh
etcdctl --endpoints=127.0.0.1:2379 endpoint status
```

## Versionning de l'API {#api-versioning}

Les réponses de l'API `v3` ne doivent pas changer après la version 3.0.0, mais de nouvelles fonctionnalités seront ajoutées au fil du temps.
