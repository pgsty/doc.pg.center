---
title: etcd в сравнении с другими хранилищами ключей и значений
weight: 2875
description: История и применение etcd, сравнение с другими инструментами
categories: [Концепция]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/why.md"
aliases: [/etcd/learning/why/]
---

Название «etcd» образовано из двух идей: каталога Unix «/etc» и распределённых
(«d»istributed) систем. В «/etc» хранятся данные конфигурации одной системы,
тогда как etcd хранит конфигурацию крупных распределённых систем. Поэтому
распределённый («d»istributed) «/etc» называется «etcd».

etcd задуман как универсальная основа крупных распределённых систем. Такие
системы не допускают split-brain и готовы ради этого пожертвовать доступностью.
etcd хранит метаданные согласованно и отказоустойчиво. Кластер etcd предоставляет
хранилище ключей и значений с лучшими в своём классе стабильностью, надёжностью,
масштабируемостью и производительностью.

Распределённые системы используют etcd как согласованное хранилище ключей и
значений для управления конфигурацией, обнаружения служб и координации работы.
Многие [организации][production-users] строят на etcd производственные системы:
планировщики контейнеров, службы обнаружения и распределённые хранилища данных.
Распространённые шаблоны включают [выбор лидера][etcd-etcdctl-elect],
[распределённые блокировки][etcd-etcdctl-lock] и контроль работоспособности машин.

## Сценарии использования {#use-cases}

- Container Linux от CoreOS: приложения в [Container Linux][container-linux]
  автоматически получают обновления ядра Linux без простоя. Container Linux
  координирует обновления через [locksmith], реализующий распределённый семафор
  на etcd, чтобы одновременно перезагружалась только часть кластера.
- [Kubernetes][kubernetes] хранит в etcd конфигурацию для обнаружения служб и
  управления кластером; согласованность etcd критична для правильного планирования
  и работы служб. Сервер API Kubernetes сохраняет состояние кластера в etcd и
  использует API наблюдения для мониторинга кластера и применения критических
  изменений конфигурации.

## Сравнительная таблица {#comparison-chart}

Возможно, etcd уже кажется подходящим, но любое технологическое решение требует
осторожности. Обратите внимание, что документацию написала команда etcd. Хотя
идеал — беспристрастное сравнение технологий и функций, опыт и предпочтения
авторов неизбежно склоняются в пользу etcd. Используйте только по назначению.

Таблица позволяет быстро сравнить etcd с популярными альтернативами. Подробности
по каждому столбцу приведены в следующих разделах.

|  | etcd | ZooKeeper | Consul | NewSQL (Cloud Spanner, CockroachDB, TiDB) |
| --- | --- | --- | --- | --- |
| Примитивы конкурентности | [RPC блокировок][etcd-v3lock], [RPC выборов][etcd-v3election], [блокировки командной строки][etcd-etcdctl-lock], [выборы командной строки][etcd-etcdctl-elect], [рецепты][etcd-recipe] на Go | Внешние [рецепты curator][curator] на Java | [Встроенный API блокировок][consul-lock] | [Редко][newsql-leader], если вообще есть |
| Линеаризуемое чтение | [Да][etcd-linread] | Нет | [Да][consul-linread] | Иногда |
| Многоверсионное управление конкурентностью | [Да][etcd-mvcc] | Нет | Нет | Иногда |
| Транзакции | [Сравнение полей, чтение, запись][etcd-txn] | [Проверка версии, запись][zk-txn] | [Сравнение поля, блокировка, чтение, запись][consul-txn] | В стиле SQL |
| Уведомления об изменениях | [Исторические и текущие интервалы ключей][etcd-watch] | [Текущие ключи и каталоги][zk-watch] | [Текущие ключи и префиксы][consul-watch] | Триггеры (иногда) |
| Права пользователей | [На основе ролей][etcd-rbac] | [ACL][zk-acl] | [ACL][consul-acl] | Различаются (табличный [GRANT][cockroach-grant], роли [базы данных][spanner-roles]) |
| API HTTP/JSON | [Да][etcd-json] | Нет | [Да][consul-json] | Редко |
| Изменение состава | [Да][etcd-reconfig] | [>3.5.0][zk-reconfig] | [Да][consul-reconfig] | Да |
| Максимальный надёжный размер базы | Несколько гигабайт | Сотни мегабайт (иногда несколько гигабайт) | Сотни MB | Терабайты+ |
| Минимальная задержка линеаризации чтения | Сетевой RTT | Без линеаризации чтения | RTT + fsync | Барьеры часов (атомарные, NTP) |

