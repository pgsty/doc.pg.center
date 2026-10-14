---
title: etcdと他のキー・バリューストアの比較
weight: 2875
description: "etcdの歴史と用途、他のツールとの比較"
categories: [概念]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/why.md"
---

「etcd」という名前は、Unixの「/etc」フォルダーと、distributed systems（分散システム）の頭文字「d」に由来します。「/etc」フォルダーは単一システムの構成データを保存する場所ですが、etcdは大規模な分散システムの構成情報を保存します。つまり、分散した（distributed）「/etc」が「etcd」です。

etcdは、大規模な分散システムの汎用的な基盤として設計されています。対象となるのは、スプリットブレインでの動作を決して許容せず、そのためには可用性を犠牲にすることもいとわないシステムです。etcdは、一貫性と耐障害性を保ってメタデータを保存します。etcdクラスターは、最高水準の安定性、信頼性、拡張性、性能を備えたキー・バリューストレージの提供を目指しています。

分散システムは、構成管理、サービス検出、分散処理の調整のために、一貫性のあるキー・バリューストアとしてetcdを使用します。多くの[組織][production-users]が、コンテナースケジューラー、サービス検出サービス、分散データストレージなどの本番システムをetcdで実装しています。etcdを使う代表的な分散処理のパターンには、[リーダー選出][etcd-etcdctl-elect]、[分散ロック][etcd-etcdctl-lock]、マシンの生存監視があります。

## ユースケース {#use-cases}

- Container Linux by CoreOS：[Container Linux][container-linux]上のアプリケーションでは、Linuxカーネルが無停止で自動更新されます。Container Linuxは、更新の調整に[locksmith]を使用します。Locksmithはetcd上に分散セマフォを実装し、どの時点でも再起動するのがクラスターの一部だけになるようにします。
- [Kubernetes][kubernetes]は、サービス検出とクラスター管理のために構成データをetcdに保存します。etcdの一貫性は、サービスを正しくスケジュールし、動作させるために不可欠です。Kubernetes APIサーバーは、クラスターの状態をetcdに永続化します。また、etcdのwatch APIでクラスターを監視し、重要な構成変更を展開します。

## 比較表 {#comparison-chart}

etcdが適しているように見えても、他の技術的な判断と同じく、慎重に検討してください。このドキュメントはetcdチームが執筆しています。技術と機能を公平に比較することが理想ですが、著者の専門知識や考え方は当然etcd寄りです。その点を踏まえて利用してください。

以下の表は、etcdと主な代替製品の違いを一目で確認するための早見表です。各列の補足や詳細は、表の後のセクションで説明します。

|  | etcd | ZooKeeper | Consul | NewSQL (Cloud Spanner, CockroachDB, TiDB) |
| --- | --- | --- | --- | --- |
| 並行処理のプリミティブ | Goの[Lock RPC][etcd-v3lock]、[Election RPC][etcd-v3election]、[コマンドラインのロック][etcd-etcdctl-lock]、[コマンドラインの選挙][etcd-etcdctl-elect]、[レシピ][etcd-recipe] | Javaの外部ライブラリー[curatorのレシピ][curator] | [組み込みのロックAPI][consul-lock] | 存在しても[まれ][newsql-leader] |
| 線形化可能読み取り | [対応][etcd-linread] | 非対応 | [対応][consul-linread] | 製品による |
| 多版型同時実行制御 | [対応][etcd-mvcc] | 非対応 | 非対応 | 製品による |
| トランザクション | [フィールド比較、読み取り、書き込み][etcd-txn] | [バージョン検査、書き込み][zk-txn] | [フィールド比較、ロック、読み取り、書き込み][consul-txn] | SQL形式 |
| 変更通知 | [過去と現在のキー区間][etcd-watch] | [現在のキーとディレクトリ][zk-watch] | [現在のキーと接頭辞][consul-watch] | トリガー（一部） |
| ユーザー権限 | [ロールベース][etcd-rbac] | [ACL][zk-acl] | [ACL][consul-acl] | 製品による（テーブル単位の[GRANT][cockroach-grant]、データベース単位の[ロール][spanner-roles]） |
| HTTP/JSON API | [対応][etcd-json] | 非対応 | [対応][consul-json] | まれ |
| メンバーシップの再構成 | [対応][etcd-reconfig] | [>3.5.0][zk-reconfig] | [対応][consul-reconfig] | 対応 |
| 信頼性を保てるデータベースの最大サイズ | 数GB | 数百MB（場合によっては数GB） | 数百MB | TB以上 |
| 読み取りを線形化する最小レイテンシー | ネットワークRTT | 読み取りの線形化なし | RTT + fsync | クロックバリア（原子時計、NTP） |

