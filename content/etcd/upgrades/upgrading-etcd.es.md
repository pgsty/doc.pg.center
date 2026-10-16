---
title: Actualización de clústeres y aplicaciones etcd
weight: 6500
description: Lista de documentación para actualizar clústeres y aplicaciones etcd
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrading-etcd.md"
---

Esta sección contiene documentos específicos para la actualización de clústeres y aplicaciones etcd.

## Política de actualización {#upgrade-policy}

Antes de actualizar, ten en cuenta que etcd solo admite los dos siguientes casos de actualización:

* **Actualización de parche:** Actualización entre versiones de parche dentro de la misma versión menor (por ejemplo, 3.7.0 - 3.7.1).
* **Actualización de versión menor:** Actualización de una versión menor a la vez (por ejemplo, 3.6 - 3.7). Las actualizaciones que se saltan una versión menor no se admiten y es probable que fallen. Actualiza a la versión de parche más reciente antes de pasar a la siguiente versión menor.

## Actualización de un clúster etcd v3.x {#upgrading-an-etcd-v3x-cluster}

* [Actualiza etcd de 3.0 a 3.1](/es/etcd/upgrades/upgrade_3_1/)
* [Actualiza etcd de 3.1 a 3.2](/es/etcd/upgrades/upgrade_3_2/)
* [Actualiza etcd de 3.2 a 3.3](/es/etcd/upgrades/upgrade_3_3/)
* [Actualiza etcd de 3.3 a 3.4](/es/etcd/upgrades/upgrade_3_4/)
* [Actualiza etcd de 3.4 a 3.5](/es/etcd/upgrades/upgrade_3_5/)
* [Actualiza etcd de 3.5 a 3.6](/es/etcd/upgrades/upgrade_3_6/)
* [Actualiza etcd de 3.6 a 3.7](/es/etcd/upgrades/upgrade_3_7/)

## Actualización desde etcd v2.3 {#upgrading-from-etcd-v23}

* [Actualiza un clúster v2.3 a v3.0](/es/etcd/upgrades/upgrade_3_0/)
