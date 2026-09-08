---
title: Обновление кластеров etcd и приложений
weight: 6500
description: Список документации по обновлению кластеров etcd и приложений
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/upgrades/upgrading-etcd.md"
aliases: [/etcd/upgrades/upgrading-etcd/]
---

В этом разделе содержатся документы, специфичные для обновления кластеров etcd и приложений.

## Политика обновления {#upgrade-policy}

Перед обновлением обратите внимание, что etcd поддерживает только следующие два случая обновления:

* **Обновление патча:** обновление между выпусками патча в рамках одной минорной версии (e.g. 3.7.0 - 3.7.1).
* **Минорное обновление:** обновление по одной минорной версии за раз (e.g. 3.6 - 3.7). Обновления, пропускающие минорную версию, не поддерживаются и, скорее всего, завершатся неудачно. Обновитесь до последней версии патча перед обновлением до следующей минорной версии.

## Обновление кластера etcd v3.x {#upgrading-an-etcd-v3x-cluster}

* [Обновление etcd с 3.0 до 3.1](/ru/docs/etcd/upgrades/upgrade_3_1/)  
* [Обновление etcd с 3.1 до 3.2](/ru/docs/etcd/upgrades/upgrade_3_2/)  
* [Обновление etcd с 3.2 до 3.3](/ru/docs/etcd/upgrades/upgrade_3_3/)  
* [Обновление etcd с 3.3 до 3.4](/ru/docs/etcd/upgrades/upgrade_3_4/)  
* [Обновление etcd с 3.4 до 3.5](/ru/docs/etcd/upgrades/upgrade_3_5/)  
* [Обновление etcd с 3.5 до 3.6](/ru/docs/etcd/upgrades/upgrade_3_6/)  
* [Обновление etcd с 3.6 до 3.7](/ru/docs/etcd/upgrades/upgrade_3_7/)

## Обновление с etcd v2.3 {#upgrading-from-etcd-v23}

* [Обновление кластера v2.3 до v3.0](/ru/docs/etcd/upgrades/upgrade_3_0/)
