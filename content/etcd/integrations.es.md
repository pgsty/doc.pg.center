---
title: Bibliotecas y herramientas
weight: 1300
description: Un listado de herramientas y bibliotecas cliente de etcd
icon: fa-solid fa-puzzle-piece
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/integrations.md"
---

Ten en cuenta que las bibliotecas y herramientas de terceros (no alojadas en https://github.com/etcd-io) mencionadas a continuación no están probadas ni mantenidas por el equipo de etcd. Antes de usarlas, se recomienda a los usuarios leerlas e investigarlas.

## Herramientas {#tools}

- [etcdctl](https://github.com/etcd-io/etcd/tree/main/etcdctl) - Un cliente de línea de comandos para etcd
- [etcd-dump](https://npmjs.org/package/etcd-dump) - Utilidad de línea de comandos para volcar/restaurar etcd.
- [etcd-fs](https://github.com/xetorthio/etcd-fs) - Sistema de archivos FUSE para etcd
- [etcddir](https://github.com/rekby/etcddir) - Sincronización en tiempo real entre etcd y un directorio local. Funciona con Windows y Linux.
- [etcd-browser](https://github.com/henszey/etcd-browser) - Un editor web de clave/valor para etcd que usa AngularJS
- [etcd-lock](https://github.com/datawisesystems/etcd-lock) - Implementación de elección de maestro y bloqueo distribuido de lectura/escritura usando etcd - Soporta v2
- [etcd-console](https://github.com/matishsiao/etcd-console) - Un editor web de clave/valor para etcd que usa PHP
- [etcd-viewer](https://github.com/nikfoundas/etcd-viewer) - Un editor/visor del almacén clave-valor de etcd escrito en Java
- [etcdtool](https://github.com/mickep76/etcdtool) - Exporta/Importa/Edita un directorio de etcd como JSON/YAML/TOML y valida el directorio usando un esquema JSON
- [etcdloadtest](https://github.com/sinsharat/etcdloadtest) - Un cliente de prueba de carga de línea de comandos para etcd versión 3.0 y posteriores.
- [etcd-tui](https://github.com/olamilekan000/etcd-tui) - Una interfaz de usuario de terminal (TUI) moderna para interactuar con tu base de datos etcd. Navega por las claves, consulta valores, filtra datos y gestiona tu clúster de etcd directamente desde tu terminal.
- [etcdfinder](https://etcdfinder.github.io) - Una interfaz web moderna y ultrarrápida para etcd con búsqueda instantánea. Soporta tanto etcd v2 como v3.
- [lucas](https://github.com/ringtail/lucas) - Un visor web de clave-valor para clústeres etcd3.0+ de kubernetes.
- [etcd-manager](https://etcdmanager.io) - Una herramienta GUI y cliente para etcd 3.x moderna, eficiente, multiplataforma y gratuita. Disponible para Windows, Linux y Mac.
- [etcd-backup-restore](https://github.com/gardener/etcd-backup-restore) - Utilidad para hacer copias de seguridad y restaurar etcd de forma periódica e incremental.
- [etcd-druid](https://github.com/gardener/etcd-druid) - Un operador de Kubernetes para desplegar clústeres de etcd y gestionar las operaciones day-2.
- [etcdadm](https://github.com/kubernetes-sigs/etcdadm) - Una herramienta de línea de comandos para operar un clúster de etcd.
- [etcd-defrag](https://github.com/ahrtr/etcd-defrag) - Una herramienta de desfragmentación de etcd más fácil de usar y más inteligente.
- [etcdhelper](https://github.com/tsonglew/intellij-etcdhelper) - Un plugin de la plataforma IntelliJ para etcd.

## Bibliotecas {#libraries}

Las secciones siguientes enumeran las bibliotecas cliente de etcd por lenguaje.

### Go {#go}

- [etcd/client/v3](https://github.com/etcd-io/etcd/tree/main/client/v3) - el cliente Go mantenido oficialmente para v3
- [go-etcd](https://github.com/coreos/go-etcd) - el cliente oficial obsoleto. Puede ser útil para versiones antiguas (<2.0.0) de etcd.
- [encWrapper](https://github.com/lumjjb/etcd/tree/enc_wrapper/clientwrap/encwrapper) - encWrapper es un envoltorio de cifrado para la API Keys/KV del cliente de etcd.

### Java {#java}

- [coreos/jetcd](https://github.com/etcd-io/jetcd) - Soporta v3
- [justinsb/jetcd](https://github.com/justinsb/jetcd)
- [cdancy/etcd-rest](https://github.com/cdancy/etcd-rest) - Usa jclouds para proporcionar una implementación completa de la API v2.
- [IBM/etcd-java](https://github.com/IBM/etcd-java)

### Scala {#scala}

- [maciej/etcd-client](https://github.com/maciej/etcd-client) - Soporta v2. Cliente totalmente asíncrono basado en Akka HTTP
- [eiipii/etcdhttpclient](https://bitbucket.org/eiipii/etcdhttpclient) - Soporta v2. Cliente HTTP asíncrono basado en Netty y Scala Futures.
- [mingchuno/etcd4s](https://github.com/mingchuno/etcd4s) - Soporta v3 usando gRPC con soporte opcional de Akka Stream.

### Perl {#perl}

- [hexfusion/perl-net-etcd](https://github.com/hexfusion/perl-net-etcd) - Soporta la API HTTP de la pasarela gRPC v3
- [robn/p5-etcd](https://github.com/robn/p5-etcd) - Soporta v2

### Python {#python}

- [kragniz/python-etcd3](https://github.com/kragniz/python-etcd3) - Cliente para v3
- [jplana/python-etcd](https://github.com/jplana/python-etcd) - Soporta v2
- [russellhaering/txetcd](https://github.com/russellhaering/txetcd) - una biblioteca de Python para Twisted
- [cholcombe973/autodock](https://github.com/cholcombe973/autodock) - Una herramienta de automatización de despliegue de Docker
- [lisael/aioetcd](https://github.com/lisael/aioetcd) - (Python 3.4+) Cliente de corrutinas Asyncio (Soporta v2)
- [txaio-etcd](https://github.com/crossbario/txaio-etcd) - Biblioteca cliente asincrónica solo para etcd v3, para Twisted (hoy) y asyncio (futuro)
- [dims/etcd3-gateway](https://github.com/dims/etcd3-gateway) - Biblioteca de la API etcd v3 que usa la pasarela HTTP gRPC
- [aioetcd3](https://github.com/gaopeiliang/aioetcd3) - (Python 3.6+) API etcd v3 para asyncio
- [Revolution1/etcd3-py](https://github.com/Revolution1/etcd3-py) - (python2.7 y python3.5+) Cliente Python para etcd v3, usando gRPC-JSON-Gateway

### Node {#node}

- [mixer/etcd3](https://github.com/mixer/etcd3) - Soporta v3
- [stianeikeland/node-etcd](https://github.com/stianeikeland/node-etcd) - Soporta v2 (con Coffeescript)
- [lavagetto/nodejs-etcd](https://github.com/lavagetto/nodejs-etcd) - Soporta v2
- [deedubs/node-etcd-config](https://github.com/deedubs/node-etcd-config) - Soporta v2

### Ruby {#ruby}

- [iconara/etcd-rb](https://github.com/iconara/etcd-rb)
- [jpfuentes2/etcd-ruby](https://github.com/jpfuentes2/etcd-ruby)
- [ranjib/etcd-ruby](https://github.com/ranjib/etcd-ruby) - Soporta v2
- [davissp14/etcdv3-ruby](https://github.com/davissp14/etcdv3-ruby) - Soporta v3

### C {#c}

- [apache/celix/etcdlib](https://github.com/apache/celix/tree/master/libs/etcdlib) - Soporta v2
- [jdarcy/etcd-api](https://github.com/jdarcy/etcd-api) - Soporta v2
- [shafreeck/cetcd](https://github.com/shafreeck/cetcd) - Soporta v2

### C++ {#c-1}

- [edwardcapriolo/etcdcpp](https://github.com/edwardcapriolo/etcdcpp) - Soporta v2
- [suryanathan/etcdcpp](https://github.com/suryanathan/etcdcpp) - Soporta v2 (con wait)
- [nokia/etcd-cpp-api](https://github.com/nokia/etcd-cpp-api) - Soporta v2
- [etcd-cpp-apiv3/etcd-cpp-apiv3](https://github.com/etcd-cpp-apiv3/etcd-cpp-apiv3) - Soporta v3

### Clojure {#clojure}

- [aterreno/etcd-clojure](https://github.com/aterreno/etcd-clojure)
- [dwwoelfel/cetcd](https://github.com/dwwoelfel/cetcd) - Soporta v2
- [rthomas/clj-etcd](https://github.com/rthomas/clj-etcd) - Soporta v2

### Erlang {#erlang}

- [marshall-lee/etcd.erl](https://github.com/marshall-lee/etcd.erl) - Soporta v2
- [zhongwencool/eetcd](https://github.com/zhongwencool/eetcd) - Soporta v3+ (solo GRPC)

### Elixir {#elixir}

- [team-telnyx/etcdex](https://github.com/team-telnyx/etcdex) - Soporta v3+ (solo GRPC)

### .NET {#net}

- [wangjia184/etcdnet](https://github.com/wangjia184/etcdnet) - Soporta v2
- [drusellers/etcetera](https://github.com/drusellers/etcetera)
- [shubhamranjan/dotnet-etcd](https://github.com/shubhamranjan/dotnet-etcd) - Soporta v3+ (solo GRPC)
- [SimplifyNet/Etcd.Microsoft.Extensions.Configuration](https://github.com/SimplifyNet/Etcd.Microsoft.Extensions.Configuration)

### PHP {#php}

- [linkorb/etcd-php](https://github.com/linkorb/etcd-php)
- [activecollab/etcd](https://github.com/activecollab/etcd)
- [ouqiang/etcd-php](https://github.com/ouqiang/etcd-php) - Cliente para la pasarela gRPC v3

### Haskell {#haskell}

- [wereHamster/etcd-hs](https://github.com/wereHamster/etcd-hs)

### R {#r}

- [ropensci/etseed](https://github.com/ropensci/etseed)

### Nim {#nim}

- [etcd_client](https://github.com/FedericoCeratto/nim-etcd-client)

### Tcl {#tcl}

- [efrecon/etcd-tcl](https://github.com/efrecon/etcd-tcl) - Soporta v2, excepto wait.

### Rust {#rust}

- [jimmycuadra/rust-etcd](https://github.com/jimmycuadra/rust-etcd) - Soporta v2

### Gradle {#gradle}

- [gradle-etcd-rest-plugin](https://github.com/cdancy/gradle-etcd-rest-plugin) - Soporta v2

### Lua {#lua}

- [api7/lua-resty-etcd](https://github.com/api7/lua-resty-etcd) - Soporta v2 y v3 (API HTTP de la pasarela gRPC)

## Herramientas de despliegue {#deployment-tools}

### Integraciones Chef {#chef-integrations}

- [coderanger/etcd-chef](https://github.com/coderanger/etcd-chef)

### Cookbooks de Chef {#chef-cookbooks}

- [spheromak/etcd-cookbook](https://github.com/spheromak/etcd-cookbook)

### Releases BOSH {#bosh-releases}

- [cloudfoundry-community/etcd-boshrelease](https://github.com/cloudfoundry-community/etcd-boshrelease)
- [cloudfoundry/cf-release](https://github.com/cloudfoundry/cf-release/tree/master/jobs/etcd)

## Proyectos que usan etcd {#projects-using-etcd}

- [Usuarios de Raft de etcd](https://github.com/etcd-io/raft/blob/main/README.md#notable-users) - proyectos que usan la implementación de la biblioteca raft de etcd.
- [Apache APISIX](https://github.com/apache/apisix) - Una pasarela de API que usa etcd como almacén de configuración.
- [apache/celix](https://github.com/apache/celix) - una implementación de la especificación OSGi adaptada a C y C++
- [binocarlos/yoda](https://github.com/binocarlos/yoda) - etcd + ZeroMQ
- [blox/blox](https://github.com/blox/blox) - una colección de proyectos de código abierto para la gestión y orquestación de contenedores con AWS ECS
- [calavera/active-proxy](https://github.com/calavera/active-proxy) - Proxy HTTP configurado con etcd
- [chain/chain](https://github.com/chain/chain) - software diseñado para operar y conectarse a redes blockchain autorizadas altamente escalables
- [derekchiang/etcdplus](https://github.com/derekchiang/etcdplus) - Un conjunto de primitivas de sincronización distribuida construidas sobre etcd
- [go-discover](https://github.com/flynn/go-discover) - descubrimiento de servicios en Go
- [gleicon/goreman](https://github.com/gleicon/goreman/tree/etcd) - Rama del clon Go de Foreman con soporte de etcd
- [garethr/hiera-etcd](https://github.com/garethr/hiera-etcd) - Backend hiera de Puppet que usa etcd
- [mattn/etcd-vim](https://github.com/mattn/etcd-vim) - Hacer SET y GET de claves desde dentro de vim
- [mattn/etcdenv](https://github.com/mattn/etcdenv) - Shebang «env» con integración con etcd
- [kelseyhightower/confd](https://github.com/kelseyhightower/confd) - Gestionar archivos de configuración de aplicaciones locales usando plantillas y datos de etcd
- [configdb](https://git.autistici.org/ai/configdb/tree/master) - Una abstracción relacional REST sobre backends de bases de datos arbitrarios, orientada al almacenamiento de configuraciones e inventarios.
- [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) - Gestor de clústeres de contenedores presentado por Google.
- [mailgun/vulcand](https://github.com/mailgun/vulcand) - Proxy HTTP que usa etcd como backend de configuración.
- [duedil-ltd/discodns](https://github.com/duedil-ltd/discodns) - Servidor de nombres DNS simple que usa etcd como base de datos de nombres y registros.
- [skynetservices/skydns](https://github.com/skynetservices/skydns) - Servidor DNS conforme a las RFC
- [xordataexchange/crypt](https://github.com/xordataexchange/crypt) - Almacenar valores de forma segura en etcd usando cifrado GPG
- [spf13/viper](https://github.com/spf13/viper) - Biblioteca de configuración para Go, lee valores de variables de entorno, pflags, archivos y etcd, con cifrado opcional
- [lytics/metafora](https://github.com/lytics/metafora) - Biblioteca Go de tareas distribuidas
- [ryandoyle/nss-etcd](https://github.com/ryandoyle/nss-etcd) - Un módulo NSS de GNU libc para resolver nombres desde etcd.
- [Gru](https://github.com/dnaeon/gru) - La orquestación hecha fácil con Go
- [Vitess](http://vitess.io/) - Vitess es un sistema de agrupación de bases de datos para el escalado horizontal de MySQL.
- [lclarkmichalek/etcdhcp](https://github.com/lclarkmichalek/etcdhcp) - Servidor DHCP que usa etcd para la persistencia y la coordinación.
- [openstack/networking-vpp](https://github.com/openstack/networking-vpp) - Un controlador de red que programa el [plano de datos FD.io VPP](https://wiki.fd.io/view/VPP) para proporcionar red virtual en la nube de [OpenStack](https://www.openstack.org/)
- [OpenStack](https://github.com/openstack/governance/blob/master/reference/base-services.rst) - Los servicios de OpenStack pueden apoyarse en etcd como servicio base.
- [CoreDNS](https://github.com/coredns/coredns/tree/master/plugin/etcd) - CoreDNS es un servidor DNS que encadena plugins, parte de CNCF y Kubernetes
- [Uber M3](https://github.com/m3db/m3) - M3: la plataforma de métricas de código abierto y gran escala de Uber para Prometheus
- [Rook](https://github.com/rook/rook) - Orquestación de almacenamiento para Kubernetes
- [Patroni](https://github.com/zalando/patroni) - Una plantilla para la alta disponibilidad de PostgreSQL con ZooKeeper, etcd o Consul
- [Trillian](https://github.com/google/trillian) - Trillian implementa un árbol de Merkle cuyo contenido se sirve desde una capa de almacenamiento de datos, para permitir la escalabilidad a árboles extremadamente grandes.
- [purpleidea/mgmt](https://github.com/purpleidea/mgmt) - ¡Gestión de configuración distribuida, dirigida por eventos y paralela de nueva generación!
- [Portworx/kvdb](https://docs.portworx.com/concepts/internal-kvdb/) - El kvdb interno para almacenar la configuración del clúster de Portworx.
- [Apache Pulsar](https://pulsar.apache.org/) - Apache Pulsar es una plataforma de mensajería y streaming distribuida de código abierto, construida para la nube.
