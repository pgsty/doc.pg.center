---
title: Mise à jour des clusters etcd et des applications
weight: 6500
description: Liste de documentation pour la mise à jour des clusters etcd et des applications
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/upgrades/upgrading-etcd.md"
---

Cette section contient les documents spécifiques à la mise à jour des clusters etcd et des applications.

## Politique de mise à jour {#upgrade-policy}

Avant la mise à jour, notez qu’etcd ne prend en charge que les deux cas de mise à jour suivants :

* **Mise à jour correctif :** Mise à jour entre des versions correctives du même numéro de version mineure (par exemple, 3.7.0 → 3.7.1).
* **Mise à jour mineure :** Mise à jour d'une version mineure à la fois (par exemple, 3.6 → 3.7). Les mises à jour qui sautent une version mineure ne sont pas prises en charge et risquent de échouer. Mettez à jour vers la dernière version correctif avant de passer à la version mineure suivante.

## Mise à jour d'un cluster etcd v3.x {#upgrading-an-etcd-v3x-cluster}

* [Mise à niveau d'etcd de la version 3.0 vers la 3.1](/fr/etcd/upgrades/upgrade_3_1/)
* [Mise à niveau d'etcd de la version 3.1 vers la 3.2](/fr/etcd/upgrades/upgrade_3_2/)
* [Mise à niveau d'etcd de la version 3.2 vers la 3.3](/fr/etcd/upgrades/upgrade_3_3/)
* [Mise à niveau d'etcd de la version 3.3 vers la 3.4](/fr/etcd/upgrades/upgrade_3_4/)
* [Mise à niveau d'etcd de la version 3.4 vers la 3.5](/fr/etcd/upgrades/upgrade_3_5/)
* [Mise à niveau d'etcd de la version 3.5 vers la 3.6](/fr/etcd/upgrades/upgrade_3_6/)
* [Mise à niveau d'etcd de la version 3.6 vers la 3.7](/fr/etcd/upgrades/upgrade_3_7/)

## Mise à niveau depuis etcd v2.3 {#upgrading-from-etcd-v23}

* [Mettre à jour un cluster v2.3 vers la v3.0](/fr/etcd/upgrades/upgrade_3_0/)
