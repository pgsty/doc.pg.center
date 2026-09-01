# Стандарт русского перевода документации

This file is the normative baseline for Russian translations of the English
documentation under `content/`.  English pages are authoritative.  Russian
pages live next to them and use the `<name>.ru.md` suffix; section pages use
`_index.ru.md`.

The initial Russian edition covers all six component collections:
`patroni`, `pgbackrest`, `pgbouncer`, `pgbadger`, `haproxy`, and `etcd`.

## Translation scope

- Translate the complete natural-language content: `title`, `linkTitle`,
  `description`, headings, paragraphs, callouts, list prose, table prose, and
  human-readable link labels.
- Do not summarize, omit repetitions, simplify requirements, or introduce
  facts that are absent from the English source.
- Preserve the strength of normative language.  Translate `must` as
  `должен`, `должны`, or `обязательно`; translate `should` as `следует` or
  `рекомендуется`; translate `may` and `can` as `может`, `могут`, or `можно`.
- Preserve every negation, condition, default, deprecation notice, security
  warning, version, number, unit, and operation order.
- Keep product and project spelling exact: `Patroni`, `pgBackRest`,
  `PgBouncer`, `pgBadger`, `HAProxy`, `etcd`, `etcdctl`, `PostgreSQL`,
  `Prometheus`, `Grafana`, `Kubernetes`, and `OpenSSL`.

## Structure and literals that must not change

- Keep fenced code blocks and indented code blocks byte-for-byte, including
  comments, prompts, output, logs, diagnostic messages, and error text.
- Keep inline code, commands, command options, configuration keys and values,
  API/RPC/message/field names, environment variables, metric names, log-field
  names, file names, paths, placeholders, and protocol identifiers unchanged.
- Keep Markdown structure: heading levels, explicit anchors, list markers and
  nesting, blockquotes and admonition tags, table column counts, emphasis,
  shortcodes, footnote identifiers, reference definitions, and HTML tags.
- Preserve all explicit anchors byte-for-byte.  When an English heading has no
  explicit anchor, add its rendered English anchor to the Russian heading so
  existing fragment links continue to work.
- Preserve external URLs exactly.  Local documentation links to any of the six
  component collections use the Russian route, for example
  `/patroni/rest_api/` becomes `/ru/patroni/rest_api/`.
- Shared assets remain language-neutral: paths to images, downloads, JSON,
  text, configuration samples, and files below `/third_party/` do not acquire
  a `/ru/` prefix.
- Preserve upstream attribution metadata, revisions, aliases, weights, icons,
  modules, and source names.  Only natural-language display metadata is
  translated.

## Legal text

License grants, warranty disclaimers, limitation-of-liability paragraphs,
copyright notices, and other quoted legal notices must remain in their
original English wording byte-for-byte.  Translate surrounding editorial
explanations and credits, but never paraphrase the legal text.  Official
license names such as `MIT License`, `ISC License`, `PostgreSQL License`,
`GNU General Public License version 2`, and `Apache License 2.0` retain their
official names.

## Russian style

- Use clear contemporary Russian for experienced Linux, networking,
  distributed-systems, and PostgreSQL operators.  Prefer established Russian
  technical vocabulary over transliteration when an unambiguous term exists.
- Write concise sentences in the neutral professional register.  Avoid
  marketing language, literal English word order, and unnecessary second-person
  pronouns.
- Use Russian punctuation and typography in prose: `«ёлочки»` for ordinary
  quotations and an em dash where Russian syntax requires it.  Do not alter
  punctuation inside protected literals.
- Keep Latin abbreviations such as ACL, API, CA, CLI, CPU, DCS, DNS, gRPC,
  HTTP, MVCC, QUIC, Raft, RPC, SNI, SPOE, SQL, TCP, TLS, TTL, and WAL.
- Translate prose around a literal configuration keyword while leaving the
  keyword itself unchanged.  For example: ``параметр `max_connections` `` and
  ``секция `backend` ``.
- Translate link labels, image alt text, and explanatory HTML text; preserve
  their destinations and attributes.

## Common terminology

