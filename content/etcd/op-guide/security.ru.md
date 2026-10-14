---
title: Модель транспортной безопасности
weight: 4125
description: Защита передаваемых данных
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/security.md"
---

etcd поддерживает автоматический TLS и аутентификацию по клиентским сертификатам как для связи клиентов с сервером, так и для связи одноранговых узлов (серверов друг с другом внутри кластера). **Обратите внимание: по умолчанию etcd не включает [аутентификацию на основе RBAC][auth] и аутентификацию на транспортном уровне, чтобы упростить начало работы с базой данных. Кроме того, изменение этого значения по умолчанию нарушило бы совместимость проекта, установленную с 2013 года. Кластер etcd без включённых функций безопасности может открыть свои данные любым клиентам.**

Для начала подготовьте сертификат CA и подписанную пару ключей для одного участника. Рекомендуется создавать и подписывать новую пару ключей для каждого участника кластера.

Для удобства инструмент [cfssl] предоставляет простой интерфейс создания сертификатов; пример его использования приведён [здесь][tls-setup]. В качестве альтернативы воспользуйтесь [руководством по созданию самоподписанных пар ключей][tls-guide].

Из-за продолжающейся разработки приведённый ниже список флагов может быть неактуален. Последние доступные флаги можно получить командой `etcd --help` или в [справке etcd][].

## Базовая настройка {#basic-setup}

etcd принимает несколько относящихся к сертификатам параметров конфигурации в виде флагов командной строки или переменных окружения:

**Связь клиента с сервером:**

`--cert-file=<path>`: сертификат, используемый для соединений SSL/TLS **с** etcd. При заданном параметре advertise-client-urls может использовать схему HTTPS.

`--key-file=<path>`: ключ сертификата. Должен быть незашифрованным.

`--client-cert-auth`: если задан, etcd проверяет во всех входящих запросах HTTPS наличие клиентского сертификата, подписанного доверенным CA; запросы без действительного клиентского сертификата завершаются ошибкой. Если включена [аутентификация][auth], сертификат предоставляет учётные данные для имени пользователя из поля Common Name.

`--trusted-ca-file=<path>`: доверенный центр сертификации.

`--auto-tls`: использовать автоматически созданные самоподписанные сертификаты для соединений TLS с клиентами.

**Связь одноранговых узлов (между серверами / в кластере):**

Параметры одноранговых узлов работают так же, как параметры связи клиента с сервером:

`--peer-cert-file=<path>`: сертификат для соединений SSL/TLS между одноранговыми узлами. Используется как при прослушивании адреса однорангового узла, так и при отправке запросов другим узлам.

`--peer-key-file=<path>`: ключ сертификата. Должен быть незашифрованным.

`--peer-client-cert-auth`: если задан, etcd проверяет во всех входящих запросах одноранговых узлов кластера действительные клиентские сертификаты, подписанные указанным CA.

`--peer-trusted-ca-file=<path>`: доверенный центр сертификации.

`--peer-auto-tls`: использовать автоматически созданные самоподписанные сертификаты для соединений TLS между одноранговыми узлами.

Если указан сертификат связи клиента с сервером или одноранговых узлов, необходимо также задать ключ. Все эти параметры конфигурации доступны и через переменные окружения `ETCD_TRUSTED_CA_FILE`, `ETCD_PEER_TRUSTED_CA_FILE` и т. д.

**Общие параметры:**

`--cipher-suites`: разделённый запятыми список поддерживаемых наборов шифров TLS между сервером и клиентом, а также между одноранговыми узлами (пустой список автоматически заполняется Go).

`--tls-min-version=<version>` задаёт минимальную версию TLS, поддерживаемую etcd.

`--tls-max-version=<version>` задаёт максимальную версию TLS, поддерживаемую etcd. Если не задана, используется максимальная версия, поддерживаемая Go.

### keyUsage и extendedKeyUsage сертификата TLS {#tls-certificate-keyusage-and-extendedkeyusage}

При создании сертификатов X.509 для защиты транспорта etcd
в них следует включать подходящие поля `keyUsage` и
`extendedKeyUsage` в зависимости от их роли. Для проверки сертификатов
etcd использует библиотеки Go `crypto/tls` и `crypto/x509`, которые
контролируют эти варианты использования во время рукопожатия TLS.

