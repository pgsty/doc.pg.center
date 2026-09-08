---
title: "Настройки конфигурации среды"
linkTitle: "Конфигурация среды"
weight: 30
icon: fa-solid fa-sliders
description: "Переменные среды для переопределения параметров конфигурации Patroni."
module: [PATRONI]
categories: [Справочник]
aliases: [/patroni/config/env/]
upstream_link: "https://patroni.readthedocs.io/en/latest/ENVIRONMENT.html"
---

<a id="env"></a>
Возможно переопределить некоторые параметры конфигурации, определённые в файле конфигурации Patroni, с помощью переменных среды системы. В данном документе перечислены все переменные среды, обрабатываемые Patroni. Значения, установленные с помощью этих переменных, всегда имеют приоритет перед значениями, заданными в файле конфигурации Patroni.

--------

## Глобальный/Всемирный {#globaluniversal}

- **PATRONI_CONFIGURATION**: конфигурацию Patroni целиком можно задать с помощью переменной среды [PATRONI_CONFIGURATION](/ru/docs/patroni/config#config). В этом случае никакие другие переменные среды не будут учитываться!
- **PATRONI_THREAD_POOL_SIZE**: размер пула потоков, используемый Patroni для выполнения асинхронных задач и обмена данными по REST API с другими участниками во время выбора лидера или проверок в аварийном режиме. Минимальное значение — `5`, значение по умолчанию — `5`.
- **PATRONI_THREAD_STACK_SIZE**: указывает размер стека, используемый для потоков, запускаемых Patroni. Значение должно быть выровнено по `64kB`. Минимальное значение — `64kB`, значение по умолчанию (устанавливается Patroni) — `512kB`.
- **PATRONI_NAME**: имя узла, на котором выполняется текущая инстанция Patroni. Должно быть уникальным для кластера. Значение `__patroni_strict_sync_replica_placeholder__` зарезервировано для внутреннего использования Patroni и не может использоваться в качестве имени узла.
- **PATRONI_NAMESPACE**: путь в хранилище конфигурации, где Patroni будет хранить информацию о кластере. Значение по умолчанию: "/service"
- **PATRONI_SCOPE**: имя кластера
- **PG_MALLOC_ARENA_MAX**: пользовательское значение переменной среды `MALLOC_ARENA_MAX` для процесса `postmaster`. Если не задано, `postmaster` унаследует значение `MALLOC_ARENA_MAX`.

--------

## Журнал {#log}

- **PATRONI_LOG_TYPE**: задаёт формат логов. Может быть либо **plain**, либо **json**. Для использования формата **json** необходимо установить [jsonlogger](/ru/docs/patroni/installation#extras). Значение по умолчанию — **plain**.
- **PATRONI_LOG_LEVEL**: задаёт уровень ведения журнала. Значение по умолчанию — **INFO** (см. [документацию по ведению журнала в Python](https://docs.python.org/3.6/library/logging.html#levels))
- **PATRONI_LOG_TRACEBACK_LEVEL**: задаёт уровень, на котором будут видны трассировки. Значение по умолчанию — **ERROR**. Установите значение **DEBUG**, если хотите видеть трассировки только при включении **PATRONI_LOG_LEVEL=DEBUG**.
- **PATRONI_LOG_FORMAT**: задаёт строку форматирования журнала. Если тип журнала — **plain**, формат журнала должен быть строкой. См. [атрибуты LogRecord](https://docs.python.org/3.6/library/logging.html#logrecord-attributes) для получения списка доступных атрибутов. Если тип журнала — **json**, формат журнала может быть списком, помимо строки. Каждый элемент списка должен соответствовать атрибуту LogRecord. Будьте осторожны: требуется только имя поля, а символы **%(** и **)** опускаются. Если необходимо вывести поле журнала с другим именем ключа, используйте словарь, где ключ словаря — это поле журнала, а значение — имя поля, которое должно быть выведено в журнале. Значение по умолчанию: **%(asctime)s %(levelname)s: %(message)s**
- **PATRONI_LOG_DATEFORMAT**: задаёт строку форматирования даты и времени. (см. документацию [formatTime()](https://docs.python.org/3.6/library/logging.html#logging.Formatter.formatTime))
- **PATRONI_LOG_STATIC_FIELDS**: добавить дополнительные поля в лог. Этот параметр доступен только при установке типа лога в **json**. Пример `PATRONI_LOG_STATIC_FIELDS="{app: patroni}"`
- **PATRONI_LOG_MAX_QUEUE_SIZE**: Patroni использует двухэтапное ведение журнала. Записи журнала записываются в очереди в оперативной памяти, а отдельный поток извлекает их из очереди и записывает в stderr или файл. Максимальный размер внутренней очереди по умолчанию ограничен **1000** записями, что достаточно для хранения журналов за последние 1 час 20 минут.
- **PATRONI_LOG_DIR**: Каталог для записи журналов приложения. Каталог должен существовать и быть доступен для записи пользователем, запускающим Patroni. Если задан этот параметр среды, приложение по умолчанию сохраняет журналы 4 25MB. Значения хранения можно настроить с помощью `PATRONI_LOG_FILE_NUM` и `PATRONI_LOG_FILE_SIZE` (см. ниже).
- **PATRONI_LOG_MODE**: Разрешения для файлов журнала (например, `0644`). Если не указано, разрешения будут установлены на основе текущего значения umask.
- **PATRONI_LOG_FILE_NUM**: Количество журналов приложений, которые необходимо сохранить.
- **PATRONI_LOG_FILE_SIZE**: Размер файла patroni.log (в байтах), при достижении которого происходит смена лог-файла.
- **PATRONI_LOG_LOGGERS**: Переопределение уровня ведения журнала для каждого модуля Python. Пример `PATRONI_LOG_LOGGERS="{patroni.postmaster: WARNING, urllib3: DEBUG}"`
- **PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS**: Если установлено в `true`, последовательные журналы heartbeat, одинаковые по содержанию, не будут выводиться. Значение по умолчанию — `false`.

> [!WARNING]
> Время выполнения цикла высокой доступности может быть очень полезной информацией при диагностике переключений при отказе из-за нехватки ресурсов и подобных проблем. Когда `PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS` установлен в `true`, журналы не будут содержать записи о выполнении цикла высокой доступности (если только не произойдёт смена лидера), и, таким образом, эта потенциально полезная информация станет недоступной в журналах.

--------

## Citus {#citus}

Включает интеграцию Patroni с [Citus](https://docs.citusdata.com). При настройке Patroni будет отвечать за регистрацию узлов-работников Citus на координаторе. Дополнительную информацию о поддержке Citus можно найти [здесь](/ru/docs/patroni/citus#citus).

- **PATRONI_CITUS_GROUP**: идентификатор группы Citus, целое число. Используйте `0` для координатора и `1`, `2` и т.д. для воркеров
- **PATRONI_CITUS_DATABASE**: база данных, в которой должен быть создан расширение [citus](/ru/docs/patroni/citus#citus). Должен быть одинаковым на координаторе и всех воркерах. В настоящее время поддерживается только одна база данных.

--------

## Consul {#consul}

- **PATRONI_CONSUL_HOST**: хост:порт для локального агента Consul.
- **PATRONI_CONSUL_URL**: URL для локального агента Consul в формате: http(s)://host:port
- **PATRONI_CONSUL_PORT**: (необязательно) порт Consul
- **PATRONI_CONSUL_SCHEME**: (необязательно) **http** или **https**, значение по умолчанию — **http**
- **PATRONI_CONSUL_TOKEN**: (необязательно) токен ACL
- **PATRONI_CONSUL_VERIFY**: (необязательно) проверять ли сертификат SSL для запросов HTTPS
- **PATRONI_CONSUL_CACERT**: (необязательно) Сертификат CA. При наличии включает проверку подлинности.
- **PATRONI_CONSUL_CERT**: (необязательно) Файл с клиентским сертификатом
- **PATRONI_CONSUL_KEY**: (необязательно) Файл с ключом клиента. Может быть пустым, если ключ входит в сертификат.
- **PATRONI_CONSUL_DC**: (необязательно) Центр обработки данных для связи. По умолчанию используется центр обработки данных хоста.
- **PATRONI_CONSUL_CONSISTENCY**: (необязательно) выберите режим согласованности Consul. Допустимые значения: `default`, `consistent` или `stale` (подробнее в [справочнике API Consul](https://www.consul.io/api/features/consistency.html/))
- **PATRONI_CONSUL_CHECKS**: (необязательно) список проверок состояния Consul, используемых для сессии. По умолчанию используется пустой список.
- **PATRONI_CONSUL_REGISTER_SERVICE**: (необязательно) указывает, следует ли регистрировать службу с именем, определённым параметром scope, и тегом master, primary, replica или standby-leader в зависимости от роли узла. По умолчанию — **false**
- **PATRONI_CONSUL_SERVICE_TAGS**: (необязательно) дополнительные статические теги, добавляемые к сервису Consul помимо роли (`primary`/`replica`/`standby-leader`). По умолчанию используется пустой список.
- **PATRONI_CONSUL_SERVICE_CHECK_INTERVAL**: (необязательно) как часто выполнять проверку состояния для зарегистрированного URL
- **PATRONI_CONSUL_SERVICE_CHECK_TLS_SERVER_NAME**: (необязательно) переопределить хост SNI при подключении через TLS, см. также справочник проверки агента Consul [ API ](https://www.consul.io/api-docs/agent/check#tlsservername).

--------

## Etcd {#etcd}

- **PATRONI_ETCD_PROXY**: URL прокси для etcd. Если вы подключаетесь к etcd через прокси, используйте этот параметр вместо **PATRONI_ETCD_URL**
- **PATRONI_ETCD_URL**: URL для etcd в формате: http(s)://(username:password@)хост:порт
- **PATRONI_ETCD_HOSTS**: список конечных точек etcd в формате 'хост1:порт1','хост2:порт2', и т.д.
- **PATRONI_ETCD_USE_PROXIES**: Если этот параметр установлен в значение true, Patroni будет считать **hosts** списком прокси-серверов и не будет выполнять обнаружение топологии кластера etcd, а будет использовать фиксированный список **hosts**.
- **PATRONI_ETCD_PROTOCOL**: http или https, если не указано — используется http. Если указан **url** или **proxy** — протокол берётся из них.
- **PATRONI_ETCD_HOST**: хост:порт для конечной точки etcd.
- **PATRONI_ETCD_SRV**: Домен для поиска записи(ей) SRV при автодиагностике кластера. Patroni будет пытаться запросить эти имена служб SRV для указанного домена (в указанном порядке до первого успешного результата): `_etcd-client-ssl`, `_etcd-client`, `_etcd-ssl`, `_etcd`, `_etcd-server-ssl`, `_etcd-server`. Если будут получены записи SRV для `_etcd-server-ssl` или `_etcd-server`, то будет использован протокол peer ETCD для запроса ETCD о доступных участниках. В противном случае будут использованы хосты из записей SRV.
- **PATRONI_ETCD_SRV_SUFFIX**: Настраивает суффикс к имени SRV, который запрашивается при обнаружении. Используйте этот флаг для различия между несколькими кластерами etcd в рамках одного домена. Работает только в сочетании с **PATRONI_ETCD_SRV**. Например, если установлены `PATRONI_ETCD_SRV_SUFFIX=foo` и `PATRONI_ETCD_SRV=example.org`, выполняется следующий запрос DNS SRV:`_etcd-client-ssl-foo._tcp.example.com` (и так далее для каждого возможного имени службы ETCD SRV).
- **PATRONI_ETCD_USERNAME**: имя пользователя для аутентификации в etcd.
- **PATRONI_ETCD_PASSWORD**: пароль для аутентификации в etcd.
- **PATRONI_ETCD_CACERT**: Сертификат CA. При его наличии будет включена проверка.
- **PATRONI_ETCD_CERT**: Файл сертификата клиента.
- **PATRONI_ETCD_KEY**: Файл с ключом клиента. Может быть пустым, если ключ входит в сертификат.

--------

## Etcdv3 {#etcdv3}

Имена переменных окружения для Etcdv3 аналогичны именам для etcd, вам нужно просто использовать `ETCD3` вместо `ETCD` в имени переменной. Пример: `PATRONI_ETCD3_HOST`, `PATRONI_ETCD3_CACERT` и так далее.

> [!WARNING]
> Ключи, созданные с использованием версии протокола 2, недоступны при использовании версии протокола 3, и наоборот, поэтому невозможно переключиться с etcd на Etcdv3 просто путём обновления конфигурации Patroni. Кроме того, Patroni использует gRPC-шлюз (прокси) etcd для взаимодействия с V3 API, что означает, что аутентификация по общему имени TLS невозможна.

--------

## ZooKeeper {#zookeeper}

- **PATRONI_ZOOKEEPER_HOSTS**: Список участников кластера ZooKeeper, разделённый запятыми: "'host1:port1','host2:port2','etc...'". Важно заключать каждый элемент в кавычки!
- **PATRONI_ZOOKEEPER_USE_SSL**: (необязательно) Указывает, используется ли SSL. Значение по умолчанию — `false`. Если установлено в `false`, все параметры, специфичные для SSL, игнорируются.
- **PATRONI_ZOOKEEPER_CACERT**: (необязательно) Сертификат ЦС. При наличии включает проверку подлинности.
- **PATRONI_ZOOKEEPER_CERT**: (необязательно) Файл с клиентским сертификатом.
- **PATRONI_ZOOKEEPER_KEY**: (необязательно) Файл с ключом клиента.
- **PATRONI_ZOOKEEPER_KEY_PASSWORD**: (необязательно) Пароль ключа клиента.
- **PATRONI_ZOOKEEPER_VERIFY**: (необязательно) Проверять сертификат или нет. Значение по умолчанию — `true`.
- **PATRONI_ZOOKEEPER_SET_ACLS**: (необязательно) Если задано, настраивает Kazoo на применение по умолчанию ACL к каждому ZNode, который он создаёт. ACL могут использовать схему `x509` (по умолчанию) или другие поддерживаемые схемы ZooKeeper, такие как `digest`. Они должны указываться как словарь, где ключ — полное имя субъекта (опционально с префиксом схемы), а значение — список разрешений. Разрешения могут быть одним или несколькими из `CREATE`, `READ`, `WRITE`, `DELETE`, `ADMIN`, или `ALL`. Например, `set_acls: {CN=principal1: [CREATE, READ], digest:principal2:+pjROuBuuwNNSujKyH8dGcEnFPQ=: [ALL]}`.
- **PATRONI_ZOOKEEPER_AUTH_DATA**: (необязательно) Учетные данные аутентификации для использования при соединении. Должно быть словарем в формате, где `scheme` — ключ, а `credential` — значение. По умолчанию — пустой словарь.

> [!NOTE]
> Необходимо установить `kazoo>=2.6.0` для поддержки SSL.

--------

## Выставщик {#exhibitor}

- **PATRONI_EXHIBITOR_HOSTS**: начальный список узлов Exhibitor (ZooKeeper) в формате: 'host1,host2,etc...'. Этот список обновляется автоматически при изменении топологии кластера Exhibitor (ZooKeeper).
- **PATRONI_EXHIBITOR_PORT**: Порт выставки.

<a id="kubernetes_environment"></a>

--------

## Kubernetes {#kubernetes}

- **PATRONI_KUBERNETES_BYPASS_API_SERVICE**: (необязательно) При взаимодействии с Kubernetes API Patroni обычно полагается на сервис [kubernetes](/ru/docs/patroni/kubernetes#kubernetes), адрес которого доступен в подах через переменную `KUBERNETES_SERVICE_HOST`. Если установлено значение `PATRONI_KUBERNETES_BYPASS_API_SERVICE`, равное `true`, Patroni будет разрешать список API узлов за сервисом и подключаться к ним напрямую.
- **PATRONI_KUBERNETES_NAMESPACE**: (необязательно) пространство имён Kubernetes, в котором выполняется под Patroni. Значение по умолчанию — `default`.
- **PATRONI_KUBERNETES_LABELS**: Метки в формате `{label1: value1, label2: value2}`. Эти метки будут использоваться для поиска существующих объектов (Pod'ов и либо Endpoints, либо ConfigMaps), связанных с текущим кластером. Также Patroni будет устанавливать их на каждый объект (Endpoint или ConfigMap), который создаёт.
- **PATRONI_KUBERNETES_SCOPE_LABEL**: (необязательно) имя метки, содержащей имя кластера. Значение по умолчанию — `cluster-name`.
- **PATRONI_KUBERNETES_BOOTSTRAP_LABELS**: (необязательно) Метки в формате `{label1: value1, label2: value2}`. Эти метки будут присвоены поду Patroni, когда его состояние будет `initializing new cluster`, `running custom bootstrap script`, `starting after custom bootstrap` или `creating replica`.
- **PATRONI_KUBERNETES_ROLE_LABEL**: (необязательно) имя метки, содержащей роль (`primary`, `replica` или другое пользовательское значение). Patroni установит эту метку в поде, в котором выполняется. Значение по умолчанию — `role`.
- **PATRONI_KUBERNETES_LEADER_LABEL_VALUE**: (необязательно) значение метки пода при роли Postgres `primary`. Значение по умолчанию — `primary`.
- **PATRONI_KUBERNETES_FOLLOWER_LABEL_VALUE**: (необязательно) значение метки пода при роли Postgres `replica`. Значение по умолчанию — `replica`.
- **PATRONI_KUBERNETES_STANDBY_LEADER_LABEL_VALUE**: (необязательно) значение метки пода при роли Postgres `standby_leader`. Значение по умолчанию — `primary`.
- **PATRONI_KUBERNETES_TMP_ROLE_LABEL**: (необязательно) имя временной метки, содержащей роль (`primary` или `replica`). Значение этой метки всегда будет использовать значение по умолчанию, соответствующее роли. Устанавливать только при необходимости.
- **PATRONI_KUBERNETES_USE_ENDPOINTS**: (необязательно) если установлено в true, Patroni будет использовать Endpoints вместо ConfigMaps для проведения выборов лидера и хранения состояния кластера.
- **PATRONI_KUBERNETES_POD_IP**: (необязательно) IP-адрес пода, в котором запущен Patroni. Это значение необходимо, когда включён `PATRONI_KUBERNETES_USE_ENDPOINTS`, и используется для заполнения подмножеств конечной точки лидера при повышении пода PostgreSQL до роли лидера.
- **PATRONI_KUBERNETES_PORTS**: (необязательно) если у объекта Service указано имя порта, то такое же имя должно присутствовать в объекте Endpoint, иначе сервис не будет работать. Например, если ваш сервис определён как `{Kind: Service, spec: {ports: [{name: postgresql, port: 5432, targetPort: 5432}]}}`, необходимо установить `PATRONI_KUBERNETES_PORTS='[{"name": "postgresql", "port": 5432}]'`, и Patroni будет использовать его для обновления подмножеств лидера Endpoint. Этот параметр используется только в том случае, если установлено `PATRONI_KUBERNETES_USE_ENDPOINTS`.
- **PATRONI_KUBERNETES_CACERT**: (необязательно) Указывает файл с CA_BUNDLE файлом сертификатов доверенных ЦС, используемых при проверке сертификатов Kubernetes API SSL. Если не указано, Patroni использует значение, предоставленное секретом ServiceAccount.
- **PATRONI_RETRIABLE_HTTP_CODES**: (необязательно) список кодов состояния HTTP от K8s API, на которых следует повторять попытку. По умолчанию Patroni повторяет попытки при кодах `500`, `503` и `504`, либо если ответ K8s API содержит заголовок `retry-after` HTTP.

--------

## Raft (устаревший) {#raft-deprecated}

- **PATRONI_RAFT_SELF_ADDR**: `ip:port` для прослушивания соединений Raft. `self_addr` должен быть доступен с других узлов кластера. Если не задан, узел не будет участвовать в согласовании.
- **PATRONI_RAFT_BIND_ADDR**: (необязательно) `ip:port` для прослушивания соединений Raft. Если не указано, будет использован `self_addr`.
- **PATRONI_RAFT_PARTNER_ADDRS**: список других узлов Patroni в кластере в формате `"'ip1:port1','ip2:port2'"`. Важно заключать каждый элемент в кавычки!
- **PATRONI_RAFT_DATA_DIR**: каталог для хранения журнала Raft и снимков. Если не указан, используется текущий рабочий каталог.
- **PATRONI_RAFT_PASSWORD**: (необязательно) Шифрование трафика Raft с указанным паролем, требует модуля `cryptography` Python.
- **PATRONI_RAFT_MIN_TIMEOUT**: (необязательно) минимальный тайм-аут выборов в секундах для базовой реализации Raft pysyncobj. Должен быть больше 3 * `PATRONI_RAFT_APPEND_ENTRIES_PERIOD`. Значение по умолчанию: `0.4`.
- **PATRONI_RAFT_MAX_TIMEOUT**: (необязательно) максимальный тайм-аут голосования в секундах для базовой реализации Raft pysyncobj. Должен быть больше, чем `PATRONI_RAFT_MIN_TIMEOUT`. Значение по умолчанию: `1.4`.
- **PATRONI_RAFT_CONNECTION_TIMEOUT**: (необязательно) время в секундах, по истечении которого соединение без полученных данных считается неработоспособным. Должно быть больше или равно `PATRONI_RAFT_MAX_TIMEOUT`. Значение по умолчанию: `3.5`.
- **PATRONI_RAFT_APPEND_ENTRIES_PERIOD**: (необязательно) интервал в секундах для отправки команд heartbeat. Должен быть меньше одной трети `PATRONI_RAFT_MIN_TIMEOUT`. Значение по умолчанию: `0.1`.
- **PATRONI_RAFT_CONNECTION_RETRY_TIME**: (необязательно) интервал в секундах между попытками повторного подключения к оффлайн-узлам. По умолчанию: `5.0`.
- **PATRONI_RAFT_LEADER_FALLBACK_TIMEOUT**: (необязательно) время в секундах, по истечении которого лидер, не получивший ответ от большинства, возвращается в состояние последователя. Должно быть больше, чем `PATRONI_RAFT_APPEND_ENTRIES_PERIOD`. Значение по умолчанию: `30.0`.

> [!NOTE]
> Patroni проверяет эти ограничения при запуске и откажется запускаться, если они нарушены. Эти значения нельзя изменить во время выполнения и требуют перезапуска. Подробности см. в [настройках Raft](/ru/docs/patroni/config/yaml#raft_settings), включая ограничение на высокую задержку.

--------

## PostgreSQL {#postgresql}

- **PATRONI_POSTGRESQL_LISTEN**: IP-адрес + порт, на которых слушает Postgres. Допускается указывать несколько адресов, разделённых запятыми, при условии, что компонент порта указывается после последнего адреса через двоеточие, i.e. `listen: 127.0.0.1,127.0.0.2:5432`. Patroni будет использовать первый адрес из этого списка для установления локальных соединений с узлом PostgreSQL.
- **PATRONI_POSTGRESQL_CONNECT_ADDRESS**: IP-адрес + порт, через которые Postgres доступен из других узлов и приложений.
- **PATRONI_POSTGRESQL_PROXY_ADDRESS**: IP-адрес + порт, через которые доступен пул соединений (e.g. PgBouncer), работающий рядом с Postgres. Значение записывается в ключ участник в DCS как `proxy_url` и может быть полезно для обнаружения сервисов.
- **PATRONI_POSTGRESQL_DATA_DIR**: Расположение каталога данных PostgreSQL, существующего или подлежащего инициализации Patroni.
- **PATRONI_POSTGRESQL_CONFIG_DIR**: Расположение каталога конфигурации PostgreSQL, по умолчанию — каталог данных. Должен быть доступен для записи Patroni.
- **PATRONI_POSTGRESQL_BIN_DIR**: Путь к бинарным файлам PostgreSQL. (pg_ctl, initdb, pg_controldata, pg_basebackup, postgres, pg_isready, pg_rewind) Значение по умолчанию — пустая строка, что означает использование переменной среды PATH для поиска исполняемых файлов.
- **PATRONI_POSTGRESQL_BIN_PG_CTL**: (необязательно) Пользовательское имя для бинарного файла `pg_ctl`.
- **PATRONI_POSTGRESQL_BIN_INITDB**: (необязательно) Пользовательское имя для бинарного файла `initdb`.
- **PATRONI_POSTGRESQL_BIN_PG_CONTROLDATA**: (необязательно) Пользовательское имя для бинарного файла `pg_controldata`.
- **PATRONI_POSTGRESQL_BIN_PG_BASEBACKUP**: (необязательно) Пользовательское имя для бинарного файла `pg_basebackup`.
- **PATRONI_POSTGRESQL_BIN_POSTGRES**: (необязательно) Пользовательское имя для бинарного файла `postgres`.
- **PATRONI_POSTGRESQL_BIN_IS_READY**: (необязательно) Пользовательское имя для бинарного файла `pg_isready`.
- **PATRONI_POSTGRESQL_BIN_PG_REWIND**: (необязательно) Пользовательское имя для бинарного файла `pg_rewind`.
- **PATRONI_POSTGRESQL_PGPASS**: путь к файлу паролей [.pgpass](https://www.postgresql.org/docs/current/static/libpq-pgpass.html). Patroni создаёт этот файл перед выполнением pg_basebackup и при некоторых других обстоятельствах. Расположение должно быть доступно для записи Patroni.
- **PATRONI_REPLICATION_USERNAME**: имя пользователя репликации; пользователь будет создан во время инициализации. Реплики будут использовать этого пользователя для доступа к источнику репликации через потоковую репликацию
- **PATRONI_REPLICATION_PASSWORD**: пароль репликации; пользователь будет создан во время инициализации.
- **PATRONI_REPLICATION_SSLMODE**: (необязательно) отображается на параметр соединения [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), позволяющий клиенту указать тип TLS режима согласования с сервером. Подробнее о том, как работает каждый режим, см. в [документации PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). Значение по умолчанию — `prefer`.
- **PATRONI_REPLICATION_SSLKEY**: (необязательно) отображается на параметр соединения [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), который указывает расположение закрытого ключа, используемого с сертификатом клиента.
- **PATRONI_REPLICATION_SSLPASSWORD**: (необязательно) отображается на параметр соединения [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), который указывает пароль для секретного ключа, указанного в `PATRONI_REPLICATION_SSLKEY`.
- **PATRONI_REPLICATION_SSLCERT**: (необязательно) отображается на параметр соединения [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), который указывает расположение сертификата клиента.
- **PATRONI_REPLICATION_SSLROOTCERT**: (необязательно) отображается на параметр соединения [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), который указывает расположение файла, содержащего один или несколько сертификатов удостоверяющих центров (CA), которые клиент будет использовать для проверки сертификата сервера.
- **PATRONI_REPLICATION_SSLCRL**: (необязательно) отображается на параметр соединения [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), указывающий путь к файлу, содержащему список отозванных сертификатов. Клиент откажет в подключении к любому серверу, сертификат которого находится в этом списке.
- **PATRONI_REPLICATION_SSLCRLDIR**: (необязательно) отображается на параметр соединения [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), указывающий путь к каталогу, содержащему файлы со списками отозванных сертификатов. Клиент откажет в подключении к любому серверу, сертификат которого находится в этом списке.
- **PATRONI_REPLICATION_SSLNEGOTIATION**: (необязательно) отображается на параметр соединения [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), управляющий процессом согласования SSL шифрования с сервером, если используется SSL.
- **PATRONI_REPLICATION_GSSENCMODE**: (необязательно) отображается на параметр соединения [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), определяющий, будет ли устанавливаться защищённое соединение GSS TCP/IP с сервером, и с какой приоритетностью
- **PATRONI_REPLICATION_CHANNEL_BINDING**: (необязательно) отображается на параметр соединения [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), управляющий использованием клиентом привязки канала.
- **PATRONI_SUPERUSER_USERNAME**: имя суперпользователя, задаётся во время инициализации (initdb) и затем используется Patroni для подключения к postgres. Также этот пользователь используется pg_rewind.
- **PATRONI_SUPERUSER_PASSWORD**: пароль суперпользователя, устанавливаемый при инициализации (initdb).
- **PATRONI_SUPERUSER_SSLMODE**: (необязательно) отображается на параметр соединения [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), позволяющий клиенту указать тип TLS режима согласования с сервером. Подробнее о том, как работает каждый режим, см. в [документации PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). Значение по умолчанию — `prefer`.
- **PATRONI_SUPERUSER_SSLKEY**: (необязательно) отображается на параметр соединения [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), который указывает расположение закрытого ключа, используемого вместе с сертификатом клиента.
- **PATRONI_SUPERUSER_SSLPASSWORD**: (необязательно) отображается на параметр соединения [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), который указывает пароль для секретного ключа, указанного в `PATRONI_SUPERUSER_SSLKEY`.
- **PATRONI_SUPERUSER_SSLCERT**: (необязательно) отображается на параметр соединения [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), который указывает расположение сертификата клиента.
- **PATRONI_SUPERUSER_SSLROOTCERT**: (необязательно) отображается на параметр соединения [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), который указывает путь к файлу, содержащему один или несколько сертификатов центров сертификации (CA), которые клиент будет использовать для проверки сертификата сервера.
- **PATRONI_SUPERUSER_SSLCRL**: (необязательно) отображается на параметр соединения [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), который указывает расположение файла, содержащего список отозванных сертификатов. Клиент откажет в подключении к любому серверу, сертификат которого находится в этом списке.
- **PATRONI_SUPERUSER_SSLCRLDIR**: (необязательно) отображается на параметр соединения [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), указывающий путь к каталогу, содержащему файлы со списками отозванных сертификатов. Клиент откажет в подключении к любому серверу, сертификат которого находится в этом списке.
- **PATRONI_SUPERUSER_SSLNEGOTIATION**: (необязательно) отображается на параметр соединения [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), управляющий процессом согласования SSL шифрования с сервером, если используется SSL.
- **PATRONI_SUPERUSER_GSSENCMODE**: (необязательно) отображается на параметр соединения [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), определяющий, будет ли устанавливаться защищённое соединение GSS TCP/IP с сервером, и с какой приоритетностью
- **PATRONI_SUPERUSER_CHANNEL_BINDING**: (необязательно) отображается на параметр соединения [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), управляющий использованием клиентом привязки канала.
- **PATRONI_REWIND_USERNAME**: (необязательно) имя пользователя для `pg_rewind`; пользователь будет создан при инициализации postgres 11+ и будут выданы все необходимые разрешения [](https://www.postgresql.org/docs/11/app-pgrewind.html#id-1.9.5.8.8).
- **PATRONI_REWIND_PASSWORD**: (необязательно) пароль для пользователя для `pg_rewind`; пользователь будет создан при инициализации.
- **PATRONI_REWIND_SSLMODE**: (необязательно) отображается на параметр соединения [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), позволяющий клиенту указать тип TLS режима согласования с сервером. Подробнее о том, как работает каждый режим, см. в [документации PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). Значение по умолчанию — `prefer`.
- **PATRONI_REWIND_SSLKEY**: (необязательно) отображается на параметр соединения [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), который указывает расположение закрытого ключа, используемого с сертификатом клиента.
- **PATRONI_REWIND_SSLPASSWORD**: (необязательно) отображается на параметр соединения [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), который указывает пароль для секретного ключа, указанного в `PATRONI_REWIND_SSLKEY`.
- **PATRONI_REWIND_SSLCERT**: (необязательно) отображается на параметр соединения [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), который указывает расположение сертификата клиента.
- **PATRONI_REWIND_SSLROOTCERT**: (необязательно) отображается на параметр соединения [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), который указывает расположение файла, содержащего один или несколько сертификатов центров сертификации (CA), которые клиент будет использовать для проверки сертификата сервера.
- **PATRONI_REWIND_SSLCRL**: (необязательно) отображается на параметр соединения [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), указывающий путь к файлу, содержащему список отозванных сертификатов. Клиент откажет в подключении к любому серверу, сертификат которого находится в этом списке.
- **PATRONI_REWIND_SSLCRLDIR**: (необязательно) отображается на параметр соединения [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), который указывает расположение каталога, содержащего файлы со списками отозванных сертификатов. Клиент откажет в подключении к любому серверу, сертификат которого находится в этом списке.
- **PATRONI_REWIND_SSLNEGOTIATION**: (необязательно) отображается на параметр соединения [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), управляющий процессом согласования SSL шифрования с сервером, если используется SSL.
- **PATRONI_REWIND_GSSENCMODE**: (необязательно) отображается на параметр соединения [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), определяющий, будет ли устанавливаться защищённое соединение GSS TCP/IP с сервером, и с какой приоритетностью
- **PATRONI_REWIND_CHANNEL_BINDING**: (необязательно) отображается на параметр соединения [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), управляющий использованием клиентом привязки канала.

--------

## REST API {#rest-api}

- **PATRONI_RESTAPI_THREAD_POOL_SIZE**: размер пула потоков, используемого Patroni для обработки запросов REST API. Минимальное значение — `5`, значение по умолчанию — `5`.
- **PATRONI_RESTAPI_CONNECT_ADDRESS**: IP-адрес и порт для доступа к REST API.
- **PATRONI_RESTAPI_LISTEN**: IP-адрес и порт, на которых Patroni будет слушать, чтобы предоставлять информацию о состоянии для HAProxy.
- **PATRONI_RESTAPI_USERNAME**: имя пользователя для аутентификации по базовой схеме для защиты небезопасных конечных точек REST API.
- **PATRONI_RESTAPI_PASSWORD**: Пароль аутентификации по базе для защиты небезопасных конечных точек REST API.
- **PATRONI_RESTAPI_CERTFILE**: Указывает файл сертификата в формате PEM. Если параметр certfile не указан или оставлен пустым, сервер API будет работать без SSL.
- **PATRONI_RESTAPI_KEYFILE**: Указывает файл с секретным ключом в формате PEM.
- **PATRONI_RESTAPI_KEYFILE_PASSWORD**: Указывает пароль для расшифровки ключевого файла.
- **PATRONI_RESTAPI_CAFILE**: Указывает файл с CA_BUNDLE, содержащий сертификаты доверенных ЦС, используемые при проверке сертификатов клиентов.
- **PATRONI_RESTAPI_CIPHERS**: (необязательно) Задаёт разрешённые наборы шифров (e.g. "ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:!SSLv1:!SSLv2:!SSLv3:!TLSv1:!TLSv1.1")
- **PATRONI_RESTAPI_VERIFY_CLIENT**: `none` (по умолчанию), `optional` или `required`. При `none` REST API проверка сертификатов клиентов не выполняется. При `required` для всех вызовов REST API требуется сертификат клиента. При `optional` для всех небезопасных конечных точек REST API требуется сертификат клиента. При `required` аутентификация клиента считается успешной, если проверка подписи сертификата прошла успешно. Для `optional` сертификат клиента проверяется только для запросов `PUT`, `POST`, `PATCH` и `DELETE`.
- **PATRONI_RESTAPI_ALLOWLIST**: (необязательно): указывает набор хостов, которые могут вызывать небезопасные конечные точки REST API. Единственный элемент может быть именем хоста, IP-адресом или сетевым адресом в нотации CIDR. По умолчанию используется `allow all`. Если установлены `allowlist` или `allowlist_include_members`, то всё, что не включено, отклоняется.
- **PATRONI_RESTAPI_ALLOWLIST_INCLUDE_MEMBERS**: (необязательно): если установлено в `true`, позволяет получать доступ к небезопасным конечным точкам REST API с других участников кластера, зарегистрированных в DCS (IP-адрес или имя хоста берётся из участников `api_url`). Будьте осторожны, возможна ситуация, при которой ОС может использовать другой IP-адрес для исходящих соединений.
- **PATRONI_RESTAPI_HTTP_EXTRA_HEADERS**: (необязательно) заголовки HTTP позволяют серверу REST API передавать дополнительную информацию в ответе HTTP.
- **PATRONI_RESTAPI_HTTPS_EXTRA_HEADERS**: (необязательно) заголовки HTTPS позволяют серверу REST API передавать дополнительную информацию в ответе HTTP при включённом TLS. Это также передаст дополнительную информацию, установленную в `http_extra_headers`.
- **PATRONI_RESTAPI_REQUEST_QUEUE_SIZE**: (необязательно): устанавливает размер очереди запросов для сокета TCP, используемого Patroni REST API. Как только очередь заполнена, последующие запросы получают ошибку «Соединение запрещено». Значение по умолчанию — 5.
- **PATRONI_RESTAPI_SERVER_TOKENS**: (необязательно) Настраивает значение заголовка `Server` HTTP. `Original` (по умолчанию) сохраняет исходное поведение и отображает версии BaseHTTP и Python, e.g. `BaseHTTP/0.6 Python/3.12.3`. `Minimal`: заголовок будет содержать только версию Patroni, e.g. `Patroni/4.0.0`. `ProductOnly`: заголовок будет содержать только имя продукта, e.g. `Patroni`.

<div class="warning">

<div class="title">

Предупреждение

</div>

- `PATRONI_RESTAPI_CONNECT_ADDRESS` должен быть доступен со всех узлов заданного кластера Patroni. Внутри Patroni он используется во время выбора лидера для определения узлов с минимальной задержкой репликации.
- Если включена проверка сертификатов клиентов (значение `PATRONI_RESTAPI_VERIFY_CLIENT` установлено в `required`), также **обязательно** предоставить **действительные сертификаты клиентов** в `PATRONI_CTL_CERTFILE`, `PATRONI_CTL_KEYFILE`, `PATRONI_CTL_KEYFILE_PASSWORD`. Если они не предоставлены, Patroni будет работать некорректно.

</div>

--------

## CTL {#ctl}

- **PATRONICTL_CONFIG_FILE**: (необязательно) расположение файла конфигурации.
- **PATRONI_CTL_USERNAME**: (необязательно) Имя пользователя для аутентификации по базовой схеме при доступе к защищённым конечным точкам REST API. Если не указано, [patronictl](/ru/docs/patroni/patronictl#patronictl) будет использовать значение, указанное для параметра "username" REST API.
- **PATRONI_CTL_PASSWORD**: (необязательно) Пароль для аутентификации по методу Basic-auth при доступе к защищённым конечным точкам REST API. Если не указан, [patronictl](/ru/docs/patroni/patronictl#patronictl) будет использовать значение, указанное для параметра "password" REST API.
- **PATRONI_CTL_INSECURE**: (необязательно) Разрешить соединения с REST API без проверки сертификатов SSL.
- **PATRONI_CTL_CACERT**: (необязательно) Указывает файл с CA_BUNDLE файлом или каталогом сертификатов доверенных ЦС, используемых при проверке REST API SSL сертификатов. Если не указано, [patronictl](/ru/docs/patroni/patronictl#patronictl) будет использовать значение, заданное для параметра REST API "cafile".
- **PATRONI_CTL_CERTFILE**: (необязательно) Указывает файл сертификата клиента в формате PEM.
- **PATRONI_CTL_KEYFILE**: (необязательно) Указывает файл с секретным ключом клиента в формате PEM.
- **PATRONI_CTL_KEYFILE_PASSWORD**: (необязательно) Указывает пароль для расшифровки ключевого файла клиента.