| English | Russian | Notes |
| --- | --- | --- |
| availability | доступность | |
| high availability | высокая доступность | Keep `HA` when used as an abbreviation. |
| backup | резервная копия | As a process, use `резервное копирование`. |
| restore | восстановление | |
| recovery | восстановление | |
| failover | переключение при отказе | Use `аварийное переключение` when contrasted with switchover. |
| switchover | плановое переключение | |
| cluster | кластер | |
| node | узел | |
| member | участник | A logical member of a distributed cluster. |
| primary | первичный сервер | Keep literal role or field values unchanged. |
| replica | реплика | |
| standby | резервный сервер | Keep literal PostgreSQL state names unchanged. |
| client | клиент | |
| server | сервер | |
| connection | соединение | |
| connection pool | пул соединений | |
| configuration | конфигурация | |
| deployment | развёртывание | |
| logging | ведение журнала | `log` as a noun is `журнал`. |
| monitoring | мониторинг | |
| repository | репозиторий | |
| release | выпуск | |
| upgrade | обновление | |
| downgrade | понижение версии | |
| troubleshooting | устранение неполадок | |
| warning | предупреждение | Preserve admonition tag `[!WARNING]`. |
| note | примечание | Preserve admonition tag `[!NOTE]`. |
| latency | задержка | |
| throughput | пропускная способность | |
| timeout | тайм-аут | Configuration keys remain unchanged. |

## Patroni terminology

| English | Russian | Notes |
| --- | --- | --- |
| distributed configuration store (DCS) | распределённое хранилище конфигурации (DCS) | |
| leader | лидер | |
| leader race | выбор лидера | |
| leader lock | блокировка лидера | |
| synchronous standby | синхронная реплика | |
| asynchronous replica | асинхронная реплика | |
| bootstrap | начальная инициализация | Literal configuration keys remain unchanged. |
| pause mode | режим паузы | |
| failsafe mode | отказоустойчивый режим | |
| watchdog | сторожевой таймер | |
| replication slot | слот репликации | |
| timeline | временная шкала | PostgreSQL timeline. |
| REST API | REST API | |
| dynamic configuration | динамическая конфигурация | |
| configuration store | хранилище конфигурации | |
| quorum commit mode | режим фиксации по кворуму | |
| scheduled restart | запланированный перезапуск | |
| pending restart | ожидающий перезапуск | |

## pgBackRest terminology

| English | Russian | Notes |
| --- | --- | --- |
| stanza | stanza | Keep the pgBackRest object and configuration key in Latin script. |
| archive | архив | |
| archive command | команда архивирования | Command names remain unchanged. |
| archive push | отправка в архив | Keep `archive-push` as a command. |
| archive get | получение из архива | Keep `archive-get` as a command. |
| backup set | набор резервной копии | |
| full backup | полная резервная копия | |
| differential backup | дифференциальная резервная копия | |
| incremental backup | инкрементная резервная копия | |
| retention | срок хранения | |
| repository host | сервер репозитория | |
| spool path | каталог очереди | Keep the configuration key unchanged. |
| delta restore | дельта-восстановление | |
| bundle | пакетирование файлов | Literal option names remain unchanged. |
| resume | возобновление | |
| manifest | манифест | |
| asynchronous archiving | асинхронное архивирование | |

## PgBouncer terminology

| English | Russian | Notes |
| --- | --- | --- |
| connection pooling | объединение соединений в пул | |
| session pooling | сеансовый режим пула | |
| transaction pooling | транзакционный режим пула | |
| statement pooling | режим пула на уровне операторов | SQL statement. |
| pool mode | режим пула | Keep `pool_mode` unchanged. |
| client connection | клиентское соединение | |
| server connection | серверное соединение | |
| reserve pool | резервный пул | |
| prepared statement | подготовленный оператор | |
| named prepared statement | именованный подготовленный оператор | |
| administration console | административная консоль | |
| authentication query | запрос аутентификации | Keep `auth_query` unchanged. |
| online restart | перезапуск без остановки обслуживания | |
| cancel request | запрос отмены | |
| peer | одноранговый узел | Keep the `peer` key unchanged. |
| database definition | определение базы данных | |

## pgBadger terminology