В таблице приведены рекомендуемые варианты использования для распространённых ролей сертификатов:

| Роль сертификата | keyUsage | extendedKeyUsage |
| ---------------- | -------- | ---------------- |
| Сервер (клиент — сервер) | digitalSignature, keyEncipherment | serverAuth |
| Клиент | digitalSignature, keyEncipherment | clientAuth |
| Одноранговый узел (сервер — сервер) | digitalSignature, keyEncipherment | serverAuth, clientAuth |

Примечания:

- При включённом `--peer-client-cert-auth` сертификаты одноранговых узлов
  используются для взаимного TLS между участниками etcd и поэтому требуют
  как `serverAuth`, так и `clientAuth`.
- В клиентских сертификатах, используемых с `--client-cert-auth`, следует указывать
  `clientAuth`.

## Пример 1: транспортная безопасность между клиентом и сервером с HTTPS {#example-1-client-to-server-transport-security-with-https}

Подготовьте сертификат CA (`ca.crt`) и подписанную пару ключей (`server.crt`, `server.key`).

Настроим простую транспортную безопасность HTTPS в etcd по шагам:

```sh
$ etcd --name infra0 --data-dir infra0 \
  --cert-file=/path/to/server.crt --key-file=/path/to/server.key \
  --advertise-client-urls=https://127.0.0.1:2379 --listen-client-urls=https://127.0.0.1:2379
```

etcd должен успешно запуститься; конфигурацию можно проверить, обратившись к etcd по HTTPS:

```sh
$ curl --cacert /path/to/ca.crt https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

Команда должна показать успешное рукопожатие. Поскольку используются самоподписанные сертификаты и собственный центр сертификации, CA необходимо передать curl с параметром `--cacert`. Другой вариант — добавить сертификат CA в системный каталог доверенных сертификатов (обычно `/etc/pki/tls/certs` или `/etc/ssl/certs`).

**Пользователям OSX 10.9+**: curl 7.30.0 в OSX 10.9+ не распознаёт сертификаты, переданные в командной строке.
Вместо этого импортируйте тестовый ca.crt непосредственно в связку ключей либо добавьте curl флаг `-k`, чтобы игнорировать ошибки.
Для проверки без флага `-k` выполните `open ./tests/fixtures/ca/ca.crt` и следуйте указаниям.
После тестирования удалите этот сертификат!
Если известно обходное решение, сообщите о нём.

## Пример 2: аутентификация клиента на сервере с клиентскими сертификатами HTTPS {#example-2-client-to-server-authentication-with-https-client-certificates}

К этому моменту клиент etcd умеет проверять подлинность сервера и обеспечивает транспортную безопасность. Клиентские сертификаты также позволяют предотвратить несанкционированный доступ к etcd.

Клиенты предъявляют серверу свои сертификаты, а сервер проверяет их подпись указанным CA и решает, обслуживать ли запрос.

Потребуются те же файлы, что и в первом примере, а также пара ключей клиента (`client.crt`, `client.key`), подписанная тем же центром сертификации.

```sh
$ etcd --name infra0 --data-dir infra0 \
  --client-cert-auth --trusted-ca-file=/path/to/ca.crt --cert-file=/path/to/server.crt --key-file=/path/to/server.key \
  --advertise-client-urls https://127.0.0.1:2379 --listen-client-urls https://127.0.0.1:2379
```

Теперь отправьте серверу тот же запрос, что и выше:

```sh
$ curl --cacert /path/to/ca.crt https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

Сервер должен отклонить запрос:

```
...
routines:SSL3_READ_BYTES:sslv3 alert bad certificate
...
```

Для успешного выполнения нужно передать серверу подписанный CA клиентский сертификат:

