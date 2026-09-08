---
title: "FAQ"
weight: 180
icon: fa-solid fa-circle-question
description: "Patroni の操作とトラブルシューティングに関するよくある質問。"
module: [PATRONI]
categories: [リファレンス]
aliases: [/docs/patroni/faq/]
upstream_link: "https://patroni.readthedocs.io/en/latest/faq.html"
---

<a id="faq"></a>
このセクションでは、Patroni に関して最もよくある質問に対する回答を示します。各サブセクションでは、さまざまな種類の質問に焦点を当てます。

これがあなたの疑問のほとんどを解決するのに役立つことを願っています。さらに懸念がある場合、または予期しない問題に直面している場合は、[おしゃべり](/ja/patroni/contributing_guidelines#chatting) および [reporting_bugs](/ja/patroni/contributing_guidelines#reporting_bugs) を参照して、ヘルプを取得したり問題を報告したりする方法を確認してください。

--------

## 他の HA ソリューションとの比較 {#comparison-with-other-ha-solutions}

`repmgr` などの他のソリューションでは必要ないのに、Patroni では DCS ノードの別個のクラスターが必要なのはなぜですか?   HA ソリューションを実装するにはさまざまな方法があり、それぞれに長所と短所があります。

`repmgr` のようなソフトウェアは、ノード間で通信を実行して、いつアクションを実行するかを決定します。

一方、Patroni は、DCS に保存されている状態に依存します。 DCS は、Patroni が何をすべきかを決定するための信頼できる情報源として機能します。

個別の DCS クラスターを使用するとアーキテクチャが肥大化する可能性がありますが、このアプローチにより、Postgres クラスター内でスプリット ブレイン シナリオが発生する可能性も低くなります。

Postgres 管理に関して、Patroni と他の HA ソリューションの違いは何ですか?   Patroni は、Postgres クラスターの高可用性を管理するだけでなく、Postgres 自体も管理します。

Postgres ノードがまだ存在しない場合は、プライマリー ノードとスタンバイ ノードのブートストラップが行われ、ノードの Postgres 構成も管理されます。 Postgres ノードがすでに存在する場合、Patroni がクラスターの管理を引き継ぎます。

上記に加えて、Patroni には自己修復機能もあります。つまり、プライマリー ノードに障害が発生した場合、Patroni はレプリカにフェイルオーバーするだけでなく、新しいプライマリーのレプリカとして元のプライマリーに再参加しようとします。同様に、レプリカに障害が発生した場合、Patroni はそのレプリカへの再参加を試みます。

これは、Patroni を「HA ソリューションのテンプレート」と呼ぶ方法です。単に物理レプリケーションを管理するだけでなく、Postgres を全体として管理します。

--------

## DCS {#dcs}

同じ `etcd` クラスターを使用して、2 つ以上の Patroni クラスターからのデータを保存できますか?   はい、できます！

Patroni クラスターに関する情報は、`namespace` および `scope` Patroni 設定がプレフィックスとして付けられたパスの下の DCS に保存されます。

異なる Patroni クラスター間で競合する名前空間とスコープがない限り、同じ DCS クラスターを使用して複数の Patroni クラスターからの情報を保存できるはずです。

同じDCSクラスターを参照する異なるPatroniクラスターで、同じ`namespace`と`scope`の組み合わせを使用するとどうなりますか？  
同じ`namespace`と`scope`を使用しようとする2つ目のPatroniクラスターは、Postgresを管理できません。同じ組み合わせの情報をDCS内に見つけますが、Postgresのシステム識別子が一致しないためです。システム識別子が一致しないと、Patroniは別のクラスターの情報を参照しており、ユーザーの設定に誤りがあると判断して、2つ目のクラスターの管理を中止します。

同じ DCS クラスターを共有する異なる Patroni クラスターを処理する場合は、必ず異なる `namespace` / `scope` を使用してください。

DCS クラスターを失った場合はどうなりますか?   DCS は、基本的に Patroni クラスターのステータスと動的構成を保存するために使用されます。

その最初の結果は、[dcs_failsafe_mode](/ja/patroni/dcs_failsafe_mode#dcs_failsafe_mode) が有効になっていない限り、その DCS に依存するすべての Patroni クラスターが読み取り専用モードになることです。

DCS クラスターを失った場合はどうすればよいですか?   DCS クラスターが失われた場合、考えられる結果は 3 つあります。

1. DCS クラスターは完全に回復されました。これには、Patroni 側からのアクションは必要ありません。 DCS クラスターが回復すると、Patroni も回復できるはずです。
2. DCS クラスターが適切な場所に再作成され、エンドポイントは同じままになります。 Patroni 側では変更は必要ありません。
3. 新しい DCS クラスターが異なるエンドポイントで作成されます。各 Patroni ノードの Patroni 構成内の DCS エンドポイントを更新する必要があります。

`2.` または `3.` のシナリオに直面した場合、Patroni はクラスターの現在のステータスに基づいてステータス情報を再度作成し、Patroni クラスターの各メンバーの Postgres データ ディレクトリ内に保存されている `patroni.dynamic.json` という名前のバックアップ ファイルに基づいて DCS 上に動的構成を再作成します。

DCS クラスターの過半数を失った場合はどうなりますか?   DCS が応答しなくなるため、Patroni は現在の読み取り/書き込み Postgres ノードを降格させます。

覚えておいてください: Patroni は、DCS の状態に依存してクラスター上でアクションを実行します。

[dcs_failsafe_mode](/ja/patroni/dcs_failsafe_mode#dcs_failsafe_mode) を使用すると、この状況を軽減できます。

--------

## patronictl {#patronictl}

Patroni ホストで [patronictl](/ja/patroni/patronictl#patronictl) を実行する必要がありますか?   いいえ、その必要はありません。

Patroni ホストにアクセスできる場合、Patroni ホストで [patronictl](/ja/patroni/patronictl#patronictl) を実行すると、[patronictl](/ja/patroni/patronictl#patronictl) アプリケーションの `patroni` エージェントからまったく同じ構成ファイルを使用できるため便利です。

ただし、[patronictl](/ja/patroni/patronictl#patronictl) は基本的にクライアントであり、リモート マシンから実行できます。必要なのは、Patroni メンバーの DCS および REST API にアクセスできるように、十分な構成を提供することだけです。

Patroni メンバーの 1 人からの情報が [patronictl_list](/ja/patroni/patronictl#patronictl_list) コマンドの出力から消えたのはなぜですか?   [patronictl_list](/ja/patroni/patronictl#patronictl_list) で表示される情報は、DCS の内容に基づいています。

メンバーに関する情報が DCS から消えた場合は、そのノード上の Patroni エージェントが実行されていないか、DCS と通信できない可能性が高くなります。

メンバーは情報を更新できないため、情報は最終的に DCS から期限切れになり、その結果メンバーは [patronictl_list](/ja/patroni/patronictl#patronictl_list) の出力に表示されなくなります。

[patronictl_list](/ja/patroni/patronictl#patronictl_list) コマンドの出力で、Patroni メンバーの 1 つに関する情報が最新ではないのはなぜですか?   [patronictl_list](/ja/patroni/patronictl#patronictl_list) で表示される情報は、DCS の内容に基づいています。

デフォルトでは、その情報は Patroni によってほぼ `loop_wait` 秒ごとに更新されます。つまり、すべてが正常に機能している場合でも、DCS に保存されている情報に最大 `loop_wait` 秒の "delay" が表示される可能性があります。

ただし、これはルールではないことに注意してください。 Patroni によって実行される一部の操作により、DCS 情報が即座に更新されます。

--------

## 構成 {#configuration}

動的構成とローカル構成の違いは何ですか?   動的構成 (またはグローバル構成) は、DCS に保管される構成であり、Patroni クラスターのすべてのメンバーに適用されます。これは主に構成を保存する場所です。

ノードに固有の設定、またはグローバル構成を上書きする設定は、目的の Patroni メンバーにのみローカル構成として設定する必要があります。そのローカル構成は、構成ファイルまたは環境変数を通じて指定できます。

詳細については、[構成](/ja/patroni/config#config) を参照してください。

Patroni の構成の種類と優先順位は何ですか?   種類は次のとおりです。

- 動的構成: すべてのメンバーに適用されます。
- ローカル構成: ローカルメンバーに適用され、動的構成をオーバーライドします。
- Environment 構成: ローカル メンバーに適用され、動的構成とローカル構成の両方がオーバーライドされます。

**注:** 一部の Postgres GUC はグローバルに、つまり動的構成を通じてのみ設定できます。これに加えて、Patroni がハードコードされた値を強制する GUC もあります。

詳細については、[構成](/ja/patroni/config#config) を参照してください。

Patroni 構成ファイルの作成に役立つ機能はありますか?   はい、あります。

`patroni --generate-sample-config` または `patroni --generate-config` コマンドを使用して、それぞれ既存の Postgres インスタンスに基づいてサンプルの Patroni 構成または Patroni 構成を生成できます。

詳細については、[generate_sample_config](/ja/patroni/config#generate_sample_config) および [generate_config](/ja/patroni/config#generate_config) を参照してください。

`bootstrap.dcs` 構成でパラメーターを変更しましたが、Patroni は変更をクラスター メンバーに適用しません。なにが問題ですか？   `bootstrap.dcs` で構成された値は、新しいクラスターをブートストラップする場合にのみ使用されます。これらの値は、ブートストラップ中に DCS に書き込まれます。

ブートストラップ フェーズが終了した後は、DCS を介してのみ動的構成を変更できます。

詳細については、次の質問を参照してください。

動的構成を変更するにはどうすればよいですか?   DCS の構成を変更する必要があります。これは、次のいずれかの方法で実現されます。

- [patronictl_edit_config](/ja/patroni/patronictl#patronictl_edit_config);または
- A `PATCH` から [config_endpoint](/ja/patroni/rest_api#config_endpoint) へのリクエスト。

ローカル設定を変更するにはどうすればよいですか?   対応する Patroni メンバーの構成ファイルを変更し、`SIHGUP` を使用して Patroni エージェントに通知する必要があります。これは、次のいずれかのアプローチを使用して実行できます。

- `POST` リクエストを REST API [reload_endpoint](/ja/patroni/rest_api#reload_endpoint) に送信します。または

- [patronictl_reload](/ja/patroni/patronictl#patronictl_reload) を実行します。または

- `SIGHUP` を使用して Patroni プロセスにローカルに通知します。

  > - systemd を通じて Patroni を開始した場合は、コマンド `systemctl reload PATRONI_UNIT.service` を使用できます。`PATRONI_UNIT` は Patroni サービスの名前です。または
  > - 他の方法で Patroni を開始した場合は、`patroni` プロセスを特定し、`kill -s HUP PID` を実行する必要があります。`PID` は、`patroni` プロセスのプロセス ID です。

**注:** [patronictl_reload](/ja/patroni/patronictl#patronictl_reload) によるリロードが機能しない場合があります。

- 期限切れの REST API 証明書: [patronictl](/ja/patroni/patronictl#patronictl) の `-k` オプションを使用することでこれを軽減できます。
- 間違った資格情報: たとえば、構成ファイル内の `restapi` または `ctl` 資格情報を変更し、同じ構成ファイルを Patroni および [patronictl](/ja/patroni/patronictl#patronictl) に使用する場合です。

環境構成を変更するにはどうすればよいですか?   環境設定は、起動時に Patroni によってのみ読み取られます。

これを念頭に置いて、環境構成を変更した場合は、対応する Patroni エージェントを再起動する必要があります。

クラスター内でフェイルオーバーが発生しないように注意してください。 [patronictl_pause](/ja/patroni/patronictl#patronictl_pause) をチェックしてみることに興味があるかもしれません。

通常の動作中に繰り返されるハートビート ログの行を減らすにはどうすればよいですか?

`Lock owner: ...` や `no action. I am ...` などの行が繰り返されるためにログにノイズが多すぎる場合は、`log.deduplicate_heartbeat_logs: true` を構成します。

これは、Patroni YAML ファイル ([ログ設定](/ja/patroni/config/yaml#log_settings)) または `PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS=true` を使用して設定できます。

これにより、ハートビート メッセージの繰り返しが抑制されるためログの量が減りますが、フェイルオーバー診断時に役立つループごとのハートビートの可視性も失われることに注意してください。

リロードが必要な Postgres GUC を変更するとどうなりますか?   前の質問で説明したように動的構成またはローカル構成を変更すると、Patroni が Postgres 構成の再ロードを処理します。

再起動が必要な Postgres GUC を変更するとどうなりますか?   Patroni は、影響を受けるメンバーに `pending restart` のフラグを付けます。

メンバーをいつ、どのように再起動するかを決定するのはあなた次第です。これは、次のいずれかの方法で実現できます。

- [patronictl_restart](/ja/patroni/patronictl#patronictl_restart);または
- A `POST` から [restart_endpoint](/ja/patroni/rest_api#restart_endpoint) へのリクエスト。

**注:** 一部の Postgres GUC では、Postgres ノードを再起動する順序に関して特別な管理が必要です。詳細については、[shared_memory_gucs](/ja/patroni/config#shared_memory_gucs) を参照してください。

Patroni 構成の `etcd` と `etcd3` の違いは何ですか?   `etcd` は `etcd` の API バージョン 2 を使用し、`etcd3` は `etcd` の API バージョン 3 を使用します。

API バージョン 2 によって保存された情報は、API バージョン 3 では管理できず、その逆も同様であることに注意してください。

次の理由から、`etcd` ではなく `etcd3` を構成することをお勧めします。

- API バージョン 2 は、etcd v3.4 以降、デフォルトで無効になっています。
- API バージョン 2 は etcd v3.6 から完全に削除されます。

Patroni 構成で `use_slots` を有効にしていますが、クラスター メンバーがしばらくオフラインになると、そのメンバーによって使用されているレプリケーション スロットが上流ノードで削除されます。その問題を回避するにはどうすればよいでしょうか?   次の 2 つのオプションがあります。

1. `member_slots_ttl` (デフォルト値 `30min`、Patroni `4.0.0` および PostgreSQL 11 以降で利用可能) を調整でき、メンバーのダウンタイムが構成されたしきい値より短い場合、欠落メンバーのレプリケーション スロットは削除されません。
2. メンバーに対して永続的な物理レプリケーション スロットを構成できます。

Patroni `3.2.0` 以降、メンバー スロットを Patroni によって管理される永続スロットとして持つことができるようになりました。

Patroni はすべてのノードに永続的な物理スロットを作成し、スロットが削除されないようにするだけでなく、メンバーによって使用された LSN に従ってすべてのノードのスロットの LSN を進めます。

後で、対応するメンバーを削除する場合は、**あなたの責任** が永続スロット構成を調整します。それ以外の場合、Patroni はスロットを永久に保持します。

`3.2.0` よりも古い Patroni 上の **注:** では、メンバー スロットを永続的な物理スロットとして構成できますが、それらは現在のリーダーでのみ管理されます。つまり、フェイルオーバー/スイッチオーバーの場合、これらのスロットは新しいリーダー上に作成されますが、存在しないノードのすべての WAL セグメントがあることは保証されません。

**注意：** Patroni `3.2.0`でも、小さな競合状態が発生する可能性があります。レプリカでスロットが作成された直後は、リーダー上の同じスロットより先に進んでいる場合があります。そのスロットを誰も使用していない場合、フェイルオーバー後に一部のファイルが欠落する可能性が残ります。このため、必要なWALのリストアやPITRを可能にする継続的アーカイブを設定することを推奨します。

`loop_wait`、`retry_timeout`、`ttl` の違いは何ですか?   Patroni は、HA サイクルと呼ばれるものを随時実行します。各 HA サイクルで、クラスターに対して一連のチェックを実行してその健全性を判断し、ステータスに応じてスタンバイへのフェイルオーバーなどのアクションを実行する場合があります。

`loop_wait` は、HA チェックの新しいサイクルを実行する前に Patroni がスリープする時間を秒単位で決定します。

`retry_timeout` は、DCS および Postgres での再試行操作のタイムアウトを設定します。たとえば、DCS が `retry_timeout` 秒を超えて応答しない場合、Patroni はセキュリティ アクションとしてプライマリー ノードを降格する可能性があります。

`ttl` は、DCS の `leader` ロックのリース時間を設定します。クラスターの現在のリーダーが、HA サイクル中に `ttl` を超えてリースを更新できない場合、リースは期限切れになり、クラスター内で `leader race` がトリガーされます。

**注:** これらの設定を変更する場合は、Patroni がドキュメントの [ダイナミックな](/ja/patroni/config/dynamic#dynamic) セクションで説明されているルールと最小値を強制することに注意してください。

--------

## Postgres 管理 {#postgres-management}

Postgres 構成で Postgres GUC を直接変更できますか?   可能ですが、それは避けるべきです。

Postgres 構成は Patroni によって管理されており、構成ファイルを編集しようとすると、最終的に構成ファイルが上書きされる可能性があるため、Patroni によって失敗する可能性があります。

Patroni によって実行される管理を回避するために使用できるオプションがいくつかあります。

- `$PGDATA/postgresql.base.conf` を通じて Postgres GUC を変更します。または
- `postgresql.base.conf` の代わりに使用される `postgresql.custom_conf` を定義して、外部で管理できるようにします。または
- `ALTER SYSTEM` / `ALTER DATABASE` / `ALTER USER` を使用して GUC を変更します。

詳細については、セクション [important_configuration_rules](/ja/patroni/config#important_configuration_rules) を参照してください。

いずれの場合も、Patroni を通じてすべての Postgres 構成を管理することをお勧めします。これにより、管理が集中化され、必要な場合の Patroni のデバッグが容易になります。

Postgres ノードを直接再起動できますか?   いいえ、**そうではない** で Postgres を直接管理する必要があります。

Patroni を使用せずに Postgres サーバーをバウンスしようとすると、クラスターがフェイルオーバーに直面する可能性があります。

Postgres サーバーを管理する必要がある場合は、Patroni によって公開されている方法で実行してください。

Patroni は、既存の Postgres クラスターの管理を引き継ぐことができますか?   はい、できます！

詳細な手順については、[existing_data](/ja/patroni/existing_data#existing_data) を参照してください。

Patroni は Postgres をどのように管理しますか?   Patroni は、`pg_ctl` や `postgres` などの Postgres バイナリを実行することによって、Postgres の起動と停止を処理します。

これを念頭に置いて、**MUST** は、systemd ユニットなど、Postgres クラスターを管理できる他のソースを無効にします。 `postgresql.service`。 Patroni のみがクラスター内の Postgres インスタンスを開始、停止、昇格できる必要があります。そうしないと、スプリット ブレイン シナリオが発生する可能性があります。たとえば、プライマリーとして実行されているノードに障害が発生し、ユニット `postgresql.service` が有効になっている場合、Postgres がバックアップされ、スプリット ブレインが発生する可能性があります。

--------

## 概念と要件 {#concepts-and-requirements}

Patroni の一部を構成するアプリケーションはどれですか?   Patroni には基本的にいくつかのアプリケーションが同梱されています。

- `patroni`: これは、Postgres ノードの管理を担当する Patroni エージェントです。
- [patronictl](/ja/patroni/patronictl#patronictl): これは、Patroni クラスターと対話する (スイッチオーバー、再起動、構成の変更などを実行する) ために使用されるコマンドライン ユーティリティです。詳細については、[patronictl](/ja/patroni/patronictl#patronictl) を参照してください。

Patroni の `standby cluster` とは何ですか?   これは、プライマリー Postgres ノードが実行されていないクラスターです。つまり、クラスター内に読み取り/書き込みメンバーがありません。

これらの種類のクラスターは、別のクラスターからデータをレプリケートするために存在し、通常、データ センター間でデータをレプリケートする場合に役立ちます。

クラスター内には、リモート Postgres ノードからの変更の複製を担当するスタンバイとなるリーダーが存在します。次に、そのようなリーダー メンバーからのカスケード レプリケーションで構成された一連のスタンバイが存在します。

**注:** スタンバイ クラスターは、複製元のソース クラスターについて何も知りません。WAL ストリーミングの代わりに `restore_command` を使用することもでき、完全に独立した DCS クラスターを使用することもあります。

詳細については、[standby_cluster](/ja/patroni/standby_cluster#standby_cluster) を参照してください。

Patroni の `leader` とは何ですか?   Patroni の `leader` は、クラスターのコーディネーターのようなものです。

通常の Patroni クラスターでは、`leader` が読み取り/書き込みノードになります。

スタンバイ Patroni クラスターでは、`leader` (AKA `standby leader`) がリモート Postgres ノードからのレプリケーションを担当し、それらの変更をスタンバイ クラスターの他のメンバーにカスケードします。

Patroni では、クラスター内に最小数の Postgres ノードが必要ですか?   いいえ、Patroni は任意の数の Postgres ノードで実行できます。

Patroni は DCS から分離されていることに注意してください。

Patroni の [一時停止する](/ja/patroni/pause#pause) は何を意味しますか?   一時停止は Patroni によって公開される操作であるため、ユーザーは Postgres 管理に関して Patroni にステップバックするよう要求できます。

これは主に、クラスターでメンテナンスを実行する必要があり、プライマリーを停止したときにスタンバイにフェイルオーバーするなど、Patroni が HA に関連する決定を行うのを避けたい場合に役立ちます。

詳細については、[一時停止する](/ja/patroni/pause#pause) を参照してください。

--------

## 自動フェイルオーバー {#automatic-failover}

Patroni の自動フェイルオーバー メカニズムはどのように機能しますか?   Patroni 自動フェイルオーバーは、`leader race` と呼ばれるものに基づいています。

Patroni は、クラスターのステータスを DCS に保存します。その中には、クラスターの現在の `leader` である Patroni メンバーの名前を保持する `leader` ロックがあります。

その `leader` ロックには有効期限が関連付けられています。リーダー ノードが `leader` ロックのリースを期限内に更新できなかった場合、キーは最終的に DCS から期限切れになります。

`leader` ロックの有効期限が切れると、Patroni による `leader race` の呼び出しがトリガーされ、すべてのノードがチェックの実行を開始して、`leader` ロールを引き継ぐ最適な候補であるかどうかを判断します。これらのチェックの一部には、他のすべての Patroni メンバーの REST API への呼び出しが含まれます。

`leader` ロックを引き継ぐための最良の候補であると判断したすべての Patroni メンバーは、引き継ぎを試みます。 `leader` ロックを取得できる最初の Patroni メンバーは、読み取り/書き込みノード (または `standby leader`) に昇格し、他のメンバーはこれに従うように構成されます。

Patroni クラスターで自動フェイルオーバーを一時的に無効にすることはできますか?   はい、できます！

これを実現するには、クラスターを一時的に停止します。これは通常、メンテナンスを実行する場合に役立ちます。

クラスターの自動フェイルオーバーを再開したい場合は、一時停止を解除するだけです。

詳細については、[一時停止する](/ja/patroni/pause#pause) を参照してください。

--------

## ブートストラップとスタンバイの作成 {#bootstrapping-and-standbys-creation}

Patroni はプライマリー Postgres ノードをどのように作成しますか?スタンバイ Postgres ノードについてはどうですか?   デフォルトでは、Patroni は `initdb` を使用して新しいクラスターをブートストラップし、`pg_basebackup` を使用して `leader` メンバーのコピーからスタンバイ ノードを作成します。

カスタム ブートストラップ メソッドとカスタム レプリカ作成メソッドを作成することで、その動作をカスタマイズできます。

カスタム メソッドは通常、pgBackRest や Barman などのバックアップ ツールによって作成されたバックアップを復元する場合に役立ちます。

詳細については、[custom_bootstrap](/ja/patroni/replica_bootstrap#custom_bootstrap) および [custom_replica_creation](/ja/patroni/replica_bootstrap#custom_replica_creation) を参照してください。

--------

## モニタリング {#monitoring}

Patroni クラスターを監視するにはどうすればよいですか?   Patroni は、[rest_api](/ja/patroni/rest_api#rest_api) でいくつかの便利なエンドポイントを公開します。

- `/metrics`: Prometheus で使用できる形式でモニタリング メトリクスを公開します。
- `/patroni`: クラスターのステータスを JSON 形式で公開します。ここに表示される情報は、`/metrics` エンドポイントによって表示される情報と非常に似ています。

これらのエンドポイントを使用して、監視チェックを実装できます。