### ZooKeeper {#zookeeper}

ZooKeeper решает ту же задачу, что и etcd: координацию распределённых систем и
хранение метаданных. Но при создании etcd учитывался инженерный и эксплуатационный
опыт проектирования ZooKeeper. Эти уроки помогли etcd поддерживать крупные системы,
такие как Kubernetes. Улучшения относительно ZooKeeper включают:

* динамическое изменение состава кластера;
* стабильное чтение и запись под высокой нагрузкой;
* модель многоверсионного управления конкурентностью;
* надёжное наблюдение за ключами без скрытой потери событий;
* примитивы аренды, отделяющие соединения от сеансов;
* API безопасных распределённых совместных блокировок.

Кроме того, etcd изначально поддерживает множество языков и фреймворков.
ZooKeeper использует собственный уникальный протокол Jute RPC, ограничивающий
[языковые привязки][zk-bindings], тогда как клиентский протокол etcd основан на
[gRPC][grpc] с привязками для Go, C++, Java и других языков. gRPC можно
сериализовать в JSON поверх HTTP, поэтому с etcd работают даже утилиты вроде
`curl`. Поскольку системы могут выбирать из множества вариантов, они строятся
на etcd с естественными для них инструментами, а не вокруг etcd с единственным
фиксированным набором технологий.

Новым приложениям, которым нужно согласованное хранилище ключей и значений,
с учётом возможностей, поддержки и стабильности лучше выбрать etcd вместо ZooKeeper.

### Consul {#consul}

Consul — комплексная среда обнаружения служб со встроенными проверками состояния,
обнаружением отказов и DNS. Она также предоставляет хранилище ключей и значений
через RESTful API HTTP. [В Consul 1.0][dbtester-comparison-results] операции с
ключами масштабировались хуже etcd и ZooKeeper: миллионы ключей приводили к
высоким задержкам и давлению на память. В API отсутствуют многоверсионные ключи,
условные транзакции и надёжные потоковые наблюдения.

etcd и Consul решают разные задачи. Для распределённого согласованного хранилища
лучше etcd. Для комплексного обнаружения служб кластера возможностей etcd
недостаточно; выберите Kubernetes, Consul или SmartStack.

### NewSQL (Cloud Spanner, CockroachDB, TiDB) {#newsql-cloud-spanner-cockroachdb-tidb}

И etcd, и базы NewSQL, например [Cockroach][cockroach], [TiDB][tidb] и
[Google Spanner][spanner], обеспечивают строгую согласованность при высокой
доступности. Но различия архитектуры приводят к разным клиентским API и характеристикам.

Базы NewSQL горизонтально масштабируются между центрами обработки данных. Они
разделяют терабайты данных между несколькими, иногда удалёнными, согласованными
группами репликации (шардами). Из-за ожидания часов и локализованных графов
зависимостей обновлений они плохо подходят для распределённой координации.
Данные организованы в таблицы с более богатым SQL, чем у etcd, ценой сложности
обработки, планирования и оптимизации запросов.

Итого: для метаданных и координации распределённых приложений выбирайте etcd.
Для объёмов более нескольких GB или полноценных запросов SQL выбирайте NewSQL.

## Использование etcd для метаданных {#using-etcd-for-metadata}