```sh
$ curl --cacert /path/to/ca.crt --cert /path/to/client.crt --key /path/to/client.key \
  -L https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

Вывод должен содержать:

```
...
SSLv3, TLS handshake, CERT verify (15):
...
TLS handshake, Finished (20)
```

А также ответ сервера:

```json
{
    "action": "set",
    "node": {
        "createdIndex": 12,
        "key": "/foo",
        "modifiedIndex": 12,
        "value": "bar"
    }
}
```

Укажите наборы шифров, чтобы заблокировать [слабые наборы шифров TLS](https://github.com/etcd-io/etcd/issues/8320).

Рукопожатие TLS завершается ошибкой, если приветствие клиента запрошено с недопустимыми наборами шифров.

Например:

```bash
$ etcd \
  --cert-file ./server.crt \
  --key-file ./server.key \
  --trusted-ca-file ./ca.crt \
  --cipher-suites TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
```

После этого клиентские запросы должны указывать один из заданных на сервере наборов шифров:

```bash
# valid cipher suite
$ curl \
  --cacert /path/to/ca.crt \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  -L [CLIENT-URL]/metrics \
  --ciphers ECDHE-RSA-AES128-GCM-SHA256

# request succeeds
etcd_server_version{server_version="3.2.22"} 1
...
```

```bash
# invalid cipher suite
$ curl \
  --cacert /path/to/ca.crt \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  -L [CLIENT-URL]/metrics \
  --ciphers ECDHE-RSA-DES-CBC3-SHA

# request fails with
(35) error:14094410:SSL routines:ssl3_read_bytes:sslv3 alert handshake failure
```

## Пример 3: транспортная безопасность и клиентские сертификаты в кластере {#example-3-transport-security--client-certificates-in-a-cluster}

etcd поддерживает ту же описанную выше модель для **связи одноранговых узлов**, то есть для обмена между участниками etcd в кластере.

Предположим, имеется `ca.crt` и два участника с собственными парами ключей (`member1.crt` и `member1.key`, `member2.crt` и `member2.key`), подписанными этим CA. Запустим etcd следующим образом:


```sh
DISCOVERY_URL=... # from https://discovery.etcd.io/new

# member1
$ etcd --name infra1 --data-dir infra1 \
  --peer-client-cert-auth --peer-trusted-ca-file=/path/to/ca.crt --peer-cert-file=/path/to/member1.crt --peer-key-file=/path/to/member1.key \
  --initial-advertise-peer-urls=https://10.0.1.10:2380 --listen-peer-urls=https://10.0.1.10:2380 \
  --discovery ${DISCOVERY_URL}

# member2
$ etcd --name infra2 --data-dir infra2 \
  --peer-client-cert-auth --peer-trusted-ca-file=/path/to/ca.crt --peer-cert-file=/path/to/member2.crt --peer-key-file=/path/to/member2.key \
  --initial-advertise-peer-urls=https://10.0.1.11:2380 --listen-peer-urls=https://10.0.1.11:2380 \
  --discovery ${DISCOVERY_URL}
```

Участники etcd образуют кластер, а весь обмен между ними шифруется и аутентифицируется клиентскими сертификатами. Вывод etcd покажет, что адреса подключений используют HTTPS.

## Пример 4: автоматическая транспортная безопасность с самоподписанными сертификатами {#example-4-automatic-self-signed-transport-security}

> [!WARNING]
> При указании ClientAutoTLS и PeerAutoTLS срок действия автоматически созданных etcd клиентского сертификата и сертификата однорангового узла составляет только 1 год. Срок действия сертификата в годах можно задать флагом --self-signed-cert-validity.

Если требуется шифрование связи без аутентификации, etcd может шифровать сообщения автоматически созданными самоподписанными сертификатами. Это упрощает развёртывание, поскольку управлять сертификатами и ключами вне etcd не требуется.
Настройте etcd на использование самоподписанных сертификатов для клиентских и одноранговых соединений флагами `--auto-tls` и `--peer-auto-tls`:

```sh
DISCOVERY_URL=... # from https://discovery.etcd.io/new

# member1
$ etcd --name infra1 --data-dir infra1 \
  --auto-tls --peer-auto-tls \
  --initial-advertise-peer-urls=https://10.0.1.10:2380 --listen-peer-urls=https://10.0.1.10:2380 \
  --discovery ${DISCOVERY_URL}

# member2
$ etcd --name infra2 --data-dir infra2 \
  --auto-tls --peer-auto-tls \
  --initial-advertise-peer-urls=https://10.0.1.11:2380 --listen-peer-urls=https://10.0.1.11:2380 \
  --discovery ${DISCOVERY_URL}
