---
title: Взаимодействие с etcd
weight: 3250
description: "etcdctl: утилита командной строки для взаимодействия с сервером etcd"
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/interacting_v3.md"
---

Пользователи чаще всего взаимодействуют с etcd, устанавливая или получая значение ключа. В этом разделе описано, как это сделать с помощью etcdctl — утилиты командной строки для взаимодействия с сервером etcd. Описанные здесь концепции должны быть применимы к API gRPC и API клиентских библиотек.

etcdctl v3.7 использует API v3. API v2 и выбор версии через `ETCDCTL_API` удалены.

> [!NOTE]
> Приведённые ниже примеры сохраняют исторический вывод команд, поэтому показанные номера версий могут отличаться от вашей установки. Старые выпуски etcd хранили ключи v2 и v3 в отдельных хранилищах; перенесите данные v2 до обновления до v3.7.


## Определение версий {#find-versions}

Версия etcdctl и версия API сервера могут быть полезны при определении подходящих команд для выполнения различных операций с etcd.

Следующая команда предназначена для поиска версий:

```bash
$ etcdctl version
etcdctl version: 3.1.0-alpha.0+git
API version: 3.1
```

## Запись ключа {#write-a-key}

Приложения сохраняют данные в кластере etcd, записывая значения ключей. Каждый сохранённый ключ реплицируется всем участникам кластера etcd через протокол Raft для достижения согласованности и надёжности.

Команда задаёт ключу `foo` значение `bar`:

```bash
$ etcdctl put foo bar
OK
```

Также ключ можно установить на определённый период времени, привязав к нему аренду.

Следующая команда предназначена для установки ключу `foo1` значения `bar1` на 10s.

```bash
$ etcdctl put foo1 bar1 --lease=1234abcd
OK
```

> [!NOTE]
> В команде выше идентификатор аренды `1234abcd` относится к идентификатору, возвращённому при создании аренды длительности 10s. Этот идентификатор можно затем прикрепить к ключу.

## Чтение ключей {#read-keys}

Приложения могут читать из кластера etcd один ключ или диапазон ключей.

Предположим, что кластер etcd содержит следующие ключи:

```bash
foo = bar
foo1 = bar1
foo2 = bar2
foo3 = bar3
```

Команда читает значение ключа `foo`:

```bash
$ etcdctl get foo
foo
bar
```

Команда читает значение ключа `foo` в шестнадцатеричном формате:

```bash
$ etcdctl get foo --hex
\x66\x6f\x6f          # Key
\x62\x61\x72          # Value
```

Команда выводит только значение ключа `foo`:

```bash
$ etcdctl get foo --print-value-only
bar
```

Команда читает диапазон ключей от `foo` до `foo3`:

```bash
$ etcdctl get foo foo3
foo
bar
foo1
bar1
foo2
bar2
```

> [!NOTE]
> `foo3` исключается, так как диапазон является полуоткрытым интервалом `[foo, foo3)`, исключающим `foo3`.

Команда читает все ключи с префиксом `foo`:

```bash
$ etcdctl get --prefix foo
foo
bar
foo1
bar1
foo2
bar2
foo3
bar3
```

Следующая команда предназначена для обхода всех ключей с префиксом `foo` и ограничением количества результатов до 2:

```bash
$ etcdctl get --prefix --limit=2 foo
foo
bar
foo1
bar1
```

