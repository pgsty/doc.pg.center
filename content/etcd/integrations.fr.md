---
title: Bibliothèques et outils
weight: 1300
description: Liste des outils et bibliothèques clientes etcd
icon: fa-solid fa-puzzle-piece
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/integrations.md"
---

Notez que les bibliothèques et outils tiers (non hébergés sur https://github.com/etcd-io) mentionnés ci-dessous ne sont pas testés ni entretenus par l'équipe etcd. Avant de les utiliser, les utilisateurs sont invités à les lire et à les examiner.

## Outils {#tools}

- [etcdctl](https://github.com/etcd-io/etcd/tree/main/etcdctl) - Client en ligne de commande pour etcd
- [etcd-dump](https://npmjs.org/package/etcd-dump) - Utilitaire en ligne de commande pour sauvegarder/restaurer etcd.
- [etcd-fs](https://github.com/xetorthio/etcd-fs) - Système de fichiers FUSE pour etcd
- [etcddir](https://github.com/rekby/etcddir) - Synchronisation en temps réel entre etcd et un répertoire local. Fonctionne sous Windows et Linux.
- [etcd-browser](https://github.com/henszey/etcd-browser) - Éditeur web de magasin clé-valeur pour etcd utilisant AngularJS
- [etcd-lock](https://github.com/datawisesystems/etcd-lock) - Implémentation d'élection de maître et de verrouillage lecture/écriture distribué utilisant etcd - Prend en charge la version 2
- [etcd-console](https://github.com/matishsiao/etcd-console) - Éditeur web de magasin clé-valeur pour etcd utilisant PHP
- [etcd-viewer](https://github.com/nikfoundas/etcd-viewer) - Éditeur/visualiseur de magasin clé-valeur etcd écrit en Java
- [etcdtool](https://github.com/mickep76/etcdtool) - Export/Import/Edit répertoire etcd en tant que JSON/YAML/TOML et validation du répertoire à l’aide d’un schéma JSON
- [etcdloadtest](https://github.com/sinsharat/etcdloadtest) - Client de test de charge en ligne de commande pour etcd 3.0 et versions ultérieures
- [etcd-tui](https://github.com/olamilekan000/etcd-tui) - Une interface utilisateur moderne en mode terminal (TUI) pour interagir avec votre base de données etcd. Parcourez les clés, affichez les valeurs, filtrez les données et gérez votre cluster etcd directement depuis votre terminal.
- [etcdfinder](https://etcdfinder.github.io) - Une interface web moderne et ultra-rapide pour etcd, avec recherche instantanée. Prend en charge à la fois etcd v2 et v3.
- [lucas](https://github.com/ringtail/lucas) - Un visualiseur de paires clé-valeur basé sur web pour les clusters etcd3.0+ de Kubernetes.
- [etcd-manager](https://etcdmanager.io) - Outil graphique et client moderne, efficace, multiplateforme et gratuit pour etcd 3.x. Disponible pour Windows, Linux et Mac.
- [etcd-backup-restore](https://github.com/gardener/etcd-backup-restore) - Utilitaire permettant de sauvegarder et de restaurer de manière périodique et incrémentielle etcd.
- [etcd-druid](https://github.com/gardener/etcd-druid) - Opérateur Kubernetes permettant de déployer des clusters etcd et de gérer les opérations de gestion de jour 2.
- [etcdadm](https://github.com/kubernetes-sigs/etcdadm) - Outil en ligne de commande pour gérer un cluster etcd.
- [etcd-defrag](https://github.com/ahrtr/etcd-defrag) - Outil de défragmentation etcd plus facile à utiliser et plus intelligent.
- [etcdhelper](https://github.com/tsonglew/intellij-etcdhelper) - Plugin pour la plateforme IntelliJ pour etcd.

## Bibliothèques {#libraries}

Les sections ci-dessous listent les bibliothèques clientes etcd par langage.

### Go {#go}

- [etcd/client/v3](https://github.com/etcd-io/etcd/tree/main/client/v3) - le client Go officiellement maintenu pour la version v3
- [go-etcd](https://github.com/coreos/go-etcd) - le client officiel déprécié. Peut être utile pour les versions plus anciennes (<2.0.0) d'etcd.
- [encWrapper](https://github.com/lumjjb/etcd/tree/enc_wrapper/clientwrap/encwrapper) - encWrapper est une enveloppe de chiffrement pour l'API Keys du client etcd/KV.

### Java {#java}

- [coreos/jetcd](https://github.com/etcd-io/jetcd) - Prise en charge de la version 3
- [justinsb/jetcd](https://github.com/justinsb/jetcd)
- [cdancy/etcd-rest](https://github.com/cdancy/etcd-rest) - Utilise jclouds pour offrir une implémentation complète de l'API version 2.
- [IBM/etcd-java](https://github.com/IBM/etcd-java)

### Scala {#scala}

- [maciej/etcd-client](https://github.com/maciej/etcd-client) - Prise en charge de la version 2. Client entièrement asynchrone basé sur Akka HTTP
- [eiipii/etcdhttpclient](https://bitbucket.org/eiipii/etcdhttpclient) - Prise en charge de la version 2. Client HTTP asynchrone basé sur Netty et les futures Scala.
- [mingchuno/etcd4s](https://github.com/mingchuno/etcd4s) - Prise en charge de la version 3 via gRPC, avec prise en charge optionnelle d'Akka Stream.

### Perl {#perl}

- [hexfusion/perl-net-etcd](https://github.com/hexfusion/perl-net-etcd) - Prise en charge de l'API HTTP du passerelle gRPC v3
- [robn/p5-etcd](https://github.com/robn/p5-etcd) - Prise en charge de la version 2

### Python {#python}

- [kragniz/python-etcd3](https://github.com/kragniz/python-etcd3) - Client pour la version 3
- [jplana/python-etcd](https://github.com/jplana/python-etcd) - Prise en charge de la version 2
- [russellhaering/txetcd](https://github.com/russellhaering/txetcd) - Bibliothèque Python Twisted
- [cholcombe973/autodock](https://github.com/cholcombe973/autodock) - Outil d'automatisation du déploiement Docker
- [lisael/aioetcd](https://github.com/lisael/aioetcd) - Client basé sur des coroutines asyncio (Python 3.4+) (Prise en charge de la version 2)
- [txaio-etcd](https://github.com/crossbario/txaio-etcd) - Bibliothèque cliente asynchrone pour etcd v3 uniquement, pour Twisted (actuellement) et asyncio (à venir)
- [dims/etcd3-gateway](https://github.com/dims/etcd3-gateway) - Bibliothèque d'API etcd v3 utilisant la passerelle HTTP grpc
- [aioetcd3](https://github.com/gaopeiliang/aioetcd3) - API etcd v3 pour asyncio (Python 3.6+)
- [Revolution1/etcd3-py](https://github.com/Revolution1/etcd3-py) - Client Python pour etcd v3 (python2.7 et python3.5+), utilisant gRPC-JSON-Gateway

### Nœud {#node}

- [mixer/etcd3](https://github.com/mixer/etcd3) - Prise en charge de la version 3
- [stianeikeland/node-etcd](https://github.com/stianeikeland/node-etcd) - Prise en charge de la version 2 (avec CoffeeScript)
- [lavagetto/nodejs-etcd](https://github.com/lavagetto/nodejs-etcd) - Prise en charge de la version 2
- [deedubs/node-etcd-config](https://github.com/deedubs/node-etcd-config) - Prise en charge de la version 2

### Ruby {#ruby}

- [iconara/etcd-rb](https://github.com/iconara/etcd-rb)
- [jpfuentes2/etcd-ruby](https://github.com/jpfuentes2/etcd-ruby)
- [ranjib/etcd-ruby](https://github.com/ranjib/etcd-ruby) - Prise en charge de la version 2
- [davissp14/etcdv3-ruby](https://github.com/davissp14/etcdv3-ruby) - Prise en charge de la version 3

### C {#c}

- [apache/celix/etcdlib](https://github.com/apache/celix/tree/master/libs/etcdlib) - Prise en charge de la version 2
- [jdarcy/etcd-api](https://github.com/jdarcy/etcd-api) - Prise en charge de la version 2
- [shafreeck/cetcd](https://github.com/shafreeck/cetcd) - Prise en charge de la version 2

### C++ {#c-1}

- [edwardcapriolo/etcdcpp](https://github.com/edwardcapriolo/etcdcpp) - Prise en charge de la version 2
- [suryanathan/etcdcpp](https://github.com/suryanathan/etcdcpp) - Prise en charge de la version 2 (avec attentes)
- [nokia/etcd-cpp-api](https://github.com/nokia/etcd-cpp-api) - Prise en charge de la version 2
- [etcd-cpp-apiv3/etcd-cpp-apiv3](https://github.com/etcd-cpp-apiv3/etcd-cpp-apiv3) - Prise en charge de la version 3

### Clojure {#clojure}

- [aterreno/etcd-clojure](https://github.com/aterreno/etcd-clojure)
- [dwwoelfel/cetcd](https://github.com/dwwoelfel/cetcd) - Prise en charge de la version 2
- [rthomas/clj-etcd](https://github.com/rthomas/clj-etcd) - Prise en charge de la version 2

### Erlang {#erlang}

- [marshall-lee/etcd.erl](https://github.com/marshall-lee/etcd.erl) - Prise en charge de la version 2
- [zhongwencool/eetcd](https://github.com/zhongwencool/eetcd) - Prise en charge de la version 3+ (GRPC uniquement)

### Élixir {#elixir}

- [team-telnyx/etcdex](https://github.com/team-telnyx/etcdex) - Prise en charge des versions v3+ (GRPC uniquement)

### .NET {#net}

- [wangjia184/etcdnet](https://github.com/wangjia184/etcdnet) - Prise en charge de la version 2
- [drusellers/etcetera](https://github.com/drusellers/etcetera)
- [shubhamranjan/dotnet-etcd](https://github.com/shubhamranjan/dotnet-etcd) - Prise en charge de la version 3+ (GRPC uniquement)
- [SimplifyNet/Etcd.Microsoft.Extensions.Configuration](https://github.com/SimplifyNet/Etcd.Microsoft.Extensions.Configuration)

### PHP {#php}

- [linkorb/etcd-php](https://github.com/linkorb/etcd-php)
- [activecollab/etcd](https://github.com/activecollab/etcd)
- [ouqiang/etcd-php](https://github.com/ouqiang/etcd-php) - Client pour la passerelle gRPC v3

### Haskell {#haskell}

- [wereHamster/etcd-hs](https://github.com/wereHamster/etcd-hs)

### R {#r}

- [ropensci/etseed](https://github.com/ropensci/etseed)

### Nim {#nim}

- [etcd_client](https://github.com/FedericoCeratto/nim-etcd-client)

### Tcl {#tcl}

- [efrecon/etcd-tcl](https://github.com/efrecon/etcd-tcl) - Prise en charge des versions v2, à l’exception de wait.

### Rust {#rust}

- [jimmycuadra/rust-etcd](https://github.com/jimmycuadra/rust-etcd) - Prise en charge de la version 2

### Gradle {#gradle}

- [gradle-etcd-rest-plugin](https://github.com/cdancy/gradle-etcd-rest-plugin) - Prise en charge de la version 2

### Lua {#lua}

- [api7/lua-resty-etcd](https://github.com/api7/lua-resty-etcd) - Prise en charge des versions v2 et v3 (API HTTP via passerelle gRPC)

## Outils de déploiement {#deployment-tools}

### Intégrations Chef {#chef-integrations}

- [coderanger/etcd-chef](https://github.com/coderanger/etcd-chef)

### Recettes Chef {#chef-cookbooks}

- [spheromak/etcd-cookbook](https://github.com/spheromak/etcd-cookbook)

### Libérations BOSH {#bosh-releases}

- [cloudfoundry-community/etcd-boshrelease](https://github.com/cloudfoundry-community/etcd-boshrelease)
- [cloudfoundry/cf-release](https://github.com/cloudfoundry/cf-release/tree/master/jobs/etcd)

## Projets utilisant etcd {#projects-using-etcd}

- [Utilisateurs Raft etcd](https://github.com/etcd-io/raft/blob/main/README.md#notable-users) - projets utilisant l'implémentation de la bibliothèque Raft d'etcd.
- [Apache APISIX](https://github.com/apache/apisix) - une passerelle API qui utilise etcd comme magasin de configuration.
- [apache/celix](https://github.com/apache/celix) - une implémentation de la spécification OSGi adaptée au C et au C++
- [binocarlos/yoda](https://github.com/binocarlos/yoda) - etcd + ZeroMQ
- [blox/blox](https://github.com/blox/blox) - une collection de projets open source pour la gestion et l'orchestration de conteneurs avec AWS ECS
- [calavera/active-proxy](https://github.com/calavera/active-proxy) - proxy HTTP configuré avec etcd
- [chain/chain](https://github.com/chain/chain) - logiciel conçu pour fonctionner et se connecter à des réseaux de blockchains permissionnées hautement évolutifs
- [derekchiang/etcdplus](https://github.com/derekchiang/etcdplus) - Un ensemble de primitives de synchronisation distribuée basées sur etcd
- [go-discover](https://github.com/flynn/go-discover) - Découverte de services en Go
- [gleicon/goreman](https://github.com/gleicon/goreman/tree/etcd) - Branche du clone Go Foreman avec prise en charge d'etcd
- [garethr/hiera-etcd](https://github.com/garethr/hiera-etcd) - Backend Puppet Hiera utilisant etcd
- [mattn/etcd-vim](https://github.com/mattn/etcd-vim) - Définir et lire des clés depuis l'intérieur de vim
- [mattn/etcdenv](https://github.com/mattn/etcdenv) - Shebang « env » avec intégration à etcd
- [kelseyhightower/confd](https://github.com/kelseyhightower/confd) - Gérer les fichiers de configuration d'applications locales à l'aide de modèles et de données provenant d'etcd
- [configdb](https://git.autistici.org/ai/configdb/tree/master) - Une abstraction relationnelle REST au-dessus de backends de bases de données arbitraires, destinée au stockage de configurations et d'inventaires.
- [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) - Gestionnaire de cluster conteneurs développé par Google.
- [mailgun/vulcand](https://github.com/mailgun/vulcand) - Proxy HTTP utilisant etcd comme backend de configuration.
- [duedil-ltd/discodns](https://github.com/duedil-ltd/discodns) - Serveur DNS simple utilisant etcd comme base de données pour les noms et les enregistrements.
- [skynetservices/skydns](https://github.com/skynetservices/skydns) - Serveur DNS conforme aux RFC
- [xordataexchange/crypt](https://github.com/xordataexchange/crypt) - Stocker en toute sécurité des valeurs dans etcd à l'aide du chiffrement GPG
- [spf13/viper](https://github.com/spf13/viper) - Bibliothèque de configuration Go, lit les valeurs depuis les variables d'environnement, les drapeaux pflags, les fichiers et etcd, avec chiffrement facultatif
- [lytics/metafora](https://github.com/lytics/metafora) - Bibliothèque Go de tâches distribuées
- [ryandoyle/nss-etcd](https://github.com/ryandoyle/nss-etcd) - Module NSS GNU libc pour résoudre les noms à partir d'etcd.
- [Gru](https://github.com/dnaeon/gru) - Orchestration simplifiée avec Go
- [Vitess](http://vitess.io/) - Vitess est un système de clustering de bases de données pour le dimensionnement horizontal de MySQL.
- [lclarkmichalek/etcdhcp](https://github.com/lclarkmichalek/etcdhcp) - Serveur DHCP utilisant etcd pour la persistance et la coordination.
- [openstack/networking-vpp](https://github.com/openstack/networking-vpp) - Un pilote de réseau qui programme le plan de données [FD.io VPP](https://wiki.fd.io/view/VPP) afin de fournir le réseau virtuel cloud [OpenStack](https://www.openstack.org/)
- [OpenStack](https://github.com/openstack/governance/blob/master/reference/base-services.rst) - Les services OpenStack peuvent s'appuyer sur etcd comme service de base.
- [CoreDNS](https://github.com/coredns/coredns/tree/master/plugin/etcd) - CoreDNS est un serveur DNS qui chaîne des plugins, membre du CNCF et de Kubernetes
- [Uber M3](https://github.com/m3db/m3) - M3 : plateforme open source à grande échelle pour les métriques, développée par Uber, compatible Prometheus
- [Rook](https://github.com/rook/rook) - Orchestration du stockage pour Kubernetes
- [Patroni](https://github.com/zalando/patroni) - Modèle pour la haute disponibilité de PostgreSQL avec ZooKeeper, etcd ou Consul
- [Trillian](https://github.com/google/trillian) - Trillian implémente un arbre de Merkle dont le contenu est fourni par une couche de stockage de données, afin de permettre une évolutivité à des arbres extrêmement volumineux.
- [purpleidea/mgmt](https://github.com/purpleidea/mgmt) - Gestion de configuration distribuée, événementielle et parallèle de nouvelle génération !
- [Portworx/kvdb](https://docs.portworx.com/concepts/internal-kvdb/) - Le kvdb interne destiné au stockage de la configuration du cluster Portworx.
- [Apache Pulsar](https://pulsar.apache.org/) - Apache Pulsar est une plateforme de messagerie et de diffusion en continu open source, distribuée, conçue pour le cloud.