etcd реплицирует все данные в одной согласованной группе. Для нескольких GB с
согласованным порядком это наиболее эффективно. Каждому изменению состояния
кластера, которое может затрагивать несколько ключей, присваивается глобальный
уникальный идентификатор — ревизия — из монотонно возрастающего счётчика,
позволяющего рассуждать о порядке. Поскольку группа репликации одна, для
фиксации запрос проходит только протокол Raft. Один консенсус обеспечивает
согласованность, низкую задержку и высокую пропускную способность при простом
протоколе.

Репликация etcd не масштабируется горизонтально без шардирования. NewSQL обычно
распределяет терабайты данных между несколькими согласованными группами. Чтобы
назначить каждому изменению глобальный возрастающий ID, запрос проходит
дополнительную координацию между группами. Возможные конфликты ID заставляют
повторять упорядоченные запросы, усложняя систему и обычно снижая производительность
строгого порядка относительно etcd.

Если приложение в основном работает с метаданными и их порядком для координации
процессов, выбирайте etcd. Для крупного хранилища между несколькими ЦОД без
сильной зависимости от глобального порядка выбирайте NewSQL.

## Использование etcd для распределённой координации {#using-etcd-for-distributed-coordination}

etcd изначально предоставляет наблюдения, аренды, выборы и распределённые
совместные блокировки. У блокировок есть неочевидные свойства, описанные ниже.
Примитивы сопровождают разработчики etcd; перенос их во внешние библиотеки
оставляет базовую распределённую систему неполной. В NewSQL их обычно реализуют
третьи стороны, у ZooKeeper есть независимая [библиотека][curator] рецептов, а
Consul предупреждает, что его встроенный API блокировок — «[не безупречный
метод][consul-bulletproof]».

Теоретически такие примитивы можно построить над любым строго согласованным
хранилищем. Но алгоритмы тонки: кажущаяся рабочей блокировка внезапно ломается
из-за эффекта лавины запросов и рассинхронизации времени. Другие примитивы,
например транзакционная память, зависят от модели MVCC etcd; одной строгой
согласованности недостаточно.

Для распределённой координации etcd снижает эксплуатационные риски и экономит инженерные усилия.

### Примечания об использовании блокировок и аренд {#notes-on-the-usage-of-lock-and-lease}
etcd предоставляет [API блокировок][etcd-v3lock] на основе [механизма аренды][lease]
и [его реализации в etcd][etcdlease]. Сервер выдаёт клиенту токен — аренду —
с TTL и отзывает её после истечения времени. Пока клиент держит неотозванную
аренду, он может заявлять владение связанным ресурсом; в etcd это ключ.
etcd предоставляет API блокировок, построенные по этой схеме. Но сами
API блокировок не обеспечивают взаимное исключение. Название lock сохранено
[по историческим причинам][chubby]; ниже показано, как API оптимизирует механизм
взаимного исключения.

Главное свойство аренды: TTL — физический интервал времени, который сервер и
клиент измеряют собственными часами. Поэтому сервер может отозвать аренду, пока
клиент всё ещё считает себя владельцем.

Следовательно, сама аренда не гарантирует взаимное исключение, а владение арендой
не гарантирует удержание блокировки ресурса.

Для ключей etcd взаимное исключение реализуется проверкой номера версии (в
других системах — compare-and-swap). В RPC `Put` и `Txn` задаются условия по
ревизии и идентификатору аренды. При невыполнении условий операция может
завершиться ошибкой. С помощью этого механизма etcd предоставляет клиентам
распределённые блокировки. Это означает, что клиент знает, что получил
блокировку ключа, когда кластер etcd успешно завершил его запрос.

Подобные схемы описаны в литературе:
* в [статье о Chubby][chubby] вводится *sequencer*, приблизительно соответствующий сочетанию ревизии и ID аренды etcd;
* в [How to do distributed locking][fencing] Martin Kleppmann вводит *fencing token*, которому в etcd соответствует ревизия;
* в [Practical Uses of Synchronized Clocks in Distributed Systems][physicalclock] описана распределённая блокировка Thor на проверке версии и аренде.