| English | Russian | Notes |
| --- | --- | --- |
| log analyzer | анализатор журналов | |
| log entry | запись журнала | |
| report | отчёт | |
| incremental report | инкрементный отчёт | |
| sample report | пример отчёта | |
| output format | формат вывода | |
| query | запрос | |
| query duration | длительность запроса | |
| histogram | гистограмма | |
| session | сеанс | |
| checkpoint | контрольная точка | |
| parser | парсер | |
| parse | разбирать | As a process, use `разбор`. |
| parallel processing | параллельная обработка | |
| log prefix | префикс журнала | |
| normalized query | нормализованный запрос | |
| top query | ведущий запрос | Prefer a natural phrase such as `запрос с наибольшим временем`. |

## HAProxy terminology

| English | Russian | Notes |
| --- | --- | --- |
| load balancer | балансировщик нагрузки | |
| load balancing | балансировка нагрузки | |
| frontend | фронтенд | Keep the configuration keyword `frontend` unchanged. |
| backend | бэкенд | Keep the configuration keyword `backend` unchanged. |
| proxy | прокси | |
| listener | слушатель | Keep configuration identifiers unchanged. |
| health check | проверка работоспособности | |
| access control list (ACL) | список контроля доступа (ACL) | |
| sample fetch | извлечение образца | HAProxy sample-fetch mechanism. |
| converter | преобразователь | HAProxy sample converter. |
| stick table | таблица привязок | Keep `stick-table` unchanged. |
| stickiness | привязка сеанса | |
| graceful reload | плавная перезагрузка конфигурации | |
| soft stop | мягкая остановка | |
| runtime API | API времени выполнения | |
| runtime CLI | CLI времени выполнения | |
| request | запрос | |
| response | ответ | |
| header | заголовок | Use `заголовок запроса` or `заголовок ответа`. |
| request rate | интенсивность запросов | |
| connection rate | интенсивность соединений | |
| queue | очередь | |
| tarpit | ловушка соединений (tarpit) | Keep the English term on first use. |
| content switching | переключение содержимого | |
| log forwarding | пересылка журналов | |
| keep-alive | постоянное соединение | Literal modes and option values remain unchanged. |
| zero downtime | без простоя | |
| section | секция | For a configuration section; ordinary document sections are `разделы`. |

## etcd terminology

| English | Russian | Notes |
| --- | --- | --- |
| distributed key-value store | распределённое хранилище ключей и значений | |
| key | ключ | |
| value | значение | |
| keyspace | пространство ключей | |
| key-value pair | пара «ключ — значение» | |
| revision | ревизия | Field names such as `mod_revision` remain unchanged. |
| compaction | компактизация | Do not confuse with data compression. |
| defragmentation | дефрагментация | |
| lease | аренда | |
| watch | наблюдение | Command and API names remain unchanged. |
| watcher | наблюдатель | |
| leader | лидер | Raft role. |
| follower | последователь | Raft role. |
| learner | обучающийся участник | Non-voting member. |
| quorum | кворум | |
| membership | состав кластера | |
| snapshot | снимок | |
| write-ahead log (WAL) | журнал предзаписи (WAL) | |
| linearizable | линеаризуемый | |
| serializable read | сериализуемое чтение | |
| election | выборы | Raft leader election. |
| term | срок полномочий | Raft term; keep field and API names unchanged. |
| transaction | транзакция | |
| endpoint | конечная точка | |
| feature gate | флаг функции | Literal gate names remain unchanged. |
| alarm | аварийный сигнал | |
| authentication | аутентификация | |
| authorization | авторизация | |
| discovery service | служба обнаружения | |
| gateway | шлюз | |
| consensus | консенсус | |
| strongly consistent | строго согласованный | |

## Acceptance criteria

- Every English Markdown page in the six component collections has exactly one
  same-directory `.ru.md` counterpart; data files and shared assets are not
  copied.
- Fenced and indented code, comments, legal notices, explicit anchors,
  shortcodes, footnote identifiers, external URLs, protected literals, and
  immutable front matter match the English source exactly.
- Heading levels, list nesting, blockquote/admonition structure, table shape,
  numbers, versions, and units remain structurally equivalent.
- Russian pages contain no untranslated English prose except protected
  literals, official names, program output, diagnostics, and legal notices.
- After source-level validation, run the Hugo production build and verify the
  `/ru/` routes, fragment links, navigation order, search, and narrow-screen
  readability.
