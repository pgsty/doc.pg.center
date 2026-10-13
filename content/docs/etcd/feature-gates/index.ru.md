---
title: Флаги функций
weight: 1175
icon: fa-solid fa-toggle-on
categories: [Справочник]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/feature-gates/index.md"
aliases: [/etcd/feature-gates/]
---

<!-- overview -->
На этой странице представлен обзор флагов функций, которые администратор
может задать для etcd.

Описание стадий возможностей приведено в разделе [стадии возможностей](#feature-stages).

<!-- body -->
## Обзор {#overview}

Флаги функций — набор пар key=value, описывающих возможности etcd.
Возможности включаются и отключаются флагом командной строки `--feature-gates`
процесса etcd.

etcd позволяет включить или отключить набор флагов функций.
Полный набор флагов функций можно увидеть с помощью флага `-h`.
Чтобы задать флаги функций, присвойте флагу `--feature-gates` список пар возможностей в командной строке:

```shell
--feature-gates=...,StopGRPCServiceOnDefrag=true
```

Или укажите `feature-gates` в конфигурационном файле YAML:

```shell
feature-gates: ...,StopGRPCServiceOnDefrag=true
```

### Изменение структуры `embed.Config` {#change-in-embedetcdserver-struct}

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

### Флаги функций для возможностей Alpha и Beta {#feature-gates-for-alpha-or-beta-features}

В следующей таблице перечислены флаги функций, которые можно настроить в etcd.

| Возможность                          | По умолчанию | Стадия | Описание                                                                               |
|----------------------------------|---------|-------|--------------------------------------------------------------------------------------|
| CompactHashCheck                 | false   | Alpha |Позволяет лидеру периодически сравнивать хеши ревизий компактизации участников кластера для обнаружения повреждения данных.                                                                              |
| InitialCorruptCheck              | false   | Alpha |Включает проверку повреждения данных до обслуживания клиентского или однорангового трафика.                                                                           |
| LeaseCheckpoint                  | false   | Alpha |Позволяет лидеру регулярно отправлять контрольные точки другим участникам, предотвращая сброс оставшегося TTL при смене лидера.                                              |
| LeaseCheckpointPersist           | false   | Alpha |Включает сохранение remainingTTL, предотвращая бесконечное автоматическое продление долгоживущих аренд.                                                                         |
| SetMemberLocalAddr               | false   | Alpha |Позволяет использовать первый заданный локальный адрес, не являющийся loopback, из initial-advertise-peer-urls как локальный адрес при связи с одноранговым участником.      |
| StopGRPCServiceOnDefrag          | false   | Alpha |Позволяет службе gRPC etcd прекратить обслуживание клиентских запросов при дефрагментации.                                                                      |
| TxnModeWriteWithSharedBuffer     | true    | Beta  |Позволяет транзакции записи использовать общий буфер при проверочных операциях только для чтения.                                                                                |

## Использование возможности {#using-a-feature}

### Стадии возможностей {#feature-stages}

Возможность может находиться на стадии *Alpha*, *Beta*, *GA* или *Deprecated*.
Стадия *Alpha* означает:

* По умолчанию возможность отключена.
* Возможны ошибки; включение может проявить их.
* Поддержка может быть прекращена в любой момент без уведомления.
* API может без уведомления несовместимо измениться в более позднем выпуске программного обеспечения.
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
* Соответствующий флаг функции больше не нужен.
* Стабильные версии возможности будут присутствовать во многих последующих выпусках программного обеспечения.

Стадия *Deprecated* означает:

* Флаг функции больше не используется.
* Возможность перешла в GA или была удалена.