### ZooKeeper {#zookeeper}

ZooKeeperは、分散システムの調整とメタデータの保存という、etcdと同じ問題を解決します。ただし、etcdはZooKeeperの設計と実装に関する開発・運用経験を、後発として生かせます。ZooKeeperから得られた教訓はetcdの設計に確実に反映され、Kubernetesのような大規模システムのサポートに役立っています。etcdがZooKeeperに対して改善した点には、次のものがあります。

* クラスターのメンバーシップの動的な再構成
* 高負荷下での安定した読み書き
* 多版型同時実行制御のデータモデル
* 通知せずにイベントを取りこぼすことのない、信頼できるキーの監視
* 接続とセッションを切り離すリースのプリミティブ
* 安全な分散共有ロックのAPI

さらに、etcdは多くの言語とフレームワークを標準でサポートしています。ZooKeeperは独自のJute RPCプロトコルを使用し、[サポートする言語バインディング][zk-bindings]が制限されます。一方、etcdのクライアントプロトコルは、Go、C++、Javaなどの言語バインディングを持つ、広く使われているRPCフレームワーク[gRPC][grpc]に基づいています。また、gRPCはHTTP上のJSONにシリアライズできるため、`curl`のような汎用コマンドラインツールでも通信できます。多様な選択肢から選べるため、単一の固定された技術群でetcdの周辺を固めるのではなく、それぞれの環境に合ったツールを使ってetcd上にシステムを構築できます。

機能、サポート、安定性を考えると、一貫性のあるキー・バリューストアとしてZooKeeperを採用する予定の新しいアプリケーションは、代わりにetcdを選ぶのがよいでしょう。

### Consul {#consul}

Consulは、サービス検出を一通り提供するフレームワークです。ヘルスチェック、障害検出、DNSサービスを内蔵しています。また、RESTfulなHTTP APIを持つキー・バリューストアも公開しています。[Consul 1.0の時点では][dbtester-comparison-results]、キー・バリュー操作におけるストレージシステムの拡張性は、etcdやZooKeeperなどに及びません。数百万のキーを必要とするシステムでは、大きなレイテンシーやメモリーへの負荷に悩まされます。キー・バリューAPIには、特に、複数バージョンのキー、条件付きトランザクション、信頼できるストリーミング監視が欠けています。

etcdとConsulは、異なる問題を解決します。分散した一貫性のあるキー・バリューストアが必要なら、Consulよりetcdが適しています。クラスターのサービス検出を一通り揃えたい場合、etcdの機能だけでは足りません。Kubernetes、Consul、SmartStackを選んでください。

### NewSQL (Cloud Spanner, CockroachDB, TiDB) {#newsql-cloud-spanner-cockroachdb-tidb}

etcdとNewSQLデータベース（[Cockroach][cockroach]、[TiDB][tidb]、[Google Spanner][spanner]など）は、いずれも高可用性と強いデータ一貫性の保証を提供します。ただし、システム設計の前提が大きく異なるため、クライアントAPIと性能の特性も大きく異なります。

