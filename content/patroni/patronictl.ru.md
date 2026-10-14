---
title: "patronictl"
weight: 50
icon: fa-solid fa-terminal
description: "Справочник по конфигурации, синтаксису и подкомандам patronictl."
module: [PATRONI]
categories: [Справочник]
upstream_link: "https://patroni.readthedocs.io/en/latest/patronictl.html"
---

<a id="patronictl"></a>
Patroni предоставляет интерфейс командной строки [patronictl](/ru/patroni/patronictl#patronictl), предназначенный главным образом для взаимодействия с REST API Patroni и DCS. Он упрощает операции с кластером и удобен как людям, так и сценариям.

<a id="patronictl_configuration"></a>

--------

## Конфигурация {#configuration}

[patronictl](/ru/patroni/patronictl#patronictl) использует 3 раздела конфигурации:

- **ctl**: способ аутентификации в REST API Patroni и проверки подлинности сервера. Подробнее см. [параметры ctl](/ru/patroni/config/yaml#patronictl_settings);
- **restapi**: способ аутентификации в REST API Patroni и проверки подлинности сервера. Используется, только если конфигурации `ctl` недостаточно. [patronictl](/ru/patroni/patronictl#patronictl) в основном использует раздел `restapi.authentication`, если отсутствует `ctl.authentication`, и параметр `restapi.cafile`, если отсутствует `ctl.cacert`. Подробнее см. [параметры REST API](/ru/patroni/config/yaml#restapi_settings);
- DCS, например **etcd**: способ подключения и аутентификации в DCS, используемом Patroni.

Эти параметры можно получить из переменных окружения или файла конфигурации. Способы их задания описаны в соответствующих разделах [Параметров конфигурации окружения](/ru/patroni/config/env#env) и [Параметров конфигурации YAML](/ru/patroni/config/yaml#yaml).

При использовании переменных окружения Patronictl просто читает и применяет их значения.

При использовании файла конфигурации сообщить о нём [patronictl](/ru/patroni/patronictl#patronictl) можно несколькими способами. По умолчанию [patronictl](/ru/patroni/patronictl#patronictl) пытается загрузить файл `patronictl.yaml` из одного из следующих путей в зависимости от системы:

- Mac OS X: `~/Library/Application Support/patroni`
- Mac OS X (POSIX): `~/.patroni`
- Unix: `~/.config/patroni`
- Unix (POSIX): `~/.patroni`
- Windows (с перемещаемым профилем): `C:\Users\<user>\AppData\Roaming\patroni`
- Windows (без перемещаемого профиля): `C:\Users\<user>\AppData\Local\patroni`

Поведение можно переопределить одним из способов:

- задать переменной окружения `PATRONICTL_CONFIG_FILE` путь к пользовательскому файлу конфигурации;
- передать путь к пользовательскому файлу в аргументе командной строки `-c` / `--config-file` команды [patronictl](/ru/patroni/patronictl#patronictl).

> [!NOTE]
> Если [patronictl](/ru/patroni/patronictl#patronictl) запускается на том же узле, что и демон `patroni`, можно использовать один файл конфигурации, если он содержит все разделы, необходимые [patronictl](/ru/patroni/patronictl#patronictl).

<a id="patronictl_usage"></a>

--------

## Использование {#usage}

[patronictl](/ru/patroni/patronictl#patronictl) предоставляет несколько удобных операций. В этом разделе описана каждая из них.

Перед рассмотрением подкоманд [patronictl](/ru/patroni/patronictl#patronictl) обратите внимание на аргументы командной строки самой [patronictl](/ru/patroni/patronictl#patronictl):

`-c` / `--config-file`  
Как описано выше, задаёт путь к файлу конфигурации [patronictl](/ru/patroni/patronictl#patronictl).

`-d` / `--dcs-url` / `--dcs`  
Задаёт строку подключения к DCS, используемому Patroni.

Аргумент переопределяет параметры DCS и `namespace` из конфигурации [patronictl](/ru/patroni/patronictl#patronictl) либо задаёт их, если они отсутствуют.

Значение должно иметь формат `DCS://HOST:PORT/NAMESPACE`. Например, `etcd3://localhost:2379/service` подключается к etcd v3 на `localhost`, где кластер Patroni хранится в пространстве имён `service`. Отсутствующие части заменяются значениями конфигурации или значениями по умолчанию.

`-k` / `--insecure`  
Флаг пропуска проверки сертификата SSL сервера REST API.

Синтаксис запуска команды [patronictl](/ru/patroni/patronictl#patronictl):

```text
patronictl [ { -c | --config-file } CONFIG_FILE ]
  [ { -d | --dcs-url | --dcs } DCS_URL ] 
  [ { -k | --insecure } ]
  SUBCOMMAND
```

> [!NOTE]
> В описании синтаксиса используются следующие правила:
>
> - Параметры в квадратных скобках необязательны;
> - Параметры в фигурных скобках означают выбор одного из набора;
> - Параметры с `[, ... ]` можно указывать несколько раз;
> - Элементы в верхнем регистре — литералы, которым нужно передать значение.
>
> Тот же синтаксис применяется к подкомандам [patronictl](/ru/patroni/patronictl#patronictl) в следующих подразделах. Синтаксис каждой подкоманды следует рассматривать как замену `SUBCOMMAND` в описании выше.

В следующих подразделах описаны все команды [patronictl](/ru/patroni/patronictl#patronictl). В примерах используются файлы конфигурации из репозитория Patroni на GitHub: `postgres0.yml`, `postgres1.yml` и `postgres2.yml`.

<a id="patronictl_demote_cluster"></a>

### patronictl demote-cluster {#patronictl-demote-cluster}

<a id="patronictl_demote_cluster_synopsis"></a>

#### Синтаксис {#synopsis}

```text
demote-cluster
  [ CLUSTER_NAME ]
  [ --host HOST ]
  [ --port PORT ]
  [ --restore-command RESTORE_COMMAND ]
  [ --primary-slot-name PRIMARY_SLOT_NAME ]
  [ --force ]
```

<a id="patronictl_demote_cluster_description"></a>

#### Описание {#description}

`patronictl demote-cluster` преобразует обычный кластер Patroni в [резервный кластер](/ru/patroni/standby_cluster#standby_cluster).

Команда добавляет в динамическую конфигурацию раздел `standby_cluster`, сформированный из параметров подключения к удалённому первичному серверу, а затем ждёт запуска лидера в роли резервного лидера. Перед изменением она выводит текущую топологию кластера и запрашивает подтверждение, если не используется `--force`.

Необходимо указать хотя бы один из параметров `--host`, `--port` или `--restore-command`.

<a id="patronictl_demote_cluster_parameters"></a>

#### Параметры {#parameters}

`CLUSTER_NAME`: имя кластера Patroni.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить его из параметра `scope`, если тот существует.

`--host`: адрес удалённого узла.

`--port`: порт удалённого узла.

`--restore-command`: команда восстановления записей WAL с удалённого первичного сервера.

`--primary-slot-name`: имя слота репликации на удалённом узле, используемого для репликации.

`--force`: флаг пропуска подтверждений при понижении кластера.

Полезно для сценариев.

<a id="patronictl_demote_cluster_examples"></a>

#### Примеры {#examples}

Преобразовать кластер в резервный, следующий за удалённой конечной точкой первичного сервера:

```bash
$ patronictl -c postgres0.yml demote-cluster batman --host 192.0.2.10 --port 5432 --primary-slot-name batman --force
```

<a id="patronictl_dsn"></a>

### patronictl dsn {#patronictl-dsn}

<a id="patronictl_dsn_synopsis"></a>

#### Синтаксис {#synopsis-1}

```text
dsn
  [ CLUSTER_NAME ]
  [ { { -r | --role } { leader | primary | standby-leader | replica | standby | any } | { -m | --member } MEMBER_NAME } ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_dsn_description"></a>

#### Описание {#description-1}

`patronictl dsn` получает строку подключения к одному участнику кластера Patroni.

Если параметрам соответствует несколько участников, выбирается один с приоритетом первичного узла.

<a id="patronictl_dsn_parameters"></a>

#### Параметры {#parameters-1}

`CLUSTER_NAME`: имя кластера Patroni.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить его из параметра `scope`, если тот существует.

`-r` / `--role`  
Выбрать участника с заданной ролью.

Допустимые роли:

- `leader`: лидер обычного или резервного кластера Patroni; либо
- `primary`: лидер обычного кластера Patroni; либо
- `standby-leader`: лидер резервного кластера Patroni; либо
- `replica`: реплика кластера Patroni; либо
- `standby`: то же, что `replica`; либо
- `any`: любая роль. Эквивалентно отсутствию параметра; либо

`-m` / `--member`  
Выбрать участника кластера с заданным именем.

`MEMBER_NAME` — имя участника.

`--group`  
Выбрать участника заданной группы Citus.

`CITUS_GROUP` — идентификатор группы Citus.

<a id="patronictl_dsn_examples"></a>

#### Примеры {#examples-1}

Получить DSN первичного узла:

``` bash
$ patronictl -c postgres0.yml dsn batman -r primary
host=127.0.0.1 port=5432
```

Получить DSN узла `postgresql1`:

``` bash
$ patronictl -c postgres0.yml dsn batman --member postgresql1
host=127.0.0.1 port=5433
```

<a id="patronictl_edit_config"></a>

### patronictl edit-config {#patronictl-edit-config}

<a id="patronictl_edit_config_synopsis"></a>

#### Синтаксис {#synopsis-2}

```text
edit-config
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { -q | --quiet } ]
  [ { -s | --set } CONFIG="VALUE" [, ... ] ]
  [ { -p | --pg } PG_CONFIG="PG_VALUE" [, ... ] ]
  [ { --apply | --replace } CONFIG_FILE ]
  [ --force ]
```

<a id="patronictl_edit_config_description"></a>

#### Описание {#description-2}

`patronictl edit-config` изменяет динамическую конфигурацию кластера и обновляет DCS.

> [!NOTE]
> При вызове из TTY команда пытается показать различия динамической конфигурации через средство постраничного просмотра. По умолчанию используется `less` или `more`. Для другого средства задайте переменной окружения `PAGER` нужное значение.

<a id="patronictl_edit_config_parameters"></a>

#### Параметры {#parameters-2}

`CLUSTER_NAME`: имя кластера Patroni.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить его из параметра `scope`, если тот существует.

`--group`  
Изменить динамическую конфигурацию заданной группы Citus.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить значение из `citus.group`, если оно существует.

`CITUS_GROUP` — идентификатор группы Citus.

`-q` / `--quiet`  
Флаг пропуска показа различий конфигурации.

`-s` / `--set`  
Задать указанному параметру динамической конфигурации указанное значение.

`CONFIG` — путь динамической конфигурации в дереве YAML, уровни которого соединены `.`.

`VALUE` — значение `CONFIG`. Если оно равно `null`, `CONFIG` удаляется из динамической конфигурации.

`-p` / `--pg`  
Задать указанному динамическому параметру Postgres указанное значение.

Это сокращение для `-s` / `--set`, где к `CONFIG` добавляется префикс `postgresql.parameters.`.

`PG_CONFIG` — имя задаваемого параметра Postgres.

`PG_VALUE` — значение `PG_CONFIG`. Если оно равно `null`, `PG_CONFIG` удаляется из динамической конфигурации.

`--apply`  
Применить динамическую конфигурацию из заданного файла.

Аналогично нескольким параметрам `-s` / `--set`, по одному для каждого параметра из `CONFIG_FILE`.

`CONFIG_FILE` — путь к файлу применяемой динамической конфигурации в формате YAML. Для чтения из `stdin` используйте `-`.

`--replace`  
Заменить динамическую конфигурацию в DCS конфигурацией из заданного файла.

`CONFIG_FILE` — путь к файлу новой динамической конфигурации в формате YAML. Для чтения из `stdin` используйте `-`.

`--force`  
Флаг пропуска подтверждений при изменении динамической конфигурации.

Полезно для сценариев.

<a id="patronictl_edit_config_examples"></a>

#### Примеры {#examples-2}

Изменить GUC Postgres `max_connections`:

``` diff
patronictl -c postgres0.yml edit-config batman --pg max_connections="150" --force
---
+++
@@ -1,6 +1,8 @@
loop_wait: 10
maximum_lag_on_failover: 1048576
postgresql:
+  parameters:
+    max_connections: 150
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host all all 0.0.0.0/0 md5

Configuration changed
```

Изменить параметры `loop_wait` и `ttl`:

``` diff
patronictl -c postgres0.yml edit-config batman --set loop_wait="15" --set ttl="45" --force
---
+++
@@ -1,4 +1,4 @@
-loop_wait: 10
+loop_wait: 15
maximum_lag_on_failover: 1048576
postgresql:
  pg_hba:
@@ -6,4 +6,4 @@
  - host all all 0.0.0.0/0 md5
  use_pg_rewind: true
retry_timeout: 10
-ttl: 30
+ttl: 45

Configuration changed
```

Удалить `maximum_lag_on_failover` из динамической конфигурации:

``` diff
patronictl -c postgres0.yml edit-config batman --set maximum_lag_on_failover="null" --force
---
+++
@@ -1,5 +1,4 @@
loop_wait: 10
-maximum_lag_on_failover: 1048576
postgresql:
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5

Configuration changed
```

<a id="patronictl_failover"></a>

### patronictl failover {#patronictl-failover}

<a id="patronictl_failover_synopsis"></a>

#### Синтаксис {#synopsis-3}

```text
failover
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  --candidate CANDIDATE_NAME
  [ --force ]
```

<a id="patronictl_failover_description"></a>

#### Описание {#description-3}

`patronictl failover` выполняет ручное аварийное переключение в кластере.

Команда предназначена для неисправного кластера, например когда:

- отсутствует лидер; либо
- в синхронном кластере нет доступного синхронного резервного сервера.

При включённом синхронном режиме она также позволяет переключиться на асинхронный узел.

> [!NOTE]
> `patronictl failover` можно запустить и в исправном кластере, однако в таком случае рекомендуется `patronictl switchover`.

> [!WARNING]
> Аварийное переключение может привести к потере данных в зависимости от отставания повышаемой реплики от первичного сервера.

<a id="patronictl_failover_parameters"></a>

#### Параметры {#parameters-3}

`CLUSTER_NAME`: имя кластера Patroni.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить его из параметра `scope`, если тот существует.

`--group`  
Выполнить аварийное переключение в заданной группе Citus.

`CITUS_GROUP` — идентификатор группы Citus.

`--candidate`  
Узел, повышаемый при аварийном переключении.

`CANDIDATE_NAME` — имя повышаемого узла.

`--force`  
Флаг пропуска подтверждений при аварийном переключении.

Полезно для сценариев.

<a id="patronictl_failover_examples"></a>

#### Примеры {#examples-3}

Выполнить аварийное переключение на узел `postgresql2`:

``` bash
$ patronictl -c postgres0.yml failover batman --candidate postgresql2 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  3 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  3 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  3 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-12 11:52:27.50978 Successfully failed over to "postgresql2"
+ Cluster: batman (7277694203142172922) -+---------+----+-------------+---------+------------+---------+
| Member      | Host           | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
| postgresql0 | 127.0.0.1:5432 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
| postgresql1 | 127.0.0.1:5433 | Replica | running |  3 |   0/4000188 |       0 |  0/4000188 |       0 |
| postgresql2 | 127.0.0.1:5434 | Leader  | running |  3 |             |         |            |         |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
```

<a id="patronictl_flush"></a>

### patronictl flush {#patronictl-flush}

<a id="patronictl_flush_synopsis"></a>

#### Синтаксис {#synopsis-4}

```text
flush
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  { restart | switchover }
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --force ]
```

<a id="patronictl_flush_description"></a>

#### Описание {#description-4}

`patronictl flush` удаляет запланированные события, если они есть.

<a id="patronictl_flush_parameters"></a>

#### Параметры {#parameters-4}

`CLUSTER_NAME`  
Имя кластера Patroni.

`MEMBER_NAME`  
Удалить запланированные события заданных участников Patroni.

Можно указать несколько участников. Если участники не заданы, рассматриваются все.

> [!NOTE]
> Используется только при удалении запланированных перезапусков.

`restart`  
Удалить запланированные перезапуски.

`switchover`  
Удалить запланированное плановое переключение.

`--group`  
Удалить запланированные события заданной группы Citus.

`CITUS_GROUP` — идентификатор группы Citus.

`-r` / `--role`  
Удалить запланированные события участников с заданной ролью.

Допустимые роли:

- `leader`: лидер обычного или резервного кластера Patroni; либо
- `primary`: лидер обычного кластера Patroni; либо
- `standby-leader`: лидер резервного кластера Patroni; либо
- `replica`: реплика кластера Patroni; либо
- `standby`: то же, что `replica`; либо
- `any`: любая роль. Эквивалентно отсутствию параметра.

> [!NOTE]
> Используется только при удалении запланированных перезапусков.

`--force`  
Флаг пропуска подтверждений при удалении событий.

Полезно для сценариев.

<a id="patronictl_flush_examples"></a>

#### Примеры {#examples-4}

Удалить запланированное плановое переключение:

``` bash
$ patronictl -c postgres0.yml flush batman switchover --force
Success: scheduled switchover deleted
```

Удалить запланированный перезапуск всех резервных узлов:

``` bash
$ patronictl -c postgres0.yml flush batman restart -r replica --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+---------------------------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Scheduled restart         |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     | 2025-03-23T18:00:00-03:00 |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
Success: flush scheduled restart for member postgresql1
Success: flush scheduled restart for member postgresql2
```

Удалить запланированный перезапуск узлов `postgresql0` и `postgresql1`:

``` bash
$ patronictl -c postgres0.yml flush batman postgresql0 postgresql1 restart --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+---------------------------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Scheduled restart         |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     | 2025-03-23T18:00:00-03:00 |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
Success: flush scheduled restart for member postgresql0
Success: flush scheduled restart for member postgresql1
```

<a id="patronictl_history"></a>

### patronictl history {#patronictl-history}

<a id="patronictl_history_synopsis"></a>

#### Синтаксис {#synopsis-5}

```text
history
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
```

<a id="patronictl_history_description"></a>

#### Описание {#description-5}

`patronictl history` показывает историю аварийных и плановых переключений кластера, если они были.

Вывод содержит следующие сведения:

`TL`  
Временная шкала Postgres, на которой произошло событие.

`LSN`  
LSN Postgres, на котором произошло событие.

`Reason`  
Причина из файла Postgres `.history`.

`Timestamp`  
Время события.

`New Leader`  
Участник Patroni, повышенный во время события.

<a id="patronictl_history_parameters"></a>

#### Параметры {#parameters-5}

`CLUSTER_NAME`  
Имя кластера Patroni.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить его из параметра `scope`, если тот существует.

`--group`  
Показать историю событий заданной группы Citus.

`CITUS_GROUP` — идентификатор группы Citus.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить значение из `citus.group`, если оно существует.

`-f` / `--format`  
Способ форматирования списка событий в выводе.

Допустимые форматы:

- `pretty`: выводит историю как форматированную таблицу; либо
- `tsv`: выводит табличные сведения со столбцами, разделёнными `\t`; либо
- `json`: выводит историю в формате JSON; либо
- `yaml`: выводит историю в формате YAML.

По умолчанию используется `pretty`.

<a id="patronictl_history_examples"></a>

#### Примеры {#examples-5}

Показать историю событий:

``` bash
$ patronictl -c postgres0.yml history batman
+----+----------+------------------------------+----------------------------------+-------------+
| TL |      LSN | Reason                       | Timestamp                        | New Leader  |
+----+----------+------------------------------+----------------------------------+-------------+
|  1 | 24392648 | no recovery target specified | 2023-09-11T22:11:27.125527+00:00 | postgresql0 |
|  2 | 50331864 | no recovery target specified | 2023-09-12T11:34:03.148097+00:00 | postgresql0 |
|  3 | 83886704 | no recovery target specified | 2023-09-12T11:52:26.948134+00:00 | postgresql2 |
|  4 | 83887280 | no recovery target specified | 2023-09-12T11:53:09.620136+00:00 | postgresql0 |
+----+----------+------------------------------+----------------------------------+-------------+
```

Показать историю событий в формате YAML:

``` bash
$ patronictl -c postgres0.yml history batman -f yaml
- LSN: 24392648
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 1
  Timestamp: '2023-09-11T22:11:27.125527+00:00'
- LSN: 50331864
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 2
  Timestamp: '2023-09-12T11:34:03.148097+00:00'
- LSN: 83886704
  New Leader: postgresql2
  Reason: no recovery target specified
  TL: 3
  Timestamp: '2023-09-12T11:52:26.948134+00:00'
- LSN: 83887280
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 4
  Timestamp: '2023-09-12T11:53:09.620136+00:00'
```

<a id="patronictl_list"></a>

### patronictl list {#patronictl-list}

<a id="patronictl_list_synopsis"></a>

#### Синтаксис {#synopsis-6}

```text
list
  [ CLUSTER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -e | --extended } ]
  [ { -t | --timestamp } ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_list_description"></a>

#### Описание {#description-6}

`patronictl list` показывает сведения о кластере Patroni и его участниках.

Вывод содержит следующие сведения:

`Cluster`  
Имя кластера Patroni.

`Member`  
Имя участника Patroni.

`Host`  
Узел, на котором находится участник.

`Role`  
Текущая роль участника.

Возможные значения:

- `Leader`: текущий лидер обычного кластера Patroni; либо
- `Standby Leader`: текущий лидер резервного кластера Patroni; либо
- `Sync Standby`: синхронный резервный сервер кластера Patroni с включённым синхронным режимом; либо
- `Replica`: обычный резервный сервер кластера Patroni.

`State`  
Текущее состояние Postgres на участнике Patroni.

Примеры возможных состояний:

- `running`: Postgres запущен и работает;
- `streaming`: участник является репликой, и Postgres получает WAL по потоковой репликации от первичного узла;
- `in archive recovery`: участник является репликой, и Postgres получает WAL из архива;
- `stopped`: Postgres остановлен;
- `crashed`: Postgres аварийно завершился.

`TL`  
Текущая временная шкала Postgres на участнике Patroni.

`Receive LSN`  
Последняя позиция журнала предзаписи, полученная потоковой репликацией участника и синхронизированная с диском (`pg_catalog.pg_last_(xlog|wal)_receive_(location|lsn)()`).

`Receive Lag`  
Отставание репликации между позицией участника `Receive LSN` и вышестоящим узлом в MB.

`Replay LSN`  
Последняя позиция журнала предзаписи, воспроизведённая при восстановлении участника (`pg_catalog.pg_last_(xlog|wal)_replay_(location|lsn)()`).

`Replay Lag`  
Отставание репликации между позицией участника `Replay LSN` и вышестоящим узлом в MB.

Кроме того, вывод может содержать:

`System identifier`  
Системный идентификатор Postgres.

> [!NOTE]
> Показывается в заголовке таблицы.
>
> Только для формата вывода `pretty`.

`Group`  
Идентификатор группы Citus.

> [!NOTE]
> Показывается в заголовке таблицы.
>
> Только для кластера Citus.

`Pending restart`  
`*` означает, что для применения конфигурации Postgres узлу требуется перезапуск. Пустое значение означает, что перезапуск не требуется.

> [!NOTE]
> Показывается как атрибут участника.
>
> Показывается, если:
>
> - При выводе в формате `pretty` или `tsv` с включённым расширенным выводом; либо
> - Если узлу требуется перезапуск.

`Scheduled restart`  
Время запланированного перезапуска экземпляра Postgres под управлением участника Patroni. Пустое значение означает отсутствие запланированного перезапуска.

> [!NOTE]
> Показывается как атрибут участника.
>
> Показывается, если:
>
> - При выводе в формате `pretty` или `tsv` с включённым расширенным выводом; либо
> - Если у узла есть запланированный перезапуск.

`Tags`  
Содержит теги участника Patroni. Пустое значение означает, что теги не настроены либо имеют значения по умолчанию.

> [!NOTE]
> Показывается как атрибут участника.
>
> Показывается, если:
>
> - При выводе в формате `pretty` или `tsv` с включённым расширенным выводом; либо
> - Если у узла есть пользовательские теги или теги по умолчанию с нестандартными значениями.

`Scheduled switchover`  
Время запланированного планового переключения кластера Patroni, если оно есть.

> [!NOTE]
> Показывается в нижнем колонтитуле таблицы.
>
> Только при наличии запланированного переключения и формате вывода `pretty`.

`Maintenance mode`

> Мониторинг кластера в настоящее время приостановлен.
>
> > [!NOTE]
> > Показывается в нижнем колонтитуле таблицы.
> >
> > Только если кластер на паузе и формат вывода — `pretty`.

<a id="patronictl_list_parameters"></a>

#### Параметры {#parameters-6}

`CLUSTER_NAME`  
Имя кластера Patroni.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить его из параметра `scope`, если тот существует.

`--group`  
Показать сведения об участниках заданной группы Citus.

`CITUS_GROUP` — идентификатор группы Citus.

`-e` / `--extended`  
Показать расширенные сведения.

Принудительно показывать атрибуты `Pending restart`, `Scheduled restart` и `Tags`, даже если их значения пусты.

> [!NOTE]
> Применяется только к форматам вывода `pretty` и `tsv`.

`-t` / `--timestamp`  
Вывести временную метку перед сведениями о кластере и участниках.

`-f` / `--format`  
Способ форматирования списка участников кластера в выводе.

Допустимые форматы:

- `pretty`: выводит участников кластера как форматированную таблицу; либо
- `tsv`: выводит табличные сведения со столбцами, разделёнными `\t`; либо
- `json`: выводит участников кластера в формате JSON; либо
- `yaml`: выводит участников кластера в формате YAML.

По умолчанию используется `pretty`.

`-W`  
Автоматически обновлять сведения каждые 2 секунды.

`-w` / `--watch`  
Автоматически обновлять сведения с заданным интервалом.

`TIME` — интервал между обновлениями в секундах.

<a id="patronictl_list_examples"></a>

#### Примеры {#examples-6}

Показать сведения о кластере в формате pretty:

``` bash
$ patronictl -c postgres0.yml list batman
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
```

Показать сведения о кластере в формате pretty с расширенными столбцами:

``` bash
$ patronictl -c postgres0.yml list batman -e
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Pending restart | Pending restart reason | Scheduled restart | Tags |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |                 |                        |                   |      |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |                 |                        |                   |      |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |                 |                        |                   |      |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
```

Показать сведения о кластере в формате YAML с временной меткой выполнения:

``` bash
$ patronictl -c postgres0.yml list batman -f yaml -t
2023-09-12 13:30:48
- Cluster: batman
  Host: 127.0.0.1:5432
  Member: postgresql0
  Role: Leader
  State: running
  TL: 5
- Cluster: batman
  Host: 127.0.0.1:5433
  Receive LSN: 0/40004E8
  Receive Lag: 0
  Replay LSN: 0/40004E8
  Replay Lag: 0
  Member: postgresql1
  Role: Replica
  State: streaming
  TL: 5
- Cluster: batman
  Host: 127.0.0.1:5434
  Receive LSN: 0/40004E8
  Receive Lag: 0
  Replay LSN: 0/40004E8
  Replay Lag: 0
  Member: postgresql2
  Role: Replica
  State: streaming
  TL: 5
```

<a id="patronictl_pause"></a>

### patronictl pause {#patronictl-pause}

<a id="patronictl_pause_synopsis"></a>

#### Синтаксис {#synopsis-7}

```text
pause
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ --wait ]
```

<a id="patronictl_pause_description"></a>

#### Описание {#description-7}

`patronictl pause` временно переводит кластер Patroni в режим обслуживания и отключает автоматическое переключение при отказе.

<a id="patronictl_pause_parameters"></a>

#### Параметры {#parameters-7}

`CLUSTER_NAME`  
Имя кластера Patroni.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить его из параметра `scope`, если тот существует.

`--group`  
Приостановить заданную группу Citus.

`CITUS_GROUP` — идентификатор группы Citus.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить значение из `citus.group`, если оно существует.

`--wait`  
Перед возвратом управления вызывающей стороне дождаться паузы всех участников Patroni.

<a id="patronictl_pause_examples"></a>

#### Примеры {#examples-7}

Перевести кластер в режим обслуживания и дождаться паузы всех узлов:

``` bash
$ patronictl -c postgres0.yml pause batman --wait
'pause' request sent, waiting until it is recognized by all nodes
Success: cluster management is paused
```

<a id="patronictl_promote_cluster"></a>

### patronictl promote-cluster {#patronictl-promote-cluster}

<a id="patronictl_promote_cluster_synopsis"></a>

#### Синтаксис {#synopsis-8}

```text
promote-cluster
  [ CLUSTER_NAME ]
  [ --force ]
```

<a id="patronictl_promote_cluster_description"></a>

#### Описание {#description-8}

`patronictl promote-cluster` преобразует резервный кластер в обычный кластер Patroni.

Команда удаляет раздел `standby_cluster` из динамической конфигурации и ждёт запуска лидера в роли первичного сервера. Перед изменением она выводит текущую топологию кластера и запрашивает подтверждение, если не используется `--force`.

<a id="patronictl_promote_cluster_parameters"></a>

#### Параметры {#parameters-8}

`CLUSTER_NAME`: имя кластера Patroni.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить его из параметра `scope`, если тот существует.

`--force`: флаг пропуска подтверждений при повышении кластера.

Полезно для сценариев.

<a id="patronictl_promote_cluster_examples"></a>

#### Примеры {#examples-8}

Повысить резервный кластер до обычного кластера Patroni:

```bash
$ patronictl -c postgres0.yml promote-cluster batman --force
```

<a id="patronictl_query"></a>

### patronictl query {#patronictl-query}

<a id="patronictl_query_synopsis"></a>

#### Синтаксис {#synopsis-9}

```text
query
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { { -r | --role } { leader | primary | standby-leader | replica | standby | any } | { -m | --member } MEMBER_NAME } ]
  [ { -d | --dbname } DBNAME ]
  [ { -U | --username } USERNAME ]
  [ --password ]
  [ --format { pretty | tsv | json | yaml } ]
  [ { { -f | --file } FILE_NAME | { -c | --command } SQL_COMMAND } ]
  [ --delimiter ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_query_description"></a>

#### Описание {#description-9}

`patronictl query` выполняет команду или сценарий SQL на участнике кластера Patroni.

<a id="patronictl_query_parameters"></a>

#### Параметры {#parameters-9}

`CLUSTER_NAME`  
Имя кластера Patroni.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить его из параметра `scope`, если тот существует.

`--group`  
Выполнить запрос к заданной группе Citus.

`CITUS_GROUP` — идентификатор группы Citus.

`-r` / `--role`  
Выбрать участника с заданной ролью.

Допустимые роли:

- `leader`: лидер обычного или резервного кластера Patroni; либо
- `primary`: лидер обычного кластера Patroni; либо
- `standby-leader`: лидер резервного кластера Patroni; либо
- `replica`: реплика кластера Patroni; либо
- `standby`: то же, что `replica`; либо
- `any`: любая роль. Эквивалентно отсутствию параметра.

`-m` / `--member`  
Выбрать участника с заданным именем.

`MEMBER_NAME` — имя выбираемого участника.

`-d` / `--dbname`  
База данных для подключения и выполнения запроса.

`DBNAME` — имя базы данных. Если не задано, по умолчанию используется `USERNAME`.

`-U` / `--username`  
Пользователь для подключения к базе данных.

`USERNAME` — имя пользователя. Если не задано, по умолчанию используется пользователь операционной системы, запустивший `patronictl query`.

`--password`  
Запросить пароль подключающегося пользователя.

Поскольку Patroni использует `libpq`, вместо этого можно создать файл `~/.pgpass` или задать переменную окружения `PGPASSWORD`.

`--format`  
Способ форматирования вывода запроса.

Допустимые форматы:

- `pretty`: выводит результат как форматированную таблицу; либо
- `tsv`: выводит табличные сведения со столбцами, разделёнными `\t`; либо
- `json`: выводит результат в формате JSON; либо
- `yaml`: выводит результат в формате YAML.

По умолчанию используется `tsv`.

`-f` / `--file`  
Использовать файл как источник команд запросов.

`FILE_NAME` — путь к исходному файлу.

`-c` / `--command`  
Выполнить заданную команду SQL.

`SQL_COMMAND` — выполняемая команда SQL.

`--delimiter`  
Разделитель при выводе в формате `tsv`; если не задан, используется `\t`.

`-W`  
Автоматически повторять запрос каждые 2 секунды.

`-w` / `--watch`  
Автоматически повторять запрос с заданным интервалом.

`TIME` — интервал между повторами в секундах.

<a id="patronictl_query_examples"></a>

#### Примеры {#examples-9}

Выполнить команду SQL от пользователя `postgres` с запросом пароля:

``` bash
$ patronictl -c postgres0.yml query batman -U postgres --password -c "SELECT now()"
Password:
now
2023-09-12 18:10:53.228084+00:00
```

Выполнить команду SQL от пользователя `postgres`, получив пароль из переменной окружения `libpq`:

``` bash
$ PGPASSWORD=patroni patronictl -c postgres0.yml query batman -U postgres -c "SELECT now()"
now
2023-09-12 18:11:37.639500+00:00
```

Выполнять команду SQL каждые 2 секунды и выводить результат в формате `pretty`:

``` bash
$ patronictl -c postgres0.yml query batman -c "SELECT now()" --format pretty -W
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:16.716235+00:00 |
+----------------------------------+
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:18.732645+00:00 |
+----------------------------------+
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:20.750573+00:00 |
+----------------------------------+
```

Выполнить команду SQL в базе `test` и вывести результат в формате YAML:

``` bash
$ patronictl -c postgres0.yml query batman -d test -c "SELECT now() AS column_1, 'test' AS column_2" --format yaml
- column_1: 2023-09-12 18:14:22.052060+00:00
  column_2: test
```

Выполнить команду SQL на участнике `postgresql2`:

``` bash
$ patronictl -c postgres0.yml query batman -m postgresql2 -c "SHOW port"
port
5434
```

Выполнить команду SQL на любом резервном сервере:

``` bash
$ patronictl -c postgres0.yml query batman -r replica -c "SHOW port"
port
5433
```

<a id="patronictl_reinit"></a>

### patronictl reinit {#patronictl-reinit}

<a id="patronictl_reinit_synopsis"></a>

#### Синтаксис {#synopsis-10}

```text
reinit
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ --wait ]
  [ --force ]
  [ --from-leader ]
```

<a id="patronictl_reinit_description"></a>

#### Описание {#description-10}

`patronictl reinit` перестраивает резервный экземпляр Postgres под управлением участника-реплики кластера Patroni.

<a id="patronictl_reinit_parameters"></a>

#### Параметры {#parameters-10}

`CLUSTER_NAME`  
Имя кластера Patroni.

`MEMBER_NAME`  
Имя участника-реплики, экземпляр Postgres которого будет перестроен.

Можно указать несколько участников-реплик. Если участники не заданы, команда ничего не делает.

`--group`  
Перестроить участника-реплику заданной группы Citus.

`CITUS_GROUP` — идентификатор группы Citus.

`--wait`  
Дождаться завершения повторной инициализации резервных узлов Postgres.

`--force`  
Флаг пропуска подтверждений при перестроении резервных экземпляров Postgres.

Полезно для сценариев.

`--from-leader`  
Флаг получения basebackup непосредственно с лидера.

<a id="patronictl_reinit_examples"></a>

#### Примеры {#examples-10}

Запросить перестроение всех участников-реплик кластера Patroni и немедленно вернуть управление вызывающей стороне:

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql1 postgresql2 --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql1
Success: reinitialize for member postgresql2
```

Запросить перестроение `postgresql2` и дождаться завершения:

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql2 --wait --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql2
Waiting for reinitialize to complete on: postgresql2
Reinitialize is completed on: postgresql2
```

Запросить перестроение `postgresql2` с получением basebackup непосредственно с лидера:

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql2 --from-leader
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql2
```

<a id="patronictl_reload"></a>

### patronictl reload {#patronictl-reload}

<a id="patronictl_reload_synopsis"></a>

#### Синтаксис {#synopsis-11}

```text
reload
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --force ]
```

<a id="patronictl_reload_description"></a>

#### Описание {#description-11}

`patronictl reload` запрашивает перезагрузку локальной конфигурации одного или нескольких участников Patroni.

Она также запускает `pg_ctl reload` на управляемом экземпляре Postgres, даже если ничего не изменилось.

<a id="patronictl_reload_parameters"></a>

#### Параметры {#parameters-11}

`CLUSTER_NAME`  
Имя кластера Patroni.

`MEMBER_NAME`  
Запросить перезагрузку локальной конфигурации заданных участников Patroni.

Можно указать несколько участников. Если участники не заданы, рассматриваются все.

`--group`  
Запросить перезагрузку участников заданной группы Citus.

`CITUS_GROUP` — идентификатор группы Citus.

`-r` / `--role`  
Выбрать участников с заданной ролью.

Допустимые роли:

- `leader`: лидер обычного или резервного кластера Patroni; либо
- `primary`: лидер обычного кластера Patroni; либо
- `standby-leader`: лидер резервного кластера Patroni; либо
- `replica`: реплика кластера Patroni; либо
- `standby`: то же, что `replica`; либо
- `any`: любая роль. Эквивалентно отсутствию параметра.

`--force`  
Флаг пропуска подтверждений при запросе перезагрузки локальной конфигурации.

Полезно для сценариев.

<a id="patronictl_reload_examples"></a>

#### Примеры {#examples-11}

Запросить перезагрузку локальной конфигурации всех участников кластера Patroni:

``` bash
$ patronictl -c postgres0.yml reload batman --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Reload request received for member postgresql0 and will be processed within 10 seconds
Reload request received for member postgresql1 and will be processed within 10 seconds
Reload request received for member postgresql2 and will be processed within 10 seconds
```

<a id="patronictl_remove"></a>

### patronictl remove {#patronictl-remove}

<a id="patronictl_remove_synopsis"></a>

#### Синтаксис {#synopsis-12}

```text
remove
  CLUSTER_NAME
  [ --group CITUS_GROUP ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
```

<a id="patronictl_remove_description"></a>

#### Описание {#description-12}

`patronictl remove` удаляет сведения о кластере из DCS.

Это интерактивное действие.

> [!WARNING]
> Операция уничтожает сведения о кластере Patroni в DCS.

<a id="patronictl_remove_parameters"></a>

#### Параметры {#parameters-12}

`CLUSTER_NAME`  
Имя кластера Patroni.

`--group`  
Удалить сведения о кластере Patroni, относящиеся к заданной группе Citus.

`CITUS_GROUP` — идентификатор группы Citus.

`-f` / `--format`  
Способ форматирования списка участников в выводе при запросе подтверждения.

Допустимые форматы:

- `pretty`: выводит участников как форматированную таблицу; либо
- `tsv`: выводит участников как табличные сведения со столбцами, разделёнными `\t`; либо
- `json`: выводит участников в формате JSON; либо
- `yaml`: выводит участников в формате YAML.

По умолчанию используется `pretty`.

<a id="patronictl_remove_examples"></a>

#### Примеры {#examples-12}

Удалить сведения о кластере Patroni `batman` из DCS:

``` bash
$ patronictl -c postgres0.yml remove batman
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Please confirm the cluster name to remove: batman
You are about to remove all information in DCS for batman, please type: "Yes I am aware": Yes I am aware
This cluster currently is healthy. Please specify the leader name to continue: postgresql0
```

<a id="patronictl_restart"></a>

### patronictl restart {#patronictl-restart}

<a id="patronictl_restart_synopsis"></a>

#### Синтаксис {#synopsis-13}

```text
restart
  CLUSTER_NAME
  [ MEMBER_NAME [, ...] ]
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --any ]
  [ --pg-version PG_VERSION ]
  [ --pending ]
  [ --timeout TIMEOUT ]
  [ --scheduled TIMESTAMP ]
  [ --force ]
```

<a id="patronictl_restart_description"></a>

#### Описание {#description-13}

`patronictl restart` запрашивает перезапуск экземпляра Postgres под управлением участника кластера Patroni.

Перезапуск можно выполнить немедленно или запланировать.

<a id="patronictl_restart_parameters"></a>

#### Параметры {#parameters-13}

`CLUSTER_NAME`  
Имя кластера Patroni.

`--group`  
Перезапустить кластер Patroni, относящийся к заданной группе Citus.

`CITUS_GROUP` — идентификатор группы Citus.

`-r` / `--role`  
Выбрать участников с заданной ролью.

Допустимые роли:

- `leader`: лидер обычного или резервного кластера Patroni; либо
- `primary`: лидер обычного кластера Patroni; либо
- `standby-leader`: лидер резервного кластера Patroni; либо
- `replica`: реплика кластера Patroni; либо
- `standby`: то же, что `replica`; либо
- `any`: любая роль. Эквивалентно отсутствию параметра.

`--any`  
Перезапустить один случайный узел среди соответствующих фильтрам.

`--pg-version`  
Выбрать только участников, версия управляемого экземпляра Postgres которых старше заданной.

`PG_VERSION` — версия Postgres для сравнения.

`--pending`  
Выбрать только участников с флагом `Pending restart`.

`--timeout`: прервать перезапуск при превышении заданного тайм-аута и выполнить аварийное переключение на реплику, если проблема возникла на первичном сервере.

`TIMEOUT` — количество секунд ожидания до прерывания перезапуска.

`--scheduled`  
Запланировать перезапуск на заданное время.

`TIMESTAMP` — время перезапуска. Укажите его в однозначном формате, желательно с часовым поясом. Для немедленного перезапуска можно использовать литерал `now`.

`--force`  
Флаг пропуска подтверждений при запросе перезапуска.

Полезно для сценариев.

<a id="patronictl_restart_examples"></a>

#### Примеры {#examples-13}

Немедленно перезапустить всех участников кластера:

``` bash
$ patronictl -c postgres0.yml restart batman --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart on member postgresql0
Success: restart on member postgresql1
Success: restart on member postgresql2
```

Немедленно перезапустить случайного участника кластера:

``` bash
$ patronictl -c postgres0.yml restart batman --any --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart on member postgresql1
```

Запланировать перезапуск на `2023-09-13T18:00-03:00`:

``` bash
$ patronictl -c postgres0.yml restart batman --scheduled 2023-09-13T18:00-03:00 --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart scheduled on member postgresql0
Success: restart scheduled on member postgresql1
Success: restart scheduled on member postgresql2
```

<a id="patronictl_resume"></a>

### patronictl resume {#patronictl-resume}

<a id="patronictl_resume_synopsis"></a>

#### Синтаксис {#synopsis-14}

```text
resume
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ --wait ]
```

<a id="patronictl_resume_description"></a>

#### Описание {#description-14}

`patronictl resume` выводит кластер Patroni из режима обслуживания и снова включает автоматическое переключение при отказе.

<a id="patronictl_resume_parameters"></a>

#### Параметры {#parameters-14}

`CLUSTER_NAME`  
Имя кластера Patroni.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить его из параметра `scope`, если тот существует.

`--group`  
Возобновить работу заданной группы Citus.

`CITUS_GROUP` — идентификатор группы Citus.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить значение из `citus.group`, если оно существует.

`--wait`  
Перед возвратом управления вызывающей стороне дождаться снятия паузы со всех участников Patroni.

<a id="patronictl_resume_examples"></a>

#### Примеры {#examples-14}

Вывести кластер из режима обслуживания:

``` bash
$ patronictl -c postgres0.yml resume batman --wait
'resume' request sent, waiting until it is recognized by all nodes
Success: cluster management is resumed
```

<a id="patronictl_show_config"></a>

### patronictl show-config {#patronictl-show-config}

<a id="patronictl_show_config_synopsis"></a>

#### Синтаксис {#synopsis-15}

```text
show-config
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_show_config_description"></a>

#### Описание {#description-15}

`patronictl show-config` показывает динамическую конфигурацию кластера, хранящуюся в DCS.

<a id="patronictl_show_config_parameters"></a>

#### Параметры {#parameters-15}

`CLUSTER_NAME`  
Имя кластера Patroni.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить его из параметра `scope`, если тот существует.

`--group`  
Показать динамическую конфигурацию заданной группы Citus.

`CITUS_GROUP` — идентификатор группы Citus.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить значение из `citus.group`, если оно существует.

<a id="patronictl_show_config_examples"></a>

#### Примеры {#examples-15}

Показать динамическую конфигурацию кластера `batman`:

``` bash
$ patronictl -c postgres0.yml show-config batman
loop_wait: 10
postgresql:
  parameters:
    max_connections: 250
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host all all 0.0.0.0/0 md5
  use_pg_rewind: true
retry_timeout: 10
ttl: 30
```

<a id="patronictl_switchover"></a>

### patronictl switchover {#patronictl-switchover}

<a id="patronictl_switchover_synopsis"></a>

#### Синтаксис {#synopsis-16}

```text
switchover
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { --leader | --primary } LEADER_NAME ]
  --candidate CANDIDATE_NAME
  [ --force ]
```

<a id="patronictl_switchover_description"></a>

#### Описание {#description-16}

`patronictl switchover` выполняет плановое переключение в кластере.

Команда предназначена для исправного кластера, например когда:

- имеется лидер;
- в синхронном кластере доступны синхронные резервные серверы.

> [!NOTE]
> Для неисправного кластера может лучше подойти `patronictl failover`.

<a id="patronictl_switchover_parameters"></a>

#### Параметры {#parameters-16}

`CLUSTER_NAME`  
Имя кластера Patroni.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить его из параметра `scope`, если тот существует.

`--group`  
Выполнить плановое переключение в заданной группе Citus.

`CITUS_GROUP` — идентификатор группы Citus.

`--leader` / `--primary`  
Указать лидера, который будет понижен при переключении.

`LEADER_NAME` следует задавать равным имени текущего лидера кластера.

`--candidate`  
Узел, повышаемый при переключении до роли первичного сервера.

`CANDIDATE_NAME` — имя повышаемого узла.

`--scheduled`  
Запланировать переключение на заданное время.

`TIMESTAMP` — время переключения. Укажите его в однозначном формате, желательно с часовым поясом. Для немедленного переключения можно использовать литерал `now`.

`--force`  
Флаг пропуска подтверждений при плановом переключении.

Полезно для сценариев.

<a id="patronictl_switchover_examples"></a>

#### Примеры {#examples-16}

Выполнить плановое переключение на узел `postgresql2`:

``` bash
$ patronictl -c postgres0.yml switchover batman --leader postgresql0 --candidate postgresql2 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-13 14:15:23.07497 Successfully switched over to "postgresql2"
+ Cluster: batman (7277694203142172922) -+---------+----+-------------+---------+------------+---------+
| Member      | Host           | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
| postgresql0 | 127.0.0.1:5432 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
| postgresql1 | 127.0.0.1:5433 | Replica | running |  6 |   0/4000188 |       0 |  0/4000188 |       0 |
| postgresql2 | 127.0.0.1:5434 | Leader  | running |  6 |             |         |            |         |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
```

Запланировать переключение между `postgresql0` и `postgresql2` на `2023-09-13T18:00:00-03:00`:

``` bash
$ patronictl -c postgres0.yml switchover batman --leader postgresql0 --candidate postgresql2 --scheduled 2023-09-13T18:00-03:00 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-13 14:18:11.20661 Switchover scheduled
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Switchover scheduled at: 2023-09-13T18:00:00-03:00
                    from: postgresql0
                    to: postgresql2
```

<a id="patronictl_topology"></a>

### patronictl topology {#patronictl-topology}

<a id="patronictl_topology_synopsis"></a>

#### Синтаксис {#synopsis-17}

```text
topology
  [ CLUSTER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_topology_description"></a>

#### Описание {#description-17}

`patronictl topology` показывает сведения о кластере Patroni и его участниках в виде дерева.

Вывод содержит следующие сведения:

`Cluster`  
Имя кластера Patroni.

> [!NOTE]
> Показывается в заголовке таблицы.

`System identifier`  
Системный идентификатор Postgres.

> [!NOTE]
> Показывается в заголовке таблицы.

`Member`  
Имя участника Patroni.

> [!NOTE]
> Сведения в столбце показываются как дерево участников по соединениям репликации.

`Host`  
Узел, на котором находится участник.

`Role`  
Текущая роль участника.

Возможные значения:

- `Leader`: текущий лидер обычного кластера Patroni; либо
- `Standby Leader`: текущий лидер резервного кластера Patroni; либо
- `Sync Standby`: синхронный резервный сервер кластера Patroni с включённым синхронным режимом; либо
- `Replica`: обычный резервный сервер кластера Patroni.

`State`  
Текущее состояние Postgres на участнике Patroni.

Примеры возможных состояний:

- `running`: Postgres запущен и работает;
- `streaming`: участник является репликой, и Postgres получает WAL по потоковой репликации от первичного узла;
- `in archive recovery`: участник является репликой, и Postgres получает WAL из архива;
- `stopped`: Postgres остановлен;
- `crashed`: Postgres аварийно завершился.

`TL`  
Текущая временная шкала Postgres на участнике Patroni.

`Receive LSN`  
Последняя позиция журнала предзаписи, полученная потоковой репликацией участника и синхронизированная с диском (`pg_catalog.pg_last_(xlog|wal)_receive_(location|lsn)()`).

`Receive Lag`  
Отставание репликации между позицией участника `Receive LSN` и вышестоящим узлом в MB.

`Replay LSN`  
Последняя позиция журнала предзаписи, воспроизведённая при восстановлении участника (`pg_catalog.pg_last_(xlog|wal)_replay_(location|lsn)()`).

`Replay Lag`  
Отставание репликации между позицией участника `Replay LSN` и вышестоящим узлом в MB.

Кроме того, вывод может содержать:

`Group`  
Идентификатор группы Citus.

> [!NOTE]
> Показывается в заголовке таблицы.
>
> Только для кластера Citus.

`Pending restart`  
`*` означает, что для применения конфигурации Postgres узлу требуется перезапуск. Пустое значение означает, что перезапуск не требуется.

> [!NOTE]
> Показывается как атрибут участника.
>
> Показывается, если узлу требуется перезапуск.

`Scheduled restart`  
Время запланированного перезапуска экземпляра Postgres под управлением участника Patroni. Пустое значение означает отсутствие запланированного перезапуска.

> [!NOTE]
> Показывается как атрибут участника.
>
> Показывается, если у узла есть запланированный перезапуск.

`Tags`  
Содержит теги участника Patroni. Пустое значение означает, что теги не настроены либо имеют значения по умолчанию.

> [!NOTE]
> Показывается как атрибут участника.
>
> Показывается, если у узла есть пользовательские теги или теги по умолчанию с нестандартными значениями.

`Scheduled switchover`  
Время запланированного планового переключения кластера Patroni, если оно есть.

> [!NOTE]
> Показывается в нижнем колонтитуле таблицы.
>
> Показывается только при наличии запланированного переключения.

`Maintenance mode`

> Мониторинг кластера в настоящее время приостановлен.
>
> > [!NOTE]
> > Показывается в нижнем колонтитуле таблицы.
> >
> > Показывается только при паузе кластера.

<a id="patronictl_topology_parameters"></a>

#### Параметры {#parameters-17}

`CLUSTER_NAME`  
Имя кластера Patroni.

Если не задано, [patronictl](/ru/patroni/patronictl#patronictl) попытается получить его из параметра `scope`, если тот существует.

`--group`  
Показать сведения об участниках заданной группы Citus.

`CITUS_GROUP` — идентификатор группы Citus.

`-W`  
Автоматически обновлять сведения каждые 2 секунды.

`-w` / `--watch`  
Автоматически обновлять сведения с заданным интервалом.

`TIME` — интервал между обновлениями в секундах.

<a id="patronictl_topology_examples"></a>

#### Примеры {#examples-17}

Показать топологию кластера `batman`, где `postgresql1` и `postgresql2` реплицируются с `postgresql0`:

``` bash
$ patronictl -c postgres0.yml topology batman
+ Cluster: batman (7277694203142172922) ---+-----------+----+-------------+-----+------------+-----+
| Member        | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+---------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0   | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| + postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| + postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+---------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
```

<a id="patronictl_version"></a>

### patronictl version {#patronictl-version}

<a id="patronictl_version_synopsis"></a>

#### Синтаксис {#synopsis-18}

```text
version
  [ CLUSTER_NAME [, ... ] ]
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_version_description"></a>

#### Описание {#description-18}

`patronictl version` получает версию приложения [patronictl](/ru/patroni/patronictl#patronictl). Кроме того, вывод может содержать версии кластеров Patroni и их участников.

<a id="patronictl_version_parameters"></a>

#### Параметры {#parameters-18}

`CLUSTER_NAME`  
Имя кластера Patroni.

`MEMBER_NAME`  
Имя участника кластера Patroni.

`--group`  
Рассматривать кластер Patroni с заданной группой Citus.

`CITUS_GROUP` — идентификатор группы Citus.

<a id="patronictl_version_examples"></a>

#### Примеры {#examples-18}

Получить только версию [patronictl](/ru/patroni/patronictl#patronictl):

``` bash
$ patronictl -c postgres0.yml version
patronictl version 4.0.0
```

Получить версию [patronictl](/ru/patroni/patronictl#patronictl) и всех участников кластера `batman`:

``` bash
$ patronictl -c postgres0.yml version batman
patronictl version 4.0.0

postgresql0: Patroni 4.0.0 PostgreSQL 16.4
postgresql1: Patroni 4.0.0 PostgreSQL 16.4
postgresql2: Patroni 4.0.0 PostgreSQL 16.4
```

Получить версию [patronictl](/ru/patroni/patronictl#patronictl) и участников `postgresql1` и `postgresql2` кластера `batman`:

``` bash
$ patronictl -c postgres0.yml version batman postgresql1 postgresql2
patronictl version 4.0.0

postgresql1: Patroni 4.0.0 PostgreSQL 16.4
postgresql2: Patroni 4.0.0 PostgreSQL 16.4
```
