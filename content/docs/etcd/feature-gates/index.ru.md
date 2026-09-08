---
title: Функциональные шлюзы
weight: 1175
icon: fa-solid fa-toggle-on
categories: [Справочник]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/feature-gates/index.md"
aliases: [/etcd/feature-gates/]
---

<!-- overview -->
На этой странице представлен обзор функциональных шлюзов, которые администратор
может задать для etcd.

Описание стадий возможностей приведено в разделе [стадий возможностей](#feature-stages).

<!-- body -->
## Обзор {#overview}

Функциональные шлюзы — набор пар key=value, описывающих возможности etcd.
Возможности включаются и отключаются флагом командной строки `--feature-gates`
процесса etcd.

etcd позволяет включить или отключить набор функциональных шлюзов.
Полный список можно увидеть с помощью флага `-h`.
Чтобы задать шлюзы, присвойте флагу `--feature-gates` список пар возможностей в командной строке:

```shell
--feature-gates=...,StopGRPCServiceOnDefrag=true
```

Или укажите `feature-gates` в конфигурационном файле YAML:

```shell
feature-gates: ...,StopGRPCServiceOnDefrag=true
```

### Изменение структуры `embed.EtcdServer` {#change-in-embedetcdserver-struct}

В 3.6 поле `ServerFeatureGate` добавлено в `embed.Config` и должно заменить перечисленные ниже экспериментальные поля:

```diff
package embed

type Config struct {
  // Deprecated: Use CompactHashCheck Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalCompactHashCheckEnabled bool `json:"experimental-compact-hash-check-enabled"`

  // Deprecated: Use InitialCorruptCheck Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalInitialCorruptCheck bool `json:"experimental-initial-corrupt-check"`

  // Deprecated: Use TxnModeWriteWithSharedBuffer Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalTxnModeWriteWithSharedBuffer bool `json:"experimental-txn-mode-write-with-shared-buffer"`

  // Deprecated: Use StopGRPCServiceOnDefrag Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalStopGRPCServiceOnDefrag bool `json:"experimental-stop-grpc-service-on-defrag"`

  // Deprecated: Use LeaseCheckpoint Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalEnableLeaseCheckpoint bool `json:"experimental-enable-lease-checkpoint"`
  
  // Deprecated: Use LeaseCheckpointPersist Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalEnableLeaseCheckpointPersist bool `json:"experimental-enable-lease-checkpoint-persist"`

+ // ServerFeatureGate is a server level feature gate
+ ServerFeatureGate featuregate.FeatureGate
  ...
```

### Функциональные шлюзы возможностей Alpha и Beta {#feature-gates-for-alpha-or-beta-features}

В следующей таблице перечислены функциональные шлюзы, которые можно настроить в etcd.

| Возможность                          | По умолчанию | Стадия | Описание                                                                               |
|----------------------------------|---------|-------|--------------------------------------------------------------------------------------|
| CompactHashCheck                 | false   | Alpha |Включает проверку повреждения данных до обслуживания клиентского или однорангового трафика.                                                                              |
| InitialCorruptCheck              | false   | Alpha |Позволяет лидеру периодически проверять хеши компактизации последователей.                                                                           |
| LeaseCheckpoint                  | false   | Alpha |Позволяет лидеру регулярно отправлять контрольные точки другим участникам, предотвращая сброс оставшегося TTL при смене лидера.                                              |
| LeaseCheckpointPersist           | false   | Alpha |Включает сохранение remainingTTL, предотвращая бесконечное автоматическое продление долгоживущих аренд.                                                                         |
| SetMemberLocalAddr               | false   | Alpha |Использует первый заданный локальный адрес без loopback из initial-advertise-peer-urls как локальный адрес для связи с одноранговым участником.      |
| StopGRPCServiceOnDefrag          | false   | Alpha |Останавливает обслуживание клиентских запросов службой gRPC etcd на время дефрагментации.                                                                      |
| TxnModeWriteWithSharedBuffer     | true    | Beta  |Позволяет транзакции записи использовать общий буфер при проверочных операциях только для чтения.                                                                                |

## Использование возможности {#using-a-feature}

### Стадии возможностей {#feature-stages}

Возможность может находиться на стадии *Alpha*, *Beta*, *GA* или *Deprecated*.
Стадия *Alpha* означает:

* По умолчанию возможность отключена.
* Возможны ошибки; включение может проявить их.
* Поддержка может быть прекращена в любой момент без уведомления.
* API может без уведомления несовместимо измениться в следующем выпуске.
* Из-за повышенного риска ошибок и отсутствия долгосрочной поддержки рекомендуется использовать только в краткоживущих тестовых кластерах.

Стадия *Beta* означает:

* По умолчанию возможность включена.
* Возможность хорошо протестирована и считается безопасной для включения.
* Поддержка возможности в целом не будет прекращена, хотя детали могут измениться.
* Рекомендуется только для некритичных сценариев: широкое применение может выявить новые труднообнаружимые ошибки.

> [!NOTE]
> Пожалуйста, испытывайте возможности *Beta* и сообщайте о результатах!
> После выхода из beta внесение дополнительных изменений может стать непрактичным.

Стадия *General Availability* (GA), также называемая *стабильной*, означает:

* Возможность всегда включена и не может быть отключена.
* Соответствующий функциональный шлюз больше не нужен.
* Стабильные версии возможности будут присутствовать во многих последующих выпусках программного обеспечения.

Стадия *Deprecated* означает:

* Функциональный шлюз больше не используется.
* Возможность перешла в GA или была удалена.
