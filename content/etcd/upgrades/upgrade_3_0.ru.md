---
title: Обновление etcd с 2.3 до 3.0
weight: 6900
description: Процесс, контрольные списки и примечания по обновлению etcd с 2.3 до 3.0
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_0.md"
---

В общем случае обновление etcd с 2.3 до 3.0 можно выполнить поэтапно без простоя:
 - по очереди останавливать процессы etcd v2.3 и заменять их процессами etcd v3.0;
 - после запуска всех процессов v3.0 кластеру станут доступны новые возможности v3.0.

Перед [началом обновления](#upgrade-procedure) прочитайте остальную часть руководства и подготовьтесь.

### Контрольные списки обновления {#upgrade-checklists}

> [!WARNING]
> При [миграции с v2 без данных v3](https://github.com/etcd-io/etcd/issues/9480) сервер etcd v3.2+ аварийно завершается при восстановлении из существующих снимков, если отсутствует файл v3 `ETCD_DATA_DIR/member/snap/db`. Это происходит, когда сервер мигрировал с v2 и ранее не содержал данных v3. Такое поведение также предотвращает случайную потерю данных v3, например при перемещении файла `db`. etcd требует, чтобы миграция на более новые версии v3 выполнялась только при наличии данных v3. Не обновляйтесь до более новых версий v3, пока сервер v3.0 не содержит данных v3.

#### Требования к обновлению {#upgrade-requirements}

Для обновления существующего развёртывания etcd до 3.0 работающий кластер должен
иметь версию 2.3 или новее. Версию ниже 2.3 сначала обновите до
[2.3](https://github.com/etcd-io/etcd/releases/tag/v2.3.8), а затем до 3.0.

Для плавного поэтапного обновления работающий кластер также должен быть исправен.
Перед продолжением проверьте его командой `etcdctl cluster-health`.

#### Подготовка {#preparation}

Перед обновлением etcd обязательно протестируйте зависящие от него службы в
промежуточной среде до развёртывания обновления в производственной.

До начала [создайте резервную копию каталога данных etcd](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).
Если обновление завершится неудачно, копия позволит [вернуться к предыдущей версии](#downgrade).

#### Смешанные версии {#mixed-versions}

Во время обновления кластер etcd поддерживает участников разных версий и работает
по протоколу наименьшей общей версии. Кластер считается обновлённым только после
обновления всех участников до 3.0. Участники etcd согласуют общую версию кластера,
которая определяет сообщаемую версию и поддерживаемые возможности.

#### Ограничения {#limitations}

Если общий объём данных превышает 50MB, новому обновлённому участнику может
потребоваться до 2 минут, чтобы догнать кластер. Оцените объём по размеру
последнего снимка. Безопаснее всего ждать 2 минуты между обновлениями участников.

При значительно большем объёме, 100MB или более, этот однократный процесс может
занять ещё больше времени. Администраторы настолько крупных кластеров etcd могут
до обновления обратиться к [команде etcd][etcd-contact] — мы с радостью дадим
рекомендации по процедуре.

#### Понижение версии {#downgrade}

После обновления всех участников до v3.0 кластер становится кластером v3.0, и
понизить версию из этого завершённого состояния **невозможно**. Пока хотя бы один
участник остаётся на v2.3, кластер и его операции сохраняют версию «v2.3», и из
такого смешанного состояния можно вернуть двоичный файл etcd v2.3 на всех участниках.

Создайте [резервную копию каталога данных](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore)
всех участников etcd, чтобы понижение версии оставалось возможным даже после
полного обновления кластера.

### Процедура обновления {#upgrade-procedure}

В примере подробно показано обновление локального кластера etcd v2.3 из трёх участников.

#### 1. Проверьте требования к обновлению {#1-check-upgrade-requirements}

Кластер исправен и работает под управлением v.2.3.x?

```
$ etcdctl cluster-health
member 6e3bd23ae5f1eae0 is healthy: got healthy result from http://localhost:22379
member 924e2e83e93f2560 is healthy: got healthy result from http://localhost:32379
member 8211f1d0f64f3269 is healthy: got healthy result from http://localhost:12379
cluster is healthy

$ curl http://localhost:2379/version
{"etcdserver":"2.3.x","etcdcluster":"2.3.8"}
```

#### 2. Остановите существующий процесс etcd {#2-stop-the-existing-etcd-process}

При остановке каждого процесса etcd другие участники записывают ожидаемые ошибки.
Это нормально, поскольку соединение с участником временно разорвано:

```
2016-06-27 15:21:48.624124 E | rafthttp: failed to dial 8211f1d0f64f3269 on stream Message (dial tcp 127.0.0.1:12380: getsockopt: connection refused)
2016-06-27 15:21:48.624175 I | rafthttp: the connection with 8211f1d0f64f3269 became inactive
```

На этом этапе рекомендуется [создать резервную копию каталога данных etcd](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore),
чтобы при проблемах сохранить возможность понижения версии:

```
$ etcdctl backup \
      --data-dir /var/lib/etcd \
      --backup-dir /tmp/etcd_backup
```

#### 3. Установите двоичный файл etcd v3.0 и запустите новый процесс etcd {#3-drop-in-etcd-v30-binary-and-start-the-new-etcd-process}

Новый etcd v3.0 опубликует свои сведения в кластере:

```
09:58:25.938673 I | etcdserver: published {Name:infra1 ClientURLs:[http://localhost:12379]} to cluster 524400597fb1d5f6
```

Убедитесь, что с новым двоичным файлом etcd v3.0 каждый участник, а затем весь кластер становятся исправными:

```
$ etcdctl cluster-health
member 6e3bd23ae5f1eae0 is healthy: got healthy result from http://localhost:22379
member 924e2e83e93f2560 is healthy: got healthy result from http://localhost:32379
member 8211f1d0f64f3269 is healthy: got healthy result from http://localhost:12379
cluster is healthy
```


До обновления всего кластера обновлённые участники будут записывать следующие
предупреждения. Это ожидаемо и прекратится после обновления всех участников до v3.0:

```
2016-06-27 15:22:05.679644 W | etcdserver: the local etcd version 2.3.7 is not up-to-date
2016-06-27 15:22:05.679660 W | etcdserver: member 8211f1d0f64f3269 has a higher version 3.0.0
```

#### 4. Повторите шаги 2–3 для остальных участников {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Завершите обновление {#5-finish}

После обновления всех участников кластер сообщит об успешном переходе на 3.0:

```
2016-06-27 15:22:19.873751 N | membership: updated the cluster version from 2.3 to 3.0
2016-06-27 15:22:19.914574 I | api: enabled capabilities for version 3.0.0
```

```
$ ETCDCTL_API=3 etcdctl endpoint health
127.0.0.1:12379 is healthy: successfully committed proposal: took = 18.440155ms
127.0.0.1:32379 is healthy: successfully committed proposal: took = 13.651368ms
127.0.0.1:22379 is healthy: successfully committed proposal: took = 18.513301ms
```

## Дополнительные соображения {#further-considerations}

- Переменные окружения etcdctl были обновлены. Если `ETCDCTL_API=2 etcdctl cluster-health`
  работает, но `ETCDCTL_API=3 etcdctl endpoints health` отвечает
  `Error:  grpc: timed out when dialing`, убедитесь, что используются
  [новые имена переменных](https://github.com/etcd-io/etcd/tree/main/etcdctl#etcdctl).

## Известные проблемы {#known-issues}

- etcd &lt; v3.1 работает неправильно при сборке с Go &gt; v1.7. Дополнительные
  сведения см. в [задаче 6951](https://github.com/etcd-io/etcd/issues/6951).
- Если в журнале сервера etcd появляется ошибка
  `transport: http2Client.notifyError got notified that the client transport was broken unexpected EOF.`,
  убедитесь, что используется готовый выпуск etcd либо сборка с (etcd v3.1+
  &amp; go v1.7+) или (etcd &lt;v3.1 &amp; go v1.6.x).
- Добавление узла v3 в кластер v2.3 во время обновления не поддерживается и
  может вызвать аварийное завершение. Дополнительные сведения см. в
  [задаче 7249](https://github.com/etcd-io/etcd/issues/7429). Смешанные версии
  участников разрешены только во время миграции на v3. Завершите обновление до
  любых изменений состава кластера.

[etcd-contact]: https://groups.google.com/g/etcd-dev
