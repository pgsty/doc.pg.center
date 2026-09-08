---
title: Библиотеки и инструменты
weight: 1300
description: Перечень инструментов и клиентских библиотек etcd
icon: fa-solid fa-puzzle-piece
categories: [Справочник]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/integrations.md"
aliases: [/etcd/integrations/]
---

Обратите внимание: перечисленные ниже сторонние библиотеки и инструменты (размещённые не на https://github.com/etcd-io) не тестируются и не сопровождаются командой etcd. Перед использованием рекомендуется прочитать и изучить их документацию и исходный код.

## Инструменты {#tools}

- [etcdctl](https://github.com/etcd-io/etcd/tree/main/etcdctl) — клиент командной строки для etcd
- [etcd-dump](https://npmjs.org/package/etcd-dump) — утилита командной строки для выгрузки и восстановления etcd.
- [etcd-fs](https://github.com/xetorthio/etcd-fs) — файловая система FUSE для etcd
- [etcddir](https://github.com/rekby/etcddir) — синхронизация etcd с локальным каталогом в реальном времени. Работает в Windows и Linux.
- [etcd-browser](https://github.com/henszey/etcd-browser) — веб-редактор ключей и значений etcd на AngularJS
- [etcd-lock](https://github.com/datawisesystems/etcd-lock) — реализация выборов главного узла и распределённой блокировки чтения/записи на основе etcd; поддерживает v2
- [etcd-console](https://github.com/matishsiao/etcd-console) — веб-редактор ключей и значений etcd на PHP
- [etcd-viewer](https://github.com/nikfoundas/etcd-viewer) — редактор и средство просмотра хранилища ключей и значений etcd, написанное на Java
- [etcdtool](https://github.com/mickep76/etcdtool) — экспорт, импорт и редактирование каталога etcd в JSON/YAML/TOML, а также проверка каталога по схеме JSON
- [etcdloadtest](https://github.com/sinsharat/etcdloadtest) — клиент командной строки для нагрузочного тестирования etcd версии 3.0 и выше.
- [etcd-tui](https://github.com/olamilekan000/etcd-tui) — современный терминальный пользовательский интерфейс (TUI) для работы с базой данных etcd. Позволяет переходить по ключам, просматривать значения, фильтровать данные и управлять кластером etcd непосредственно из терминала.
- [etcdfinder](https://etcdfinder.github.io) — сверхбыстрый современный веб-интерфейс etcd с мгновенным поиском. Поддерживает etcd v2 и v3.
- [lucas](https://github.com/ringtail/lucas) — веб-средство просмотра ключей и значений для кластера kubernetes etcd3.0+.
- [etcd-manager](https://etcdmanager.io) — современный, эффективный, многоплатформенный и бесплатный графический интерфейс и клиентский инструмент etcd 3.x. Доступен для Windows, Linux и Mac.
- [etcd-backup-restore](https://github.com/gardener/etcd-backup-restore) — утилита для периодического инкрементного резервного копирования и восстановления etcd.
- [etcd-druid](https://github.com/gardener/etcd-druid) — оператор Kubernetes для развёртывания кластеров etcd и управления эксплуатационными операциями 2-го дня.
- [etcdadm](https://github.com/kubernetes-sigs/etcdadm) — инструмент командной строки для эксплуатации кластера etcd.
- [etcd-defrag](https://github.com/ahrtr/etcd-defrag) — более удобный и интеллектуальный инструмент дефрагментации etcd.
- [etcdhelper](https://github.com/tsonglew/intellij-etcdhelper) — плагин платформы intellij для etcd.

## Библиотеки {#libraries}

В следующих разделах клиентские библиотеки etcd перечислены по языкам.

### Go {#go}

- [etcd/client/v3](https://github.com/etcd-io/etcd/tree/main/client/v3) — официально сопровождаемый клиент Go для v3
- [go-etcd](https://github.com/coreos/go-etcd) — устаревший официальный клиент. Может пригодиться для старых версий etcd (<2.0.0).
- [encWrapper](https://github.com/lumjjb/etcd/tree/enc_wrapper/clientwrap/encwrapper) — оболочка шифрования для API Keys/KV клиента etcd.

### Java {#java}

- [coreos/jetcd](https://github.com/etcd-io/jetcd) — поддерживает v3
- [justinsb/jetcd](https://github.com/justinsb/jetcd)
- [cdancy/etcd-rest](https://github.com/cdancy/etcd-rest) — использует jclouds для полной реализации API v2.
- [IBM/etcd-java](https://github.com/IBM/etcd-java)

### Scala {#scala}

- [maciej/etcd-client](https://github.com/maciej/etcd-client) — поддерживает v2. Полностью асинхронный клиент на основе Akka HTTP
- [eiipii/etcdhttpclient](https://bitbucket.org/eiipii/etcdhttpclient) — поддерживает v2. Асинхронный клиент HTTP на основе Netty и Scala Futures.
- [mingchuno/etcd4s](https://github.com/mingchuno/etcd4s) — поддерживает v3 через gRPC с необязательной поддержкой Akka Stream.

### Perl {#perl}

- [hexfusion/perl-net-etcd](https://github.com/hexfusion/perl-net-etcd) — поддерживает HTTP API шлюза grpc v3
- [robn/p5-etcd](https://github.com/robn/p5-etcd) — поддерживает v2

### Python {#python}

- [kragniz/python-etcd3](https://github.com/kragniz/python-etcd3) — клиент для v3
- [jplana/python-etcd](https://github.com/jplana/python-etcd) — поддерживает v2
- [russellhaering/txetcd](https://github.com/russellhaering/txetcd) — библиотека Twisted для Python
- [cholcombe973/autodock](https://github.com/cholcombe973/autodock) — инструмент автоматизации развёртывания Docker
- [lisael/aioetcd](https://github.com/lisael/aioetcd) — клиент на корутинах Asyncio (Python 3.4+), поддерживает v2
- [txaio-etcd](https://github.com/crossbario/txaio-etcd) — асинхронная клиентская библиотека только для etcd v3: для Twisted сейчас и asyncio в будущем
- [dims/etcd3-gateway](https://github.com/dims/etcd3-gateway) — библиотека API etcd v3, использующая HTTP-шлюз grpc
- [aioetcd3](https://github.com/gaopeiliang/aioetcd3) — API etcd v3 для asyncio (Python 3.6+)
- [Revolution1/etcd3-py](https://github.com/Revolution1/etcd3-py) — клиент Python для etcd v3 (python2.7 и python3.5+), использующий gRPC-JSON-Gateway

### Node {#node}

- [mixer/etcd3](https://github.com/mixer/etcd3) — поддерживает v3
- [stianeikeland/node-etcd](https://github.com/stianeikeland/node-etcd) — поддерживает v2 (с Coffeescript)
- [lavagetto/nodejs-etcd](https://github.com/lavagetto/nodejs-etcd) — поддерживает v2
- [deedubs/node-etcd-config](https://github.com/deedubs/node-etcd-config) — поддерживает v2

### Ruby {#ruby}

- [iconara/etcd-rb](https://github.com/iconara/etcd-rb)
- [jpfuentes2/etcd-ruby](https://github.com/jpfuentes2/etcd-ruby)
- [ranjib/etcd-ruby](https://github.com/ranjib/etcd-ruby) — поддерживает v2
- [davissp14/etcdv3-ruby](https://github.com/davissp14/etcdv3-ruby) — поддерживает v3

### C {#c}

- [apache/celix/etcdlib](https://github.com/apache/celix/tree/master/libs/etcdlib) — поддерживает v2
- [jdarcy/etcd-api](https://github.com/jdarcy/etcd-api) — поддерживает v2
- [shafreeck/cetcd](https://github.com/shafreeck/cetcd) — поддерживает v2

### C++ {#c-1}

- [edwardcapriolo/etcdcpp](https://github.com/edwardcapriolo/etcdcpp) — поддерживает v2
- [suryanathan/etcdcpp](https://github.com/suryanathan/etcdcpp) — поддерживает v2 (с ожиданиями)
- [nokia/etcd-cpp-api](https://github.com/nokia/etcd-cpp-api) — поддерживает v2
- [etcd-cpp-apiv3/etcd-cpp-apiv3](https://github.com/etcd-cpp-apiv3/etcd-cpp-apiv3) — поддерживает v3

### Clojure {#clojure}

- [aterreno/etcd-clojure](https://github.com/aterreno/etcd-clojure)
- [dwwoelfel/cetcd](https://github.com/dwwoelfel/cetcd) — поддерживает v2
- [rthomas/clj-etcd](https://github.com/rthomas/clj-etcd) — поддерживает v2

### Erlang {#erlang}

- [marshall-lee/etcd.erl](https://github.com/marshall-lee/etcd.erl) — поддерживает v2
- [zhongwencool/eetcd](https://github.com/zhongwencool/eetcd) — поддерживает v3+ (только GRPC)

### Elixir {#elixir}

- [team-telnyx/etcdex](https://github.com/team-telnyx/etcdex) — поддерживает v3+ (только GRPC)

### .NET {#net}

- [wangjia184/etcdnet](https://github.com/wangjia184/etcdnet) — поддерживает v2
- [drusellers/etcetera](https://github.com/drusellers/etcetera)
- [shubhamranjan/dotnet-etcd](https://github.com/shubhamranjan/dotnet-etcd) — поддерживает v3+ (только GRPC)
- [SimplifyNet/Etcd.Microsoft.Extensions.Configuration](https://github.com/SimplifyNet/Etcd.Microsoft.Extensions.Configuration)

### PHP {#php}

- [linkorb/etcd-php](https://github.com/linkorb/etcd-php)
- [activecollab/etcd](https://github.com/activecollab/etcd)
- [ouqiang/etcd-php](https://github.com/ouqiang/etcd-php) — клиент для шлюза gRPC v3

### Haskell {#haskell}

- [wereHamster/etcd-hs](https://github.com/wereHamster/etcd-hs)

### R {#r}

- [ropensci/etseed](https://github.com/ropensci/etseed)

### Nim {#nim}

- [etcd_client](https://github.com/FedericoCeratto/nim-etcd-client)

### Tcl {#tcl}

- [efrecon/etcd-tcl](https://github.com/efrecon/etcd-tcl) — поддерживает v2, кроме ожидания.

### Rust {#rust}

- [jimmycuadra/rust-etcd](https://github.com/jimmycuadra/rust-etcd) — поддерживает v2

### Gradle {#gradle}

- [gradle-etcd-rest-plugin](https://github.com/cdancy/gradle-etcd-rest-plugin) — поддерживает v2

### Lua {#lua}

- [api7/lua-resty-etcd](https://github.com/api7/lua-resty-etcd) — поддерживает v2 и v3 (HTTP API шлюза grpc)

## Инструменты развёртывания {#deployment-tools}

### Интеграции Chef {#chef-integrations}

- [coderanger/etcd-chef](https://github.com/coderanger/etcd-chef)

### Рецепты Chef {#chef-cookbooks}

- [spheromak/etcd-cookbook](https://github.com/spheromak/etcd-cookbook)

### Выпуски BOSH {#bosh-releases}

- [cloudfoundry-community/etcd-boshrelease](https://github.com/cloudfoundry-community/etcd-boshrelease)
- [cloudfoundry/cf-release](https://github.com/cloudfoundry/cf-release/tree/master/jobs/etcd)

## Проекты, использующие etcd {#projects-using-etcd}

- [Пользователи Raft etcd](https://github.com/etcd-io/raft/blob/main/README.md#notable-users) — проекты, использующие реализацию библиотеки raft от etcd.
- [Apache APISIX](https://github.com/apache/apisix) — шлюз API, использующий etcd как хранилище конфигурации.
- [apache/celix](https://github.com/apache/celix) — адаптированная для C и C++ реализация спецификации OSGi
- [binocarlos/yoda](https://github.com/binocarlos/yoda) — etcd + ZeroMQ
- [blox/blox](https://github.com/blox/blox) — набор проектов с открытым исходным кодом для управления контейнерами и оркестрации с AWS ECS
- [calavera/active-proxy](https://github.com/calavera/active-proxy) — HTTP-прокси, настраиваемый с помощью etcd
- [chain/chain](https://github.com/chain/chain) — программное обеспечение для работы и соединения высокомасштабируемых блокчейн-сетей с контролем доступа
- [derekchiang/etcdplus](https://github.com/derekchiang/etcdplus) — набор примитивов распределённой синхронизации на основе etcd
- [go-discover](https://github.com/flynn/go-discover) — обнаружение служб на Go
- [gleicon/goreman](https://github.com/gleicon/goreman/tree/etcd) — ветвь клона Foreman на Go с поддержкой etcd
- [garethr/hiera-etcd](https://github.com/garethr/hiera-etcd) — бэкенд Puppet hiera на основе etcd
- [mattn/etcd-vim](https://github.com/mattn/etcd-vim) — операции SET и GET с ключами из vim
- [mattn/etcdenv](https://github.com/mattn/etcdenv) — шебанг "env" с интеграцией etcd
- [kelseyhightower/confd](https://github.com/kelseyhightower/confd) — управление локальными файлами конфигурации приложений с помощью шаблонов и данных etcd
- [configdb](https://git.autistici.org/ai/configdb/tree/master) — реляционная абстракция REST над произвольными бэкендами баз данных для хранения конфигураций и инвентарных данных.
- [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) — диспетчер контейнерных кластеров, созданный Google.
- [mailgun/vulcand](https://github.com/mailgun/vulcand) — HTTP-прокси, использующий etcd как бэкенд конфигурации.
- [duedil-ltd/discodns](https://github.com/duedil-ltd/discodns) — простой DNS-сервер имён, использующий etcd как базу данных имён и записей.
- [skynetservices/skydns](https://github.com/skynetservices/skydns) — DNS-сервер, соответствующий RFC
- [xordataexchange/crypt](https://github.com/xordataexchange/crypt) — безопасное хранение значений в etcd с шифрованием GPG
- [spf13/viper](https://github.com/spf13/viper) — библиотека конфигурации Go, читающая значения из ENV, pflags, файлов и etcd с необязательным шифрованием
- [lytics/metafora](https://github.com/lytics/metafora) — библиотека распределённых задач на Go
- [ryandoyle/nss-etcd](https://github.com/ryandoyle/nss-etcd) — модуль GNU libc NSS для разрешения имён из etcd.
- [Gru](https://github.com/dnaeon/gru) — упрощённая оркестрация на Go
- [Vitess](http://vitess.io/) — система кластеризации баз данных для горизонтального масштабирования MySQL.
- [lclarkmichalek/etcdhcp](https://github.com/lclarkmichalek/etcdhcp) — сервер DHCP, использующий etcd для постоянного хранения и координации.
- [openstack/networking-vpp](https://github.com/openstack/networking-vpp) — сетевой драйвер, программирующий [плоскость данных FD.io VPP](https://wiki.fd.io/view/VPP) для создания облачной виртуальной сети [OpenStack](https://www.openstack.org/)
- [OpenStack](https://github.com/openstack/governance/blob/master/reference/base-services.rst) — службы OpenStack могут использовать etcd как базовую службу.
- [CoreDNS](https://github.com/coredns/coredns/tree/master/plugin/etcd) — DNS-сервер CoreDNS, объединяющий плагины в цепочку и входящий в CNCF и Kubernetes
- [Uber M3](https://github.com/m3db/m3) — M3: крупномасштабная платформа метрик Uber с открытым исходным кодом для Prometheus
- [Rook](https://github.com/rook/rook) — оркестрация хранилища для Kubernetes
- [Patroni](https://github.com/zalando/patroni) — шаблон высокой доступности PostgreSQL с ZooKeeper, etcd или Consul
- [Trillian](https://github.com/google/trillian) — реализация дерева Меркла, содержимое которого обслуживается из уровня хранения данных, что позволяет масштабироваться до чрезвычайно больших деревьев.
- [purpleidea/mgmt](https://github.com/purpleidea/mgmt) — новое поколение распределённого, событийного и параллельного управления конфигурацией!
- [Portworx/kvdb](https://docs.portworx.com/concepts/internal-kvdb/) — внутреннее хранилище kvdb для конфигурации кластера Portworx.
- [Apache Pulsar](https://pulsar.apache.org/) — распределённая платформа обмена сообщениями и потоковой обработки с открытым исходным кодом, созданная для облака.
