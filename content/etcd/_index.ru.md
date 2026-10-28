---
title: "Документация etcd 3.7"
linkTitle: "etcd 3.7"
description: "Официальные руководства etcd 3.7 для разработчиков, операторов, обновлений, API и внутренней работы."
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
weight: 60
icon: fa-solid fa-gear
sidebar_root_for: self
sidebar_root_link_self: true
section_index: cards
section_index_columns: 3
upstream_source: etcd
categories: [Концепция]
search_keywords: [v3.7.3, "Go 1.26.10", NewJournalWriter]
upstream_link: "https://github.com/etcd-io/website/tree/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7"
cascade:
  upstream_source: etcd
  type: docs
  module: [ETCD]
---

etcd — это строго согласованное распределённое хранилище ключей и значений. Эти руководства охватывают установку и эксплуатацию etcd, разработку приложений с использованием его API, понимание архитектуры, измерение производительности, а также обновление или понижение версии кластеров в линейке выпусков 3.7.

Начните с [Краткого руководства](/ru/etcd/quickstart/) для локального кластера из одного участника, [Установки](/ru/etcd/install/) для поддерживаемых путей установки или [Руководства по эксплуатации](/ru/etcd/op-guide/) для промышленных развёртываний.

## etcd v3.7.3 {#etcd-v3-7-3}

Текущий корректирующий выпуск — [v3.7.3](https://github.com/etcd-io/etcd/releases/tag/v3.7.3). Примеры установки, Docker и Kubernetes в этой редакции рассчитаны на этот выпуск.

- Исправлены гонки данных между `Hash` и `Restore` в хранилище MVCC и в операциях `RangeStream`, возвращающих только ключи, а также регрессия производительности репликации, вызванная отправкой сообщений `MsgApp` лидером в обратном порядке.
- Сборка выполняется с Go 1.26.10; зависимости OpenTelemetry и `golang.org/x/net` обновлены для устранения известных проблем безопасности.
- `NewJournalWriter` в `client/pkg/v3/logutil` объявлен устаревшим; удаление запланировано в v3.8.

Полный список изменений приведён в [журнале изменений исходного проекта](https://github.com/etcd-io/etcd/blob/f164b70fdf458a17aba05dfefc685d7de4c9ca37/CHANGELOG/CHANGELOG-3.7.md#v373-2026-10-22).