```

Самоподписанные сертификаты не подтверждают подлинность, поэтому curl вернёт ошибку:

```sh
curl: (60) SSL certificate problem: Invalid certificate chain
```

Чтобы отключить проверку цепочки сертификатов, вызовите curl с флагом `-k`:

```sh
$ curl -k https://127.0.0.1:2379/v2/keys/foo -Xput -d value=bar -v
```

## Примечания по DNS SRV {#notes-for-dns-srv}

Начиная с v3.1.0 (кроме v3.2.9), начальная инициализация через SRV аутентифицирует `ServerName` по корневому доменному имени из флага `--discovery-srv`. Для защиты от атак «человек посередине» с сертификатами требуется, чтобы сертификат содержал совпадающее корневое доменное имя в поле Subject Alternative Name (SAN). Например, `etcd --discovery-srv=etcd.local` аутентифицирует одноранговые узлы и клиентов, только если предоставленные сертификаты содержат корневой домен `etcd.local` в поле Subject Alternative Name (SAN)

## Примечания для прокси etcd {#notes-for-etcd-proxy}

> [!NOTE]
> Этот раздел описывает исторический прокси v2, который уже удалён. Для etcd 3.7 используйте [прокси gRPC v3](/ru/etcd/op-guide/grpc_proxy/).

Прокси etcd терминирует TLS своего клиента, если соединение защищено, а для связи с участниками etcd использует собственные ключ и сертификат прокси, заданные в `--peer-key-file` и `--peer-cert-file`.

Прокси связывается с участниками etcd как через `--advertise-client-urls`, так и через `--advertise-peer-urls` соответствующего участника. Он пересылает клиентские запросы на объявленные клиентские URL участников etcd и синхронизирует исходную конфигурацию кластера через объявленные URL их одноранговых узлов.

Когда для участника etcd включена аутентификация клиентов, администратор должен убедиться, что сертификат однорангового узла из параметра прокси `--peer-cert-file` действителен для этой аутентификации. При включённой аутентификации одноранговых узлов сертификат прокси также должен быть действителен для неё.

## Примечания по аутентификации TLS {#notes-for-tls-authentication}

Начиная с [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09), [сертификаты TLS перезагружаются при каждом клиентском соединении](https://github.com/etcd-io/etcd/pull/7829). Это позволяет заменять истекающие сертификаты без остановки серверов etcd, перезаписывая старые сертификаты новыми. Обновление сертификатов для каждого соединения не должно создавать значительных накладных расходов, однако в будущем его можно улучшить уровнем кэширования. Примеры тестов находятся [здесь](https://github.com/etcd-io/etcd/blob/b041ce5d514a4b4aaeefbffb008f0c7570a18986/integration/v3_grpc_test.go#L1601-L1757).

Начиная с [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09), [сервер отклоняет входящие сертификаты одноранговых узлов с неверным IP в `SAN`](https://github.com/etcd-io/etcd/pull/7687). Если сертификат однорангового узла содержит IP-адреса в поле Subject Alternative Name (SAN), сервер аутентифицирует узел только при совпадении удалённого IP-адреса с одним из них. Это предотвращает присоединение к кластеру неавторизованных конечных точек. Например, CSR однорангового узла B (созданный с `cfssl`) имеет вид:

```json
{
  "CN": "etcd peer",
  "hosts": [
    "*.example.default.svc",
    "*.example.default.svc.cluster.local",
    "10.138.0.27"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "US",
      "L": "CA",
      "ST": "San Francisco"
    }
  ]
}
```

при этом фактический IP-адрес узла B равен `10.138.0.2`, а не `10.138.0.27`. Когда B пытается присоединиться к кластеру, узел A отклоняет его с ошибкой `x509: certificate is valid for 10.138.0.27, not 10.138.0.2`, поскольку удалённый IP-адрес B не совпадает с адресом в поле Subject Alternative Name (SAN).

Начиная с [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09), [при проверке `SAN` сервер разрешает TLS `DNSNames`](https://github.com/etcd-io/etcd/pull/7767). Если сертификат однорангового узла содержит в поле Subject Alternative Name (SAN) только DNS-имена без IP-адресов, сервер аутентифицирует узел лишь тогда, когда прямое разрешение этих DNS-имён (`dig b.com`) даёт IP, совпадающий с удалённым адресом. Например, CSR однорангового узла B (созданный с `cfssl`) имеет вид:

```json
{
  "CN": "etcd peer",
  "hosts": [
    "b.com"
  ],
```

при этом удалённый IP-адрес узла B равен `10.138.0.2`. Когда B пытается присоединиться к кластеру, узел A разрешает входящее имя `b.com`, получая список IP-адресов (например, командой `dig b.com`). Если список не содержит IP `10.138.0.2`, A отклоняет B с ошибкой `tls: 10.138.0.2 does not match any of DNSNames ["b.com"]`.

Начиная с [v3.2.2](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v322-2017-07-07), [при совпадении IP сервер принимает соединение без проверки записей DNS](https://github.com/etcd-io/etcd/pull/8223). Если сертификат однорангового узла содержит в поле Subject Alternative Name (SAN) IP-адреса и DNS-имена, а удалённый IP совпадает с одним из адресов, сервер принимает соединение без дальнейшей проверки DNS-имён. Например, CSR однорангового узла B (созданный с `cfssl`) имеет вид:

```json
{
  "CN": "etcd peer",
  "hosts": [
    "invalid.domain",
    "10.138.0.2"
  ],
```

при этом удалённый IP-адрес узла B равен `10.138.0.2`, а `invalid.domain` — недопустимое имя узла. Когда B пытается присоединиться к кластеру, узел A успешно аутентифицирует его, поскольку поле Subject Alternative Name (SAN) содержит действительный совпадающий IP-адрес. Подробнее см. [issue#8206](https://github.com/etcd-io/etcd/issues/8206).

Начиная с [v3.2.5](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v325-2017-08-04), [сервер поддерживает обратное разрешение шаблонных DNS `SAN`](https://github.com/etcd-io/etcd/pull/8281). Если сертификат однорангового узла содержит в поле Subject Alternative Name (SAN) только DNS-имена без IP-адресов, сервер сначала выполняет обратное разрешение удалённого IP и получает список соответствующих ему имён (например, командой `nslookup IPADDR`). Затем соединение принимается, если одно из имён совпадает с DNS-именем сертификата точно или по шаблону. Если совпадений нет, сервер выполняет прямое разрешение каждой записи DNS сертификата (например, разрешает `example.default.svc` для записи `*.example.default.svc`) и принимает соединение, только когда среди разрешённых адресов узла есть IP, совпадающий с удалённым IP однорангового узла. Например, CSR узла B (созданный с `cfssl`) имеет вид:

```json
{
  "CN": "etcd peer",
  "hosts": [
    "*.example.default.svc",
    "*.example.default.svc.cluster.local"
  ],
```

при этом удалённый IP-адрес узла B равен `10.138.0.2`. Когда B пытается присоединиться к кластеру, узел A выполняет обратное разрешение IP `10.138.0.2` и получает список имён узлов. Затем он точно или по шаблону сопоставляет их с DNS-именами в поле Subject Alternative Name (SAN) сертификата B. Если ни обратное, ни прямое разрешение не дало совпадений, возвращается ошибка `"tls: "10.138.0.2" does not match any of DNSNames ["*.example.default.svc","*.example.default.svc.cluster.local"]`. Подробнее см. [issue#8268](https://github.com/etcd-io/etcd/issues/8268).

В [v3.3.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) добавлен флаг [`etcd --peer-cert-allowed-cn`](https://github.com/etcd-io/etcd/pull/8616), поддерживающий [аутентификацию соединений одноранговых узлов по CN (Common Name)](https://github.com/etcd-io/etcd/issues/8262). Начальная инициализация TLS в Kubernetes включает создание динамических сертификатов для участников etcd и других системных компонентов (например, сервера API, kubelet и т. д.). Отдельные CA для каждого компонента обеспечивают более строгий контроль доступа к кластеру etcd, но часто неудобны. При заданном флаге --peer-cert-allowed-cn узел может присоединиться только с совпадающим общим именем, даже если CA общий. Сопоставление является точным сравнением строки с полем Common Name (CN) сертификата; шаблоны и префиксы не поддерживаются. При фильтрации по имени узла с --peer-cert-allowed-hostname или --client-cert-allowed-hostname используется x509.Certificate.VerifyHostname() из Go, поддерживающий как точные имена, так и шаблонные записи (например, *.example.com). Например, каждый участник кластера из 3 узлов настраивается со следующими CSR (созданными с cfssl):




```json
{
  "CN": "etcd.local",
  "hosts": [
    "m1.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

```json
{
  "CN": "etcd.local",
  "hosts": [
    "m2.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

```json
{
  "CN": "etcd.local",
  "hosts": [
    "m3.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

При заданном `--peer-cert-allowed-cn etcd.local` аутентифицируются только одноранговые узлы с совпадающими общими именами. Узлы с другими CN в CSR или другим `--peer-cert-allowed-cn` отклоняются:

```bash
$ etcd --peer-cert-allowed-cn m1.etcd.local

I | embed: rejected connection from "127.0.0.1:48044" (error "CommonName authentication failed", ServerName "m1.etcd.local")
I | embed: rejected connection from "127.0.0.1:55702" (error "remote error: tls: bad certificate", ServerName "m3.etcd.local")
```

Каждый процесс следует запускать с параметром:

```bash
etcd --peer-cert-allowed-cn etcd.local

I | pkg/netutil: resolving m3.etcd.local:32380 to 127.0.0.1:32380
I | pkg/netutil: resolving m2.etcd.local:22380 to 127.0.0.1:22380
I | pkg/netutil: resolving m1.etcd.local:2380 to 127.0.0.1:2380
I | etcdserver: published {Name:m3 ClientURLs:[https://m3.etcd.local:32379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | etcdserver: published {Name:m1 ClientURLs:[https://m1.etcd.local:2379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | etcdserver: published {Name:m2 ClientURLs:[https://m2.etcd.local:22379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | embed: serving client requests on 127.0.0.1:32379
I | embed: serving client requests on 127.0.0.1:22379
I | embed: serving client requests on 127.0.0.1:2379
```

В [v3.2.19](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md) и [v3.3.4](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) исправлена перезагрузка TLS, когда [поле SAN сертификата содержит только IP-адреса без доменных имён](https://github.com/etcd-io/etcd/issues/9541). Например, участник настраивается со следующим CSR (созданным с `cfssl`):

```json
{
  "CN": "etcd.local",
  "hosts": [
    "127.0.0.1"
  ],
```

В Go сервер вызывает `(*tls.Config).GetCertificate` для перезагрузки TLS тогда и только тогда, когда поле сервера `(*tls.Config).Certificates` пусто либо `(*tls.ClientHelloInfo).ServerName` непусто и содержит действительный SNI клиента. Ранее etcd всегда заполнял `(*tls.Config).Certificates` при первом клиентском рукопожатии TLS, делая поле непустым. Поэтому клиент всегда должен был передавать совпадающий SNI, чтобы пройти проверку TLS и вызвать `(*tls.Config).GetCertificate` для перезагрузки ресурсов TLS.

Однако сертификат, поле SAN которого [не содержит доменных имён, а только IP-адреса](https://github.com/etcd-io/etcd/issues/9541), запрашивает `*tls.ClientHelloInfo` с пустым полем `ServerName`, поэтому при первом рукопожатии TLS перезагрузка не запускается. Это становится проблемой при замене истёкших сертификатов без остановки службы.

Теперь при первом клиентском рукопожатии TLS `(*tls.Config).Certificates` создаётся пустым, чтобы сначала вызвать `(*tls.Config).GetCertificate`, а затем заполнять остальные сертификаты при каждом новом соединении TLS, даже если SNI клиента пуст (например, сертификат содержит только IP-адреса).

## Примечания по белому списку узлов {#notes-for-host-whitelist}

Флаг `etcd --host-whitelist` задаёт допустимые имена узлов из клиентских запросов HTTP. Политика происхождения клиента защищает незащищённые серверы etcd от атак ["DNS Rebinding"](https://en.wikipedia.org/wiki/DNS_rebinding). Любой веб-сайт может создать разрешённое DNS-имя и направить DNS на `"localhost"` или любой другой адрес. Тогда все конечные точки HTTP сервера etcd, слушающего `"localhost"`, становятся доступны и уязвимы для атак повторной привязки DNS. Подробнее см. [CVE-2018-5702](https://bugs.chromium.org/p/project-zero/issues/detail?id=1447#c2).

Политика происхождения клиента работает следующим образом:

1. Если клиентское соединение защищено HTTPS, разрешаются любые имена узлов.
2. Если клиентское соединение не защищено и `"HostWhitelist"` не пуст, разрешаются только запросы HTTP, поле Host которых указано в белом списке.

Для более строгого контроля политика происхождения клиента применяется независимо от того, включена ли аутентификация.

По умолчанию `etcd --host-whitelist` и `embed.Config.HostWhitelist` имеют значение `*`, разрешающее все имена узлов. Пустой белый список также разрешает все имена узлов. Обратите внимание: при указании имён адреса обратной петли автоматически не добавляются. Чтобы разрешить интерфейсы обратной петли, внесите их в белый список вручную (например, `"localhost"`, `"127.0.0.1"` и т. д.).

## Часто задаваемые вопросы {#frequently-asked-questions}

### При клиентской аутентификации TLS появляется ошибка рукопожатия SSLv3 alert handshake failure? {#im-seeing-a-sslv3-alert-handshake-failure-when-using-tls-client-authentication}

Пакет `crypto/tls` языка `golang` проверяет назначение открытого ключа сертификата перед его использованием.
Чтобы применять открытый ключ сертификата для аутентификации клиента, при его создании нужно добавить `clientAuth` в `Extended Key Usage`.

Это выполняется следующим образом:

Добавьте в openssl.cnf следующий раздел:

```
[ ssl_client ]
...
  extendedKeyUsage = clientAuth
...
```

При создании сертификата обязательно укажите его во флаге `-extensions`:

```
$ openssl ca -config openssl.cnf -policy policy_anything -extensions ssl_client -out certs/machine.crt -infiles machine.csr
```

### При аутентификации сертификата однорангового узла появляется "certificate is valid for 127.0.0.1, not $MY_IP" {#with-peer-certificate-authentication-i-receive-certificate-is-valid-for-127001-not-my_ip}
Убедитесь, что сертификаты подписаны с Subject Name, содержащим общедоступный IP-адрес участника. Например, инструмент `etcd-ca` предоставляет параметр `--ip=` для команды `new-cert`.

Сертификат должен быть подписан для FQDN участника в Subject Name; для добавления IP-адреса используйте Subject Alternative Names (кратко — IP SAN). Инструмент `etcd-ca` предоставляет параметр `--domain=` для команды `new-cert`, а openssl также умеет [это][alt-name].

### Шифрует ли etcd данные, хранящиеся на дисках? {#does-etcd-encrypt-data-stored-on-disk-drives}
Нет. etcd не шифрует данные ключей и значений, хранящиеся на дисках. Если данные etcd необходимо шифровать, доступны следующие варианты:
* выполнять шифрование и расшифрование в клиентских приложениях
* использовать функцию нижележащей системы хранения для шифрования сохранённых данных, например [dm-crypt]

### В журнале появляется предупреждение "directory X exist without recommended permission -rwx------" {#im-seeing-a-log-warning-that-directory-x-exist-without-recommended-permission--rwx}
При создании некоторых новых каталогов etcd задаёт права доступа 700, чтобы по возможности предотвратить непривилегированный доступ. Однако если пользователь уже создал каталог с собственными правами, etcd использует существующий каталог и записывает предупреждение, если права отличаются от 700.

[alt-name]: http://wiki.cacert.org/FAQ/subjectAltName
[auth]: /ru/etcd/op-guide/authentication/
[cfssl]: https://github.com/cloudflare/cfssl
[dm-crypt]: https://en.wikipedia.org/wiki/Dm-crypt
[tls-guide]: https://github.com/coreos/docs/blob/master/os/generate-self-signed-certificates.md
[tls-setup]: https://github.com/etcd-io/etcd/tree/main/hack/tls-setup
[etcd help]: https://github.com/etcd-io/etcd/blob/main/server/etcdmain/help.go
