---
title: "Bibliotheken und Werkzeuge"
weight: 1300
description: "Eine Übersicht über etcd-Werkzeuge und Clientbibliotheken"
icon: fa-solid fa-puzzle-piece
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/integrations.md"
aliases: [/etcd/integrations/]
---

Die unten aufgeführten Bibliotheken und Werkzeuge von Drittanbietern, die nicht unter https://github.com/etcd-io gehostet werden, werden vom etcd-Team weder getestet noch gepflegt. Es wird empfohlen, sich vor der Verwendung darüber zu informieren und sie zu prüfen.

## Werkzeuge {#tools}

- [etcdctl](https://github.com/etcd-io/etcd/tree/main/etcdctl) - Ein Befehlszeilenclient für etcd
- [etcd-dump](https://npmjs.org/package/etcd-dump) - Befehlszeilenwerkzeug zum Exportieren und Wiederherstellen von etcd.
- [etcd-fs](https://github.com/xetorthio/etcd-fs) - FUSE-Dateisystem für etcd
- [etcddir](https://github.com/rekby/etcddir) - Echtzeitsynchronisierung zwischen etcd und einem lokalen Verzeichnis. Funktioniert unter Windows und Linux.
- [etcd-browser](https://github.com/henszey/etcd-browser) - Ein webbasierter Schlüssel-Wert-Editor für etcd mit AngularJS
- [etcd-lock](https://github.com/datawisesystems/etcd-lock) - Implementierung von Master-Wahl und verteilten Lese-/Schreibsperren mit etcd – Unterstützt v2
- [etcd-console](https://github.com/matishsiao/etcd-console) - Ein webbasierter Schlüssel-Wert-Editor für etcd mit PHP
- [etcd-viewer](https://github.com/nikfoundas/etcd-viewer) - Ein in Java geschriebener Editor und Betrachter für den etcd-Schlüssel-Wert-Speicher
- [etcdtool](https://github.com/mickep76/etcdtool) - etcd-Verzeichnisse als JSON/YAML/TOML exportieren, importieren und bearbeiten sowie mit JSON-Schema validieren
- [etcdloadtest](https://github.com/sinsharat/etcdloadtest) - Ein Befehlszeilenclient für Lasttests mit etcd ab Version 3.0.
- [etcd-tui](https://github.com/olamilekan000/etcd-tui) - Eine moderne Terminaloberfläche (TUI) für die Interaktion mit einer etcd-Datenbank. Durch Schlüssel navigieren, Werte anzeigen, Daten filtern und den etcd-Cluster direkt im Terminal verwalten.
- [etcdfinder](https://etcdfinder.github.io) - Eine sehr schnelle, moderne Weboberfläche (UI) für etcd mit Sofortsuche. Unterstützt sowohl etcd v2 als auch v3.
- [lucas](https://github.com/ringtail/lucas) - Ein webbasierter Betrachter für Schlüssel-Wert-Paare in Kubernetes-Clustern mit etcd3.0+.
- [etcd-manager](https://etcdmanager.io) - Eine moderne, effiziente, plattformübergreifende und kostenlose GUI samt Clientwerkzeug für etcd 3.x. Verfügbar für Windows, Linux und Mac.
- [etcd-backup-restore](https://github.com/gardener/etcd-backup-restore) - Werkzeug für regelmäßige inkrementelle Backups und die Wiederherstellung von etcd.
- [etcd-druid](https://github.com/gardener/etcd-druid) - Ein Kubernetes-Operator zum Bereitstellen von etcd-Clustern und zur Verwaltung des laufenden Betriebs (day-2).
- [etcdadm](https://github.com/kubernetes-sigs/etcdadm) - Ein Befehlszeilenwerkzeug zum Betreiben eines etcd-Clusters.
- [etcd-defrag](https://github.com/ahrtr/etcd-defrag) - Ein einfacher bedienbares und intelligenteres Werkzeug zur Defragmentierung von etcd.
- [etcdhelper](https://github.com/tsonglew/intellij-etcdhelper) - Ein etcd-Plugin für die IntelliJ-Plattform.

## Bibliotheken {#libraries}

Die folgenden Abschnitte führen etcd-Clientbibliotheken nach Programmiersprache auf.

### Go {#go}

- [etcd/client/v3](https://github.com/etcd-io/etcd/tree/main/client/v3) - Der offiziell gepflegte Go-Client für v3
- [go-etcd](https://github.com/coreos/go-etcd) - Der veraltete offizielle Client. Kann für ältere etcd-Versionen (<2.0.0) nützlich sein.
- [encWrapper](https://github.com/lumjjb/etcd/tree/enc_wrapper/clientwrap/encwrapper) - encWrapper ist ein Verschlüsselungs-Wrapper für die Keys API/KV des etcd-Clients.

### Java {#java}

- [coreos/jetcd](https://github.com/etcd-io/jetcd) - Unterstützt v3
- [justinsb/jetcd](https://github.com/justinsb/jetcd)
- [cdancy/etcd-rest](https://github.com/cdancy/etcd-rest) - Verwendet jclouds für eine vollständige Implementierung der v2-API.
- [IBM/etcd-java](https://github.com/IBM/etcd-java)

### Scala {#scala}

- [maciej/etcd-client](https://github.com/maciej/etcd-client) - Unterstützt v2. Vollständig asynchroner Client auf Basis von Akka HTTP
- [eiipii/etcdhttpclient](https://bitbucket.org/eiipii/etcdhttpclient) - Unterstützt v2. Asynchroner HTTP-Client auf Basis von Netty und Scala Futures.
- [mingchuno/etcd4s](https://github.com/mingchuno/etcd4s) - Unterstützt v3 über gRPC, mit optionaler Unterstützung für Akka Stream.

### Perl {#perl}

- [hexfusion/perl-net-etcd](https://github.com/hexfusion/perl-net-etcd) - Unterstützt die HTTP-API des gRPC-Gateways für v3
- [robn/p5-etcd](https://github.com/robn/p5-etcd) - Unterstützt v2

### Python {#python}

- [kragniz/python-etcd3](https://github.com/kragniz/python-etcd3) - Client für v3
- [jplana/python-etcd](https://github.com/jplana/python-etcd) - Unterstützt v2
- [russellhaering/txetcd](https://github.com/russellhaering/txetcd) - Eine Python-Bibliothek für Twisted
- [cholcombe973/autodock](https://github.com/cholcombe973/autodock) - Ein Werkzeug zur Automatisierung von Docker-Bereitstellungen
- [lisael/aioetcd](https://github.com/lisael/aioetcd) - (Python 3.4+) Client mit Asyncio-Koroutinen (Unterstützt v2)
- [txaio-etcd](https://github.com/crossbario/txaio-etcd) - Asynchrone Clientbibliothek ausschließlich für etcd v3, für Twisted (heute) und asyncio (künftig)
- [dims/etcd3-gateway](https://github.com/dims/etcd3-gateway) - Bibliothek für die etcd-v3-API über das HTTP-gRPC-Gateway
- [aioetcd3](https://github.com/gaopeiliang/aioetcd3) - (Python 3.6+) etcd-v3-API für asyncio
- [Revolution1/etcd3-py](https://github.com/Revolution1/etcd3-py) - (python2.7 und python3.5+) Python-Client für etcd v3 über das gRPC-JSON-Gateway

### Node {#node}

- [mixer/etcd3](https://github.com/mixer/etcd3) - Unterstützt v3
- [stianeikeland/node-etcd](https://github.com/stianeikeland/node-etcd) - Unterstützt v2 (mit Coffeescript)
- [lavagetto/nodejs-etcd](https://github.com/lavagetto/nodejs-etcd) - Unterstützt v2
- [deedubs/node-etcd-config](https://github.com/deedubs/node-etcd-config) - Unterstützt v2

### Ruby {#ruby}

- [iconara/etcd-rb](https://github.com/iconara/etcd-rb)
- [jpfuentes2/etcd-ruby](https://github.com/jpfuentes2/etcd-ruby)
- [ranjib/etcd-ruby](https://github.com/ranjib/etcd-ruby) - Unterstützt v2
- [davissp14/etcdv3-ruby](https://github.com/davissp14/etcdv3-ruby) - Unterstützt v3

### C {#c}

- [apache/celix/etcdlib](https://github.com/apache/celix/tree/master/libs/etcdlib) - Unterstützt v2
- [jdarcy/etcd-api](https://github.com/jdarcy/etcd-api) - Unterstützt v2
- [shafreeck/cetcd](https://github.com/shafreeck/cetcd) - Unterstützt v2

### C++ {#c-1}

- [edwardcapriolo/etcdcpp](https://github.com/edwardcapriolo/etcdcpp) - Unterstützt v2
- [suryanathan/etcdcpp](https://github.com/suryanathan/etcdcpp) - Unterstützt v2 (mit Warteoperationen)
- [nokia/etcd-cpp-api](https://github.com/nokia/etcd-cpp-api) - Unterstützt v2
- [etcd-cpp-apiv3/etcd-cpp-apiv3](https://github.com/etcd-cpp-apiv3/etcd-cpp-apiv3) - Unterstützt v3

### Clojure {#clojure}

- [aterreno/etcd-clojure](https://github.com/aterreno/etcd-clojure)
- [dwwoelfel/cetcd](https://github.com/dwwoelfel/cetcd) - Unterstützt v2
- [rthomas/clj-etcd](https://github.com/rthomas/clj-etcd) - Unterstützt v2

### Erlang {#erlang}

- [marshall-lee/etcd.erl](https://github.com/marshall-lee/etcd.erl) - Unterstützt v2
- [zhongwencool/eetcd](https://github.com/zhongwencool/eetcd) - Unterstützt v3+ (nur GRPC)

### Elixir {#elixir}

- [team-telnyx/etcdex](https://github.com/team-telnyx/etcdex) - Unterstützt v3+ (nur GRPC)

### .NET {#net}

- [wangjia184/etcdnet](https://github.com/wangjia184/etcdnet) - Unterstützt v2
- [drusellers/etcetera](https://github.com/drusellers/etcetera)
- [shubhamranjan/dotnet-etcd](https://github.com/shubhamranjan/dotnet-etcd) - Unterstützt v3+ (nur GRPC)
- [SimplifyNet/Etcd.Microsoft.Extensions.Configuration](https://github.com/SimplifyNet/Etcd.Microsoft.Extensions.Configuration)

### PHP {#php}

- [linkorb/etcd-php](https://github.com/linkorb/etcd-php)
- [activecollab/etcd](https://github.com/activecollab/etcd)
- [ouqiang/etcd-php](https://github.com/ouqiang/etcd-php) - Client für das gRPC-Gateway von v3

### Haskell {#haskell}

- [wereHamster/etcd-hs](https://github.com/wereHamster/etcd-hs)

### R {#r}

- [ropensci/etseed](https://github.com/ropensci/etseed)

### Nim {#nim}

- [etcd_client](https://github.com/FedericoCeratto/nim-etcd-client)

### Tcl {#tcl}

- [efrecon/etcd-tcl](https://github.com/efrecon/etcd-tcl) - Unterstützt v2, außer wait.

### Rust {#rust}

- [jimmycuadra/rust-etcd](https://github.com/jimmycuadra/rust-etcd) - Unterstützt v2

### Gradle {#gradle}

- [gradle-etcd-rest-plugin](https://github.com/cdancy/gradle-etcd-rest-plugin) - Unterstützt v2

### Lua {#lua}

- [api7/lua-resty-etcd](https://github.com/api7/lua-resty-etcd) - Unterstützt v2 und v3 (HTTP-API des gRPC-Gateways)

## Werkzeuge zur Bereitstellung {#deployment-tools}

### Chef-Integrationen {#chef-integrations}

- [coderanger/etcd-chef](https://github.com/coderanger/etcd-chef)

### Chef-Cookbooks {#chef-cookbooks}

- [spheromak/etcd-cookbook](https://github.com/spheromak/etcd-cookbook)

### BOSH-Releases {#bosh-releases}

- [cloudfoundry-community/etcd-boshrelease](https://github.com/cloudfoundry-community/etcd-boshrelease)
- [cloudfoundry/cf-release](https://github.com/cloudfoundry/cf-release/tree/master/jobs/etcd)

## Projekte, die etcd verwenden {#projects-using-etcd}

- [Nutzer von etcd-Raft](https://github.com/etcd-io/raft/blob/main/README.md#notable-users) - Projekte, die die Raft-Bibliotheksimplementierung von etcd verwenden.
- [Apache APISIX](https://github.com/apache/apisix) - Ein API-Gateway, das etcd als Konfigurationsspeicher verwendet.
- [apache/celix](https://github.com/apache/celix) - Eine für C und C++ angepasste Implementierung der OSGi-Spezifikation
- [binocarlos/yoda](https://github.com/binocarlos/yoda) - etcd + ZeroMQ
- [blox/blox](https://github.com/blox/blox) - Eine Sammlung von Open-Source-Projekten zur Containerverwaltung und -orchestrierung mit AWS ECS
- [calavera/active-proxy](https://github.com/calavera/active-proxy) - Ein mit etcd konfigurierter HTTP-Proxy
- [chain/chain](https://github.com/chain/chain) - Software zum Betreiben hochskalierbarer zugangsbeschränkter Blockchain-Netzwerke und zum Herstellen von Verbindungen zu ihnen
- [derekchiang/etcdplus](https://github.com/derekchiang/etcdplus) - Eine Sammlung verteilter Synchronisationsprimitive auf Basis von etcd
- [go-discover](https://github.com/flynn/go-discover) - Diensterkennung in Go
- [gleicon/goreman](https://github.com/gleicon/goreman/tree/etcd) - Zweig des Go-Foreman-Klons mit etcd-Unterstützung
- [garethr/hiera-etcd](https://github.com/garethr/hiera-etcd) - Puppet-hiera-Backend mit etcd
- [mattn/etcd-vim](https://github.com/mattn/etcd-vim) - Schlüssel mit SET und GET direkt in vim schreiben und lesen
- [mattn/etcdenv](https://github.com/mattn/etcdenv) - „env“-Shebang mit etcd-Integration
- [kelseyhightower/confd](https://github.com/kelseyhightower/confd) - Lokale Anwendungskonfigurationsdateien mit Vorlagen und Daten aus etcd verwalten
- [configdb](https://git.autistici.org/ai/configdb/tree/master) - Eine relationale REST-Abstraktion über beliebigen Datenbank-Backends zum Speichern von Konfigurationen und Inventaren.
- [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) - Von Google eingeführte Verwaltung für Containercluster.
- [mailgun/vulcand](https://github.com/mailgun/vulcand) - HTTP-Proxy, der etcd als Konfigurations-Backend verwendet.
- [duedil-ltd/discodns](https://github.com/duedil-ltd/discodns) - Einfacher DNS-Nameserver, der etcd als Datenbank für Namen und Einträge verwendet.
- [skynetservices/skydns](https://github.com/skynetservices/skydns) - RFC-konformer DNS-Server
- [xordataexchange/crypt](https://github.com/xordataexchange/crypt) - Werte mit GPG-Verschlüsselung sicher in etcd speichern
- [spf13/viper](https://github.com/spf13/viper) - Go-Konfigurationsbibliothek; liest Werte aus ENV, pflags, Dateien und etcd, mit optionaler Verschlüsselung
- [lytics/metafora](https://github.com/lytics/metafora) - Go-Bibliothek für verteilte Aufgaben
- [ryandoyle/nss-etcd](https://github.com/ryandoyle/nss-etcd) - Ein GNU-libc-NSS-Modul zur Namensauflösung aus etcd.
- [Gru](https://github.com/dnaeon/gru) - Orchestrierung mit Go leicht gemacht
- [Vitess](http://vitess.io/) - Vitess ist ein Datenbank-Clustersystem zur horizontalen Skalierung von MySQL.
- [lclarkmichalek/etcdhcp](https://github.com/lclarkmichalek/etcdhcp) - DHCP-Server, der etcd für Persistenz und Koordination verwendet.
- [openstack/networking-vpp](https://github.com/openstack/networking-vpp) - Ein Netzwerktreiber, der die [FD.io-VPP-Datenebene](https://wiki.fd.io/view/VPP) programmiert, um virtuelle Cloud-Netzwerke für [OpenStack](https://www.openstack.org/) bereitzustellen
- [OpenStack](https://github.com/openstack/governance/blob/master/reference/base-services.rst) - OpenStack-Dienste können etcd als Basisdienst verwenden.
- [CoreDNS](https://github.com/coredns/coredns/tree/master/plugin/etcd) - CoreDNS ist ein DNS-Server mit verketteten Plugins und Teil von CNCF und Kubernetes
- [Uber M3](https://github.com/m3db/m3) - M3: Ubers Open-Source-Metrikplattform für Prometheus im großen Maßstab
- [Rook](https://github.com/rook/rook) - Speicherorchestrierung für Kubernetes
- [Patroni](https://github.com/zalando/patroni) - Eine Vorlage für PostgreSQL-Hochverfügbarkeit mit ZooKeeper, etcd oder Consul
- [Trillian](https://github.com/google/trillian) - Trillian implementiert einen Merkle-Baum, dessen Inhalte aus einer Datenspeicherschicht bereitgestellt werden, um die Skalierung auf extrem große Bäume zu ermöglichen.
- [purpleidea/mgmt](https://github.com/purpleidea/mgmt) - Verteilte, ereignisgesteuerte, parallele Konfigurationsverwaltung der nächsten Generation!
- [Portworx/kvdb](https://docs.portworx.com/concepts/internal-kvdb/) - Die interne kvdb zum Speichern der Portworx-Clusterkonfiguration.
- [Apache Pulsar](https://pulsar.apache.org/) - Apache Pulsar ist eine quelloffene, verteilte Messaging- und Streaming-Plattform für die Cloud.
