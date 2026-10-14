---
title: "Справочник API: конкурентность"
weight: 3900
description: "Справочник по API конкурентности etcd"
categories: [Справочник]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/api_concurrency_reference_v3.md"
---

Этот справочник API автоматически создан из указанных файлов `.proto`.

##### служба `Lock` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#service-lock-serveretcdserverapiv3lockv3lockpbv3lockproto}

Служба блокировок предоставляет клиентские средства блокировки через интерфейс gRPC.

| Метод | Тип запроса | Тип ответа | Описание |
| ------ | ------------ | ------------- | ----------- |
| Lock | LockRequest | LockResponse | Lock получает распределённую совместную блокировку с указанным именем. При успехе возвращается уникальный ключ, существующий, пока вызывающая сторона удерживает блокировку. Вместе с транзакциями ключ позволяет безопасно гарантировать, что etcd обновляется только при владении блокировкой. Блокировка удерживается до вызова Unlock для ключа или истечения аренды владельца. |
| Unlock | UnlockRequest | UnlockResponse | Unlock принимает ключ, возвращённый Lock, и освобождает блокировку. Следующий ожидающий вызов Lock пробуждается и получает владение блокировкой. |

##### сообщение `LockRequest` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-lockrequest-serveretcdserverapiv3lockv3lockpbv3lockproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| name | name — идентификатор получаемой распределённой совместной блокировки. | bytes |
| lease | lease — идентификатор аренды, привязанной к владению блокировкой. Если удерживающая блокировку аренда истекает или отзывается, блокировка освобождается автоматически. Вызовы Lock с одной арендой считаются одним получением; повторная блокировка с той же арендой ничего не делает. | int64 |

##### сообщение `LockResponse` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-lockresponse-serveretcdserverapiv3lockv3lockpbv3lockproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| key | key — ключ, существующий в etcd, пока вызывающая Lock сторона владеет блокировкой. Пользователи не должны изменять ключ, иначе поведение блокировки не определено. | bytes |

##### сообщение `UnlockRequest` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-unlockrequest-serveretcdserverapiv3lockv3lockpbv3lockproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| key | key — ключ владения блокировкой, выданный Lock. | bytes |

##### сообщение `UnlockResponse` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-unlockresponse-serveretcdserverapiv3lockv3lockpbv3lockproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### служба `Election` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#service-election-serveretcdserverapiv3electionv3electionpbv3electionproto}

Служба выборов предоставляет клиентские средства выборов через интерфейс gRPC.

| Метод | Тип запроса | Тип ответа | Описание |
| ------ | ------------ | ------------- | ----------- |
| Campaign | CampaignRequest | CampaignResponse | Campaign ожидает получения лидерства на выборах и при успехе возвращает представляющий его LeaderKey. Затем LeaderKey можно использовать для публикации новых значений выборов, транзакционной защиты запросов API условием сохранения лидерства и отказа от участия. |
| Proclaim | ProclaimRequest | ProclaimResponse | Proclaim заменяет опубликованное лидером значение новым. |
| Leader | LeaderRequest | LeaderResponse | Leader возвращает текущее объявление выборов, если оно существует. |
| Observe | LeaderRequest | LeaderResponse | Observe потоково передаёт объявления выборов в порядке их публикации избранными лидерами. |
| Resign | ResignRequest | ResignResponse | Resign освобождает лидерство, чтобы его мог получить другой кандидат. |

##### сообщение `CampaignRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-campaignrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| name | name — идентификатор выборов для кампании. | bytes |
| lease | lease — идентификатор аренды, привязанной к лидерству на выборах. Если аренда истекает или отзывается до отказа от лидерства, оно передаётся следующему кандидату, если он есть. | int64 |
| value | value — начальное объявленное значение, задаваемое после победы кандидата. | bytes |

##### сообщение `CampaignResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-campaignresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| leader | leader описывает ресурсы, используемые для удержания лидерства на выборах. | LeaderKey |

##### сообщение `LeaderKey` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderkey-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| name | name — идентификатор выборов, соответствующий ключу лидерства. | bytes |
| key | key — непрозрачный ключ, представляющий владение выборами. При удалении ключа лидерство теряется. | bytes |
| rev | rev — ревизия создания ключа. В транзакциях она позволяет проверить владение выборами, сравнив ревизию создания ключа с rev. | int64 |
| lease | lease — идентификатор аренды лидера выборов. | int64 |

##### сообщение `LeaderRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| name | name — идентификатор выборов для сведений о лидерстве. | bytes |

##### сообщение `LeaderResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| kv | kv — пара «ключ — значение», представляющая последнее обновление лидера. | mvccpb.KeyValue |

##### сообщение `ProclaimRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-proclaimrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| leader | leader — удерживаемое лидерство на выборах. | LeaderKey |
| value | value — обновление, заменяющее текущее значение лидера. | bytes |

##### сообщение `ProclaimResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-proclaimresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### сообщение `ResignRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-resignrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| leader | leader — лидерство, освобождаемое при отказе. | LeaderKey |

##### сообщение `ResignResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-resignresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### сообщение `Event` (api/mvccpb/kv.proto) {#message-event-apimvccpbkvproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| type | type — вид события. PUT означает запись новых данных в ключ, DELETE — удаление ключа. | EventType |
| kv | kv содержит KeyValue события. Событие PUT содержит текущую пару kv. PUT с kv.Version=1 означает создание ключа. DELETE/EXPIRE содержит удалённый ключ, ревизия изменения которого равна ревизии удаления. | KeyValue |
| prev_kv | prev_kv содержит пару «ключ — значение» до события. | KeyValue |

##### сообщение `KeyValue` (api/mvccpb/kv.proto) {#message-keyvalue-apimvccpbkvproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| key | key — ключ в байтах. Пустой ключ запрещён. | bytes |
| create_revision | create_revision — ревизия последнего создания этого ключа. | int64 |
| mod_revision | mod_revision — ревизия последнего изменения этого ключа. | int64 |
| version | version — версия ключа. Удаление сбрасывает версию в ноль, а любое изменение увеличивает её. | int64 |
| value | value — значение ключа в байтах. | bytes |
| lease | lease — идентификатор аренды, привязанной к ключу. После истечения аренды ключ удаляется. Если lease равно 0, аренда к ключу не привязана. | int64 |
