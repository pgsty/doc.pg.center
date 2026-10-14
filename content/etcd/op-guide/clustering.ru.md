---
title: Руководство по кластеризации
weight: 4150
description: "Начальная инициализация кластера etcd: статическая, обнаружение etcd и обнаружение DNS"
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/clustering.md"
---

## Обзор {#overview}

При статическом запуске кластера etcd каждый участник должен знать других участников кластера. В некоторых случаях IP-адреса участников заранее неизвестны. Тогда кластер etcd можно инициализировать с помощью службы обнаружения.

После запуска кластера etcd участники добавляются и удаляются посредством [динамического изменения конфигурации][runtime-conf]. Чтобы лучше понять конструкцию этого механизма, рекомендуется прочитать [документ о конструкции динамической конфигурации][runtime-reconf-design].

В руководстве рассматриваются следующие механизмы начальной инициализации кластера etcd:

* [Статическая инициализация](#static)
* [Обнаружение etcd](#etcd-discovery)
* [Обнаружение DNS](#dns-discovery)

Каждый механизм будет использован для создания кластера etcd из трёх машин со следующими параметрами:

|Имя|Адрес|Имя узла|
|------|---------|------------------|
|infra0|10.0.1.10|infra0.example.com|
|infra1|10.0.1.11|infra1.example.com|
|infra2|10.0.1.12|infra2.example.com|

## Статическая инициализация {#static}

Поскольку участники, их адреса и размер кластера известны до запуска, можно применить автономную конфигурацию начальной инициализации, задав флаг `initial-cluster`. Каждая машина получает следующие переменные окружения либо параметры командной строки:

```
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380"
ETCD_INITIAL_CLUSTER_STATE=new
```

```
--initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
--initial-cluster-state new
```

Обратите внимание: URL в `initial-cluster` — это _объявленные URL одноранговых узлов_, поэтому они должны совпадать со значением `initial-advertise-peer-urls` на соответствующих узлах.

При запуске нескольких кластеров (либо многократном создании и уничтожении одного кластера) с одинаковой конфигурацией для тестирования настоятельно рекомендуется задавать каждому кластеру уникальный `initial-cluster-token`. Тогда etcd создаёт уникальные идентификаторы кластера и участников, даже если остальные параметры полностью совпадают. Это защищает etcd от взаимодействия между кластерами, способного их повредить.

Для приёма клиентского трафика etcd слушает адреса [`listen-client-urls`][conf-listen-client]. Участник etcd объявляет URL из [`advertise-client-urls`][conf-adv-client] другим участникам, прокси и клиентам. Убедитесь, что `advertise-client-urls` доступны предполагаемым клиентам. Распространённая ошибка — указать в `advertise-client-urls` localhost или оставить значение по умолчанию, когда к etcd должны обращаться удалённые клиенты.

На каждой машине запустите etcd со следующими флагами:

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```

При последующих запусках etcd параметры командной строки, начинающиеся с `--initial-cluster`, игнорируются. После исходной инициализации переменные окружения или флаги командной строки можно удалить. Если конфигурацию потребуется изменить позднее (например, добавить участника в кластер или удалить его), обратитесь к руководству по [динамической конфигурации][runtime-conf].

### TLS {#tls}

etcd поддерживает шифрованную связь по протоколу TLS. Каналы TLS можно использовать как для шифрования внутреннего обмена между одноранговыми узлами кластера, так и для шифрования клиентского трафика. В этом разделе приведены примеры настройки кластера с TLS для одноранговых и клиентских соединений. Подробности о поддержке TLS в etcd см. в [руководстве по безопасности][security-guide].

#### Самоподписанные сертификаты {#self-signed-certificates}

Кластер с самоподписанными сертификатами одновременно шифрует трафик и аутентифицирует соединения. Для запуска такого кластера каждый участник должен иметь уникальную пару ключей (`member.crt`, `member.key`), подписанную общим сертификатом CA кластера (`ca.crt`) для одноранговых и клиентских соединений. Сертификаты можно создать по примеру [настройки TLS][tls-setup] в etcd.

На каждой машине etcd запускается со следующими флагами:

```
$ etcd --name infra0 --initial-advertise-peer-urls https://10.0.1.10:2380 \
  --listen-peer-urls https://10.0.1.10:2380 \
  --listen-client-urls https://10.0.1.10:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra0-client.crt --key-file=/path/to/infra0-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra0-peer.crt --peer-key-file=/path/to/infra0-peer.key
```
```
$ etcd --name infra1 --initial-advertise-peer-urls https://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls https://10.0.1.11:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra1-client.crt --key-file=/path/to/infra1-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra1-peer.crt --peer-key-file=/path/to/infra1-peer.key
```
```
$ etcd --name infra2 --initial-advertise-peer-urls https://10.0.1.12:2380 \
  --listen-peer-urls https://10.0.1.12:2380 \
  --listen-client-urls https://10.0.1.12:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra2-client.crt --key-file=/path/to/infra2-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra2-peer.crt --peer-key-file=/path/to/infra2-peer.key
```

#### Автоматические сертификаты {#automatic-certificates}

Если кластеру требуется шифрованная связь, но не нужна аутентификация соединений, etcd можно настроить на автоматическое создание ключей. При инициализации каждый участник создаёт собственный набор ключей на основе объявленных IP-адресов и имён узлов.

На каждой машине etcd запускается со следующими флагами:

```
$ etcd --name infra0 --initial-advertise-peer-urls https://10.0.1.10:2380 \
  --listen-peer-urls https://10.0.1.10:2380 \
  --listen-client-urls https://10.0.1.10:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```
```
$ etcd --name infra1 --initial-advertise-peer-urls https://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls https://10.0.1.11:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```
```
$ etcd --name infra2 --initial-advertise-peer-urls https://10.0.1.12:2380 \
  --listen-peer-urls https://10.0.1.12:2380 \
  --listen-client-urls https://10.0.1.12:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```

### Случаи ошибок {#error-cases}

В следующем примере новый узел не включён в перечень узлов. Для нового кластера узел _обязательно_ должен быть добавлен в список исходных участников.

```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380 \
  --initial-cluster-state new
etcd: infra1 not listed in the initial cluster config
exit 1
```

В этом примере узел (infra0) сопоставляется с адресом (127.0.0.1:2380), отличным от указанного для него в списке кластера (10.0.1.10:2380). Если узел должен слушать несколько адресов, все они _обязательно_ должны быть отражены в директиве конфигурации "initial-cluster".

```
$ etcd --name infra0 --initial-advertise-peer-urls http://127.0.0.1:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state=new
etcd: error setting up initial cluster: infra0 has different advertised URLs in the cluster and advertised peer URLs list
exit 1
```

Если одноранговый узел с другим набором параметров конфигурации попытается присоединиться к кластеру, etcd сообщит о несовпадении идентификатора кластера и завершит работу.

```
$ etcd --name infra3 --initial-advertise-peer-urls http://10.0.1.13:2380 \
  --listen-peer-urls http://10.0.1.13:2380 \
  --listen-client-urls http://10.0.1.13:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.13:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra3=http://10.0.1.13:2380 \
  --initial-cluster-state=new
etcd: conflicting cluster ID to the target cluster (c6ab534d07e8fcc4 != bc25ea2a74fb18b0). Exiting.
exit 1
```

## Обнаружение {#discovery}

В некоторых случаях IP-адреса одноранговых узлов кластера заранее неизвестны. Такое часто происходит при использовании облачных провайдеров или DHCP в сети. Тогда вместо статической конфигурации для начальной инициализации нового кластера используется существующий кластер etcd. Этот процесс называется «обнаружением».

Для обнаружения доступны два метода:

* служба обнаружения etcd
* записи DNS SRV

### Обнаружение etcd {#etcd-discovery}

> [!NOTE]
> Примеры службы обнаружения в этом разделе описывают устаревший протокол v2, удалённый в etcd 3.7. Для нового кластера v3.7 используйте [обнаружение v3](/ru/etcd/dev-internal/discovery_protocol/) либо описанные в этом руководстве способы статической инициализации и обнаружения через DNS SRV.

Чтобы лучше понять конструкцию протокола службы обнаружения, рекомендуется прочитать [документацию][discovery-proto] протокола.

#### Срок жизни URL обнаружения {#lifetime-of-a-discovery-url}

URL обнаружения идентифицирует уникальный кластер etcd. Вместо повторного использования существующего URL каждый экземпляр etcd получает новый общий URL обнаружения для начальной инициализации нового кластера.

Кроме того, URL обнаружения следует использовать ТОЛЬКО для исходной инициализации кластера. Для изменения состава уже работающего кластера обратитесь к руководству по [динамическому изменению конфигурации][runtime-conf].

#### Пользовательская служба обнаружения etcd {#custom-etcd-discovery-service}

Для обнаружения и начальной инициализации используется существующий кластер. При использовании частного кластера etcd создайте URL следующим образом:

```
$ curl -X PUT https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83/_config/size -d value=3
```

Задание ключа размера по этому URL создаёт URL обнаружения с ожидаемым размером кластера 3.

В этом случае используется URL `https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83`, а участники etcd при запуске регистрируются в каталоге `https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83`.

**Для каждого участника должен быть задан уникальный флаг имени. Подходящим выбором может быть `Hostname` или `machine-id`. Иначе обнаружение завершится ошибкой из-за повторяющегося имени.**

Теперь запустим etcd с соответствующими флагами для каждого участника:

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```

Каждый участник зарегистрируется в пользовательской службе обнаружения etcd, а после регистрации всех машин кластер начнёт работу.

#### Общедоступная служба обнаружения etcd {#public-etcd-discovery-service}

Если существующего кластера нет, используйте общедоступную службу обнаружения на `discovery.etcd.io`. Чтобы создать частный URL обнаружения через конечную точку "new", выполните команду:

```
$ curl https://discovery.etcd.io/new?size=3
https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

Будет создан кластер с исходным размером 3 участника. Если размер не указан, по умолчанию также используется 3.

```
ETCD_DISCOVERY=https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

```
--discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

**Для каждого участника должен быть задан уникальный флаг имени, иначе обнаружение завершится ошибкой из-за повторяющихся имён. Подходящим выбором может быть `Hostname` или `machine-id`.**

Теперь запустим etcd с соответствующими флагами для каждого участника:

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

Каждый участник зарегистрируется в службе обнаружения, а после регистрации всех участников кластер начнёт работу.

Чтобы etcd подключался к службе обнаружения через HTTP-прокси, задайте переменную окружения `ETCD_DISCOVERY_PROXY`.

#### Случаи ошибок и предупреждений {#error-and-warning-cases}

##### Ошибки сервера обнаружения {#discovery-server-errors}


```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
etcd: error: the cluster doesn’t have a size configuration value in https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de/_config
exit 1
```

##### Предупреждения {#warnings}

Это безвредное предупреждение означает, что URL обнаружения будет проигнорирован на этой машине.

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
etcdserver: discovery token ignored since a cluster has already been initialized. Valid log found at /var/lib/etcd
```

### Обнаружение DNS {#dns-discovery}

В качестве механизма обнаружения можно использовать [записи SRV][rfc-srv] DNS.
Флаг `--discovery-srv` задаёт доменное имя DNS, в котором находятся записи SRV обнаружения.
При значении `--discovery-srv example.com` записи DNS SRV ищутся в следующем порядке:

* _etcd-server-ssl._tcp.example.com
* _etcd-server._tcp.example.com

Если найдена `_etcd-server-ssl._tcp.example.com`, etcd попытается выполнить начальную инициализацию через TLS.

Чтобы клиенты могли обнаружить кластер etcd, следующие записи DNS SRV ищутся в указанном порядке:

* _etcd-client._tcp.example.com
* _etcd-client-ssl._tcp.example.com

Если найдена `_etcd-client-ssl._tcp.example.com`, клиенты попытаются связаться с кластером etcd через SSL/TLS.

Если etcd использует TLS, запись SRV обнаружения (например, `example.com`) вместе с именем узла должна входить в DNS SAN сертификата SSL, иначе кластеризация завершится ошибкой с сообщениями журнала наподобие следующего:

```
[...] rejected connection from "10.0.1.11:53162" (error "remote error: tls: bad certificate", ServerName "example.com")
```

Если etcd использует TLS без пользовательского центра сертификации, домен обнаружения (например, example.com) должен совпадать с доменом записи SRV (например, infra1.example.com). Это снижает риск атак с поддельными записями SRV, указывающими на другой домен: такой домен мог бы иметь действительный сертификат PKI, но контролироваться неизвестной третьей стороной.

Флаг `-discovery-srv-name` дополнительно задаёт суффикс имени SRV, запрашиваемого при обнаружении.
Используйте его, чтобы различать несколько кластеров etcd в одном домене.
Например, при значениях `discovery-srv=example.com` и `-discovery-srv-name=foo` выполняются следующие запросы DNS SRV:

* _etcd-server-ssl-foo._tcp.example.com
* _etcd-server-foo._tcp.example.com

#### Создание записей DNS SRV {#create-dns-srv-records}

```
$ dig +noall +answer SRV _etcd-server._tcp.example.com
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra0.example.com.
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra1.example.com.
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra2.example.com.
```

```
$ dig +noall +answer SRV _etcd-client._tcp.example.com
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra0.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra1.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra2.example.com.
```

```
$ dig +noall +answer infra0.example.com infra1.example.com infra2.example.com
infra0.example.com.  300  IN  A  10.0.1.10
infra1.example.com.  300  IN  A  10.0.1.11
infra2.example.com.  300  IN  A  10.0.1.12
```

#### Начальная инициализация кластера etcd через DNS {#bootstrap-the-etcd-cluster-using-dns}

Участники кластера etcd могут объявлять доменные имена или IP-адреса; при начальной инициализации разрешаются записи DNS A.
Начиная с 3.2 (в 3.1 выводятся предупреждения), `--listen-peer-urls` и `--listen-client-urls` отклоняют доменное имя при привязке сетевого интерфейса.

Разрешённый адрес из `--initial-advertise-peer-urls` *должен совпадать* с одним из разрешённых адресов целевых узлов SRV. Участник etcd считывает разрешённый адрес, чтобы определить, принадлежит ли он кластеру, заданному записями SRV.

```
$ etcd --name infra0 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra0.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra0.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

```
$ etcd --name infra1 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra1.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra1.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

```
$ etcd --name infra2 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra2.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra2.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

Кластер также можно инициализировать по IP-адресам вместо доменных имён:

```
$ etcd --name infra0 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.10:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.10:2379 \
--listen-client-urls http://10.0.1.10:2379 \
--listen-peer-urls http://10.0.1.10:2380
```

```
$ etcd --name infra1 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.11:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.11:2379 \
--listen-client-urls http://10.0.1.11:2379 \
--listen-peer-urls http://10.0.1.11:2380
```

```
$ etcd --name infra2 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.12:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.12:2379 \
--listen-client-urls http://10.0.1.12:2379 \
--listen-peer-urls http://10.0.1.12:2380
```

Начиная с v3.1.0 (кроме v3.2.9), когда `etcd --discovery-srv=example.com` настроен с TLS, сервер аутентифицирует одноранговые узлы и клиентов только в том случае, если предоставленные сертификаты содержат корневой домен `example.com` в поле Subject Alternative Name (SAN). См. [примечания по DNS SRV][security-guide-dns-srv].

### Шлюз {#gateway}

Шлюз etcd — простой TCP-прокси, пересылающий сетевые данные кластеру etcd. Подробнее см. в [руководстве по шлюзу][gateway].

### Прокси {#proxy}

Старые выпуски etcd поддерживали [режим прокси][proxy] только для v2 через `--proxy`. Этот режим удалён и недоступен в etcd 3.7. Для API v3 используйте [прокси gRPC](/ru/etcd/op-guide/grpc_proxy/).

Для настройки кластера etcd с прокси API v2 прочитайте [документ о кластеризации в выпуске etcd 2.3][clustering_etcd2].

[clustering_etcd2]: https://github.com/etcd-io/etcd/blob/release-2.3/Documentation/clustering.md
[conf-adv-client]: /ru/etcd/op-guide/configuration/#clustering
[conf-listen-client]: /ru/etcd/op-guide/configuration/#member
[discovery-proto]: /ru/etcd/dev-internal/discovery_protocol/
[gateway]: /ru/etcd/op-guide/gateway/
[proxy]: https://github.com/etcd-io/etcd/blob/release-2.3/Documentation/proxy.md
[rfc-srv]: http://www.ietf.org/rfc/rfc2052.txt
[runtime-conf]: /ru/etcd/op-guide/runtime-configuration/
[runtime-reconf-design]: /ru/etcd/op-guide/runtime-reconf-design/
[security-guide-dns-srv]: /ru/etcd/op-guide/security/#notes-for-dns-srv
[security-guide]: /ru/etcd/op-guide/security/
[tls-setup]: https://github.com/etcd-io/etcd/tree/main/hack/tls-setup