Следующая команда предназначена для обхода всех ключей с префиксом `foo` с использованием RPC [`RangeStream`](/ru/etcd/learning/api/#rangestream). Результат идентичен унарному `Range`:

```bash
$ etcdctl get --stream --prefix foo
foo
bar
foo1
bar1
foo2
bar2
foo3
bar3
```

`--stream` не поддерживает `--order`, `--sort-by` и фильтры ревизий.

## Чтение предыдущих версий ключей {#read-past-version-of-keys}

Приложения могут захотеть прочитать устаревшие версии ключа. Например, приложение может захотеть откатиться к старой конфигурации, обратившись к более ранней версии ключа. Кроме того, приложение может получить согласованное представление над несколькими ключами через несколько запросов, обратившись к истории ключа.
Поскольку каждое изменение хранилища ключей и значений кластера etcd увеличивает глобальную ревизию кластера etcd, приложение может прочитать замещённые ключи, предоставив более старую ревизию etcd.

Предположим, что кластер etcd уже содержит следующие ключи:

```bash
foo = bar         # revision = 2
foo1 = bar1       # revision = 3
foo = bar_new     # revision = 4
foo1 = bar1_new   # revision = 5
```

Ниже приведён пример, как получить доступ к прошлым версиям ключей:

```bash
$ etcdctl get --prefix foo # access the most recent versions of keys
foo
bar_new
foo1
bar1_new

$ etcdctl get --prefix --rev=4 foo # access the versions of keys at revision 4
foo
bar_new
foo1
bar1

$ etcdctl get --prefix --rev=3 foo # access the versions of keys at revision 3
foo
bar
foo1
bar1

$ etcdctl get --prefix --rev=2 foo # access the versions of keys at revision 2
foo
bar

$ etcdctl get --prefix --rev=1 foo # access the versions of keys at revision 1
```

## Читать ключи, которые не меньше указанного ключа по байтовому значению {#read-keys-which-are-greater-than-or-equal-to-the-byte-value-of-the-specified-key}

Приложениям может потребоваться прочитать ключи, которые больше или равны байтовому значению указанного ключа.

Предположим, что кластер etcd уже содержит следующие ключи:

```bash
a = 123
b = 456
z = 789
```

Команда читает ключи, байтовое значение которых не меньше ключа `b`:

```bash
$ etcdctl get --from-key b
b
456
z
789
```

## Удаление ключей {#delete-keys}

Приложения могут удалить ключ или диапазон ключей из кластера etcd.

Предположим, что кластер etcd уже содержит следующие ключи:

```bash
foo = bar
foo1 = bar1
foo3 = bar3
zoo = val
zoo1 = val1
zoo2 = val2
a = 123
b = 456
z = 789
```

Следующая команда предназначена для удаления ключа `foo`:

```bash
$ etcdctl del foo
1 # one key is deleted
```

Следующая команда предназначена для удаления ключей от `foo` до `foo9`:

```bash
$ etcdctl del foo foo9
2 # two keys are deleted
```

Команда удаляет `zoo` и возвращает удалённую пару «ключ — значение»:

```bash
$ etcdctl del --prev-kv zoo
1   # one key is deleted
zoo # deleted key
val # the value of the deleted key
```

Команда удаляет ключи с префиксом `zoo`:

```bash
$ etcdctl del --prefix zoo
2 # two keys are deleted
```

Команда удаляет ключи, байтовое значение которых не меньше ключа `b`:

```bash
$ etcdctl del --from-key b
2 # two keys are deleted
```

## Наблюдение за изменениями ключа {#watch-key-changes}

Приложения могут наблюдать за ключом или диапазоном ключей для мониторинга любых обновлений.

Следующая команда предназначена для наблюдения за ключом `foo`:

```bash
$ etcdctl watch foo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
```

Команда наблюдает за ключом `foo` в шестнадцатеричном формате:

```bash
$ etcdctl watch foo --hex
# in another terminal: etcdctl put foo bar
PUT
\x66\x6f\x6f          # Key
\x62\x61\x72          # Value
```

Следующая команда предназначена для наблюдения за диапазоном ключей от `foo` до `foo9`:

```bash
$ etcdctl watch foo foo9
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put foo1 bar1
PUT
foo1
bar1
```

Следующая команда предназначена для наблюдения за ключами с префиксом `foo`:

```bash
$ etcdctl watch --prefix foo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put fooz1 barz1
PUT
fooz1
barz1
```

Команда наблюдает за несколькими ключами `foo` и `zoo`:

```bash
$ etcdctl watch -i
$ watch foo
$ watch zoo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put zoo val
PUT
zoo
val
```

## Наблюдение за историческими изменениями ключей {#watch-historical-changes-of-keys}

Приложения могут захотеть наблюдать за историческими изменениями ключей в etcd. Например, приложение может захотеть получать все модификации ключа; если приложение останется подключено к etcd, то `watch` будет достаточно. Однако, если приложение или etcd даст сбой, изменение может произойти во время сбоя, и приложение не получит обновление в реальном времени. Чтобы гарантировать доставку обновления, приложение должно быть способно наблюдать за историческими изменениями ключей. Для этого приложение может указать историческую ревизию при наблюдении, как при чтении прошлых версий ключей.

Предположим, что мы завершили следующую последовательность операций:

```bash
$ etcdctl put foo bar         # revision = 2
OK
$ etcdctl put foo1 bar1       # revision = 3
OK
$ etcdctl put foo bar_new     # revision = 4
OK
$ etcdctl put foo1 bar1_new   # revision = 5
OK
```

Ниже приведён пример наблюдения за историческими изменениями:

```bash
# watch for changes on key `foo` since revision 2
$ etcdctl watch --rev=2 foo
PUT
foo
bar
PUT
foo
bar_new
```

```bash
# watch for changes on key `foo` since revision 3
$ etcdctl watch --rev=3 foo
PUT
foo
bar_new
```

Ниже приведён пример наблюдения только с последнего исторического изменения:

```bash
# watch for changes on key `foo` and return last revision value along with modified value
$ etcdctl watch --prev-kv foo
# in another terminal: etcdctl put foo bar_latest
PUT
foo         # key
bar_new     # last value of foo key before modification
foo         # key
bar_latest  # value of foo key after modification
```

## Наблюдение за прогрессом {#watch-progress}

Приложение может проверять ход наблюдения, чтобы определить актуальность потока.
Например, если наблюдение используется для обновления кэша, полезно знать,
не устарел ли он относительно ревизии, полученной чтением по кворуму.

Запросы прогресса можно отправлять с помощью команды "progress" в интерактивном сеансе наблюдения, чтобы попросить сервер etcd отправлять уведомление о прогрессе в потоке наблюдения:

```bash
$ etcdctl watch -i
$ watch a
$ progress
progress notify: 1
# in another terminal: etcdctl put x 0
# in another terminal: etcdctl put y 1
$ progress
progress notify: 3
```

> [!NOTE]
> Номер ревизии в ответе на уведомление о прогрессе — это номер ревизии локального узла сервера etcd, к которому подключён поток наблюдения. Если этот узел отсечён и не является частью кворума, то номер ревизии уведомления о прогрессе может быть ниже номера ревизии, возвращаемого чтением по кворуму на неотсечённом узле сервера etcd.

## Компактизированные ревизии {#compacted-revisions}

Как мы уже упоминали, etcd хранит ревизии, чтобы приложения могли читать прошлые версии ключей. Однако, чтобы избежать накопления неограниченного количества истории, важно компактизировать прошлые ревизии. После компактизации etcd удаляет исторические ревизии, освобождая ресурсы для будущего использования. Все замещённые данные с ревизиями, предшествующими компактизированной ревизии, станут недоступны.

Следующая команда предназначена для компактизации ревизий:

```bash
$ etcdctl compact 5
compacted revision 5

# any revisions before the compacted one are not accessible
$ etcdctl get --rev=4 foo
Error:  rpc error: code = 11 desc = etcdserver: mvcc: required revision has been compacted
```

> [!NOTE]
> Текущую ревизию сервера etcd можно найти с помощью команды get для любого ключа (существующего или несуществующего) в формате json. Пример показан ниже для ключа mykey, который не существует на сервере etcd:

```bash
$ etcdctl get mykey -w=json
{"header":{"cluster_id":14841639068965178418,"member_id":10276657743932975437,"revision":15,"raft_term":4}}
```

## Выдача аренды {#grant-leases}

Приложения могут выдавать аренды для ключей из кластера etcd. Когда ключ прикреплён к аренде, его срок жизни связан со сроком жизни аренды, который в свою очередь регулируется сроком жизни (TTL). Каждая аренда имеет минимальное значение срока жизни (TTL), указанное приложением при выдаче. Фактическое значение TTL аренды составляет не менее минимального TTL и выбирается кластером etcd. После истечения TTL аренды она истекает, и все прикреплённые ключи удаляются.

Команда выдаёт аренду:

```bash
# grant a lease with 60 second TTL
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)

# attach key foo to lease 32695410dcc0ca06
$ etcdctl put --lease=32695410dcc0ca06 foo bar
OK
```

## Отзыв аренды {#revoke-leases}

Приложения отзывают аренды по идентификатору аренды. Отзыв аренды удаляет все связанные с ней ключи.

Предположим, что мы завершили следующую последовательность операций:

```bash
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)
$ etcdctl put --lease=32695410dcc0ca06 foo bar
OK
```

Команда отзывает ту же аренду:

```bash
$ etcdctl lease revoke 32695410dcc0ca06
lease 32695410dcc0ca06 revoked

$ etcdctl get foo
# empty response since foo is deleted due to lease revocation
```

## Поддержание активности аренды {#keep-leases-alive}

Приложения могут поддерживать аренду активной обновлением её TTL, чтобы она не истекла.

Предположим, что мы завершили следующую последовательность операций:

```bash
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)
```

Команда поддерживает ту же аренду активной:

```bash
$ etcdctl lease keep-alive 32695410dcc0ca06
lease 32695410dcc0ca06 keepalived with TTL(60)
lease 32695410dcc0ca06 keepalived with TTL(60)
lease 32695410dcc0ca06 keepalived with TTL(60)
...
```

## Получение сведений об аренде {#get-lease-information}

Приложению могут потребоваться сведения об аренде, чтобы продлить её или проверить, существует ли она и не истёк ли срок её действия. Также может потребоваться список ключей, привязанных к определённой аренде.

Предположим, что мы завершили следующую последовательность операций:

```bash
# grant a lease with 500 second TTL
$ etcdctl lease grant 500
lease 694d5765fc71500b granted with TTL(500s)

# attach key zoo1 to lease 694d5765fc71500b
$ etcdctl put zoo1 val1 --lease=694d5765fc71500b
OK

# attach key zoo2 to lease 694d5765fc71500b
$ etcdctl put zoo2 val2 --lease=694d5765fc71500b
OK
```

Команда получает сведения об аренде:

```bash
$ etcdctl lease timetolive 694d5765fc71500b
lease 694d5765fc71500b granted with TTL(500s), remaining(258s)
```

Команда получает сведения об аренде вместе с привязанными ключами:

```bash
$ etcdctl lease timetolive --keys 694d5765fc71500b
lease 694d5765fc71500b granted with TTL(500s), remaining(132s), attached keys([zoo2 zoo1])

# if the lease has expired or does not exist it will give the below response:
Error:  etcdserver: requested lease not found
```
