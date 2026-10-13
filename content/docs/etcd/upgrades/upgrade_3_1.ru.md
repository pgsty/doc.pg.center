---
title: Обновление etcd с 3.0 до 3.1
weight: 6850
description: Процесс, контрольные списки и примечания по обновлению etcd с 3.0 до 3.1
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_1.md"
aliases: [/etcd/upgrades/upgrade_3_1/]
---

В общем случае обновление etcd с 3.0 до 3.1 можно выполнить поэтапно без простоя:
 - по очереди останавливать процессы etcd v3.0 и заменять их процессами etcd v3.1;
 - после запуска всех процессов v3.1 кластеру станут доступны новые возможности v3.1.

Перед [началом обновления](#upgrade-procedure) прочитайте остальную часть руководства и подготовьтесь.

### Контрольные списки обновления {#upgrade-checklists}

> [!WARNING]
> При [миграции с v2 без данных v3](https://github.com/etcd-io/etcd/issues/9480) сервер etcd v3.2+ аварийно завершается при восстановлении из существующих снимков, если отсутствует файл v3 `ETCD_DATA_DIR/member/snap/db`. Это происходит, когда сервер мигрировал с v2 и ранее не содержал данных v3. Такое поведение также предотвращает случайную потерю данных v3, например при перемещении файла `db`. etcd требует, чтобы миграция на более новые версии v3 выполнялась только при наличии данных v3. Не обновляйтесь до более новых версий v3, пока сервер v3.0 не содержит данных v3.

#### Мониторинг {#monitoring}

Следующие метрики v3.0.x устарели в пользу [go-grpc-prometheus](https://github.com/grpc-ecosystem/go-grpc-prometheus):

- `etcd_grpc_requests_total`
- `etcd_grpc_requests_failed_total`
- `etcd_grpc_active_streams`
- `etcd_grpc_unary_requests_duration_seconds`

#### Требования к обновлению {#upgrade-requirements}

Для обновления существующего развёртывания etcd до 3.1 работающий кластер должен
иметь версию 3.0 или новее. Версию ниже 3.0 сначала [обновите до 3.0](/ru/docs/etcd/upgrades/upgrade_3_0),
а затем до 3.1.

Для плавного поэтапного обновления работающий кластер также должен быть исправен.
Перед продолжением проверьте его командой `etcdctl endpoint health`.

#### Подготовка {#preparation}

Перед обновлением etcd обязательно протестируйте зависящие от него службы в
промежуточной среде до развёртывания обновления в производственной.

До начала [создайте резервную копию данных etcd](/ru/docs/etcd/op-guide/maintenance/#snapshot-backup).
Если обновление завершится неудачно, копия позволит [вернуться к предыдущей
версии](#downgrade). Обратите внимание: команда `snapshot` копирует только
данные v3. Для данных v2 см. [резервное копирование хранилища v2](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

#### Смешанные версии {#mixed-versions}

Во время обновления кластер etcd поддерживает участников разных версий и работает
по протоколу наименьшей общей версии. Кластер считается обновлённым только после
обновления всех участников до 3.1. Участники etcd согласуют общую версию кластера,
которая определяет сообщаемую версию и поддерживаемые возможности.

#### Ограничения {#limitations}

Примечание: ограничение не относится к кластеру, содержащему только данные v3 без данных v2.

Если кластер обслуживает набор данных v2 больше 50MB, новому обновлённому
участнику может потребоваться до двух минут, чтобы догнать кластер. Оцените объём
по размеру последнего снимка. Безопаснее всего ждать 2 минуты между обновлениями участников.

При значительно большем объёме, 100MB или более, этот однократный процесс может
занять ещё больше времени. Администраторы настолько крупных кластеров etcd могут
до обновления обратиться к [команде etcd][etcd-contact] — мы с радостью дадим
рекомендации по процедуре.

#### Понижение версии {#downgrade}

После обновления всех участников до v3.1 кластер становится кластером v3.1, и
понизить версию из этого завершённого состояния **невозможно**. Пока хотя бы один
участник остаётся на v3.0, кластер и его операции сохраняют версию "v3.0", и из
такого смешанного состояния можно вернуть двоичный файл etcd v3.0 на всех участниках.

Создайте [резервную копию каталога данных](/ru/docs/etcd/op-guide/maintenance#snapshot-backup)
всех участников etcd, чтобы понижение версии оставалось возможным даже после
полного обновления кластера.

### Процедура обновления {#upgrade-procedure}

В примере показано обновление локального кластера etcd v3.0 из 3 участников.

#### 1. Проверьте требования к обновлению {#1-check-upgrade-requirements}

Кластер исправен и работает под управлением v3.0.x?

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.0.16","etcdcluster":"3.0.0"}
```

#### 2. Остановите существующий процесс etcd {#2-stop-the-existing-etcd-process}

При остановке каждого процесса etcd другие участники записывают ожидаемые ошибки.
Это нормально, поскольку соединение с участником временно разорвано:

```
2017-01-17 09:34:18.352662 I | raft: raft.node: 1640829d9eea5cfb elected leader 1640829d9eea5cfb at term 5
2017-01-17 09:34:18.359630 W | etcdserver: failed to reach the peerURL(http://localhost:2380) of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
2017-01-17 09:34:18.359679 W | etcdserver: cannot get the version of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
2017-01-17 09:34:18.548116 W | rafthttp: lost the TCP streaming connection with peer fd32987dcd0511e0 (stream Message writer)
2017-01-17 09:34:19.147816 W | rafthttp: lost the TCP streaming connection with peer fd32987dcd0511e0 (stream MsgApp v2 writer)
2017-01-17 09:34:34.364907 W | etcdserver: failed to reach the peerURL(http://localhost:2380) of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
```

На этом этапе рекомендуется [создать резервную копию данных etcd](/ru/docs/etcd/op-guide/maintenance#snapshot-backup),
чтобы при проблемах сохранить возможность понижения версии:

```
$ etcdctl snapshot save backup.db
```

#### 3. Установите двоичный файл etcd v3.1 и запустите новый процесс etcd {#3-drop-in-etcd-v31-binary-and-start-the-new-etcd-process}

Новый etcd v3.1 опубликует свои сведения в кластере:

```
2017-01-17 09:36:00.996590 I | etcdserver: published {Name:my-etcd-1 ClientURLs:[http://localhost:2379]} to cluster 46bc3ce73049e678
```

Убедитесь, что с новым двоичным файлом etcd v3.1 каждый участник, а затем весь кластер становятся исправными:

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321671ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

До обновления всего кластера обновлённые участники будут записывать следующие
предупреждения. Это ожидаемо и прекратится после обновления всех участников до v3.1:

```
2017-01-17 09:36:38.406268 W | etcdserver: the local etcd version 3.0.16 is not up-to-date
2017-01-17 09:36:38.406295 W | etcdserver: member fd32987dcd0511e0 has a higher version 3.1.0
2017-01-17 09:36:42.407695 W | etcdserver: the local etcd version 3.0.16 is not up-to-date
2017-01-17 09:36:42.407730 W | etcdserver: member fd32987dcd0511e0 has a higher version 3.1.0
```

#### 4. Повторите шаги 2–3 для остальных участников {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Завершите обновление {#5-finish}

После обновления всех участников кластер сообщит об успешном переходе на 3.1:

```
2017-01-17 09:37:03.100015 I | etcdserver: updating the cluster version from 3.0 to 3.1
2017-01-17 09:37:03.104263 N | etcdserver/membership: updated the cluster version from 3.0 to 3.1
2017-01-17 09:37:03.104374 I | etcdserver/api: enabled capabilities for version 3.1
```

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 2.312897ms
localhost:22379 is healthy: successfully committed proposal: took = 2.553476ms
localhost:32379 is healthy: successfully committed proposal: took = 2.516902ms
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
