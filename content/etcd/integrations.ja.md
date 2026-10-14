---
title: "ライブラリーとツール"
weight: 1300
description: "etcdのツールとクライアントライブラリーの一覧"
icon: fa-solid fa-puzzle-piece
categories: [リファレンス]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/integrations.md"
---

以下に挙げるサードパーティーのライブラリーやツール（https://github.com/etcd-io 以外で公開されているもの）は、etcdチームによるテストや保守の対象外です。利用する前に、それぞれのドキュメントを読み、調査することを推奨します。

## ツール {#tools}

- [etcdctl](https://github.com/etcd-io/etcd/tree/main/etcdctl) - etcd用コマンドラインクライアント。
- [etcd-dump](https://npmjs.org/package/etcd-dump) - etcdのダンプとリストアを行うコマンドラインユーティリティー。
- [etcd-fs](https://github.com/xetorthio/etcd-fs) - etcd用のFUSEファイルシステム。
- [etcddir](https://github.com/rekby/etcddir) - etcdとローカルディレクトリをリアルタイムに同期します。WindowsとLinuxで動作します。
- [etcd-browser](https://github.com/henszey/etcd-browser) - AngularJSを使用した、etcd用のWebベースのキー・バリューエディター。
- [etcd-lock](https://github.com/datawisesystems/etcd-lock) - etcdを使用したマスター選出と分散読み書きロックの実装。v2に対応します。
- [etcd-console](https://github.com/matishsiao/etcd-console) - PHPを使用した、etcd用のWebベースのキー・バリューエディター。
- [etcd-viewer](https://github.com/nikfoundas/etcd-viewer) - Javaで書かれた、etcdキー・バリューストアのエディター兼ビューアー。
- [etcdtool](https://github.com/mickep76/etcdtool) - etcdディレクトリのJSON/YAML/TOML形式でのエクスポート、インポート、編集と、JSONスキーマによるディレクトリの検証を行います。
- [etcdloadtest](https://github.com/sinsharat/etcdloadtest) - etcdバージョン3.0以降向けのコマンドライン負荷テストクライアント。
- [etcd-tui](https://github.com/olamilekan000/etcd-tui) - etcdデータベースを操作するためのモダンなターミナルユーザーインターフェース（TUI）。キーの参照、値の表示、データの絞り込み、etcdクラスターの管理をターミナルから直接行えます。
- [etcdfinder](https://etcdfinder.github.io) - 即時検索を備えた、etcd用の高速でモダンなWeb UI。etcd v2とv3の両方に対応します。
- [lucas](https://github.com/ringtail/lucas) - Kubernetesのetcd3.0以降のクラスター向けの、Webベースのキー・バリュービューアー。
- [etcd-manager](https://etcdmanager.io) - モダンで効率的な、複数のプラットフォームに対応する無料のetcd 3.x GUI兼クライアントツール。Windows、Linux、Macで利用できます。
- [etcd-backup-restore](https://github.com/gardener/etcd-backup-restore) - etcdの定期的な増分バックアップとリストアを行うユーティリティー。
- [etcd-druid](https://github.com/gardener/etcd-druid) - etcdクラスターのデプロイと導入後の運用を管理するKubernetesオペレーター。
- [etcdadm](https://github.com/kubernetes-sigs/etcdadm) - etcdクラスターを運用するためのコマンドラインツール。
- [etcd-defrag](https://github.com/ahrtr/etcd-defrag) - より使いやすく、賢く動作するetcdのデフラグメンテーションツール。
- [etcdhelper](https://github.com/tsonglew/intellij-etcdhelper) - etcd用のIntelliJプラットフォームプラグイン。

## ライブラリー {#libraries}

以下では、etcdのクライアントライブラリーを言語別に紹介します。

### Go {#go}

- [etcd/client/v3](https://github.com/etcd-io/etcd/tree/main/client/v3) - 公式に保守されているv3用Goクライアント。
- [go-etcd](https://github.com/coreos/go-etcd) - 非推奨となった公式クライアント。古いetcd（2.0.0未満）では役立つ場合があります。
- [encWrapper](https://github.com/lumjjb/etcd/tree/enc_wrapper/clientwrap/encwrapper) - etcdクライアントのKeys API/KV向けの暗号化ラッパー。

### Java {#java}

- [coreos/jetcd](https://github.com/etcd-io/jetcd) - v3に対応します。
- [justinsb/jetcd](https://github.com/justinsb/jetcd)
- [cdancy/etcd-rest](https://github.com/cdancy/etcd-rest) - jcloudsを使用したv2 APIの完全な実装。
- [IBM/etcd-java](https://github.com/IBM/etcd-java)

### Scala {#scala}

- [maciej/etcd-client](https://github.com/maciej/etcd-client) - v2に対応します。Akka HTTPベースの完全非同期クライアント。
- [eiipii/etcdhttpclient](https://bitbucket.org/eiipii/etcdhttpclient) - v2に対応します。NettyとScala Futuresを基盤とする非同期HTTPクライアント。
- [mingchuno/etcd4s](https://github.com/mingchuno/etcd4s) - gRPCでv3に対応し、必要に応じてAkka Streamも使用できます。

### Perl {#perl}

- [hexfusion/perl-net-etcd](https://github.com/hexfusion/perl-net-etcd) - v3 grpcゲートウェイのHTTP APIに対応します。
- [robn/p5-etcd](https://github.com/robn/p5-etcd) - v2に対応します。

### Python {#python}

- [kragniz/python-etcd3](https://github.com/kragniz/python-etcd3) - v3用クライアント。
- [jplana/python-etcd](https://github.com/jplana/python-etcd) - v2に対応します。
- [russellhaering/txetcd](https://github.com/russellhaering/txetcd) - Twisted用のPythonライブラリー。
- [cholcombe973/autodock](https://github.com/cholcombe973/autodock) - Dockerのデプロイ自動化ツール。
- [lisael/aioetcd](https://github.com/lisael/aioetcd) - （Python 3.4以降）Asyncioコルーチンクライアント。v2に対応します。
- [txaio-etcd](https://github.com/crossbario/txaio-etcd) - Twisted（現時点）とasyncio（将来）向けの、etcd v3専用の非同期クライアントライブラリー。
- [dims/etcd3-gateway](https://github.com/dims/etcd3-gateway) - HTTP grpcゲートウェイを使用するetcd v3 APIライブラリー。
- [aioetcd3](https://github.com/gaopeiliang/aioetcd3) - （Python 3.6以降）asyncio用のetcd v3 API。
- [Revolution1/etcd3-py](https://github.com/Revolution1/etcd3-py) - （python2.7およびpython3.5以降）gRPC-JSON-Gatewayを使用するetcd v3用Pythonクライアント。

### Node {#node}

- [mixer/etcd3](https://github.com/mixer/etcd3) - v3に対応します。
- [stianeikeland/node-etcd](https://github.com/stianeikeland/node-etcd) - v2に対応します（Coffeescriptを使用）。
- [lavagetto/nodejs-etcd](https://github.com/lavagetto/nodejs-etcd) - v2に対応します。
- [deedubs/node-etcd-config](https://github.com/deedubs/node-etcd-config) - v2に対応します。

### Ruby {#ruby}

- [iconara/etcd-rb](https://github.com/iconara/etcd-rb)
- [jpfuentes2/etcd-ruby](https://github.com/jpfuentes2/etcd-ruby)
- [ranjib/etcd-ruby](https://github.com/ranjib/etcd-ruby) - v2に対応します。
- [davissp14/etcdv3-ruby](https://github.com/davissp14/etcdv3-ruby) - v3に対応します。

### C {#c}

- [apache/celix/etcdlib](https://github.com/apache/celix/tree/master/libs/etcdlib) - v2に対応します。
- [jdarcy/etcd-api](https://github.com/jdarcy/etcd-api) - v2に対応します。
- [shafreeck/cetcd](https://github.com/shafreeck/cetcd) - v2に対応します。

### C++ {#c-1}

- [edwardcapriolo/etcdcpp](https://github.com/edwardcapriolo/etcdcpp) - v2に対応します。
- [suryanathan/etcdcpp](https://github.com/suryanathan/etcdcpp) - v2に対応します（待機機能あり）。
- [nokia/etcd-cpp-api](https://github.com/nokia/etcd-cpp-api) - v2に対応します。
- [etcd-cpp-apiv3/etcd-cpp-apiv3](https://github.com/etcd-cpp-apiv3/etcd-cpp-apiv3) - v3に対応します。

### Clojure {#clojure}

- [aterreno/etcd-clojure](https://github.com/aterreno/etcd-clojure)
- [dwwoelfel/cetcd](https://github.com/dwwoelfel/cetcd) - v2に対応します。
- [rthomas/clj-etcd](https://github.com/rthomas/clj-etcd) - v2に対応します。

### Erlang {#erlang}

- [marshall-lee/etcd.erl](https://github.com/marshall-lee/etcd.erl) - v2に対応します。
- [zhongwencool/eetcd](https://github.com/zhongwencool/eetcd) - v3以降に対応します（GRPCのみ）。

### Elixir {#elixir}

- [team-telnyx/etcdex](https://github.com/team-telnyx/etcdex) - v3以降に対応します（GRPCのみ）。

### .NET {#net}

- [wangjia184/etcdnet](https://github.com/wangjia184/etcdnet) - v2に対応します。
- [drusellers/etcetera](https://github.com/drusellers/etcetera)
- [shubhamranjan/dotnet-etcd](https://github.com/shubhamranjan/dotnet-etcd) - v3以降に対応します（GRPCのみ）。
- [SimplifyNet/Etcd.Microsoft.Extensions.Configuration](https://github.com/SimplifyNet/Etcd.Microsoft.Extensions.Configuration)

### PHP {#php}

- [linkorb/etcd-php](https://github.com/linkorb/etcd-php)
- [activecollab/etcd](https://github.com/activecollab/etcd)
- [ouqiang/etcd-php](https://github.com/ouqiang/etcd-php) - v3 gRPCゲートウェイ用クライアント。

### Haskell {#haskell}

- [wereHamster/etcd-hs](https://github.com/wereHamster/etcd-hs)

### R {#r}

- [ropensci/etseed](https://github.com/ropensci/etseed)

### Nim {#nim}

- [etcd_client](https://github.com/FedericoCeratto/nim-etcd-client)

### Tcl {#tcl}

- [efrecon/etcd-tcl](https://github.com/efrecon/etcd-tcl) - waitを除き、v2に対応します。

### Rust {#rust}

- [jimmycuadra/rust-etcd](https://github.com/jimmycuadra/rust-etcd) - v2に対応します。

### Gradle {#gradle}

- [gradle-etcd-rest-plugin](https://github.com/cdancy/gradle-etcd-rest-plugin) - v2に対応します。

### Lua {#lua}

- [api7/lua-resty-etcd](https://github.com/api7/lua-resty-etcd) - v2およびv3（grpcゲートウェイのHTTP API）に対応します。

## デプロイツール {#deployment-tools}

### Chefとの連携 {#chef-integrations}

- [coderanger/etcd-chef](https://github.com/coderanger/etcd-chef)

### Chefクックブック {#chef-cookbooks}

- [spheromak/etcd-cookbook](https://github.com/spheromak/etcd-cookbook)

### BOSHリリース {#bosh-releases}

- [cloudfoundry-community/etcd-boshrelease](https://github.com/cloudfoundry-community/etcd-boshrelease)
- [cloudfoundry/cf-release](https://github.com/cloudfoundry/cf-release/tree/master/jobs/etcd)

## etcdを使用しているプロジェクト {#projects-using-etcd}

- [etcd Raftの利用例](https://github.com/etcd-io/raft/blob/main/README.md#notable-users) - etcdのraftライブラリー実装を使用するプロジェクト。
- [Apache APISIX](https://github.com/apache/apisix) - etcdを設定ストアとして使用するAPIゲートウェイ。
- [apache/celix](https://github.com/apache/celix) - OSGi仕様をCとC++向けに適応した実装。
- [binocarlos/yoda](https://github.com/binocarlos/yoda) - etcd + ZeroMQ
- [blox/blox](https://github.com/blox/blox) - AWS ECSを利用したコンテナー管理とオーケストレーションのためのオープンソースプロジェクト群。
- [calavera/active-proxy](https://github.com/calavera/active-proxy) - etcdで設定するHTTPプロキシ。
- [chain/chain](https://github.com/chain/chain) - 高い拡張性を持つ許可型ブロックチェーンネットワークの運用と接続のために設計されたソフトウェア。
- [derekchiang/etcdplus](https://github.com/derekchiang/etcdplus) - etcd上に構築された分散同期プリミティブ群。
- [go-discover](https://github.com/flynn/go-discover) - Goによるサービスディスカバリー。
- [gleicon/goreman](https://github.com/gleicon/goreman/tree/etcd) - etcdに対応した、Go製Foremanクローンのブランチ。
- [garethr/hiera-etcd](https://github.com/garethr/hiera-etcd) - etcdを使用するPuppet hieraバックエンド。
- [mattn/etcd-vim](https://github.com/mattn/etcd-vim) - vim内からキーをSETおよびGETします。
- [mattn/etcdenv](https://github.com/mattn/etcdenv) - etcd連携機能を備えた「env」shebang。
- [kelseyhightower/confd](https://github.com/kelseyhightower/confd) - テンプレートとetcdのデータを使用して、ローカルアプリケーションの設定ファイルを管理します。
- [configdb](https://git.autistici.org/ai/configdb/tree/master) - 任意のデータベースバックエンド上にRESTによるリレーショナルな抽象化を提供し、設定やインベントリーの保存を目的とします。
- [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) - Googleが発表したコンテナークラスターマネージャー。
- [mailgun/vulcand](https://github.com/mailgun/vulcand) - etcdを設定バックエンドとして使用するHTTPプロキシ。
- [duedil-ltd/discodns](https://github.com/duedil-ltd/discodns) - etcdを名前とレコードのデータベースとして使用するシンプルなDNSネームサーバー。
- [skynetservices/skydns](https://github.com/skynetservices/skydns) - RFC準拠のDNSサーバー。
- [xordataexchange/crypt](https://github.com/xordataexchange/crypt) - GPG暗号化を使用して、etcdに値を安全に保存します。
- [spf13/viper](https://github.com/spf13/viper) - Go用の設定ライブラリー。ENV、pflags、ファイル、etcdから値を読み込み、必要に応じて暗号化できます。
- [lytics/metafora](https://github.com/lytics/metafora) - Go用の分散タスクライブラリー。
- [ryandoyle/nss-etcd](https://github.com/ryandoyle/nss-etcd) - etcdから名前を解決するためのGNU libc NSSモジュール。
- [Gru](https://github.com/dnaeon/gru) - Goでオーケストレーションを容易にします。
- [Vitess](http://vitess.io/) - MySQLの水平スケーリングを実現するデータベースクラスターシステム。
- [lclarkmichalek/etcdhcp](https://github.com/lclarkmichalek/etcdhcp) - 永続化と協調にetcdを使用するDHCPサーバー。
- [openstack/networking-vpp](https://github.com/openstack/networking-vpp) - [FD.io VPPデータプレーン](https://wiki.fd.io/view/VPP)を制御し、[OpenStack](https://www.openstack.org/)クラウドの仮想ネットワークを提供するネットワークドライバー。
- [OpenStack](https://github.com/openstack/governance/blob/master/reference/base-services.rst) - OpenStackのサービスは、基盤サービスとしてetcdに依存できます。
- [CoreDNS](https://github.com/coredns/coredns/tree/master/plugin/etcd) - プラグインを連結して処理するDNSサーバー。CNCFとKubernetesの一部です。
- [Uber M3](https://github.com/m3db/m3) - M3：Uberによる、Prometheus向けのオープンソースの大規模メトリクスプラットフォーム。
- [Rook](https://github.com/rook/rook) - Kubernetes向けのストレージオーケストレーション。
- [Patroni](https://github.com/zalando/patroni) - ZooKeeper、etcd、Consulを使用するPostgreSQL高可用性のテンプレート。
- [Trillian](https://github.com/google/trillian) - データストレージ層から内容を提供するMerkle木の実装で、極めて大きな木にも拡張できます。
- [purpleidea/mgmt](https://github.com/purpleidea/mgmt) - 次世代の分散型、イベント駆動型の並列設定管理。
- [Portworx/kvdb](https://docs.portworx.com/concepts/internal-kvdb/) - Portworxのクラスター設定を保存する内部kvdb。
- [Apache Pulsar](https://pulsar.apache.org/) - クラウド向けに構築された、オープンソースの分散メッセージング・ストリーミングプラットフォーム。