NewSQLデータベースは、データセンターをまたいで水平に拡張することを目的としています。通常、データを、離れた場所にあることもある複数の一貫性を持つ複製グループ（シャード）に分割し、TB以上の規模のデータセットを保存します。このような拡張方式は、クロックを待つことによる長いレイテンシーがあり、更新の依存関係グラフがおおむね局所的であることを想定するため、分散協調にはあまり適しません。データはテーブルに整理され、etcdより豊かな意味論を持つSQL形式のクエリー機能を備えますが、その分、クエリーの処理、計画、最適化は複雑になります。

メタデータの保存や分散アプリケーションの調整には、etcdを選んでください。数GBを超えるデータを保存する場合や、完全なSQLクエリーが必要な場合は、NewSQLデータベースを選んでください。

## メタデータにetcdを使う {#using-etcd-for-metadata}

etcdは、単一の一貫性を持つ複製グループ内ですべてのデータを複製します。一貫した順序を保ちながら数GBまでのデータを保存するには、これが最も効率的な方式です。クラスターの状態の各変更には、単調増加するカウンターから、etcdでリビジョンと呼ぶ、グローバルに一意のIDが割り当てられます。これによって変更の順序を判断できます。1つの変更が複数のキーを変えることもあります。複製グループが1つだけなので、変更リクエストはコミットのためにRaftプロトコルを経由するだけで済みます。コンセンサスの対象を1つの複製グループに限定することで、etcdは単純なプロトコルで分散した一貫性を実現しながら、低レイテンシーと高スループットを達成します。

etcdの複製方式は、データのシャーディングがないため、水平には拡張できません。対して、NewSQLデータベースは通常、複数の一貫性を持つ複製グループにデータを分割し、TB以上の規模のデータセットを保存します。ただし、各変更にグローバルに一意で増加するIDを割り当てるには、各リクエストが複製グループ間の追加の調整プロトコルを経由する必要があります。この追加の調整段階では、グローバルIDで競合が起こり、順序を付けるリクエストが再試行を迫られる可能性があります。その結果、方式は複雑になり、厳密な順序付けでは、通常etcdより性能が低下します。

プロセスの調整など、主にメタデータやその順序を扱うアプリケーションにはetcdを選んでください。複数のデータセンターにまたがる大きなデータストアが必要で、強いグローバルな順序の性質にあまり依存しない場合は、NewSQLデータベースを選んでください。

## 分散協調にetcdを使う {#using-etcd-for-distributed-coordination}

etcdは、イベントの監視、リース、選挙、分散共有ロックなどの分散協調のプリミティブを標準で提供します。ただし、分散共有ロックには分かりにくい性質があるため、使用時には注意が必要です。詳細は後述します。これらのプリミティブは、etcd開発者が保守し、サポートしています。このようなプリミティブを外部ライブラリーに任せるのは、分散ソフトウェアの基盤を開発する責任を放棄し、実質的にシステムを未完成のままにすることです。NewSQLデータベースは通常、こうした分散協調のプリミティブを第三者が作成することを想定しています。同様に、ZooKeeperにも、協調処理のレシピを集めた独立した別の[ライブラリー][curator]があることはよく知られています。組み込みのロックAPIを提供するConsulでさえ、「[確実な方法ではない][consul-bulletproof]」と断っています。

理論上は、強い一貫性を持つ任意のストレージシステムの上に、これらのプリミティブを構築できます。しかし、アルゴリズムには微妙な点が多く、一見動いているロックアルゴリズムが、要求の一斉集中やタイミングのずれによって突然破綻することも珍しくありません。さらに、トランザクショナルメモリーなど、etcdがサポートする他のプリミティブは、etcdのMVCCデータモデルに依存しています。単に強い一貫性があるだけでは不十分です。

分散協調にetcdを選ぶことは、運用上の悩みを防ぎ、開発の労力を減らすことにつながります。

### ロックとリースの使用上の注意 {#notes-on-the-usage-of-lock-and-lease}
etcdは、[リースの仕組み][lease]と[そのetcdでの実装][etcdlease]に基づく[ロックAPI][etcd-v3lock]を提供します。リースの基本的な考え方は、サーバーが要求元のクライアントに、リースと呼ぶトークンを付与するというものです。サーバーは付与時にTTLをリースに関連付けます。TTLを超える時間の経過を検出すると、サーバーはリースを取り消します。クライアントは、取り消されていないリースを保持している間、そのリースに関連付けられたリソースへのアクセス権を所有していると主張できます。etcdの場合、そのリソースはetcdのキー空間内のキーです。etcdは、この方式でロックAPIを提供します。ただし、ロックAPIだけを相互排他の仕組みとして使うことはできません。ロックという名前は、[歴史的な理由][chubby]によるものです。一方、以下で説明するように、ロックAPIは相互排他を最適化する仕組みとして使用できます。

リースの仕組みで最も重要なのは、TTLが物理的な時間間隔として定義されることです。サーバーもクライアントも、自身の時計で時間の経過を測ります。そのため、サーバーはリースを取り消しているのに、クライアントはまだ所有していると主張する状況が起こり得ます。

では、リースの仕組みは、ロックの相互排他をどのように保証するのでしょうか。実際には、リース自体は相互排他を保証しません。リースを所有していても、その所有者がリソースのロックを保持しているとは保証できません。

etcd自身のキーへの相互アクセスをetcdのロックで制御する場合、相互排他はバージョン番号の検証によって実装されます。これは、Consulなどの他のシステムでcompare and swapと呼ばれることもあります。`Put`や`Txn`などのetcdのRPCでは、操作に必要なリビジョン番号やリースIDの条件を指定できます。条件が満たされなければ、操作は失敗することがあります。この仕組みによって、etcdはクライアントに分散ロックを提供します。つまり、クライアントは自身のリクエストがetcdクラスターで正常に完了したとき、キーのロックを取得していることを認識します。

分散ロックに関する文献にも、同様の設計が記載されています。
* [Chubbyの論文][chubby]では、*sequencer*という概念が導入されています。ここでは、sequencerはetcdのリビジョン番号とリースIDの組み合わせにほぼ相当すると解釈しています。
* [分散ロックの実装方法][fencing]では、Martin Kleppmannが*fencing token*という考え方を紹介しています。著者らは、etcdではリビジョン番号がfencing tokenに相当すると解釈しています。
* [分散システムにおける同期時計の実用的な使用法][physicalclock]には、Thorがバージョン番号の検証とリースに基づく分散ロック機構を実装しているという説明があります。

etcdや他のシステムは、バージョン番号の検証で相互排他を実現するのに、なぜリースを提供するのでしょうか。リースは、中止されるリクエストの数を減らすための最適化機構を提供するからです。

etcdのキーは、リースとバージョン番号の検証によって効率的にロックできます。ただし、etcdと関係のないリソースを保護するには、そのリソース側にも、etcdのキーのようなバージョン番号の検証と、レプリカ間の一貫性の仕組みが必要です。etcdのロック機能だけでは、外部リソースを保護できません。

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
[etcd-commonname]: /ja/etcd/op-guide/authentication/#using-tls-common-name
[etcd-etcdctl-elect]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#elect-options-election-name-proposal
[etcd-etcdctl-lock]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#lock-options-lockname-command-arg1-arg2-
[etcd-json]: /ja/etcd/dev-guide/api_grpc_gateway/
[etcd-linread]: /ja/etcd/learning/api_guarantees/#linearizability
[etcd-mvcc]: /ja/etcd/learning/data_model/
[etcd-rbac]: /ja/etcd/op-guide/authentication/rbac
[etcd-recipe]: https://godoc.org/github.com/etcd-io/etcd/client/v3/experimental/recipes
[etcd-reconfig]: /ja/etcd/op-guide/runtime-configuration
[etcd-txn]: /ja/etcd/learning/api/#transaction
[etcd-v3election]: https://pkg.go.dev/go.etcd.io/etcd/server/v3/etcdserver/api/v3election/v3electionpb
[etcd-v3lock]: https://pkg.go.dev/go.etcd.io/etcd/server/v3/etcdserver/api/v3lock/v3lockpb
[etcd-watch]: /ja/etcd/learning/api/#watch-streams
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
