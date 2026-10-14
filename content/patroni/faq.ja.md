---
title: "FAQ"
weight: 180
icon: fa-solid fa-circle-question
description: "Patroni の操作とトラブルシューティングに関するよくある質問。"
module: [PATRONI]
categories: [リファレンス]
upstream_link: "https://patroni.readthedocs.io/en/latest/faq.html"
---

<a id="faq"></a>
このセクションでは、Patroni に関して最もよくある質問に対する回答を示します。各サブセクションでは、さまざまな種類の質問に焦点を当てます。

これがあなたの疑問のほとんどを解決するのに役立つことを願っています。さらに懸念がある場合、または予期しない問題に直面している場合は、[チャット](/ja/patroni/contributing_guidelines#chatting) および [バグの報告](/ja/patroni/contributing_guidelines#reporting_bugs) を参照して、ヘルプを取得したり問題を報告したりする方法を確認してください。

--------

## 他の HA ソリューションとの比較 {#comparison-with-other-ha-solutions}

`repmgr` などの他のソリューションでは必要ないのに、Patroni では DCS ノードの別個のクラスターが必要なのはなぜですか？

HA ソリューションを実装するにはさまざまな方法があり、それぞれに長所と短所があります。

`repmgr` のようなソフトウェアは、ノード間で通信を実行して、いつアクションを実行するかを決定します。

一方、Patroni は、DCS に保存されている状態に依存します。 DCS は、Patroni が何をすべきかを決定するための信頼できる情報源として機能します。

個別の DCS クラスターを使用するとアーキテクチャが肥大化する可能性がありますが、このアプローチにより、Postgres クラスター内でスプリット ブレイン シナリオが発生する可能性も低くなります。

Postgres 管理に関して、Patroni と他の HA ソリューションの違いは何ですか？

Patroni は、Postgres クラスターの高可用性を管理するだけでなく、Postgres 自体も管理します。

Postgres ノードがまだ存在しない場合は、プライマリー ノードとスタンバイ ノードのブートストラップが行われ、ノードの Postgres 構成も管理されます。 Postgres ノードがすでに存在する場合、Patroni がクラスターの管理を引き継ぎます。

上記に加えて、Patroni には自己修復機能もあります。つまり、プライマリー ノードに障害が発生した場合、Patroni はレプリカへのフェイルオーバーを行うだけでなく、元のプライマリーを新しいプライマリーのレプリカとして再参加させようとします。同様に、レプリカに障害が発生した場合、Patroni はそのレプリカの再参加を試みます。

だからこそ、Patroni は「HA ソリューションのテンプレート」と呼ばれるのです。物理レプリケーションの管理にとどまらず、Postgres 全体を管理します。

--------

## DCS {#dcs}

同じ `etcd` クラスターを使用して、2 つ以上の Patroni クラスターからのデータを保存できますか？

はい、できます！

Patroni クラスターに関する情報は、Patroni の `namespace` および `scope` 設定がプレフィックスとして付けられたパスの下の DCS に保存されます。

異なる Patroni クラスター間で `namespace` と `scope` が競合しない限り、同じ DCS クラスターを使用して複数の Patroni クラスターからの情報を保存できるはずです。

同じDCSクラスターを参照する異なるPatroniクラスターで、同じ`namespace`と`scope`の組み合わせを使用するとどうなりますか？  
2つ目のクラスターのPostgresシステム識別子が異なる場合、PatroniはそのDCSパス内のデータが一致しないことを検出します。ポーズモード以外では、保存された状態が別のクラスターに属し、Patroniの設定に誤りがあると判断して、2つ目のクラスターを管理せずに終了します。

同じ DCS クラスターを共有する異なる Patroni クラスターを処理する場合は、必ず異なる `namespace` / `scope` を使用してください。

DCS クラスターを失った場合はどうなりますか？

DCS は、基本的に Patroni クラスターのステータスと動的構成を保存するために使用されます。

その最初の結果は、[DCS フェイルセーフモード](/ja/patroni/dcs_failsafe_mode#dcs_failsafe_mode) が有効になっていない限り、その DCS に依存するすべての Patroni クラスターが読み取り専用モードになることです。

DCS クラスターを失った場合はどうすればよいですか？

DCS クラスターが失われた場合、考えられる結果は 3 つあります。

1. DCS クラスターが完全に復旧した場合：これには、Patroni 側からのアクションは必要ありません。 DCS クラスターが回復すると、Patroni も回復できるはずです。
2. DCS クラスターが元の場所で再作成され、エンドポイントは同じままになります。 Patroni 側では変更は必要ありません。
3. 新しい DCS クラスターが異なるエンドポイントで作成されます。各 Patroni ノードの Patroni 構成内の DCS エンドポイントを更新する必要があります。

`2.` または `3.` のシナリオに直面した場合、Patroni はクラスターの現在のステータスに基づいてステータス情報を再度作成し、Patroni クラスターの各メンバーの Postgres データ ディレクトリ内に保存されている `patroni.dynamic.json` という名前のバックアップ ファイルに基づいて DCS 上に動的構成を再作成します。

DCS クラスターの過半数を失った場合はどうなりますか？

DCS が応答しなくなるため、Patroni は現在の読み取り/書き込み Postgres ノードを降格させます。

覚えておいてください: Patroni は、DCS の状態に依存してクラスター上でアクションを実行します。

[DCS フェイルセーフモード](/ja/patroni/dcs_failsafe_mode#dcs_failsafe_mode) を使用すると、この状況を軽減できます。

--------

## patronictl {#patronictl}

Patroni ホストで [patronictl](/ja/patroni/patronictl#patronictl) を実行する必要がありますか？

いいえ、その必要はありません。

Patroni ホストにアクセスできる場合、そのホストで [patronictl](/ja/patroni/patronictl#patronictl) を実行すると、`patroni` エージェントとまったく同じ構成ファイルを [patronictl](/ja/patroni/patronictl#patronictl) アプリケーションに使用できるため便利です。

ただし、[patronictl](/ja/patroni/patronictl#patronictl) は基本的にクライアントであり、リモート マシンから実行できます。必要なのは、DCS および Patroni メンバーの REST API に到達できるように、十分な構成を提供することだけです。

1 つの Patroni メンバーの情報が [`patronictl list`](/ja/patroni/patronictl#patronictl_list) コマンドの出力から消えたのはなぜですか？

[`patronictl list`](/ja/patroni/patronictl#patronictl_list) で表示される情報は、DCS の内容に基づいています。

メンバーに関する情報が DCS から消えた場合は、そのノード上の Patroni エージェントが実行されていないか、DCS と通信できない可能性が高くなります。

メンバーは情報を更新できないため、情報は最終的に DCS から期限切れになり、その結果メンバーは [`patronictl list`](/ja/patroni/patronictl#patronictl_list) の出力に表示されなくなります。

[`patronictl list`](/ja/patroni/patronictl#patronictl_list) コマンドの出力で、Patroni メンバーの 1 つに関する情報が最新ではないのはなぜですか？

[`patronictl list`](/ja/patroni/patronictl#patronictl_list) で表示される情報は、DCS の内容に基づいています。

デフォルトでは、その情報は Patroni によってほぼ `loop_wait` 秒ごとに更新されます。つまり、すべてが正常に機能している場合でも、DCS に保存されている情報に最大 `loop_wait` 秒の遅れが生じる可能性があります。

ただし、これはルールではないことに注意してください。 Patroni によって実行される一部の操作により、DCS 情報が即座に更新されます。

--------

## 構成 {#configuration}

動的構成とローカル構成の違いは何ですか？

動的構成 (またはグローバル構成) は、DCS に保管される構成であり、Patroni クラスターのすべてのメンバーに適用されます。これは主に、構成を保存すべき場所です。

ノードに固有の設定、またはグローバル構成を上書きする設定は、目的の Patroni メンバーにのみローカル構成として設定する必要があります。そのローカル構成は、構成ファイルまたは環境変数を通じて指定できます。

詳細については、[構成](/ja/patroni/config#config) を参照してください。

Patroni の構成の種類と優先順位は何ですか？

種類は次のとおりです。

- 動的構成: すべてのメンバーに適用されます。
- ローカル構成: ローカルメンバーに適用され、動的構成をオーバーライドします。
- 環境構成: ローカル メンバーに適用され、動的構成とローカル構成の両方を上書きします。

**注:** 一部の Postgres GUC はグローバルに、つまり動的構成を通じてのみ設定できます。これに加えて、Patroni がハードコードされた値を強制する GUC もあります。

詳細については、[構成](/ja/patroni/config#config) を参照してください。

Patroni 構成ファイルの作成に役立つ機能はありますか？

はい、あります。

`patroni --generate-sample-config` または `patroni --generate-config` コマンドを使用して、それぞれサンプルの Patroni 構成、および既存の Postgres インスタンスに基づく Patroni 構成を生成できます。

詳細については、[サンプル構成の生成](/ja/patroni/config#generate_sample_config) および [構成の生成](/ja/patroni/config#generate_config) を参照してください。

`bootstrap.dcs` 構成でパラメーターを変更しましたが、Patroni は変更をクラスター メンバーに適用しません。なにが問題ですか？

`bootstrap.dcs` で構成された値は、新しいクラスターをブートストラップする場合にのみ使用されます。これらの値は、ブートストラップ中に DCS に書き込まれます。

ブートストラップ フェーズが終了した後は、DCS を介してのみ動的構成を変更できます。

詳細については、次の質問を参照してください。

動的構成を変更するにはどうすればよいですか？

DCS の構成を変更する必要があります。これは、次のいずれかの方法で実現されます。

- [`patronictl edit-config`](/ja/patroni/patronictl#patronictl_edit_config);または
- [構成エンドポイント](/ja/patroni/rest_api#config_endpoint) への `PATCH` リクエスト。

ローカル設定を変更するにはどうすればよいですか？

対応する Patroni メンバーの構成ファイルを変更し、`SIGHUP` を使用して Patroni エージェントに通知する必要があります。これは、次のいずれかのアプローチを使用して実行できます。

- `POST` リクエストを REST API [再読み込みエンドポイント](/ja/patroni/rest_api#reload_endpoint) に送信します。または

- [`patronictl reload`](/ja/patroni/patronictl#patronictl_reload) を実行します。または

- `SIGHUP` を使用して Patroni プロセスにローカルに通知します。

  > - systemd を通じて Patroni を開始した場合は、コマンド `systemctl reload PATRONI_UNIT.service` を使用できます。`PATRONI_UNIT` は Patroni サービスの名前です。または
  > - 他の方法で Patroni を開始した場合は、`patroni` プロセスを特定し、`kill -s HUP PID` を実行する必要があります。`PID` は、`patroni` プロセスのプロセス ID です。

**注:** [`patronictl reload`](/ja/patroni/patronictl#patronictl_reload) によるリロードが機能しない場合があります。

- 期限切れの REST API 証明書: [patronictl](/ja/patroni/patronictl#patronictl) の `-k` オプションを使用することでこれを軽減できます。
- 間違った資格情報: たとえば、構成ファイル内の `restapi` または `ctl` 資格情報を変更し、同じ構成ファイルを Patroni および [patronictl](/ja/patroni/patronictl#patronictl) に使用する場合です。

環境構成を変更するにはどうすればよいですか？

環境構成は、Patroni の起動時にのみ読み取られます。

これを念頭に置いて、環境構成を変更した場合は、対応する Patroni エージェントを再起動する必要があります。

クラスターでフェイルオーバーが発生しないよう注意してください。[`patronictl pause`](/ja/patroni/patronictl#patronictl_pause) の確認をお勧めします。

通常の動作中に繰り返されるハートビート ログの行を減らすにはどうすればよいですか?

`Lock owner: ...` や `no action. I am ...` などの行が繰り返されるためにログにノイズが多すぎる場合は、`log.deduplicate_heartbeat_logs: true` を構成します。

これは、Patroni YAML ファイル ([ログ設定](/ja/patroni/config/yaml#log_settings)) または `PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS=true` を使用して設定できます。

これにより、ハートビート メッセージの繰り返しが抑制されるためログの量が減りますが、フェイルオーバー診断時に役立つループごとのハートビートの可視性も失われることに注意してください。

リロードが必要な Postgres GUC を変更するとどうなりますか？

前の質問で説明したように動的構成またはローカル構成を変更すると、Patroni が Postgres 構成の再ロードを処理します。

再起動が必要な Postgres GUC を変更するとどうなりますか？

Patroni は、影響を受けるメンバーに `pending restart` のフラグを付けます。

メンバーをいつ、どのように再起動するかを決定するのはあなた次第です。これは、次のいずれかの方法で実現できます。

- [`patronictl restart`](/ja/patroni/patronictl#patronictl_restart);または
- [再起動エンドポイント](/ja/patroni/rest_api#restart_endpoint) への `POST` リクエスト。

**注:** 一部の Postgres GUC では、Postgres ノードを再起動する順序に関して特別な管理が必要です。詳細については、[共有メモリーのパラメーター](/ja/patroni/config#shared_memory_gucs) を参照してください。

Patroni 構成の `etcd` と `etcd3` の違いは何ですか？

`etcd` は `etcd` の API バージョン 2 を使用し、`etcd3` は `etcd` の API バージョン 3 を使用します。

API バージョン 2 によって保存された情報は、API バージョン 3 では管理できず、その逆も同様であることに注意してください。

次の理由から、`etcd` ではなく `etcd3` を構成することをお勧めします。

- API バージョン 2 は、etcd v3.4 以降、デフォルトで無効になっています。
- API バージョン 2 は etcd v3.6 で完全に削除されました。

Patroni 構成で `use_slots` を有効にしていますが、クラスター メンバーがしばらくオフラインになると、そのメンバーによって使用されているレプリケーション スロットが上流ノードで削除されます。その問題を回避するにはどうすればよいでしょうか？

次の 2 つのオプションがあります。

1. `member_slots_ttl` (デフォルト値 `30min`、Patroni `4.0.0` および PostgreSQL 11 以降で利用可能) を調整でき、メンバーのダウンタイムが構成されたしきい値より短い場合、不在メンバーのレプリケーション スロットは削除されません。
2. メンバーに対して永続的な物理レプリケーション スロットを構成できます。

Patroni `3.2.0` 以降、メンバー スロットを Patroni によって管理される永続スロットとして持つことができるようになりました。

PostgreSQL 11 以降では、Patroni はすべてのノードに永続的な物理スロットを作成し、スロットが削除されないようにするだけでなく、メンバーによって使用された LSN に従ってすべてのノードのスロットの LSN を進めます。

後で対応するメンバーを削除することにした場合、永続スロットの構成を調整するのは**あなたの責任**です。そうしないと、Patroni はそれらのスロットを永久に保持し続けます。

**注:** `3.2.0` より古い Patroni でも、メンバー スロットを永続的な物理スロットとして構成することは可能でしたが、それらは現在のリーダーでのみ管理されます。つまり、フェイルオーバー/スイッチオーバーが発生した場合、これらのスロットは新しいリーダー上に作成されますが、不在ノードに必要なすべての WAL セグメントがそこにあることは保証されません。

**注:** Patroni `3.2.0` であっても、小さな競合状態が発生する可能性が残ります。レプリカ上でスロットが作成された直後は、リーダー上の同じスロットより先に進んでいる場合があり、誰もそのスロットを消費していない場合、フェイルオーバー後に一部のファイルが欠落する可能性が依然としてあります。このことを念頭に置き、必要な WAL のリストアや PITR を可能にする継続的アーカイブを構成することを推奨します。

`loop_wait`、`retry_timeout`、`ttl` の違いは何ですか？

Patroni は、HA サイクルと呼ばれるものを随時実行します。各 HA サイクルで、クラスターに対して一連のチェックを実行してその健全性を判断し、ステータスに応じてスタンバイへのフェイルオーバーなどのアクションを実行する場合があります。

`loop_wait` は、HA チェックの新しいサイクルを実行する前に Patroni がスリープする時間を秒単位で決定します。

`retry_timeout` は、DCS および Postgres での再試行操作のタイムアウトを設定します。たとえば、DCS が `retry_timeout` 秒を超えて応答しない場合、Patroni は安全のためにプライマリー ノードを降格する可能性があります。

`ttl` は、DCS の `leader` ロックのリース時間を設定します。クラスターの現在のリーダーが、HA サイクル中に `ttl` を超えてリースを更新できない場合、リースは期限切れになり、クラスター内で `leader race` がトリガーされます。

**注:** これらの設定を変更する場合は、Patroni がドキュメントの [動的](/ja/patroni/config/dynamic#dynamic) セクションで説明されているルールと最小値を強制することに注意してください。

--------

## Postgres 管理 {#postgres-management}

Postgres 構成で Postgres GUC を直接変更できますか？

可能ですが、それは避けるべきです。

Postgres 構成は Patroni によって管理されており、構成ファイルを直接編集しようとしても、Patroni が最終的にそれらを上書きするため、編集は無駄に終わる可能性があります。

Patroni によって実行される管理を回避するために使用できるオプションがいくつかあります。

- `$PGDATA/postgresql.base.conf` を通じて Postgres GUC を変更します。または
- `postgresql.base.conf` の代わりに使用される `postgresql.custom_conf` を定義して、外部で管理できるようにします。または
- `ALTER SYSTEM` / `ALTER DATABASE` / `ALTER USER` を使用して GUC を変更します。

詳細については、セクション [重要な構成ルール](/ja/patroni/config#important_configuration_rules) を参照してください。

いずれの場合も、Patroni を通じてすべての Postgres 構成を管理することをお勧めします。これにより、管理が集中化され、必要な場合の Patroni のデバッグが容易になります。

Postgres ノードを直接再起動できますか？

いいえ、Postgres を直接管理しようとするべきでは**ありません**!

Patroni を使用せずに Postgres サーバーを再起動しようとすると、クラスターがフェイルオーバーに直面する可能性があります。

Postgres サーバーを管理する必要がある場合は、Patroni によって公開されている方法で実行してください。

Patroni は、既存の Postgres クラスターの管理を引き継ぐことができますか？

はい、できます！

詳細な手順については、[既存データの引き継ぎ](/ja/patroni/existing_data#existing_data) を参照してください。

Patroni は Postgres をどのように管理しますか？

Patroni は、`pg_ctl` や `postgres` などの Postgres バイナリを実行することによって、Postgres の起動と停止を処理します。

これを念頭に置いて、systemd ユニット (例: `postgresql.service`) など、Postgres クラスターを管理し得る他のソースを無効化することが**必須**です。クラスター内の Postgres インスタンスを開始、停止、昇格できるのは Patroni のみであるべきです。そうしないと、スプリット ブレイン シナリオが発生する可能性があります。たとえば、プライマリーとして動作していたノードが障害で停止し、ユニット `postgresql.service` が有効になっている場合、そのユニットが Postgres を再び起動し、スプリット ブレインを引き起こす可能性があります。

--------

## 概念と要件 {#concepts-and-requirements}

Patroni の一部を構成するアプリケーションはどれですか？

Patroni には基本的に 2 つのアプリケーションが同梱されています。

- `patroni`: これは、Postgres ノードの管理を担当する Patroni エージェントです。
- [patronictl](/ja/patroni/patronictl#patronictl): これは、Patroni クラスターと対話する (スイッチオーバー、再起動、構成の変更などを実行する) ために使用されるコマンドライン ユーティリティです。詳細については、[patronictl](/ja/patroni/patronictl#patronictl) を参照してください。

Patroni の `standby cluster` とは何ですか？

これは、プライマリー Postgres ノードが実行されていないクラスターです。つまり、クラスター内に読み取り/書き込みメンバーがありません。

これらの種類のクラスターは、別のクラスターからデータをレプリケートするために存在し、通常、データ センター間でデータをレプリケートする場合に役立ちます。

クラスター内には、リモート Postgres ノードからの変更のレプリケーションを担当するスタンバイとなるリーダーが存在します。次に、そのようなリーダー メンバーからのカスケード レプリケーションで構成された一連のスタンバイが存在します。

**注:** スタンバイ クラスターは、レプリケーション元のソース クラスターについて何も知りません。WAL ストリーミングの代わりに `restore_command` を使用することもでき、完全に独立した DCS クラスターを使用することもできます。

詳細については、[スタンバイクラスター](/ja/patroni/standby_cluster#standby_cluster) を参照してください。

Patroni の `leader` とは何ですか？

Patroni の `leader` は、クラスターのコーディネーターのようなものです。

通常の Patroni クラスターでは、`leader` が読み取り/書き込みノードになります。

スタンバイ Patroni クラスターでは、`leader` (別名 `standby leader`) がリモート Postgres ノードからのレプリケーションを担当し、それらの変更をスタンバイ クラスターの他のメンバーにカスケードします。

Patroni では、クラスター内に最小数の Postgres ノードが必要ですか？

いいえ、Patroni は任意の数の Postgres ノードで実行できます。

Patroni は DCS から分離されていることを覚えておいてください。

Patroni の [一時停止](/ja/patroni/pause#pause) とはどういう意味ですか？

一時停止は、Postgres 管理から一歩引くようユーザーが Patroni に要請できるようにするために、Patroni が提供する操作です。

これは主に、クラスターでメンテナンスを実行する必要があり、プライマリーを停止したときにスタンバイにフェイルオーバーするなど、Patroni が HA に関連する決定を行うのを避けたい場合に役立ちます。

詳細については、[一時停止](/ja/patroni/pause#pause) を参照してください。

--------

## 自動フェイルオーバー {#automatic-failover}

Patroni の自動フェイルオーバー メカニズムはどのように機能しますか？

Patroni の自動フェイルオーバーは、`leader race` と呼ばれるものに基づいています。

Patroni は、クラスターのステータスを DCS に保存します。その中には、クラスターの現在の `leader` である Patroni メンバーの名前を保持する `leader` ロックがあります。

その `leader` ロックには有効期限が関連付けられています。リーダー ノードが `leader` ロックのリースを期限内に更新できなかった場合、キーは最終的に DCS から期限切れになります。

`leader` ロックの有効期限が切れると、Patroni が `leader race` と呼ぶものがトリガーされ、すべてのノードがチェックの実行を開始して、`leader` ロールを引き継ぐ最適な候補であるかどうかを判断します。これらのチェックの一部には、他のすべての Patroni メンバーの REST API への呼び出しが含まれます。

`leader` ロックを引き継ぐための最良の候補であると判断したすべての Patroni メンバーは、引き継ぎを試みます。 `leader` ロックを取得できる最初の Patroni メンバーは、読み取り/書き込みノード (または `standby leader`) に昇格し、他のメンバーはこれに従うように構成されます。

Patroni クラスターで自動フェイルオーバーを一時的に無効にすることはできますか？

はい、できます！

これを実現するには、クラスターを一時的に一時停止します。これは通常、メンテナンスを実行する場合に役立ちます。

クラスターの自動フェイルオーバーを再開したい場合は、一時停止を解除するだけです。

詳細については、[一時停止](/ja/patroni/pause#pause) を参照してください。

--------

## ブートストラップとスタンバイの作成 {#bootstrapping-and-standbys-creation}

Patroni はプライマリー Postgres ノードをどのように作成しますか？スタンバイ Postgres ノードについてはどうですか？

デフォルトでは、Patroni は `initdb` を使用して新しいクラスターをブートストラップし、`pg_basebackup` を使用して `leader` メンバーのコピーからスタンバイ ノードを作成します。

カスタム ブートストラップ メソッドとカスタム レプリカ作成メソッドを作成することで、その動作をカスタマイズできます。

カスタム メソッドは通常、pgBackRest や Barman などのバックアップ ツールによって作成されたバックアップを復元する場合に役立ちます。

詳細については、[カスタムブートストラップ](/ja/patroni/replica_bootstrap#custom_bootstrap) および [カスタムレプリカの作成](/ja/patroni/replica_bootstrap#custom_replica_creation) を参照してください。

--------

## モニタリング {#monitoring}

Patroni クラスターを監視するにはどうすればよいですか？

Patroni は、[REST API](/ja/patroni/rest_api#rest_api) でいくつかの便利なエンドポイントを公開します。

- `/metrics`: Prometheus で使用できる形式でモニタリング メトリクスを公開します。
- `/patroni`: ローカルの Patroni/Postgres ノードの状態を JSON 形式で公開します。ここに表示される情報は、`/metrics` エンドポイントによって表示される情報と非常に似ています。

これらのエンドポイントを使用して、監視チェックを実装できます。