Аренды нужны даже при проверке версий, поскольку уменьшают число прерванных запросов.

Ключи etcd эффективно блокируются благодаря аренде и проверке версии. Внешние
ресурсы должны сами предоставлять проверку версий и согласованность реплик,
подобную ключам etcd. Блокировки etcd не могут непосредственно защищать внешние ресурсы.

[chubby]: https://research.google/pubs/pub27897/
[cockroach]: https://github.com/cockroachdb/cockroach
[cockroach-grant]: https://www.cockroachlabs.com/docs/stable/grant.html
[consul-acl]: https://www.consul.io/docs/security/acl
[consul-bulletproof]: https://www.consul.io/docs/dynamic-app-config/sessions
[consul-json]: https://www.consul.io/api-docs#formatted-json-output
[consul-linread]: https://www.consul.io/api-docs#consistency
[consul-lock]: https://www.consul.io/commands/lock
[consul-reconfig]: https://developer.hashicorp.com/consul/tutorials/datacenter-operations/add-remove-servers
[consul-txn]: https://www.consul.io/api/kv#txn
[consul-watch]: https://www.consul.io/docs/dynamic-app-config/watches
[container-linux]: https://coreos.com/why
[curator]: http://curator.apache.org/
[dbtester-comparison-results]: https://github.com/coreos/dbtester/tree/master/test-results/2018Q1-02-etcd-zookeeper-consul
[etcd-commonname]: /ru/docs/etcd/op-guide/authentication/#using-tls-common-name
[etcd-etcdctl-elect]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#elect-options-election-name-proposal
[etcd-etcdctl-lock]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#lock-options-lockname-command-arg1-arg2-
[etcd-json]: /ru/docs/etcd/dev-guide/api_grpc_gateway/
[etcd-linread]: /ru/docs/etcd/learning/api_guarantees/#linearizability
[etcd-mvcc]: /ru/docs/etcd/learning/data_model/
[etcd-rbac]: /ru/docs/etcd/op-guide/authentication/rbac
[etcd-recipe]: https://godoc.org/github.com/etcd-io/etcd/client/v3/experimental/recipes
[etcd-reconfig]: /ru/docs/etcd/op-guide/runtime-configuration
[etcd-txn]: /ru/docs/etcd/learning/api/#transaction
[etcd-v3election]: https://pkg.go.dev/go.etcd.io/etcd/server/v3/etcdserver/api/v3election/v3electionpb
[etcd-v3lock]: https://pkg.go.dev/go.etcd.io/etcd/server/v3/etcdserver/api/v3lock/v3lockpb
[etcd-watch]: /ru/docs/etcd/learning/api/#watch-streams
[etcdlease]: https://godoc.org/github.com/etcd-io/etcd/client/v3/leasing
[fencing]: https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
[grpc]: https://www.grpc.io
[kubernetes]: https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/
[lease]: https://web.stanford.edu/class/cs240/readings/leases.pdf
[locksmith]: https://github.com/coreos/locksmith
[newsql-leader]: http://dl.acm.org/citation.cfm?id=2960999
[physicalclock]: https://web.archive.org/web/20190725151657/http://www.dainf.cefetpr.br/~tacla/SDII/PracticalUseOfClocks.pdf
[production-users]: https://github.com/etcd-io/etcd/blob/main/ADOPTERS.md
[spanner]: https://cloud.google.com/spanner/
[spanner-roles]: https://cloud.google.com/spanner/docs/iam#roles
[tidb]: https://github.com/pingcap/tidb
[zk-acl]: https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers.html#sc_ZooKeeperAccessControl
[zk-bindings]: https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers.html#ch_bindings
[zk-reconfig]: https://zookeeper.apache.org/doc/current/zookeeperReconfig.html
[zk-txn]: https://zookeeper.apache.org/doc/r3.4.3/api/org/apache/zookeeper/ZooKeeper.html#multi(java.lang.Iterable)
[zk-watch]: https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkWatches
