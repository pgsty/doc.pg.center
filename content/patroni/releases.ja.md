---
title: "リリースノート"
weight: 190
icon: fa-solid fa-scroll
description: "時系列の Patroni リリース ノートと変更履歴。"
module: [PATRONI]
categories: [リファレンス]
aliases: [/docs/patroni/releases/]
upstream_link: "https://patroni.readthedocs.io/en/latest/releases.html"
---

<a id="releases"></a>

--------

## バージョン 4.1.5 {#version-415}

2026-08-12 をリリース

**互換性の向上**

- PostgreSQL との互換性 14.24、15.19、16.15、17.11、18.6 (Alexander Kukushkin)

新しい `output_plugin_libraries` GUC を追加します。これは、論理デコード出力プラグインを制限します。

**改善点**

- Log REST API 接続は `WARNING` ではなく `DEBUG` でリセットされます (Kyle McLaren)

本物の (接続以外の) エラーの処理に影響を与えることなく、一般的な「書き込み中にクライアントが消えた」という亜種が沈黙していることを確認します。

**バグ修正**

- `thread_stack_size` 検証の調整を修正 (Sundong Kim)

`thread_stack_size` スキーマ エントリの `aligned` 値を `65535` から `65536` に修正します。以前は、`patroni --validate-config` は、デーモン自体によって適用される `524288` デフォルトを含む、ほぼすべての現実的な値を拒否していました。

- `'quorum'` およびブール型の文字列を受け入れるための `synchronous_mode` の検証を許可します (Eray Araz)

`patroni --validate-config` は、以前は、実行時に受け入れられる `quorum` や PostgreSQL スタイルのブール文字列などの `synchronous_mode` 値を拒否していました。

## バージョン 4.1.4 {#version-414}

2026-07-07 をリリース

**バグ修正**

- `systemd` パッケージを使用する前に `NOTIFY_SOCKET` 環境変数を確認してください (Polina Bungina)

`FileNotFoundError: [Errno 2] No such file or directory` 例外を回避するために、`NOTIFY_SOCKET` 環境変数が設定されている場合にのみ、パッケージをインポートして使用してください。

- `pg_replication_slots` クエリーを統合 (Polina Bungina)

`failover` 値と `synced` 値の不適切な処理により、不適切な論理レプリケーション スロットの削除中に `KeyError` 例外が発生していました。

- 構成生成時にバージョン固有の認証パラメーターを考慮する (Polina Bungina)

`patroni --generate-config` コマンドでは、PostgreSQL 接続から取得したバージョンに基づいて、環境から誤って取得された適用できない認証パラメーターをすべて削除します。

- PostgreSQL インスタンスがスタンバイとして起動している間に `pg_rewind` を処理します (Alexander Kukushkin)

PostgreSQL インスタンスが実行中であるがまだ接続を受け入れていない場合は、`pg_controldata` 情報にフォールバックします。

- `patroni_postgres_timeline` の Prometheus メトリック タイプを修正しました (Huseyin Demir)

`patroni_postgres_timeline` メトリクスは、常に単調増加するとは限らないため、`counter` ではなく `gauge` として宣言します (たとえば、PostgreSQL インスタンスが実行されていない場合は、0 にリセットされる可能性があります)。

- クライアントのバックエンドが完全に停止するまでウォッチドッグを停止しないでください。 (Alexander Kukushkin)

以前は、`primary_stop_timeout` が最小ウォッチドッグ タイムアウトより短く、停止タイムアウトが実際に期限切れになった場合、すべてのクライアント バックエンドが終了する前に Patroni がウォッチドッグを無効にしていました。

- Handle クエリー監視のステートメント タイムアウト エラー (Alexander Kukushkin)

ステートメントのタイムアウト エラーが発生した場合は、キャッシュされたロールをフォールバックとして使用して、プライマリーの降格を回避します。さらに、高価な `pg_stat_statements` GC 呼び出しを回避するために、監視クエリーの `pg_stat_statements.track` を `none` に強制的に設定します。

- `wal_status=lost` を使用した Patroni 管理のレプリケーション スロットの削除 (Alexander Kukushkin)

`wal_status=lost` を使用したレプリケーション スロットは使用できなくなりました。 Patroni は、そのようなスロットを削除し、必要に応じて再作成するようになりました。

- patronictl メンバー検証エラーのロール表現を修正しました (Polina Bungina)

例外メッセージ内で正しい文字列表現が使用されていることを確認し、エラーが `Error: No CtlPostgresqlRole.REPLICA among provided members` のような形式になるのを防ぎます。

## バージョン 4.1.3 {#version-413}

2026-05-05 をリリース

**安定性の向上**

- ラベルが間違っている etcd エラーを適切に処理する (Ants Aasma)

現在の etcd バージョンでは、リースの更新中に etcd リーダーが失われると、`Unknown` エラーが発生します。 Patroni は、報告されたエラー コードを `Unavailable` にオーバーライドします。

**バグ修正**

- `PG_VERSION` ファイルが存在しない場合はバイナリ バージョンを使用する (Polina Bungina)

場合によっては、たとえばカスタム ブートストラップを使用する場合、`PG_VERSION` ファイルがデータ ディレクトリに存在しないことがあります。この場合、Patroni はバージョンを 0.0 として扱っていたため、バージョン固有のロジックの一部で問題が発生していました。この修正により、Patroni はそのような場合にバイナリからバージョンを取得しようとします。

- 初期のログメッセージの欠落を避けるためにロガーの初期化をリファクタリングしました。 (Alexander Kukushkin)

初期のログ メッセージをキャプチャするには、`Config` をロードする前に `PatroniLogger` を作成します。

- `RELOADING=1` systemd 通知に `MONOTONIC_USEC` を含めます (Alexander Kukushkin)

systemd 257+ では、`Type=notify-reload` サービス用に `RELOADING=1` とともに `MONOTONIC_USEC` が必要です。これがないと、`systemctl reload` は無期限にハングします。

**改善点**

- `backup_label` が存在する場合、シングルユーザーのクラッシュ リカバリをスキップします。 (Vadim Ponomarev)

(カスタム ブートストラップ メソッドを使用せずに) 外部バックアップから復元されたレプリカを起動するときは、シングル ユーザー クラッシュ リカバリをスキップし、通常の起動中に PostgreSQL に処理させます。

- `python-systemd` パッケージを使用せずに `systemd` で実行すると Warn が表示されるようになりました。 (Alexander Kukushkin)

起動時に「systemd 統合はサポートされていません」とログに記録する代わりに、`NOTIFY_SOCKET` を確認し、`python-systemd` パッケージがインストールされていない `systemd` で実際に実行している場合にのみ警告します。

## バージョン 4.1.2 {#version-412}

2026-04-21 をリリース

**Systemd サポートの改善**

- `notify-reload` systemd ユニット タイプのサポートを追加しました (Ronan Dunklau)

`RELOADING=1` および `READY=1` 通知を systemd に送信することで、Patroni が実際に構成のリロードを処理するまで、`systemctl reload` が待機できるようにします。

- シャットダウン時に `STOPPING=1` 通知を systemd に送信します (Alexander Kukushkin)

Patroni は、systemd 通知プロトコルに従って、systemd にシャットダウンしていることを適切に通知するようになりました。

- PostgreSQL に systemd を通知させないでください。 (Alexander Kukushkin)

サンプルの systemd ユニット ファイルから `NotifyAccess=all` を削除します。 PostgreSQL の起動時に環境から `NOTIFY_SOCKET` をフィルターして、`READY=1` または `STOPPING=1` が systemd に送信されないようにします。 Patroni より前に開始され、すでに `NOTIFY_SOCKET` がある PostgreSQL を引き継ぐ場合は、PostgreSQL のシャットダウン中に `READY=1` を再アサートして、その `STOPPING=1` を無効にします。

## バージョン 4.1.1 {#version-411}

2026-04-08 をリリース

**安定性の向上**

- Python のスレッド変更との互換性 3.11+ (Alexander Kukushkin)

実行時にスレッドを開始/停止しないようにします。 REST API および非同期タスクを実行するためのスレッド プールを導入します。グローバル `thread_pool_size` および `restapi.thread_pool_size` の構成を許可します。

- Python との互換性 3.14 (Alexander Kukushkin)

Python 3.14 に対してテストを実行し、互換性の問題を修正します。

- v3.6.9、v3.5.28、v3.4.42 の etcd セキュリティ修正との互換性 (Alexander Kukushkin)

これらの etcd リリースでは CVE に対処し、動作が変更されたため、クラスター トポロジの読み取りとリース キープアライブは認証なしでは許可されなくなりました。 Patroni は、メンバー検出パスとリースキープアライブ パスで認証し、認証失敗時に再認証し、それに応じてリクエストを再試行することでこれを処理するようになりました。

- Etcd3 エラー処理の改善 (Alexander Kukushkin)

壊れた JSON 応答を処理し、JSON エラーの解析方法を柔軟にし、etcd 内部エラーのレポートを改善します。

**バグ修正**

- 一時的な Kubernetes `403` エラーでリーダーの更新を再試行します (Sophia Ruan、Alexander Kukushkin)

Kubernetes API が一時的に `403 Permission Denied` を返す場合 (たとえば、一時的な RBAC の問題中)、Patroni は現在のノードがまだリーダーシップを保持しているかどうかを確認し、すぐに降格するのではなく `retry_timeout` 内でリーダーの更新を再試行するようになりました。

- 同期モードおよび一時停止時のリーダーノードの名前変更に関する問題を修正しました。 (Alexander Kukushkin)

`/sync` キーは、一時停止中の Patroni 再起動 (Postgres 再起動なし) でリーダー ノードの名前を変更した後、更新されませんでした。これにより、次回の再起動後に一時停止せずに Patroni が昇格できなくなりました。

- Trigger `pg_rewind` チェックは、同じプライマリーがタイムラインを増やしたときに行われます。 (Alexander Kukushkin)

このようなタイムラインの増加は、シングル ユーザー モードでのクラッシュ リカバリと、他のレプリカ ノードが DCS から分離されている間にリーダー キーを取得した後のプロモートの結果として発生する可能性があります。この場合、リーダー、したがって `primary_conninfo` が変更されなかったため、レプリカ ノードは `pg_rewind` ステート マシンをトリガーしませんでした。

- スーパーユーザーのパスワードが空でない場合は、`initdb` ブートストラップ中にのみ書き込みます。 (Michael Bank)

`initdb` ブートストラップ中に空のパスワードを書き込むと問題が発生していました。

- `failover_priority` のバグを `synchronous_mode=on` で修正しました (Alexander Kukushkin)

`synchronous_node_count > 1` の場合、`tag.failover_priority` 値は無視されました。

- `primary_conninfo` パスワード比較のバグを修正しました (Alexander Kukushkin)

PostgreSQL 10 以降、Patroni は `primary_conninfo` でパスファイルを使用しますが、リロードを伴う yaml ファイル構成でレプリケーション パスワードが更新された後、パスファイルの更新に失敗しました。

- `nofailover` タグを使用してレプリカを一時停止モードで再起動しないでください。 (Alexander Kukushkin)

Patroni は、`nofailover` タグが `true` に設定されている場合、手動でシャットダウンした PostgreSQL レプリカを一時停止モードで起動していました。

- PostgreSQL が開始状態の場合の `check_recovery_conf()` を修正しました。 (Alexander Kukushkin)

PostgreSQL v12 以降の場合、サーバーがまだ起動中で接続を受け入れていない間は、`pg_settings` をクエリーできません。 `postgresql.conf` を書き込むときに、不足している回復パラメーターが内部状態に追加されるようになりました。さらに、`Ha.is_healthiest_node()` の `Postgresql.is_starting()` チェックを復元します。

- `initdb`/`basebackup` のユーザー オプションを辞書形式で検証します (m4rrypro)

`initdb` または `basebackup` オプションが (リストではなく) ディクショナリとして提供された場合、`option_is_allowed()` 検証がバイパスされ、ブロックされたオプションの使用が可能になりました。

- `basebackup` オプションのサーバー側圧縮を許可する (m4rrypro)

`compress` オプションは `basebackup` では完全にブロックされていましたが、PostgreSQL 15 以降、サーバー側の圧縮は便利で、プレーンな形式で透過的に機能します。クライアント側の圧縮は依然として拒否されます。

- カスタム ブートストラップの実行中に PostgreSQL 設定をリロードしないでください。 (Alexander Kukushkin)

カスタム ブートストラップは複雑で、PostgreSQL の起動と停止が複数回行われる可能性があります。このプロセス中に PostgreSQL 構成をリロードすると、予期しない動作が発生する可能性があります。

- `postgresql.parameters` が辞書であることを確認します。 (Alexander Kukushkin)

`postgresql.parameters` が辞書ではない場合、新しい設定を破棄します。

## バージョン 4.1.0 {#version-410}

2025-09-23 をリリース

**新機能**

- systemd "notify" ユニット タイプのサポートを追加しました (Ronan Dunklau)

通知ユニット タイプを使用しない場合、Patroni を開始し、systemd を使用してすぐに SIGHUP シグナルを送信し、シグナル ハンドラーを設定する前に事実上強制終了することができます。

- API および ctl で受信および再生 LSN/ラグ情報を提供します (Polina Bungina)

Patroni REST API `/cluster` エンドポイントと `patronictl list` コマンドは、各レプリカ メンバーの受信 LSN、リプレイ LSN、受信ラグ、およびリプレイ ラグ情報を提供するようになりました。

- スタンバイ クラスターへの完全な降格を確実にする (Polina Bungina)

動的構成に [standby_cluster](/ja/patroni/standby_cluster#standby_cluster) セクションを導入すると、クラスターが適切に降格されるようにしてください。

- `patronictl demote-cluster` および `promote-cluster` コマンドを実装する (Polina Bungina)

クラスターの降格と昇格のための新しいコマンドは、動的構成の編集と結果ステータスの確認の両方を処理します。

- `sync_priority` タグを実装する (Polina Bungina)

このパラメータは、[synchronous_mode](/ja/patroni/replication_modes#synchronous_mode) が `on` に設定されている場合に、同期レプリカの選択中にメンバーが持つべき優先順位を制御します。

- `--validate-config` の `--print` オプションを実装します (Polina Bungina)

検証が成功したら、ローカル構成 (環境構成の上書きを含む) を出力します。

- `kubernetes.bootstrap_labels` の実装 (Polina Bungina)

この機能を使用すると、`initializing new cluster`、`running custom bootstrap script`、`starting after custom bootstrap`、または `creating replica` 状態にあるときにメンバー ポッドに割り当てられるラベルを定義できます。

- 重複するハートビート ログを抑制する構成オプションを追加しました (Michael Morris)

`true` に設定すると、同一のハートビートログが連続して出力されなくなります。

- オプションの `cluster_type` 属性を永続レプリケーション スロットに追加しました (Michael Bank)

これにより、特定の永続レプリケーション スロットを常に作成するか、プライマリー クラスターまたはスタンバイ クラスター上にのみ作成するかを設定できます。

- HTTP サーバー ヘッダーを構成可能にする (David Grierson)

HTTP サーバー ヘッダーで公開される情報を制限できる `restapi.server_tokens` 構成パラメーターを導入します。

- 実装の準備状況 API はレプリカ メンバーのレプリケーションをチェックします (Ants Aasma)

以前の実装では、PostgreSQL が開始されるとすぐにレプリカが準備完了したとみなされました。この変更により、レプリカ ポッドは、PostgreSQL がレプリケート中で、リーダーからそれほど遠くない場合にのみ準備ができているとみなされます。

**改善点**

- ウォッチドッグ構成エラーのログ レベルを下げる (Ants Aasma)

ウォッチドッグが `required` モードで構成されていない限り、デバッグ ログ レベルで `Could not activate Linux watchdog device` ログ行を表示します。以前は情報レベルで表示されていました。

- `pg_stat_wal_receiver` の `written_lsn` と `latest_end_lsn` を活用します (Alexander Kukushkin)

`written_lsn` (実際の書き込み LSN) は、`pg_last_wal_receive_lsn()` によって返されるもの (実際にはフラッシュ LSN) よりも優先されるようになりました。 `latest_end_lsn` は、ソース ホスト上の WAL フラッシュを指します。プライマリーの場合、DCS に格納されている値は `loop_wait` 秒ごとにのみ更新されるため、リプレイ ラグをより適切に計算できます。

- `failover=true` オプションで作成されたスロットとの相互作用を回避します。 (Alexander Kukushkin)

この変更は、論理フェイルオーバー スロット機能を完全に機能させるために必要です。

- PostgreSQL 状態を `/metrics` REST API エンドポイントに追加します (Ivan Filianin)

PostgreSQL インスタンスの状態情報が、`/metrics` REST API エンドポイントの Prometheus 形式の出力で利用できるようになりました。

--------

## バージョン 4.0.7 {#version-407}

2025-09-22 をリリース

**新機能**

- PostgreSQL 18 RC1 のサポートを追加 (Alexander Kukushkin)

GUC のバリデータ ルールが拡張されました。 Patroni は、新しいバックグラウンド I/O ワーカーを適切に処理するようになりました。

**バグ修正**

- Windows でのローカルホストの IPv6 への解決に関する潜在的な問題を修正しました。 (András Váczi)

PostgreSQL で `listen_addresses` を構成する場合、`0.0.0.0` または `127.0.0.1` を使用すると、IPv6 を除く IPv4 のみのリスニングが制限されます。ただし、一般的な Windows システムでは、`localhost` はデフォルトで IPv6 アドレス `::1` に解決されることがよくあります。互換性を確保するために、Patroni は、Windows システム上で `localhost` ではなく `127.0.0.1` をリッスンするように PostgreSQL を構成するようになりました。

- `/config` キーが DCS に存在する場合のみグローバル設定を返すようにしました。 (Alexander Kukushkin)

Patroni REST API は、`/config` キーが DCS にない場合、エラーを生成する代わりに空の構成を返していました。

- Etcd が利用できない場合にフェイルセーフ モードがトリガーされない問題を修正しました。 (Alexander Kukushkin)

Patroni は、`etcd3` 例外を常に適切に処理するとは限らず、その結果、フェイルセーフ モードがトリガーされませんでした。

- シグナル ハンドラーの再入デッドロックを修正 (Waynerv)

`PID=1` を使用して Docker コンテナーで実行されている Patroni は、いくつかの特殊な場合に、`SIGCHLD` を受信した後にデッドロックが発生していました。

- WAL が予約されていない場合に (永続的な) 物理スロットを再作成します (Israel Barth Rubio)

WAL を予約せずに Patroni スコープ外で作成された永続的な物理レプリケーション スロットにより、`replication slot cannot be advanced` エラーが発生していました。これを回避するために、Patroni はそのようなスロットを再作成するようになりました。

- `etcd3` の監視キャンセル メッセージを適切に処理するようにしました。 (Alexander Kukushkin)

`etcd3` が監視チャネルにキャンセル メッセージを送信するとき、接続は閉じられません。これにより、Patroni が古いデータを使用することになります。 Patroni は、チャンク化された応答を読み取るループを中断し、Patroni 側の接続を閉じることで問題を解決するようになりました。

- `HTTPConnection` ソケットが `pyopenssl` でラップされている場合の処理 (Alexander Kukushkin)

Patroni は、`python-etcd` で強制されている `pyopenssl` インターフェイスを正しく使用していませんでした。

**ドキュメントの改善**

- 2 ノード クラスター ガイダンスを改善しました (Nikolay Samokhvalov)

フェイルオーバー中の動作と DCS 要件を明確にします。

--------

## バージョン 4.0.6 {#version-406}

2025-06-06 をリリース

**バグ修正**

- 優先順位の高いリーダーからのフェイルオーバーのバグを修正しました。 (Alexander Kukushkin)

Patroni が現在のノードと同じ `LSN` を報告する場合、優先順位の高い以前のリーダーを無視するようにしてください。

- `PGDATA` の外部で作成された `postgresql.conf` ファイルの権限を修正しました (Michael Bank)

`PGDATA` ディレクトリの外に `postgresql.conf` ファイルを作成する場合は、システム全体の umask 値を尊重してください。

- `synchronous_mode=quorum` のスイッチオーバーに関するバグを修正しました。 (Alexander Kukushkin)

候補者が指定されている場合は、定足数要件をチェックしません。

- クラスター用語を比較して古い etcd ノードを無視します (Alexander Kukushkin)

etcd クラスターの最後の既知の "raft_term" を記憶し、クライアント リクエストを実行するときに、それを etcd ノードによって報告された "raft_term" と比較します。

- `SIGHUP` 上の PostgreSQL 構成ファイルを更新します (Alexander Kukushkin)

以前は、Patroni は、グローバルまたはローカル構成の変更が検出された場合にのみ、PostgreSQL 構成ファイルを置き換えていました。

- `etcd3` によって発生した `Unavailable` 例外を適切に処理するようにしました。 (Alexander Kukushkin)

Patroni は同じ `etcd3` ノードでそのようなリクエストを再試行するために使用されますが、別のノードに切り替える方がより良い戦略です。

- `etcd3` リース処理を改善しました (Alexander Kukushkin)

Patroni が HA ループごとに少なくとも 1 回、`etcd3` リースを更新するようにしてください。

- リーダー ロックを取得しようとするときに、409 ステータス コードの注釈を再確認します。 (Alexander Kukushkin)

Patroni バージョン 4.0.3 で読み取られたリーダー オブジェクトに対して行われたのと同じ動作を実装します。

- スロットを進めるときは `replay_lsn` を考慮してください (Polina Bungina)

`replay_lsn` を超えてレプリカのスロットを進めようとしないでください。さらに、レプリカ上のこのスロットの `confirmed_flush_lsn` を既に超えているが、レプリカがこのスロットがプライマリー上にある実際の `LSN` をまだ再生していない場合は、スロットを `replay_lsn` の位置に進めます。

- プロモート後に `CHECKPOINT` が実行されていることを確認してください。 (Alexander Kukushkin)

`CHECKPOINT` がまだ終了していないため、チェックポイント タスクが降格時にリセットされなかった可能性があります。その結果、次のプロモートがトリガーされるときに、古い `result` が使用されることになりました。

- "offline" 降格を同時に実行しないでください。 (Alexander Kukushkin)

シャットダウンが遅い場合、次のハートビート ループで DCS エラー処理メソッドが再度ヒットし、`AsyncExecutor is busy, demoting from the main thread` 警告が発生し、オフライン降格が再び開始される可能性があります。

- 初期化失敗時にデータ ディレクトリの名前を変更する前に `data_dir` 値を正規化します (Waynerv)

`data_dir` パラメーター値の末尾のスラッシュによって、初期化の失敗後に名前変更プロセスが中断されないようにします。

- `synchronous_standby_names` に期待値が含まれていることを確認します (Alexander Kukushkin)

以前は、非クォーラム同期レプリケーションのステート マシンを実装するメカニズムは、`synchronous_standby_names` の実際の値をチェックしませんでした。その結果、`pg_stat_replication` が `synchronous_standby_names` のサブセットである場合、`synchronous_standby_names` の古い値が使用されていました。

--------

## バージョン 4.0.5 {#version-405}

2025-02-20 をリリース

**安定性の向上**

- `python-json-logger>=3.1` との互換性 (Alexander Kukushkin)

古い API の使用法によって生成される警告を削除します。

- Python 3.13 との互換性 (Alexander Kukushkin)

Python 3.13 に対してテストを実行します。

- `pyinstaller>=4.4` との互換性 (Joe Jensen)

`pyinstaller` `toc` 属性が存在しない場合は、デフォルトの `iter_modules` にフォールバックします。

- PostgreSQL 9.5 サポートに関する問題を修正しました (Alexander Kukushkin)

  - `pg_rewind` 出力形式を適切に処理します。
  - `synchronous_standby_names` 形式が "num" 仕様をサポートしていないことを考慮してください。

- `urlparse` の最新の変更との互換性 (Alexander Kukushkin)

`urlparse` は、URL に `[]` 文字を含む複数のホストを受け入れなくなりました。この問題を軽減するには、可能な場合は `libpq` から `PQconninfoParse()` のネイティブ ラッパーに切り替え、古いバージョンの `libpq` にリンクされている古い `psycopg2` バージョンに対してのみ実装を使用してください。

**バグ修正**

- 再起動の確認時に再起動されるメンバーのみを表示します (András Váczi)

以前は、`patronictl restart <clustername> --pending` を実行すると、再起動が保留されているかどうかに関係なく、確認ですべてのメンバーがリストされていました。

- Patroni で長時間実行されているジョブをキャンセルし、レプリカ ブートストラップの失敗時にデータ ディレクトリを停止して削除します。 (Alexander Kukushkin)

以前は、`pg_basebackup` / `wal-g` / `pgBackRest` / `barman` などの動作を継続しながら、Patroni がレプリカ ブートストラップを実行できました。

- `patronictl edit-config` でスラッシュを含むクラスター名を適切に処理するようにしました。 (Antoni Mur)

`cluster_name` のスラッシュをアンダースコアに置き換えます。

- 物理スロットを早期に削除しないようにします (Alexander Kukushkin)

フェイルオーバー後に、`xmin` を含む物理レプリケーション スロットの削除を延期します。新しいプライマリーでは、このメンバーが昇格されるまで、レプリカでは、クラスター内にリーダーが存在するまで延期します。

- `controldata()` のサブプロセスによって発生したすべての例外を処理します。 (Alexander Kukushkin)

Patroni は、`pg_controldata` ユーティリティの呼び出し時に発生する可能性のあるすべての例外を適切に処理していませんでした。

- フェイルオーバー時に元リーダーのスロットが保持されないバグを修正しました。 (Alexander Kukushkin)

フェイルオーバー時に前のリーダーの `/member` キーが同時に期限切れになるときに、DCS に存在するメンバーに誤って依存することを避けてください。

- クォーラム ステート マシンのいくつかのバグを修正しました (Alexander Kukushkin)

  - リーダー レースに健全なノードがあるかどうかを評価する場合、降格する前にクォーラム要件を考慮する必要があります。これがないと、元のリーダーが非同期ノードに囲まれて回復することになる可能性があります。
  - `QuorumStateResolver` は、レプリカ ノードがすぐに参加して切断される場合を正しく処理していませんでした。

**改善点**

- 空の設定ファイルまたは辞書以外の設定ファイルでのエラーを改善しました (Julian)

Patroni 構成ファイルに有効な `Mapping` オブジェクトが含まれているかどうかを検証するときに、より明示的な例外をスローします。

--------

## バージョン 4.0.4 {#version-404}

2024-11-22 をリリース

**安定性の向上**

- `py-consul` モジュールとの互換性を追加しました (Alexander Kukushkin)

`python-consul` モジュールは長い間メンテナンスされていませんが、`py-consul` が正式な代替品です。 python-consul との下位互換性は維持されます。

- `prettytable>=3.12.0` モジュールとの互換性を追加しました (Alexander Kukushkin)

非推奨の警告に対処します。

- `ydiff==1.4.2` モジュールとの互換性 (Alexander Kukushkin)

最新バージョンの互換性の問題を修正し、`requirements.txt` でバージョンを制限し、最新バージョンの互換性テストを導入します。

**バグ修正**

- プライマリー リカバリの失敗後に `on_role_change` コールバックを実行する (Polina Bungina、Alexander Kukushkin)

さらに、クラッシュ後に起動に失敗したプライマリーに対して `on_role_change` コールバックを実行して、レプリカとしてのその後の起動が失敗した場合でも、コールバックが実行される可能性を高めます。

- `patronictl list -W` のスレッド リークを修正しました (Alexander Kukushkin)

DCS インスタンス オブジェクトをキャッシュして、スレッド リークを回避します。

- サポートされているパラメータのみが接続文字列に書き込まれるようにしました。 (Alexander Kukushkin)

Patroni は、新しいバージョンで導入されたパラメータを接続文字列に渡していたため、接続エラーが発生していました。

--------

## バージョン 4.0.3 {#version-403}

2024-10-18 をリリース

**バグ修正**

- パスワードを公開しないユーザーを作成するときに `pgaudit` を無効にする (kviset)

`pgaudit` 拡張機能が有効になっている場合、Patroni は作成時に `superuser`、`replication`、および `rewind` のパスワードをログに記録していました。

- 混合セットアップの問題を修正しました: Patroni 以前のプライマリーと v4 と v4+ のレプリカ (Alexander Kukushkin)

リーダー上で実行されている Patroni バージョンが 4.0.0 より前の場合は、`/status` キーからメンバーのスロット位置を取得しようとするのではなく、`/members` キーから抽出された `xlog_location` を使用します。そうしないと、レプリカ上に WAL が蓄積されてしまいます。

- Patroni バリデーターを持たない有効な PostgreSQL GUC を無視しないでください (Polina Bungina)

GUC に Patroni バリデーターがなくても、実際には有効な GUC であるかどうかを、引き続き `postgres --describe-config` に対してチェックします。

**改善点**

- K8s でリーダー オブジェクトを読み取るときに、409 ステータス コードの注釈を再確認します。 (Alexander Kukushkin)

リクエストがターゲットを正常に更新している間に、`PATCH` リクエストが Patroni によってキャンセルされた場合は、追加の更新を回避します。

- `sslnegotiation` クライアント側接続オプションのサポートを追加しました (Alexander Kukushkin)

`sslnegotiation` は、最終的な PostgreSQL 17 リリースに追加されました。

--------

## バージョン 4.0.2 {#version-402}

2024-09-17 をリリース

**バグ修正**

- 構成検証ファイルの検出中に例外を処理します (Alexander Kukushkin)

Patroni にリスト操作を実行するための十分な権限がないディレクトリをスキップします。

- 非アクティブなホット物理レプリケーション スロットが `xmin` を保持しないようにします (Alexander Kukushkin、Polina Bungina)

バージョン 3.2.0 以降、Patroni はレプリカ上のすべてのメンバーに対して物理レプリケーション スロットを作成し、`pg_replication_slot_advance()` 関数を使用してそれらを定期的に前方に移動します。ただし、何らかの理由で `hot_standby_feedback` が有効で、プライマリーがレプリカに降格された場合、現在非アクティブなスロットの `NOT NULL` `xmin` 値が新しいプライマリーに伝播されます。その結果、`xmin` ホライズンは前方に移動されず、バキュームはデッドタプルをクリーンアップできなくなります。この修正により、Patroni は、非アクティブであるはずだが `NOT NULL` `xmin` 値を持つ物理レプリケーション スロットを再作成します。

- 起動フェーズ中に未処理の `DCSError` を修正しました (Waynerv)

ノード名の一意性を確認する前に、DCS 接続を確認してください。

- `pg_settings` のクエリー時に `CMDLINE_OPTIONS` GUC を明示的に含めるようになりました。 (Alexander Kukushkin)

Patroni が実行中のスタンバイに参加するときに、コマンド ライン パラメーターとしてポストマスターに渡されるすべての GUC が復元されていることを確認してください。これは、Patroni 3.2.2 で修正されたバグのフォローアップです。

- `synchronous_standby_names` 引用ロジックのバグを修正しました (Alexander Kukushkin)

PostgreSQL ドキュメントによると、`ANY` および `FIRST` キーワードは二重引用符で囲まれることになっていますが、Patroni では以前は二重引用符で囲まれていませんでした。

- キープアライブ接続の範囲外の問題を修正 (hadizamani021)

`ttl` セットに基づいて計算された `keepalive` オプション値が、現在のプラットフォームで許可されている最大値を超えていないことを確認してください。

--------

## バージョン 4.0.1 {#version-401}

2024-08-30 をリリース

**バグ修正**

- Patroni はそれ自体に不要なレプリケーション スロットを作成していました。 (Alexander Kukushkin)

この問題は、`name` に大文字または特殊文字が含まれている場合に発生していました。

--------

## バージョン 4.0.0 {#version-400}

2024-08-29 をリリース

> [!WARNING]
> - このバージョンでは、"master" という用語を削除し、"primary" を使用する作業が完了しました。これは、いくつかの重大な変更を意味します。リリース ノートをよく読んでください。 Patroni 4+ へのアップグレードは、Patroni 3.1.0 以降を実行している場合にのみ確実に機能します。古いバージョンから 4+ に直接アップグレードすることは可能ですが、残りのノードが他の Patroni バージョンで実行されているときにプライマリーで障害が発生すると、予期しない動作が発生する可能性があります。

**重大な変更**

- Patroni コード内の非包括的な "master" 用語を削除する際に、次の重大な変更が導入されました。
  - Kubernetes では、Patroni はデフォルトで `role` ラベルを `primary` に設定します。以前の動作を維持し、ダウンタイムや長時間にわたる複雑な移行を回避したい場合は、パラメーター `kubernetes.leader_label_value` および `kubernetes.standby_leader_label_value` を `master` に構成できます。続きを読む [ここで](/ja/patroni/kubernetes#kubernetes_role_values)。
  - Patroni ロールは、`master` ではなく `primary` として DCS に書き込まれます。
  - Patroni REST API によって返される Patroni ロールが `master` から `primary` に変更されました。
  - Patroni REST API は、`/switchover`、`/failover`、`/restart` エンドポイントへのリクエストで `role=master` を受け入れなくなりました。
  - `/metrics` REST API エンドポイントは `patroni_master` メトリックを報告しなくなります。
  - [patronictl](/ja/patroni/patronictl#patronictl) は、どのコマンドでも `--master` オプションを受け入れなくなりました。代わりに `--leader` または `--primary` オプションを使用する必要があります。
  - カスタム レプリカ作成メソッドの宣言的構成の `no_master` オプションは特別なオプションとして扱われなくなりました。代わりに `no_leader` を使用してください。
  - `patroni_wale_restore` スクリプトは `--no_master` オプションを受け入れなくなりました。
  - `patroni_barman` スクリプトは `--role=master` オプションを受け入れなくなりました。
  - すべてのコールバック スクリプトは、`role=master` の代わりに渡された `role=primary` オプションを使用して実行されます。
- `patronictl failover` は、Patroni 3.2.0 以降非推奨となった `--leader` オプションを受け入れません。
- ユーザー作成機能 (`bootstrap.users` 構成セクション) は、Patroni 3.2.0 が削除されたため非推奨になりました。

**新機能**

- Quorum ベースのフェイルオーバー (Ants Aasma、Alexander Kukushkin)

この機能は、クォーラム ベースの同期レプリケーション (PostgreSQL v10 から利用可能) を実装します。これにより、1 つのスタンバイへのレプリケーションの待ち時間が長くなっても、他のスタンバイで補うことができるため、通常の運用中であっても最悪の場合の待ち時間を短縮できます。 Patroni は、受信した最新のトランザクションに基づいてフェイルオーバー候補を選択することにより、ユーザーに見えるデータ損失を防ぐ追加の保護手段を実装します。

- Citus セカンダリを `pg_dist_node` に登録します (Alexander Kukushkin)

Patroni は、`role==replica`、`state==running` を含むノードのリストと、`pg_dist_node` 内の `noloadbalance` [タグ](/ja/patroni/config/yaml#tags_settings) を含まないノードのリストを維持するようになりました。

- メンバーのレプリケーション スロットの保持を構成可能 (Alexander Kukushkin)

メンバー キーが存在しない場合にメンバー レプリケーション スロットを維持する期間を制御する `member_slots_ttl` グローバル構成パラメーターのサポートを実装します。

- Patroni によって作成されたログ ファイルのアクセス許可を設定可能にしました (Alexander Kukushkin)

Patroni によって作成されたログ ファイルに特定のアクセス許可を設定できます。指定しない場合、現在の `umask` 値に基づいて権限が設定されます。

- PostgreSQL 17 beta3 との互換性 (Alexander Kukushkin)

GUC のバリデータ ルールが拡張されました。 Patroni はシャットダウン中にすべての新しい補助バックエンドを処理し、論理レプリケーション スロットの同期に必要な `dbname` を `primary_conninfo` に設定します。

- Patroni 構成検証用の `--ignore-listen-port` オプションを実装します (Sahil Naphade)

`patroni --validate-config` の実行時に、すでにバインドされているポートを無視できるようにします。

**改善点**

- `wal_log_hints` を構成可能にする (Paul_Kim)

`use_pg_rewind` が `off` に設定されている場合に、`wal_log_hints` 構成が有効になることによるオーバーヘッドを回避できます。

- `DEBUG` レベルの Log `pg_basebackup` コマンド (Waynerv)

失敗した初期化のデバッグを容易にします。

**バグ修正**

- フェイルセーフ時のカスケード ノードの永続スロットを拡張しました (Alexander Kukushkin)

フェールセーフ モードがアクティブになっているときに、カスケード レプリカのスロットがプライマリー上で適切に前進していることを確認します。これは、`POST /failsafe` REST API リクエストに対するレプリカの応答を `xlog_location` で拡張することによって行われます。

- 現在のノードを同期として選択させないでください。 (Alexander Kukushkin)

現在のプライマリー ノードから、現在のプライマリーの名前と一致する `application_name` を含む "something" ストリーミングが存在する可能性があります。 Patroni はこの状況を適切に処理していなかったので、プライマリーが同期ノードとして宣言される可能性があり、その結果、スイッチオーバーがブロックされていました。

- POST /failsafe の `restapi.allowlist_include_members` を無視します (Alexander Kukushkin)

- GUC 検証を改善しました (Polina Bungina)

`postgres --describe-config` コマンドの実行による追加の検証のため、以前は Patroni 構成を通じてそこにリストされていない GUC を設定することはできませんでした。この制限は現在では削除されています。

- UNIX ソケットが検出された場合、`localhost` の行を `.pgpass` ファイルに追加しました。 (Alexander Kukushkin)

指定された `host` パラメータが `/` 文字で始まる場合、Patroni は `.pgpass` ファイルに追加行を追加します。これにより、`host` がデフォルトのソケット ディレクトリ パスと一致する場合の特殊なケースに対処できます。

- ログの問題を修正 (Waynerv)

フェールセーフ処理ログに適切なリクエスト URL を定義し、ポストマスター チェック ログのタイムスタンプの順序を修正しました。

--------

## バージョン 3.3.2 {#version-332}

2024-07-11 をリリース

**バグ修正**

- プレーンな Postgres 同期レプリケーション モードを修正しました (Israel Barth Rubio)

[synchronous_mode](/ja/patroni/replication_modes#synchronous_mode) が Patroni に導入されて以来、プレーンな Postgres 同期レプリケーションは機能しませんでした。このバグ修正により、[synchronous_mode](/ja/patroni/replication_modes#synchronous_mode) が無効になっている場合、Patroni はユーザーの構成に従って `synchronous_standby_names` の値を設定します。

- スタンバイで論理スロットの無効化を処理します (Polina Bungina)

スタンバイ上の PG16 論理レプリケーション スロットは Horizon: により無効化される可能性があるため、これ以降、Patroni は無効化されたスロットのコピー (つまり、再作成) を強制します。

- 論理スロットのアドバンスとコピーによる競合状態を修正しました。 (Alexander Kukushkin)

このバグにより、無効化された論理レプリケーション スロットが PostgreSQL 再起動で複数回コピーされる場合に発生する可能性がありました。

--------

## バージョン 3.3.1 {#version-331}

2024-06-17 をリリース

**安定性の向上**

- Python 3.12 との互換性 (Alexander Kukushkin)

`logging.LogRecord` に追加された新しい属性を処理します。

**バグ修正**

- `replicatefrom` タグ処理における無限再帰を修正しました。 (Alexander Kukushkin)

この修正の一環として、`is_physical_slot()` のチェックと調整のドキュメントも改善されます。

- スタンバイクラスターでの間違ったロールレポートを修正しました。 (Alexander Kukushkin)

`synchronous_standby_names` と同期レプリケーションは実際のプライマリー ノードでのみ機能し、カスケード レプリケーションの場合は Postgres によって単純に無視されます。この修正が行われる前は、`patronictl list` と `GET /cluster` は一部のノードを同期していると誤って報告していました。

- `allow_in_place_tablespaces` GUC の可用性を修正 (Polina Bungina)

`allow_in_place_tablespaces` は PostgreSQL 15 に追加されただけでなく、PostgreSQL 10-14 にもバックパッチされました。

--------

## バージョン 3.3.0 {#version-330}

2024-04-04 をリリース

> [!WARNING]
> すべての古い Partoni バージョンは `ydiff>=1.3` と互換性がありません。
>
> 問題の "fix" に使用できるオプションは次のとおりです。
>
> 1.  Patroni を最新バージョンにアップグレードします
> 2.  Patroni をインストールした後、インストール `ydiff<1.3`
> 3.  `cdiff` モジュールをインストールする

**新機能**

- `auth_data` を Zookeeper クライアントに渡す機能を追加しました (Aras Mumcuyan)

接続に使用する認証資格情報を指定できます。

- `Barman` 統合用の contrib スクリプトを追加しました (Israel Barth Rubio)

`Barman` 操作をリモートで実行できるようにし、カスタム ブートストラップ/カスタム レプリカ メソッドまたは `on_role_change` コールバックとして使用できるアプリケーション `patroni_barman` を提供します。詳細については、[ここで](/ja/patroni/tools_integration#tools_integration) を確認してください。

- サポート `JSON` ログ形式 (alisalemmi)

`plain` (デフォルト) とは別に、Patroni は `json` ログ形式もサポートするようになりました。 `python-json-logger>=2.0.2` ライブラリをインストールする必要があります。

- `pending_restart_reason` 情報を表示 (Polina Bungina)

`pending_restart` フラグが設定される原因となった PostgreSQL パラメーターに関する拡張情報を提供します。 `patronictl list` と `/patroni` REST API エンドポイントの両方で、パラメーター名とその "diff" が `pending_restart_reason` として表示されるようになりました。

- `nostream` タグを実装する (Grigory Smolkin)

`nostream` タグが `true` に設定されている場合、ノードは WAL をストリーミングするためにレプリケーション プロトコルを使用せず、代わりにアーカイブ リカバリに依存します (`restore_command` が構成されている場合)。また、ノード自体とそのすべてのカスケード レプリカ上の永続的な論理レプリケーション スロットのコピーと同期も無効になります。

**改善点**

- `log` セクションの検証を実装します (Alexander Kukushkin)

これまで、バリデーターは提供されたログ構成の正確性をチェックしていませんでした。

- PostgreSQL パラメーター変更のログを改善しました (Polina Bungina)

古い値を人間が判読できる形式に変換し、`pg_controldata` と Patroni のグローバル構成の不一致に関する情報をログに記録します。

**バグ修正**

- 許可されていない `pg_basebackup` オプションを適切に除外しました (Israel Barth Rubio)

バグのため、Patroni は、`- setting: value` 形式で提供されている場合、`basebackup` レプリカ ブートストラップ メソッドに構成された許可されていないオプションを適切にフィルターで除外していませんでした。

- `etcd3` 認証エラー処理を修正しました (Alexander Kukushkin)

リクエストを実行する直前に認証が行われなかった場合、`etcd3` 認証エラーが発生した場合は常に 1 回再試行します。また、再認証時にウォッチャーを再起動しないでください。

- バリデーター ファイル検出のロジックを改善 (Waynerv)

可能な場合は、`importlib` ライブラリを使用して、利用可能な構成パラメータを持つファイルを検出します (Python 3.9+ の場合)。この実装はより安定しており、`zip` アーカイブに基づく Patroni ディストリビューションを壊すことはありません。

- [standby_cluster](/ja/patroni/standby_cluster#standby_cluster) セクションで複数のホストが指定されている場合にのみ `target_session_attrs` を使用するようにしました。 (Alexander Kukushkin)

`standby_cluster.host` セクションにカンマで区切られた複数のホストが含まれている場合にのみ、`target_session_attrs=read-write` がスタンバイ リーダー ノードの `primary_conninfo` に追加されるようになりました。

- `ydiff` ライブラリ バージョン 1.3+ の互換性コードを追加しました (Alexander Kukushkin)

Patroni は、Python モジュールではなく単なる端末ツールであると想定されているため、公開されていない `ydiff` の一部の API に依存しています。残念ながら、1.3 の API の変更により、古い Patroni バージョンが壊れてしまいました。

--------

## バージョン 3.2.2 {#version-322}

2024-01-17 をリリース

**バグ修正**

- DCS がワイプされたときにレプリカ復元でキーを初期化させないでください。 (Alexander Kukushkin)

この問題は、Patroni がスタンドアロンの PG クラスターを引き継ぐメソッドで発生していました。

- Consul から更新されたばかりの同期キーを取得するときに一貫した読み取りを使用します。 (Alexander Kukushkin)

Consul には、更新したばかりのキーの `ModifyIndex` をすぐに取得するためのインターフェイスが提供されていないため、明示的な読み取り操作を実行する必要があります。デフォルトでは古い読み取りが許可されているため、古いバージョンのキーを取得することがありました。

- 再起動が必要なパラメータが元の値にリセットされた場合、Reload Postgres 設定を実行しました (Polina Bungina)

以前は、Patroni は構成を更新せず、`pending_restart` をリセットするだけでした。

- 同期モードで非同期候補へのフェイルオーバーを実行する際の確認プロンプト メッセージの誤った反転ロジックを修正しました (Polina Bungina)

この問題は [patronictl](/ja/patroni/patronictl#patronictl) にのみ存在しました。

- [patronictl](/ja/patroni/patronictl#patronictl) のフェイルオーバー候補からリーダーを除外します (Polina Bungina)

クラスターが正常な場合、既存のリーダーへのフェイルオーバーは何も行われません。

- Citus データベースと拡張機能をべき等に作成する (Alexander Kukushkin、Zhao Junwang)

Citus データベースにさらに依存関係を追加する必要がある場合に備えて、`post_bootstrap` スクリプトでそれらを作成できるようになります。

- 矛盾する `nofailover` タグをフィルタリングしないでください (Polina Bungina)

ノードに設定された構成 `{nofailover: false, failover_priority: 0}` ではレースに参加できませんでしたが、`nofailover` タグが優先されるため、レースに参加できるはずです。

- PyInstaller の凍結問題を修正しました (Sophia Ruan)

`freeze_support()` が `argparse` の後に呼び出されたため、Patroni は Postgres を開始できませんでした。

- [patronictl](/ja/patroni/patronictl#patronictl) および [Citus](/ja/patroni/citus#citus) 構成の構成ジェネレーターのバグを修正しました (Israel Barth Rubio)

これにより、環境変数を介して設定された [patronictl](/ja/patroni/patronictl#patronictl) および [Citus](/ja/patroni/citus#citus) 構成パラメーターが、生成された構成に書き込まれることが妨げられました。

- 実行中のスタンバイに参加するときに、リカバリ GUC と一部の Patroni 管理パラメータを復元します (Alexander Kukushkin)

Patroni は、内部構造の 1 つで `port` が欠落しているというエラーにより、Postgres v12 以降の再起動に失敗していました。

- `pending_restart` フラグ周りの修正 (Polina Bungina)

`recovery_target_action = promote` を使用したカスタム ブートストラップの場合、または誰かが `ALTER SYSTEM` などを使用して `hot_standby` または `wal_log_hints` を変更した場合は、`pending_restart` を公開しないでください。

--------

## バージョン 3.2.1 {#version-321}

2023-11-30 をリリース

**バグ修正**

- [patronictl](/ja/patroni/patronictl#patronictl) の `--format` 引数に受け入れられる値を制限しました (Alexander Kukushkin)

以前は任意の文字列を受け入れ、値が認識されない場合は出力を生成していませんでした。

- リーダー キーを解放する前に、シャットダウン時にレプリカ ノードがチェックポイント LSN を受信したことを確認します。 (Alexander Kukushkin)

以前は、場合によっては、SWITCH レコードの LSN に続いて CHECKPOINT を使用していました (アーカイブ モードが有効な場合)。その結果、以前のプライマリーは `pg_rewind` を実行する必要がある場合がありましたが、データ損失は発生しませんでした。

- ノード名の一意性チェックを実行するときに実際の HTTP リクエストを実行します。 (Alexander Kukushkin)

  コンテナー内でPatroniを実行すると、ポートをリッスンして着信接続を受け入れる`docker-proxy`経由でトラフィックがルーティングされる場合があります。このことが誤検出の原因になっていました。

- Etcd による Citus サポートを修正 v2 (Alexander Kukushkin)

Patroni は、etcd v2 を使用した新しい Citus クラスターのデプロイに失敗していました。

- Postgres v16+ での `pg_rewind` の動作を修正しました。 (Alexander Kukushkin)

`pg_waldump` のエラー メッセージ形式が v16 で変更されたため、必要でない場合でも `pg_rewind` が Patroni によって呼び出されるようになりました。

- カスタム ブートストラップのバグを修正しました (Alexander Kukushkin)

Patroni は、ブートストラップ コマンドそのものである `--command` 引数を誤って適用していました。

- REST API ヘルスチェックエンドポイントの問題を修正しました (Sophia Ruan)

接続が適切に閉じられなかったために、Postgres の再起動後に Postgres の `unknown` 状態が返される可能性がありました。

- Cache `postgres --describe-config` 出力結果 (Waynerv)

これらは、PostgreSQL 構成の検証にどの GUC が利用できるかを判断するために使用され、Patroni の実行中にこのリストが変更されることは想定されていません。

--------

## バージョン 3.2.0 {#version-320}

2023-10-25 をリリース

**非推奨の通知**

- `bootstrap.users` サポートはバージョン 4.0.0 で削除されます。新しいクラスターのデプロイ後にユーザーを作成する必要がある場合は、`bootstrap.post_bootstrap` フックを使用してください。

**重大な変更**

- `loop_wait + 2*retry_timeout <= ttl` ルールを強制し、可能な最小値をハードコードします (Alexander Kukushkin)

最小値: `loop_wait=2`、`retry_timeout=3`、`ttl=20`。値が小さい場合、またはルールに違反している場合は、値が調整され、警告が Patroni ログに書き込まれます。

**新機能**

- フェイルオーバーの優先順位 (Mark Pekala)

`tags.failover_priority` の助けを借りて、リーダー レース中にノードをより優先させることができるようになりました。詳細については、ドキュメント (ref タグ) を参照してください。

- `patroni --generate-config [--dsn DSN]` および `patroni --generate-sample-config` を実装しました (Polina Bungina)

実行中の PostgreSQL クラスターの構成ファイル、または新しい Patroni クラスターのサンプル構成ファイルを生成できます。

- Patroni REST API には Postgres への専用接続を使用します (Alexander Kukushkin)

システムにストレスがかかっている場合に、メインのハートビート ループがブロックされるのを避けるのに役立ちます。

- ノードの `name` を使用して一部のエンドポイントを強化します (sskserk)

モニタリング エンドポイントの場合は `name` が `scope` の隣に追加され、メトリクス エンドポイントの場合は `name` がタグに追加されます。

- フェイルオーバー/スイッチオーバーの厳密な違いを確保する (Polina Bungina)

ログ メッセージをより正確にし、正常な同期クラスター内の非同期ノードへのフェイルオーバーを許可します。

- 永続的な物理レプリケーション スロットを永続的な論理スロットと同様に動作させるようにしました。 (Alexander Kukushkin)

リーダーになることが許可されているすべてのノード上に永続的な物理レプリケーション スロットを作成し、`pg_replication_slot_advance()` 関数を使用してスタンバイ ノード上のスロットの `restart_lsn` を進めます。

- [patronictl](/ja/patroni/patronictl#patronictl) の `--dcs` 引数を通じて名前空間を指定する機能を追加しました (Israel Barth Rubio)

構成ファイルなしで [patronictl](/ja/patroni/patronictl#patronictl) を使用すると便利です。

- カスタム ブートストラップ構成に追加パラメーターのサポートを追加しました (Israel Barth Rubio)

以前は、カスタム引数を `command` に追加することしかできませんでしたが、現在はそれらをマッピングとしてリストできるようになりました。

**改善点**

- `citus.local_hostname` GUC を、Patroni が Postgres に接続するために使用するのと同じ値に設定します。 (Alexander Kukushkin)

Citus がローカルの Postgres への接続を必要とする場合があります。デフォルトでは `localhost` が使用されますが、常に使用できるわけではありません。

**バグ修正**

- スタンバイ クラスターの [synchronous_mode](/ja/patroni/replication_modes#synchronous_mode) 設定を無視する (Polina Bungina)

Postgres はカスケード同期レプリケーションをサポートしておらず、[synchronous_mode](/ja/patroni/replication_modes#synchronous_mode) がスタンバイ クラスターでのスイッチオーバーを中断していたことは無視されません。

- `on_reload` コールバックの Handle SIGCHLD (Alexander Kukushkin)

そうしないとゾンビ プロセスが発生し、次の `on_reload` が実行されるときにのみ取得されます。

- etcd v3 を使用する場合の Handle `AuthOldRevision` エラー (Alexander Kukushkin、Kenny Do)

このエラーは、etcd が JWT を使用するように構成されている場合、および etcd のユーザー データベースが更新されたときに発生します。

--------

## バージョン 3.1.2 {#version-312}

2023-09-26 をリリース

**バグ修正**

- `wal_keep_size` チェックのバグを修正しました (Alexander Kukushkin)

`wal_keep_size` は、通常はユニットを持つ GUC ですが、Patroni はその値を `int` にキャストできませんでした。その結果、`bootstrap.dcs` の値はその後 `/config` キーに書き込まれませんでした。

- `/sync` キーと `synchronous_standby_names` 間の不一致を検出して解決します。 (Alexander Kukushkin)

通常、Patroni は非常に特定の順序で `/sync` と `synchronous_standby_names` を更新しますが、バグが発生した場合、または手動で `synchronous_standby_names` をリセットした場合、Patroni は矛盾した状態になりました。その結果、非同期ノードでフェイルオーバーが発生する可能性がありました。

- 実行中の Postgres に参加するときに GUC の値を読み取ります (Alexander Kukushkin)

[一時停止する](/ja/patroni/pause#pause) で再起動すると、Patroni は `postgresql.conf` から `synchronous_standby_names` GUC を破棄していました。これを解決し、同様の問題を回避するために、Patroni は、すでに実行中の Postgres に結合する場合、GUC の値を読み取ります。

- ノードの一意性をチェックする際の煩わしい警告をサイレントにしました (Alexander Kukushkin)

Patroni がすぐに再起動されると、`WARNING` メッセージが `urllib3` によって生成されます。

--------

## バージョン 3.1.1 {#version-311}

2023-09-20 をリリース

**バグ修正**

- プロモート時にフェイルセーフ状態をリセット (ChenChangAo)

フェールセーフ モードがアクティブ化された直後にスイッチオーバー/フェイルオーバーが発生した場合、フェールセーフが非アクティブになった後、新たに昇格されたプライマリーは自身を降格していました。

- [patronictl](/ja/patroni/patronictl#patronictl) で無用な警告をサイレントにしました (Alexander Kukushkin)

[patronictl](/ja/patroni/patronictl#patronictl) が Patroni と同じ patroni.yaml ファイルを使用し、`PGDATA` ディレクトリにアクセスできる場合、グローバル構成の不正な値に関する煩わしい警告が表示されていた可能性があります。

- 特殊なケースに対して同期モードを明示的に有効にしました (Alexander Kukushkin)

プライマリーからストリーミングするレプリカがない場合、同期モードは事実上アクティブ化されません。

- `0` 整数値の検証に関するバグを修正しました (Israel Barth Rubio)

ほとんどの場合、警告が表示されるだけで、問題は発生しませんでした。

- スタンバイクラスターの論理スロットを返さないようにしました。 (Alexander Kukushkin)

Patroni はスタンバイ クラスターに論理レプリケーション スロットを作成できないため、グローバル構成で定義されている場合は無視する必要があります。

- `patronictl --help` 出力で docstring を表示しないようにしました (Israel Barth Rubio)

`click` モジュールは、そのための特別なヒントを取得する必要があります。

- `kubernetes.standby_leader_label_value` のバグを修正しました (Alexander Kukushkin)

この機能は事実上、まったく機能しませんでした。

- クラスター システム識別子を `patronictl list` 出力に返しました (Polina Bungina)

この問題は、Citus のサポートを実装する際に発生しました。識別子はコーディネーターとすべてのワーカーで異なるため、識別子を隠す必要があります。

- Kubernetes 実装の Override `write_leader_optime` メソッド (Alexander Kukushkin)

このメソッドは、新しいプライマリーとなる使用可能な正常なレプリカがない場合に、リーダー エンドポイント/ConfigMap にシャットダウン LSN を書き込むことになっています。

- 一時停止中の停止した postgres を開始しないでください。 (Alexander Kukushkin)

競合状態のため、Patroni は、一部のリカバリ パラメーター (`primary_conninfo` など) が変更されたため、スタンバイを再起動する必要があると誤って想定していました。

- `patronictl query` コマンドのバグを修正しました (Israel Barth Rubio)

`-m` 引数のみが指定された場合、または `-r` または `-m` がいずれも指定されなかった場合は機能しませんでした。

- postgres を起動するためにコマンドラインで使用される整数パラメーターを適切に処理します (Polina Bungina)

値が文字列として提供され、整数にキャストされていない場合、Citus クラスターの `max_connections` に基づく `max_prepared_transactions` の計算が正しく行われませんでした。

- `pg_rewind` を決定するときは `pg_stat_wal_receiver` に依存しないでください (Alexander Kukushkin)

レプリケーション接続を介して `DENTIFY_SYSTEM` によって報告されるタイムラインが常に正しい一方で、`pg_stat_wal_receiver` によって報告される `received_tli` が実際に再生されるタイムラインよりも進んでいることが発生する可能性があります。

--------

## バージョン 3.1.0 {#version-310}

2023-08-03 をリリース

**重大な変更**

- `restapi.keyfile` および `restapi.certfile` のセマンティクスを変更しました (Alexander Kukushkin)

以前は、Patroni は、`ctl` セクションにそれぞれの構成パラメーターがない場合、フォールバックとして `restapi.keyfile` および `restapi.certfile` をクライアント証明書として使用していました。

> [!WARNING]
> クライアント証明書の検証を有効にした場合 (`restapi.verify_client` が `required` に設定されている場合)、**しなければならない** は `ctl.certfile`、`ctl.keyfile`、`ctl.keyfile_password` で **有効なクライアント証明書** も提供します。指定しない場合、Patroni は正しく動作しません。

**新機能**

- Pod ロール ラベルを構成可能にする (Waynerv)

値は、`kubernetes.leader_label_value`、`kubernetes.follower_label_value`、および `kubernetes.standby_leader_label_value` パラメーターを使用してカスタマイズできます。この機能は、`master` ロールを `primary` に変更するときに非常に役立ちます。機能と移行手順の詳細については、[ここで](/ja/patroni/kubernetes#kubernetes_role_values) をご覧ください。

**改善点**

- `patroni --validate-config` のさまざまな改善 (Alexander Kukushkin)

さまざまな DCS、`bootstrap.dcs`、`ctl`、`restapi`、および [番犬](/ja/patroni/watchdog#watchdog) セクションのパラメーター検証が改善されました。

- Start Postgres は、Patroni の実行中にリカバリ中にクラッシュした場合、リカバリ中ではありません。 (Alexander Kukushkin)

これにより、回復時間が短縮され、不必要なタイムラインの増加を防ぐことができます。

- `/status` キーの不必要な更新を避ける (Alexander Kukushkin)

永続的な論理スロットがない場合、プライマリーの LSN が先に進まない場合でも、Patroni はハートビート ループごとに `/status` を更新していました。

- 党首争いで陳腐な予備選が勝つことを許さないでください (Alexander Kukushkin)

リソース不足により Patroni が長時間ハングしていた場合、リーダー ロックを取得する前に、他のノードが Postgres を昇格していないかどうかがさらにチェックされます。

- 特定の PostgreSQL パラメーター検証の可視性を実装しました (Alexander Kukushkin、Feike Steenbergen)

`max_connections`、`max_wal_senders`、`max_prepared_transactions`、`max_locks_per_transaction`、`max_replication_slots`、または `max_worker_processes` の検証が失敗した場合、Patroni は適切なデフォルト値を使用していました。これに加えて、警告も表示されます。

- `PGDATA` で作成されたファイルとディレクトリのアクセス許可を設定します (Alexander Kukushkin)

Patroni によって作成されたすべてのファイルには、所有者の読み取り/書き込み権限のみがありました。この動作により、別のユーザーで実行され、グループの読み取り権限に依存するバックアップ ツールが機能しなくなります。現在、Patroni は `PGDATA` に対するアクセス許可を尊重し、`PGDATA` 内に作成されるすべてのディレクトリとファイルに対するアクセス許可を正しく設定します。

**バグ修正**

- シェル (Waynerv) を介して `archive_command` を実行します。

Patroni は、シングルユーザー モードでクラッシュ リカバリを実行する前、または `pg_rewind` の前に、一部の WAL セグメントをアーカイブする場合があります。 archive_command に `&&` などのいくつかのシェル演算子が含まれている場合、Patroni では機能しませんでした。

- 「スイッチオーバー時」シャットダウンチェックを修正しました (Polina Bungina)

指定された候補がまだストリーミング中であり、シャットダウン チェックを受信していない可能性がありますが、他のいくつかのノードが正常であったためにリーダー キーが削除されました。

- 「プライマリーである」チェックを修正しました (Alexander Kukushkin)

リーダーのレース中、レプリカは古いリーダーの Postgres がまだプライマリーとして実行されていることを認識できませんでした。

- 修正 `patronictl list` (Alexander Kukushkin)

`tsv`、`json`、および `yaml` 出力形式にクラスター名フィールドがありませんでした。

- 一時停止後の `pg_rewind` の動作を修正しました (Alexander Kukushkin)

特定の条件下では、Patroni は、メンテナンス モードを終了した後、偽のプライマリーを `pg_rewind` を使用してクラスターに戻すことができませんでした。

- Etcd v3 実装のバグを修正しました (Alexander Kukushkin)

リビジョンの不一致により、`create_revision`/`mod_revision` フィールドを使用してキー更新が実行された場合、内部 KV キャッシュを無効にします。

- 一時停止中のスタンバイ クラスターのレプリカの動作を修正しました (Alexander Kukushkin)

リーダー キーの有効期限が切れると、スタンバイ クラスターのレプリカはリモート ノードに従わず、`primary_conninfo` をそのまま保持します。

--------

## バージョン 3.0.4 {#version-304}

2023-07-13 をリリース

**新機能**

- スタンバイ ノードのレプリケーション ステータスを表示するようにしました (Alexander Kukushkin)

PostgreSQL の場合、9.6+ Patroni は、スタンバイが他のノードからストリーミングしている場合はレプリケーション状態を `streaming` として報告し、レプリケーション接続がなく、`restore_command` が設定されている場合は `in archive recovery` として報告します。状態は、DCS の `member` キー、REST API、および `patronictl list` 出力に表示されます。

**改善点**

- Etcd のエラー メッセージを改善しました v3 (Alexander Kukushkin)

etcd v3 クラスターにアクセスできない場合、Patroni は `/v2` エンドポイントにアクセスできないことを報告していました。

- 可能であれば、[patronictl](/ja/patroni/patronictl#patronictl) で読み取られたクォーラムを使用してください。 (Alexander Kukushkin)

etcd または Consul クラスターは読み取り専用に低下する可能性がありますが、[patronictl](/ja/patroni/patronictl#patronictl) ビューからはすべて問題ありませんでした。今はエラーが出て失敗します。

- 構成内でのスプリットブレイン名の重複を防止します (Mark Pekala)

Patroni の起動時に、同じ名前のノードが DCS に登録されているかどうかを確認し、その REST API のクエリーを試みます。 REST API にアクセスできる場合、Patroni はエラーで終了します。人的ミスから守るのに役立ちます。

- Patroni の実行中にクラッシュした場合、Start Postgres がリカバリーされません。 (Alexander Kukushkin)

これにより、回復時間が短縮され、不必要なタイムラインの増加を防ぐことができます。

**バグ修正**

- REST API SSL 証明書は、SIGHUP の受信時にリロードされませんでした (Israel Barth Rubio)

回帰は 3.0.3 で導入されました。

- `max_connections` のようなパラメータの整数 GUC 検証を修正しました (Feike Steenbergen)

Patroni は引用符で囲まれた数値を好みませんでした。回帰は 3.0.3 で導入されました。

- [synchronous_mode](/ja/patroni/replication_modes#synchronous_mode) の問題を修正しました (Alexander Kukushkin)

`synchronous_mode_strict` が有効なときに、欠落している同期スタンバイを誤って待機しないように、`synchronous_commit=off` を使用して `txid_current()` を実行します。

--------

## バージョン 3.0.3 {#version-303}

2023-06-22 をリリース

**新機能**

- PostgreSQL 16 beta1 との互換性 (Alexander Kukushkin)

GUC のバリデータ ルールを拡張しました。

- PostgreSQL GUC のバリデーターを拡張可能にします (Israel Barth Rubio)

バリデータ ルールは、`patroni/postgresql/available_parameters/` ディレクトリにある YAML ファイルからロードされます。ファイルはアルファベット順に並べられ、次々に適用されます。これにより、非標準の Postgres ディストリビューション用のカスタム バリデーターを使用できるようになります。

- `restapi.request_queue_size` オプションを追加しました (Andrey Zidenkov、Aleksei Sukhov)

Patroni REST API によって使用される TCP ソケットのリクエスト キュー サイズを設定します。キューがいっぱいになると、それ以降のリクエストでは「接続が拒否されました」エラーが発生します。デフォルト値は 5 です。

- 新しいクラスターを初期化するときに `initdb` を直接呼び出します (Matt Baker)

以前は `pg_ctl` を介して呼び出されていましたが、`initdb` に渡すパラメーターの特別な引用符が必要でした。

- 停止フックの前に追加 (Le Duane)

フックは `postgresql.before_stop` を介して設定でき、`pg_ctl stop` の直前に実行されます。終了コードはシャットダウン プロセスには影響しません。

- カスタム Postgres バイナリ名のサポートを追加しました (Israel Barth Rubio、Polina Bungina)

カスタム Postgres ディストリビューションを使用する場合、Postgres バイナリが、コミュニティの Postgres ディストリビューションで使用されるものとは異なる名前でコンパイルされる場合があります。カスタム バイナリ名は、`postgresql.bin_name.*` および `PATRONI_POSTGRESQL_BIN_*` 環境変数を使用して構成できます。

**改善点**

- `patroni --validate-config` のさまざまな改善 (Polina Bungina)

  - `bootstrap.initdb` をオプションにします。これは新しいクラスターの場合にのみ必要ですが、構成に欠落していると `patroni --validate-config` がエラーを出しました。
  - `postgresql.bin_dir` が空の場合、または設定されていない場合にエラーを発生させません。代わりに、まずデフォルトの PATH で Postgres バイナリを検索してみてください。
  - `postgresql.authentication.rewind` セクションをオプションにします。これが存在しない場合、Patroni はスーパーユーザーを使用しています。

- [patronictl](/ja/patroni/patronictl#patronictl) のエラーレポートを改善しました (Israel Barth Rubio)

`\n` シンボルは、実際の改行シンボルではなく、そのままレンダリングされました。

**バグ修正**

- Citus サポートの問題を修正しました (Alexander Kukushkin)

昇格されたワーカーからコーディネーターへの REST API 呼び出しがスイッチオーバー中に失敗した場合、指定された Citus グループは無期限にブロックされたままになります。

- [patronictl](/ja/patroni/patronictl#patronictl) の `--dcs-url` オプションで `etcd3` URL を許可します (Israel Barth Rubio)

ユーザーが [patronictl](/ja/patroni/patronictl#patronictl) の `--dcs-url` オプションを介して `etcd3` URL を渡そうとすると、例外が発生します。

--------

## バージョン 3.0.2 {#version-302}

2023-03-24 をリリース

> [!WARNING]
> バージョン 3.0.2 は、3.6 よりも古い Python のサポートを終了しました。

**新機能**

- 同期スタンバイ レプリカ ステータスを `/metrics` エンドポイントに追加しました (Thomas von Dein、Alexander Kukushkin)

以前は `primary`/`standby_leader`/`replica`. のみをレポートしていました

- [patronictl](/ja/patroni/patronictl#patronictl) での `PAGER` のユーザーフレンドリーな処理 (Israel Barth Rubio)

これにより、`PAGER` 環境変数を介してページャーを構成できるようになり、デフォルトの `less` および `more` がオーバーライドされます。

- K8s を再試行可能にする HTTP ステータス コードを構成可能にする (Alexander Kukushkin)

一部の管理対象プラットフォームでは、ステータス コード `401 Unauthorized` を取得する可能性がありますが、数回再試行すると解決される場合があります。

**改善点**

- `recovery_target_action` が `promote` に設定されている場合にのみ、カスタム ブートストラップ中に `hot_standby` を `off` に設定します。 (Alexander Kukushkin)

`recovery_target_action=pause` を正しく動作させるために必要でした。

- `on_reload` コールバックが他のコールバックを強制終了することを許可しないでください。 (Alexander Kukushkin)

`on_start`/`on_stop`/`on_role_change` は通常、仮想 IP の追加/削除に使用されますが、`on_reload` はそれらを妨げるべきではありません。

- AWS コールバック サンプル スクリプトで `IMDSFetcher` に切り替えました (Polina Bungina)

`IMDSv2` では動作するトークンが必要ですが、`IMDSFetcher` はそれを透過的に処理します。

**バグ修正**

- Kubernetes 上で実行されている Citus クラスターの `patronictl switchover` を修正しました (Lukáš Lalinský)

`default` とは異なる名前空間では機能しませんでした。

- メジャー バージョンが不明な場合は `PGDATA` に書き込まないでください。 (Alexander Kukushkin)

開始直後の `PGDATA` が空だった場合 (まだマウントされていない可能性があります)、Patroni は、実際のメジャー バージョンが v10+. であっても、PostgreSQL バージョンについて誤った仮定を立て、誤って `recovery.conf` ファイルを作成していました。

- コーディネーターフェイルオーバー後のCitusメタデータのバグを修正しました (Alexander Kukushkin)

`citus_set_coordinator_host()` 呼び出しではメタデータの同期は発生せず、変更はワーカー ノードでは認識されませんでした。この問題は、`citus_update_node()` に切り替えることで解決されます。

- すべての etcd ノードが "failed" である場合、構成ファイルにリストされている etcd ホストをフォールバックとして使用します (Alexander Kukushkin)

etcd クラスターは時間の経過とともにトポロジを変更する可能性があり、Patroni はそれに従おうとします。ある時点ですべてのノードが到達不能になった場合、Patroni は、再接続を試行するときに、構成のノードと最後に知られているトポロジの組み合わせを使用します。

--------

## バージョン 3.0.1 {#version-301}

2023-02-16 をリリース

**バグ修正**

- `on_role_change` コールバック スクリプトに適切なロール名を渡します。 (Alexander Kukushkin, Polina Bungina)

Patroni は、昇格時に `promoted` ロールを `on_role_change` コールバック スクリプトに誤って渡していました。渡されたロール名が `master` に戻りました。 This regression was introduced in 3.0.0.

--------

## バージョン 3.0.0 {#version-300}

2023-01-30 をリリース

このバージョンでは、[Citus](https://www.citusdata.com) との統合が追加され、プライマリーを降格することなく、一時的な DCS の停止に耐えることが可能になります。

> [!WARNING]
> - Version 3.0.0 は、Python 2.7 をサポートする最後のリリースです。今後のリリースでは、3.7 よりも古い Python バージョンのサポートが終了します。
>
> - RAFT サポートは非推奨になりました。メンテナンスには最善を尽くしますが、起こり得る問題については保証も責任も負いません。
> - このバージョンは、"master" を削除し、"primary" を使用するための最初のステップです。次のメジャー リリースへのアップグレードは、少なくとも 3.0.0 を実行している場合にのみ確実に機能します。

**新機能**

- DCS フェイルセーフ モード (Alexander Kukushkin、Polina Bungina)

この機能が有効になっている場合、Patroni クラスターは一時的な DCS の停止にも耐えることができます。詳細については、[ドキュメント](/ja/patroni/dcs_failsafe_mode#dcs_failsafe_mode) を参照してください。

- Citus サポート (Alexander Kukushkin、Polina Bungina、Jelte Fenema)

Patroni を使用すると、HA を使用した [Citus](https://www.citusdata.com) クラスターのデプロイと管理が容易になります。詳細については、[ここで](/ja/patroni/citus#citus) ページを確認してください。

**改善点**

- 不明だがアクティブなレプリケーション スロットを削除するときに繰り返されるエラーを抑制しました (Michael Bank)

Patroni は引き続きこれらのログを書き込みますが、DEBUG にのみ書き込みます。

- HA ループごとに監視クエリーを 1 つだけ実行します (Alexander Kukushkin)

同期レプリケーションが有効な場合はそうではありませんでした。

- 失敗した最新のデータ ディレクトリのみを保持する (William Albertus Dembo)

ブートストラップが失敗した場合、Patroni はタイムスタンプ サフィックスを付けて \$PGDATA フォルダーの名前を変更するために使用されていました。今後、サフィックスは `.failed` になり、そのようなフォルダーが存在する場合は、名前を変更する前に削除されます。

- 同期レプリケーション接続のチェックを改善しました (Alexander Kukushkin)

新しいホストが `synchronous_standby_names` に追加されると、`pg_stat_replication.sync_state = 'sync'` に加えてプライマリーに追いついた場合にのみ、DCS で同期として設定されます。

**削除された機能**

- `patronictl scaffold` を削除 (Alexander Kukushkin)

これを導入した唯一の理由は、スタンバイ クラスターを実行するハッキングな方法でした。

--------

## バージョン 2.1.7 {#version-217}

2023-01-04 をリリース

**バグ修正**

- レガシー Python モジュールとの小さな非互換性を修正しました (Alexander Kukushkin)

これらにより、Debian バスター/Ubuntu バイオニック上で Patroni をビルド/実行できなくなりました。

--------

## バージョン 2.1.6 {#version-216}

2022-12-30 をリリース

**改善点**

- SSL ソケットのシャットダウン時の迷惑な例外を修正しました。 (Alexander Kukushkin)

HAProxy は、HTTP ステータス コードを取得するとすぐに接続を閉じているため、Patroni が SSL 接続を適切にシャットダウンする時間がありません。

- arm64 用の Dockerfile の例を調整 (Polina Bungina)

明示的な `amd64` と `x86_64` を削除します。`libnss_files.so.*` は削除しないでください。

**セキュリティの向上**

- 非レプリケーション接続に対して `search_path=pg_catalog` を強制する (Alexander Kukushkin)

Patroni はスーパーユーザー接続に大きく依存しているため、`pg_catalog` の対応するオブジェクトと同じ名前と署名を持つ `public` スキーマのユーザー定義関数や演算子を使用して実行される可能性のある攻撃から保護したいと考えています。そのため、Patroni によって作成されたすべての接続に対して `search_path=pg_catalog` が適用されます (レプリケーション接続を除く)。

- パスワードが `pg_stat_statements` に記録されないようにする (Feike Steenbergen)

これは、ユーザーの作成時に `pg_stat_statements.track_utility=off` を設定することで実現されます。

**バグ修正**

- Declare `proxy_address` as optional (Denis Laxalde)

これは事実上必須ではないオプションであるためです。

- insecureオプションの動作を改善しました（Alexander Kukushkin）。

  REST API要求にクライアント証明書を使用していると、ctlの`insecure`オプションが正しく動作していませんでした。

- 新しいクラスターがブートストラップされるときに、`bootstrap.dcs` からウォッチドッグ構成を取得します (Matt Baker)

Patroni は、DCS のブートストラップに使用される構成を取得するのではなく、新しいクラスターをブートストラップするときにデフォルトでウォッチドッグを最初に構成していました。

- WIN32で実行可能ファイルを探す際のファイル拡張子の扱いを修正しました（Martín Marqués）。

ファイル名に拡張子がまだない場合のみ、`.exe` を追加してください。

- Fix Consul TTL setup (Alexander Kukushkin)

HTTPClient で値を設定するときに `ttl/2.0` を使用しましたが、クラスのプロパティで現在の値に 2 を乗算するのを忘れていました。 It was resulting in Consul TTL off by twice.

**削除された機能**

- `patronictl configure` を削除 (Polina Bungina)

There is no more need for a separate [patronictl](/ja/patroni/patronictl#patronictl) config creation.

--------

## バージョン 2.1.5 {#version-215}

2022-11-28 をリリース

このバージョンでは、PostgreSQL 15 との互換性が強化され、etcd v3 のサポートが実稼働対応として宣言されています。 Raft の Patroni はベータ版のままです。

**新機能**

- `patroni --validate-config` の改善 (Denis Laxalde)

構成が無効な場合はコード 1 で終了し、エラーを標準エラー出力に出力します。

- 一時停止中にレプリケーション スロットを削除しないでください。 (Alexander Kukushkin)

Patroni は、メンバーがクラスターに参加またはクラスターから離脱するときに、物理レプリケーション スロットを自動的に作成または削除します。一時停止中のスロットは削除されなくなります。

- エンドポイントを監視するための `HEAD` リクエスト メソッドをサポートします (Robert Cutajar)

`GET` の代わりに Patroni を使用すると、HTTP ステータス コードのみが返されます。

- Windows での動作テストをサポート (Alexander Kukushkin)

新しい REST API エンドポイント `POST /sigterm` を導入することにより、Windows で正常な Patroni シャットダウン (`SIGTERM`) をエミュレートします。

- `postgresql.proxy_address` の紹介 (Alexander Kukushkin)

これは、DCS のメンバー キーに `proxy_url` として書き込まれ、サービスの検出に使用または役立つ可能性があります。

**安定性の向上**

- スレッドから `pg_replication_slot_advance()` を呼び出します (Alexander Kukushkin)

多くの論理レプリケーション スロットを持つビジーなクラスターでは、`pg_replication_slot_advance()` 呼び出しがメインの HA ループに影響を及ぼし、メンバー キーの有効期限が切れる可能性がありました。

- 古いプライマリーで `pg_rewind` を呼び出す前に、欠落している可能性のある WAL をアーカイブします (Polina Bungina)

プライマリーがクラッシュして長時間ダウンした場合、一部の WAL ファイルがアーカイブと新しいプライマリーから失われる可能性があります。 `pg_rewind` が古いプライマリーからこれらの WAL ファイルを削除し、スタンバイとして起動できなくなる可能性があります。 `ready` WAL ファイルをアーカイブすることで、この問題が軽減されるだけでなく、一般的に継続的なアーカイブ エクスペリエンスが向上します。

- Kubernetes サービスを作成しようとするときの `403` エラーを無視する (Nick Hudson、Polina Bungina)

Patroni は、サービスの作成に失敗してログをスパム送信していましたが、実際にはすでに存在している可能性があります。

- liveness プローブの改善 (Alexander Kukushkin)

ハートビート ループがプライマリーの `ttl` よりも長く実行されている場合、またはレプリカの `2\*ttl` よりも長く実行されている場合、活性の問題は失敗し始めます。これにより、Kubernetes 上の [番犬](/ja/patroni/watchdog#watchdog) の代替として使用できるようになります。

- スイッチオーバー時に同期ノードのみがロックを取得しようとするようにしました。 (Alexander Kukushkin、Polina Bungina)

以前は、ターゲットを指定せずに手動スイッチオーバーが実行された場合、最新の非同期メンバーがリーダーになる可能性はほとんどありませんでした。

- ブートストラップの実行中にクローン作成を避ける (Ants Aasma)

クラスターのブートストラップの実行中に、リーダーのトリガーを必要としないレプリカ作成メソッドを許可しないでください。

- kazoo-2.9.0 との互換性 (Alexander Kukushkin)

Python のバージョンによっては、クローズされたソケットで `select()` が呼び出された場合、`SequentialThreadingHandler.select()` メソッドで `TypeError` 例外と `IOError` 例外が発生する場合があります。

- ソケットのシャットダウン前にSSL接続を明示的にシャットダウンしました。 (Alexander Kukushkin)

これを行わないと、OpenSSL 3.0 で `unexpected eof while reading` エラーが発生しました。

- `prettytable\>=2.2.0` との互換性 (Alexander Kukushkin)

内部の API 変更により、クラスター名のヘッダーが間違った行に表示されていました。

**バグ修正**

- Etcd リース_グラントの期限切れトークンを処理します (monsterxx03)

エラーが発生した場合は、新しいトークンを取得してリクエストを再試行します。

- `GET /read-only-sync` エンドポイントのバグを修正しました (Alexander Kukushkin)

これは以前のリリースで導入されましたが、実際には機能しませんでした。

- データ ディレクトリ ストレージが消失した場合の処理 (Alexander Kukushkin)

Patroni は、PGDATA が存在し空ではないかを定期的にチェックしますが、ストレージに問題が発生した場合、`os.listdir()` は `OSError` 例外を発生させ、ハートビート ループを中断します。

- ユーザー バックエンドが閉じるのを待機するときに `master_stop_timeout` を適用します (Alexander Kukushkin)

ユーザー バックエンドのように見えるものは、実際には停止に失敗しているバックグラウンド ワーカー (Citus メンテナンス デーモンなど) である可能性があります。

- `postgresql.listen` に対して `*:<port>` を受け入れます (Denis Laxalde)

`patroni --validate-config` は無効であると訴えていました。

- Raft での Timeouts の修正 (Alexander Kukushkin)

Patroni または patronictl は、起動時に既知のメンバーから Raft クラスター トポロジを取得しようとします。これらの呼び出しは適切なタイムアウトなしで行われました。

- トークンが変更された場合は領事サービスを強制的に更新します (John A. Lotoski)

そうしないと、「呼び出し実行中の rpc エラー: 呼び出し実行中の rpc エラー: ACL が見つかりません」というエラーが発生します。

--------

## バージョン 2.1.4 {#version-214}

2022-06-01 をリリース

**新機能**

- 典型的な Debian/Ubuntu システムでの `pg_rewind` の動作を改善しました (Gunnar "Nick" Bluth)

`postgresql.conf` をデータ ディレクトリの外に保持する Postgres セットアップ (例: Ubuntu/Debian パッケージ) では、`pg_rewind --restore-target-wal` は `restore_command` の値を把握できません。

- Consul サービス チェックで `TLSServerName` の設定を許可する (Michael Gmelin)

チェックが IP によって実行され、Consul `node_name` が FQDN ではない場合に便利です。

- ウォッチドッグに `ppc64le` サポートを追加しました (Jean-Michel Scheiwiler)

また、一部の非 x86 プラットフォームでのウォッチドッグのサポートが修正されました。

- aws.py コールバックを `boto` から `boto3` に切り替えました (Alexander Kukushkin)

> `boto` 2.x は 2018 以降放棄され、Python 3.9 で失敗します。

- K8 上のサービス アカウント トークンを定期的に更新します (Haitao Li)

Kubernetes 以降、v1.21 サービス アカウント トークンは 1 時間で期限切れになります。

- `/read-only-sync` 監視エンドポイントを追加しました (Dennis4b)

これは `/read-only` に似ていますが、同期レプリカのみが含まれます。

**安定性の向上**

- プライマリーとの論理デコード設定に構成の不一致がある場合は、論理レプリケーション スロットをレプリカにコピーしないでください。 (Alexander Kukushkin)

スロットが `plugin` または `database` 構成オプションと一致しない場合、レプリカはプライマリーから論理レプリケーション スロットをコピーしなくなります。以前は、スロットがこれらの構成オプションと一致するかどうかのチェックは、レプリカがスロットをコピーしてそれを使用して開始するまで実行されず、不必要な再起動が繰り返されていました。

- PostgreSQL のリカバリ構成パラメータの特別な処理 v12+ (Alexander Kukushkin)

レプリカとして開始するとき、Patroni は、`pg_settings` からクエリーする代わりに現在のパラメーター値をキャッシュすることで、リーダー アドレスが変更された場合に `postgresql.conf` を更新し、再起動/リロードできる必要があります。

- `postgresql.listen` パラメータでの IPv6 アドレスの処理が改善されました (Alexander Kukushkin)

`listen` パラメータにはポートがあるため、IPv6 アドレスを角括弧内に入れようとしますが、リストに複数の IP がある場合、角括弧は正しく削除されませんでした。

- PostgreSQL v10 以前でのみ相違チェックを実行する場合は、`replication` 資格情報を使用します。 (Alexander Kukushkin)

`rewind` が有効な場合、Patroni は、新しい Postgres バージョンで `superuser` または `rewind` 資格情報を再度使用します。

**バグ修正**

- `dateutil.parser` のインポートが欠落していたのを修正しました (Wesley Mendes)

テストが失敗したのは、他のモジュールからもインポートされていたためだけではありません。

- `optime` アノテーションが文字列であることを確認します。 (Sebastian Hasler)

場合によっては、Patroni が数値として渡そうとしていました。

- 失敗した`pg_rewind`試行の処理を改善しました (Alexander Kukushkin)

`pg_rewind` 中にプライマリーが使用できなくなると、`$PGDATA` は壊れた状態のままになります。その後、構成で許可されていない場合でも、Patroni はデータ ディレクトリを削除します。

- PostgreSQL の準備ができていない場合は、リーダー `ConfigMap`/`Endpoint` から `slots` アノテーションを削除しないでください。 (Alexander Kukushkin)

`slots` 値が渡されない場合、アノテーションは現在の値を保持します。

- K8s の同時実行性の問題を処理する API ウォッチャー (Alexander Kukushkin)

特定の (未知の) 条件下では、ウォッチャーが期限切れになる可能性があります。その結果、`attempt_to_acquire_leader()` メソッドは、HTTP ステータス コード 409 により失敗する可能性があります。その場合、ウォッチャーの接続をリセットし、最初から再起動します。

--------

## バージョン 2.1.3 {#version-213}

2022-02-18 をリリース

**新機能**

- [patronictl](/ja/patroni/patronictl#patronictl) の暗号化された TLS キーのサポートを追加しました。 (Alexander Kukushkin)

これは、`ctl.keyfile_password` または `PATRONI_CTL_KEYFILE_PASSWORD` 環境変数を介して構成できます。

- /metrics エンドポイントにメトリクスを追加しました (Alexandre Pereira)

具体的には、`patroni_pending_restart` と `patroni_is_paused` です。

- スタンバイクラスター構成で複数ホストを指定できるようにしました。 (Michael Bank)

スタンバイ クラスターが Patroni クラスターからレプリケートされている場合は、PostgreSQL v10 以降の `libpq` で利用できるクライアント側のフェイルオーバーを利用するとよいでしょう。つまり、スタンバイ リーダーの `primary_conninfo` と、接続文字列の `target_session_attrs=read-write` を設定する `pg_rewind` です。 `pgpass` ファイルは複数行 (ホストごとに 1 行) で生成され、プライマリー クラスター ノードで `CHECKPOINT` を呼び出す代わりに、スタンバイ クラスターは `pg_control` が更新されるのを待ちます。

**安定性の向上**

- 従来の `psycopg2` との互換性 (Alexander Kukushkin)

たとえば、Ubuntu 18.04 パッケージからインストールされた `psycopg2` には、`UndefinedFile` 例外がまだありません。

- すべての etcd ノードが応答しない場合は `etcd3` ウォッチャーを再起動します (Alexander Kukushkin)

ウォッチャーが生きている場合、すべての etcd ノードに障害が発生していても、`get_cluster()` メソッドは古い情報を返し続けます。

- 一時停止中にスタンバイクラスターのリーダーロックを削除しないでください。 (Alexander Kukushkin)

以前は、ロックはスタンバイ リーダーではなくプライマリーとして実行されているノードによってのみ維持されていました。

**バグ修正**

- スタンバイ リーダー ブートストラップのバグを修正しました (Alexander Kukushkin)

Patroni は、Postgres が 60 秒後に接続の受け入れを開始しない場合、ブートストラップが失敗したとみなしていました。このバグは 2.1.2 リリースで導入されました。

- カスケード スタンバイへのフェイルオーバーに関するバグを修正しました (Alexander Kukushkin)

カスケード スタンバイでどのスロットを作成するかを判断する際、リーダーが存在しない可能性があることを考慮するのを忘れていました。

- Postgres 構成バリデーターの小さな問題を修正しました (Alexander Kukushkin)

PostgreSQL v14 で導入された整数パラメータは、validator.py で最小値と最大値が引用符で囲まれていたため、検証に失敗していました。

- リーダーのステータスを確認するときにレプリケーション資格情報を使用する (Alexander Kukushkin)

`remove_data_directory_on_diverged_timelines` が設定されているものの、`rewind_credentials` が定義されておらず、ノード間のスーパーユーザー アクセスが許可されていない可能性があります。

- REST API 証明書の置換での「ポートが使用中」エラーを修正しました (Ants Aasma)

証明書を切り替えるときに、同時の API リクエストで競合状態が発生しました。交換期間中にアクティブなサーバーがある場合、交換はポート使用中エラーでエラーとなり、Patroni はアクティブな API サーバーがない状態でスタックします。

- パスワードに `%` 文字が含まれている場合のクラスター ブートストラップのバグを修正しました。 (Bastien Wirtz)

ブートストラップ メソッドは、すべてのパラメーターを適切に引用符で囲んで `DO` ブロックを実行しますが、`cursor.execute()` メソッドはパラメーターが渡された空のリストを好みませんでした。

- 「AttributeError: 属性がありません 'leader'」例外を修正しました。 (Hrvoje Milković)

これは、同期モードが有効で、DCS コンテンツが消去された場合に発生する可能性があります。

- 発散タイムラインチェックのバグを修正しました (Alexander Kukushkin)

Patroni は、タイムラインが分岐していると誤って想定していました。 pg_rewind の場合は問題は発生しませんでしたが、pg_rewind が許可されておらず、`remove_data_directory_on_diverged_timelines` が設定されている場合は、以前のリーダーが再初期化されることになります。

--------

## バージョン 2.1.2 {#version-212}

2021-12-03 をリリース

**新機能**

- `psycopg>=3.0` との互換性 (Alexander Kukushkin)

デフォルトでは、`psycopg2` が優先されます。 `psycopg\>=3.0` は、`psycopg2` が利用できない場合、またはバージョンが古すぎる場合にのみ使用されます。

- `dcs_last_seen` フィールドを REST API に追加します (Michael Bank)

このフィールドには、クラスター メンバーが最後に (UNIX エポックとして) DCS と正常に通信した時刻が記録されます。これは、ネットワーク パーティションの特定や分析に役立ちます。

- `pg_controldata` が「シャットダウン」を報告したときにリーダーのロックを解除します。 (Alexander Kukushkin)

`archive_command` が遅い/障害が発生している場合のスイッチオーバー/シャットダウンが遅いという問題を解決するために、Patroni は、`pg_controldata` が PGDATA を `shut down` として正確に報告し始め、すべての変更を受信したレプリカが少なくとも 1 つあることを確認した直後にリーダー キーを削除します。この条件を満たすレプリカがない場合、リーダー キーは削除されず、古い動作が保持されます。つまり、Patroni はロックを更新し続けます。

- `sslcrldir` 接続パラメータのサポートを追加しました (Kostiantyn Nemchenko)

新しい接続パラメータが PostgreSQL v14 に導入されました。

- Zookeeper で ZNode の ACL 設定を許可する (Alwyn Davis)

新しい構成オプション `zookeeper.set_acls` を導入して、Kazoo が作成する各 ZNode にデフォルトの ACL を適用するようにします。

**安定性の向上**

- 次回のリカバリの試行を次の HA ループまで遅らせます。 (Alexander Kukushkin)

(たとえば) ディスク容量不足により Postgres がクラッシュし、そのために起動に失敗した場合、Patroni は熱心にリカバリしようとするため、ログが溢れます。

- 降格する前にログを追加します。これには時間がかかる場合があります (Michael Bank)

降格が完了するまでに時間がかかる場合があり、ログを見ても実際に何が起こっているのかが明らかではない場合があります。

- 「私は」ステータス メッセージを改善しました (Michael Bank)

`no action. I am a secondary ({0})` と `no action. I am ({0}), a secondary`

- `wal_keep_size` に変換するときに int `wal_keep_segments` にキャストします。 (Jorge Solórzano)

`wal_keep_segments` をグローバル [動的構成](/ja/patroni/config/dynamic#dynamic) の文字列として指定することができますが、Python は動的に型付けされた言語であるため、文字列は単純に乗算されます。例: `wal_keep_segments: "100"` は `100100100100100100100100100100100100100100100100MB` に変換されました。

- 同期レプリケーションが有効な場合、同期ノードのみにスイッチオーバーを許可します。 (Alexander Kukushkin)

それに加えて、リーダーは既知の同期ノードに対してのみレースを行います。

- Postgres が遅い場合にキャッシュされたロールをフォールバックとして使用します。 (Alexander Kukushkin)

極端な場合には、Postgres が非常に遅くなり、通常の監視クエリーが数秒で終了しないことがあります。 `statement_timeout` 例外が適切に処理されないと、リーダー キーの有効期限が切れたり、更新が失敗したりしたときに、Postgres が時間どおりに降格されないという状況が発生する可能性があります。このような例外が発生した場合、Patroni はキャッシュされた `role` を使用して、Postgres がプライマリーとして実行されているかどうかを判断します。

- メンバー ZNode の不必要な更新を回避します (Alexander Kukushkin)

メンバー データの値が変更されていない場合、更新は行われません。

- プロモート後のチェックポイントの最適化 (Alexander Kukushkin)

最新のタイムラインがすでに `pg_control` に保存されている場合は、`CHECKPOINT` を実行しないでください。 `initdb` で新しいクラスターを初期化した直後の不要な `CHECKPOINT` を回避するのに役立ちます。

- 同期ノードを選択する際に `nofailover` のないメンバーを優先します (Alexander Kukushkin)

以前は、同期ノードはレプリケーション ラグにのみ基づいて選択されていたため、`nofailover` タグを持つノードは他のノードと同じ同期になる可能性がありました。プライマリーに障害が発生した場合、フェイルオーバーが自動的に実行できないため、この動作は混乱を招くと同時に危険でもありました。

- etcd マシン キャッシュから重複したホストを削除します (Michael Bank)

etcd クラスター内のアドバタイズされたクライアント URL が正しく構成されていない可能性があります。この場合、Patroni 内の重複を削除するのは簡単な成果です。

**バグ修正**

- スロット管理中に一時レプリケーション スロットをスキップします (Alexander Kukushkin)

v10 から開始すると、`pg_basebackup` は WAL ストリーミング用の一時レプリケーション スロットを作成しますが、スロット名が不明であるため、Patroni はそれを削除しようとしていました。これを修正するために、`pg_stat_replication_slots` ビューをクエリーするときにすべての一時スロットをスキップします。

- `pg_replication_slot_advance()` がタイムアウトしないようにします (Alexander Kukushkin)

この場合、Patroni はデフォルトの `statement_timeout` を使用していたため、呼び出しが失敗すると回復できない可能性が非常に高く、その結果、`pg_wal` と `pg_catalog` のサイズが増大して肥大化します。

- `/status` は降格時に更新されませんでした (Alexander Kukushkin)

PostgreSQL を降格した後、古いリーダーは DCS 内の最後の LSN を更新します。 `2.1.0` から、新しい `/status` キーが導入されましたが、optime は依然として `/optime/leader` に書き込まれていました。

- 降格時に DCS 例外を処理します (Alexander Kukushkin)

リーダー ロックの更新に失敗したためにマスターを降格しているときに、DCS が完全にダウンし、`get_cluster()` 呼び出しで例外が発生する可能性があります。適切に処理されないと、DCS が回復するまで Postgres が停止したままになります。

- `use_unix_socket_repl` が機能しない場合もありました (Alexander Kukushkin)

具体的には、`postgresql.unix_socket_directories` が設定されていない場合です。この場合、Patroni は `libpq` のデフォルト値を使用することになります。

- Patroni REST API に関するいくつかの問題を修正しました (Alexander Kukushkin)

`clusters_unlocked` を定義できない場合があり、`GET /metrics` エンドポイントで例外が発生しました。さらに、エラー処理方法では、`connect_address` タプルには常に 2 つの要素があると想定していましたが、実際には IPv6 の場合はさらに多くの要素がある可能性があります。

- 巻き戻しを決定する前に、新しく昇格したノードが回復を完了するまで待ちます。 (Alexander Kukushkin)

実際のプロモーションが行われて新しいタイムラインが作成されるまでには、しばらく時間がかかる場合があります。待機せずに、レプリカは巻き戻しが必要ではないという結論に達する可能性があります。

- 巻き戻しを決定する際に、履歴ファイル内で欠落しているタイムラインを処理するようになりました。 (Alexander Kukushkin)

現在のレプリカ タイムラインがプライマリーの履歴ファイルにない場合、レプリカは巻き戻しが必要ないと誤って想定しています。

--------

## バージョン 2.1.1 {#version-211}

2021-08-19 をリリース

**新機能**

- ETCD SRV 名前サフィックスのサポート (David Pavlicek)

etcd を使用すると、同じドメイン内の複数の etcd クラスターを区別できるようになり、今後は Patroni もサポートされます。

- 新しいリーダーとともに歴史を豊かにしましょう (huiyalin525)

新しい列が `patronictl history` 出力に追加されます。

- CA バンドルをクラスター内 Kubernetes 構成用に構成可能にします (Aron Parsons)

デフォルトでは、Patroni は `/var/run/secrets/kubernetes.io/serviceaccount/ca.crt` を使用しており、この新機能によりカスタム `kubernetes.cacert` を指定できます。

- Consul サービスとしての動的な登録/登録解除とタグの変更をサポートします (Tommy Li)

以前は、Patroni の再起動が必要でした。

**バグ修正**

- REST API の不必要なリロードを回避します (Alexander Kukushkin)

以前のリリースでは、ディスク上で変更された場合に REST API 証明書を再ロードする機能が追加されました。残念ながら開始直後に無条件でリロードが発生してしまいました。

- `etcd.use_proxies` が設定されている場合はクラスター メンバーを解決しません。 (Alexander Kukushkin)

Patroni は起動時にメンバーのリストをクエリーして etcd クラスターの健全性をチェックします。それに加えて、ホスト名を解決しようとしましたが、これはプロキシ経由で etcd を操作する場合には必要なく、不要な警告を引き起こしていました。

- `pg_stat_replication` 内の NULL 値を持つ行をスキップします (Alexander Kukushkin)

`state = 'streaming'` の場合でも、`pg_stat_replication` ビューの `replay_lsn`、`flush_lsn`、または `write_lsn` フィールドに NULL 値が含まれる可能性があるようです。

--------

## バージョン 2.1.0 {#version-210}

2021-07-06 をリリース

このバージョンでは、PostgreSQL v14 との互換性が追加され、フェイルオーバー/スイッチオーバーに耐えられる論理レプリケーション スロットが作成され、REST API のホワイトリストのサポートが実装され、ログの数もハートビートごとに 1 行に削減されます。

**新機能**

- PostgreSQL v14 との互換性 (Alexander Kukushkin)

Patroni 自体が "pause" モードでない場合は、WAL 再生の一時停止を解除します。プライマリーの `max_connections` などの特定のパラメーターの変更により、"paused" になる可能性があります。

- フェイルオーバー論理スロット (Alexander Kukushkin)

PostgreSQL でのフェイルオーバー/スイッチオーバーで論理レプリケーション スロットを存続させる v11+. レプリケーション スロットは、再起動によってプライマリーからレプリカにコピーされ、その後、[pg_replication_slot_advance()](https://www.postgresql.org/docs/11/functions-admin.html#id-1.5.8.31.8.5.2.2.8.1.1) 関数を使用して前に移動されます。その結果、スロットはフェイルオーバー前にすでに存在しており、イベントが失われることはありませんが、一部のイベントが複数回配信される可能性があります。

- Patroni REST API の許可リストを実装しました (Alexander Kukushkin)

構成されている場合、ルールに一致する IP のみが安全でないエンドポイントの呼び出しを許可されます。それに加えて、クラスターのメンバーの IP をリストに自動的に含めることもできます。

- UNIX ソケット経由のレプリケーション接続のサポートを追加しました (Mohamd El-Rifai)

以前は、Patroni はレプリケーション接続に常に TCP を使用していたため、SSL 検証で問題が発生する可能性がありました。 UNIX ソケットを使用すると、レプリケーション ユーザーを SSL 検証から免除できます。

- ユーザー定義タグのヘルスチェック (Arman Jafari Tehrani)

[事前定義されたタグ:](/ja/patroni/config/yaml#tags_settings) とともに、`patronictl list` 出力および REST API に表示されるカスタム タグをいくつでも指定できます。今後、ヘルスチェックでカスタムタグを使用できるようになります。

- Prometheus `/metrics` エンドポイントを追加しました (Mark Mercado、Michael Bank)

`/patroni` と同じメトリクスを公開するエンドポイント。

- Patroni ログのおしゃべり性を軽減しました (Alexander Kukushkin)

すべてが正常に進むと、HA ループの実行ごとに 1 行だけが書き込まれます。

**重大な変更**

- 古い `permanent logical replication slots` 機能は、PostgreSQL v10 以前では動作しなくなります。 (Alexander Kukushkin)

プロモーションを実行した後に論理スロットを作成する戦略では、論理イベントが失われ、無効になることがないことを保証できません。

- ノードがロックを保持している場合、`/leader` エンドポイントは常に 200 を返します (Alexander Kukushkin)

スタンバイ クラスターを昇格するには、ロード バランサーのヘルス チェックを更新する必要がありますが、これはあまり便利ではなく、忘れがちです。これを解決するために、`/leader` ヘルス チェック エンドポイントの動作を変更します。クラスターが正常であるか [standby_cluster](/ja/patroni/standby_cluster#standby_cluster) であるかを考慮せずに、200 を返します。

**Raft サポートの改善**

- Raft トラフィック暗号化の信頼できるサポート (Alexander Kukushkin)

`PySyncObj` のさまざまな問題により、暗号化サポートは非常に不安定でした

- Raft 実装における DNS の問題を処理します (Alexander Kukushkin)

`self_addr` および/または `partner_addrs` が IP の代わりに DNS 名を使用して構成されている場合、`PySyncObj` はオブジェクトの作成時に 1 回だけ効果的に解決を実行していました。同じノードが別の IP でオンラインに戻ると問題が発生していました。

**安定性の向上**

- `psycopg2-2.9+` との互換性 (Alexander Kukushkin)

`psycopg2` では、`autocommit = True` は `with connection` ブロックで無視され、レプリケーション プロトコル接続が切断されます。

- Zookeeper で実行される過剰な HA ループを修正しました。 (Alexander Kukushkin)

メンバー ZNodes の更新により連鎖反応が発生し、HA ループが連続して複数回実行されることになりました。

- REST API 証明書がディスク上で変更された場合、リロードします (Michael Todorovic)

REST API 証明書ファイルが適切に更新された場合、Patroni はリロードを実行しませんでした。

- kerberos 認証が使用されている場合は pgpass ディレクトリを作成しないでください。 (Kostiantyn Nemchenko)

Kerberos とパスワード認証は相互に排他的です。

- カスタム ブートストラップに関する小さな問題を修正しました (Alexander Kukushkin)

PITR を実行する場合にのみ Postgres を `hot_standby=off` で開始し、PITR が完了した後に再起動します。

**バグ修正**

- `kazoo-2.7+` との互換性 (Alexander Kukushkin)

Patroni は独自に再試行を処理するため、使用可能な接続がない場合は Zookeeper クラスターへのリクエストが直ちに破棄されるという `kazoo` の古い動作に依存しています。

- プロキシ経由で接続していることがわかっている場合、etcd v3 クラスターのバージョンを明示的に要求します。 (Alexander Kukushkin)

Patroni は、gPRC-gateway 経由で etcd v3 クラスターと連携しており、クラスターのバージョンに応じて、異なるエンドポイント (`/v3`、`/v3beta`、または `/v3alpha`) を使用する必要があります。このバージョンはクラスター トポロジと一緒にのみ解決されましたが、プロキシ経由で接続する場合は後者が実行されなかったためです。

--------

## バージョン 2.0.2 {#version-202}

2021-02-22 をリリース

**新機能**

- 外部管理のレプリケーション スロットを無視する機能 (James Coleman)

Patroni は、未知のレプリケーション スロットを削除しようとしていますが、レプリケーション スロットを外部で管理する必要がある場合は確かにあります。今後は、削除してはならないスロットを設定できるようになります。

- REST API の暗号スイート制限のサポートを追加しました (Gunnar "Nick" Bluth)

これは、`restapi.ciphers` または `PATRONI_RESTAPI_CIPHERS` 環境変数を介して構成できます。

- REST API の暗号化された TLS キーのサポートを追加しました (Jonathan S. Katz)

これは、`restapi.keyfile_password` または `PATRONI_RESTAPI_KEYFILE_PASSWORD` 環境変数を介して構成できます。

- REST API 認証資格情報の定数時間比較 (Alex Brasetvik)

タイミング攻撃に対して脆弱な `==` の代わりに `hmac.compare_digest()` を使用してください。

- レプリケーション ラグに基づいて同期ノードを選択する (Krishna Sarabu)

同期ノード上のレプリケーション ラグが設定されたしきい値を超え始めた場合、そのノードは非同期に降格されるか、他のノードに置き換えられるか、あるいはその両方になる可能性があります。動作は `maximum_lag_on_syncnode` で制御されます。

**安定性の向上**

- カスタム ブートストラップを実行するときに `hot_standby = off` で postgres を開始します (Igor Yanchenko)

カスタム ブートストラップ中、Patroni はベースバックアップを復元し、Postgres を起動して、リカバリが完了するまで待機します。スタンバイ上の一部の PostgreSQL パラメーターはプライマリーよりも小さくすることができず、新しい値 (WAL から復元された) が構成された値より大きい場合、Postgres はパニックを起こして停止します。このような動作を回避するために、`hot_standby` モードを使用せずにカスタム ブートストラップを実行します。

- 必要なウォッチドッグが正常でない場合にユーザーに警告します。 (Nicolas Tauvin)

ウォッチドッグ デバイスが書き込み可能でない場合、または必須モードで見つからない場合、メンバーを昇格することはできません。この構成ミスを検索する場所をユーザーに示す警告を追加しました。

- シングルユーザー モードのリカバリの冗長性が向上しました (Alexander Kukushkin)

Patroni が PostgreSQL が明確にシャットダウンされていないことに気付いた場合、場合によっては、Postgres をシングル ユーザー モードで起動することによってクラッシュ リカバリが実行されます。 (ディスク上のスペース不足などにより) リカバリが失敗しても、エラーが飲み込まれる可能性があります。

- `python-consul2` モジュールとの互換性を追加しました (Alexander Kukushkin、Wilfried Roset)

古き良き `python-consul` は数年前からメンテナンスされていないため、誰かが新機能とバグ修正を備えたフォークを作成しました。

- [patronictl](/ja/patroni/patronictl#patronictl) を実行する場合は `bypass_api_service` を使用しないでください。 (Alexander Kukushkin)

K8s ポッドが非 `default` 名前空間で実行されている場合、[Kubernetes](/ja/patroni/kubernetes#kubernetes) エンドポイントをクエリーするための十分な権限があるとは限りません。この場合、Patroni は警告を表示し、`bypass_api_service` 設定を無視します。 [patronictl](/ja/patroni/patronictl#patronictl) の場合、警告は少し面倒でした。

- `raft.data_dir` が存在しない場合は作成するか、書き込み可能であることを確認してください (Mark Mercado)

使いやすさと使いやすさを向上させます。

**バグ修正**

- 一時停止中にリーダーのロックが失われた場合、再起動またはプロモートを中断しないでください。 (Alexander Kukushkin)

一時停止中は、ロックなしで postgres をプライマリーとして実行できます。

- REST API の `shutdown_request()` に関する問題を修正しました (Nicolas Limage)

SSL 接続の処理を改善し、スレッドが開始されるまでハンドシェイクを遅らせるために、Patroni は `HTTPServer` のいくつかのメソッドをオーバーライドします。 `shutdown_request()` メソッドが忘れられていました。

- Zookeeper使用時のスリープ時間の問題を修正しました。 (Alexander Kukushkin)

HA コードの実行の間に、Patroni が最大 2 倍長くスリープしている可能性がありました。

- ブートストラップの失敗後にデータ ディレクトリを移動するときの無効な `os.symlink()` 呼び出しを修正しました。 (Andrew L'Ecuyer)

ブートストラップが失敗した場合、Patroni はデータ ディレクトリ、pg_wal、およびすべてのテーブルスペースの名前を変更します。その後、シンボリックリンクを更新して、ファイルシステムの一貫性を保ちます。 `src` 引数と `dst` 引数が交換されているため、シンボリックリンクの作成は失敗していました。

- post_bootstrap() メソッドのバグを修正しました (Alexander Kukushkin)

スーパーユーザーのパスワードが構成されていない場合、Patroni は `post_init` スクリプトの呼び出しに失敗し、そのためブートストラップ全体が失敗していました。

- スタンバイ クラスターの pg_rewind に関する問題を修正しました (Alexander Kukushkin)

スーパーユーザー名が Postgres と異なる場合は、接続文字列にデータベース名が含まれていないため、スタンバイ クラスターの `pg_rewind` が失敗していました。

- Etcd v3 による認証が明示的に失敗した場合のみ終了します。 (Alexander Kukushkin)

起動時に Patroni は etcd クラスター トポロジの検出を実行し、必要に応じて認証を行います。 etcd サーバーの 1 つがアクセスできず、Patroni がこのサーバーで認証を実行しようとして、次のノードで再試行せずに失敗することが考えられます。

- psutil cmdline() が空のリストを返す場合の処理 (Alexander Kukushkin)

ゾンビプロセスは依然としてポストマスターの子ですが、cmdline() を持っていません。

- `PATRONI_KUBERNETES_USE_ENDPOINTS` 環境変数をブール値として扱います。 (Alexander Kukushkin)

そうしないと、環境経由で `kubernetes.use_endpoints` を無効にすることができなくなりました。

- 同時エンドポイント更新エラーの処理を改善しました (Alexander Kukushkin)

Patroni は現在のエンドポイント オブジェクトを明示的にクエリーし、現在のポッドがまだリーダー ロックを保持していることを確認して、更新を繰り返します。

--------

## バージョン 2.0.1 {#version-201}

2020-10-01 をリリース

**新機能**

- `less` が利用できない場合は、`patronictl edit-config` のポケットベルとして `more` を使用します (Pavel Golub)

Windows では、`more.com` になります。それに加えて、`requirements.txt` では `cdiff` が `ydiff` に変更されましたが、[patronictl](/ja/patroni/patronictl#patronictl) は互換性のために両方をサポートしています。

- `raft` `bind_addr` および `password` のサポートを追加しました (Alexander Kukushkin)

`raft.bind_addr` は、NAT の背後で実行する場合に便利です。 `raft.password` はトラフィック暗号化を有効にします (`cryptography` モジュールが必要です)。

- `sslpassword` 接続パラメータのサポートを追加しました (Kostiantyn Nemchenko)

接続パラメーターは PostgreSQL 13 で導入されました。

**安定性の向上**

- 一時停止時の動作を変更しました (Alexander Kukushkin)

  1. `PGDATA` ディレクトリが見つからない、または空の場合、Patroni は `bootstrap` メソッドを呼び出しません。
  2. Patroni は、一時停止中に sysid が一致しない場合には終了せず、警告をログに記録するだけです。
  3. Postgres がリカバリ中ではなく実行されている (書き込みを受け入れている) が、sysid が初期化キーと一致しない場合、ノードは一時停止モードでリーダー キーを取得しようとしません。

- クラッシュ リカバリの実行時に `master_start_timeout` を適用します (Alexander Kukushkin)

Postgres がリーダー ノードでクラッシュした場合、Patroni はシングル ユーザー モードで Postgres を起動することによってクラッシュ リカバリを実行します。クラッシュリカバリ中に、リーダーのロックが更新されます。クラッシュ リカバリが `master_start_timeout` 秒以内に終了しなかった場合、Patroni はクラッシュ リカバリを強制的に停止し、リーダー ロックを解放します。

- `urllib3` 要件から追加の `secure` を削除しました (Alexander Kukushkin)

これを追加した唯一の理由は、Python 2.7 の `ipaddress` 依存関係でした。

**バグ修正**

- `Kubernetes.update_leader()` のバグを修正しました。 (Alexander Kukushkin)

リーダー オブジェクトの更新が失敗した場合、未処理の例外によりプライマリーの降格が妨げられていました。

- RAFT 使用時のハングする [patronictl](/ja/patroni/patronictl#patronictl) を修正しました。 (Alexander Kukushkin)

Patroni 構成で [patronictl](/ja/patroni/patronictl#patronictl) を使用する場合、`self_addr` を `partner_addrs` に追加する必要があります。

- `get_guc_value()` のバグを修正しました (Alexander Kukushkin)

Patroni は、PostgreSQL 12 の `restore_command` の値の取得に失敗していたため、`pg_rewind` の欠落している WAL を取得できませんでした。

--------

## バージョン 2.0.0 {#version-200}

2020-09-02 をリリース

このバージョンでは、PostgreSQL 13 との互換性が強化され、複数の同期スタンバイのサポートが追加され、`pg_rewind` の処理が大幅に改善され、純粋な RAFT (etcd、Consul、または Zookeeper なし) での etcd v3 および Patroni のサポートが追加され、オプションで `pre_promote` を呼び出すことが可能になります。 （フェンシング）スクリプト。

**PostgreSQL 13 のサポート**

- PostgreSQL 13+ で `standby_leader` に昇格するときに `on_reload` を起動しないでください。 (Alexander Kukushkin)

`standby_leader` に昇格する場合、`primary_conninfo` を変更し、ロールを更新して、Postgres をリロードします。 `on_role_change` と `on_reload` は実質的に相互に重複するため、Patroni は `on_role_change` のみを呼び出します。

- `gssencmode` および `channel_binding` 接続パラメータのサポートを追加しました。 (Alexander Kukushkin)

PostgreSQL 12 では、`gssencmode` および 13 `channel_binding` 接続パラメータが導入されており、`postgresql.authentication` セクションで定義されている場合はそれらを使用できるようになりました。

- ハンドル名が `wal_keep_segments` から `wal_keep_size` に変更されました (Alexander Kukushkin)

構成に誤りがある場合 (13 では `wal_keep_segments`、古いバージョンでは `wal_keep_size`)、Patroni が自動的に構成を調整します。

- 可能であれば、13 で `pg_rewind` を `--restore-target-wal` とともに使用してください (Alexander Kukushkin)

PostgreSQL 13 では、Patroni が `restore_command` が構成されているかどうかを確認し、`pg_rewind` にそれを使用するように指示します。

**新機能**

- \[BETA\] 純粋な RAFT に Patroni のサポートを実装しました。 (Alexander Kukushkin)

これにより、etcd、Consul、Zookeeper などのサードパーティの依存関係なしで Patroni を実行できるようになります。 HA の場合は、3 つの Patroni ノード、または Patroni を含む 2 つのノードと `patroni_raft_controller` を含む 1 つのノードを実行する必要があります。詳細については、[ドキュメント](/ja/patroni/config/yaml#raft_settings) を確認してください。

- \[BETA\] gPRC ゲートウェイ経由で etcd v3 プロトコルのサポートを実装しました (Alexander Kukushkin)

etcd 3.0 は 4 年以上前にリリースされており、etcd 3.4 では v2 がデフォルトで無効になっています。 v2 が etcd から完全に削除される可能性もあるため、etcd v3 のサポートを Patroni に実装しました。これを使用するには、Patroni 構成ファイルである `etcd3` セクションを明示的に作成する必要があります。

- 複数の同期スタンバイのサポート (Krishna Sarabu)

これにより、複数の同期レプリカを含むクラスターを実行できます。同期レプリカの最大数は、新しいパラメータ `synchronous_node_count` によって制御されます。デフォルトでは 1 に設定されており、[synchronous_mode](/ja/patroni/replication_modes#synchronous_mode) が `off` に設定されている場合は効果がありません。

- `pre_promote` スクリプトを呼び出す可能性を追加しました (Sergey Dudoladov)

コールバックとは異なり、`pre_promote` スクリプトは、リーダー ロックを取得した後、Postgres をプロモートする前に同期的に呼び出されます。スクリプトが失敗するか、ゼロ以外の終了コードで終了すると、現在のノードはリーダー ロックを解放します。

- 構成ディレクトリのサポートを追加しました (Floris van Nee)

ディレクトリ内の YAML ファイルがアルファベット順にロードされ、適用されます。

- PostgreSQL パラメータの高度な検証 (Alexander Kukushkin)

特定のパラメーターが現在の PostgreSQL バージョンでサポートされていない場合、またはその値が正しくない場合、Patroni はパラメーターを完全に削除するか、値の修正を試みます。

- プロモート後の強制チェックポイントが完了したらメインスレッドを起動します。 (Alexander Kukushkin)

レプリカは、DCS のリーダーのメンバー キーを介してチェックポイントの指示を待っています。通常、キーは HA ループごとに 1 回だけ更新されます。メインスレッドを起動しないと、レプリカは必要以上に最大 `loop_wait` 秒長く待機する必要があります。

- 9.6+ での `pg_stat_wal_receiver` ビューの使用 (Alexander Kukushkin)

ビューには `primary_conninfo` と `primary_slot_name` の最新の値が含まれていますが、`recovery.conf` の内容は古い可能性があります。

- Patroni 設定ファイルでの IPv6 アドレスの処理を改善しました (Mateusz Kowalski)

IPv6 アドレスは角括弧で囲む必要がありますが、Patroni はプレーンなアドレスを取得することを期待していました。現在は両方の形式がサポートされています。

- Consul `service_tags` 設定パラメータを追加しました (Robert Edström)

これらは、ロード バランサーなどによる動的なサービス検出に役立ちます。

- Zookeeper の SSL サポートを実装しました (Kostiantyn Nemchenko)

`kazoo>=2.6.0` が必要です。

- カスタム ブートストラップ メソッドの `no_params` オプションを実装しました (Kostiantyn Nemchenko)

これにより、`wal-g`、`pgBackRest`、およびその他のバックアップ ツールをシェル スクリプトにラップせずに呼び出すことができます。

- 初期化に失敗した後に WAL とテーブルスペースを移動します (Feike Steenbergen)

`reinit` を実行すると、Patroni は `PGDATA` だけでなく、シンボリックリンクされた WAL ディレクトリとテーブルスペースもすでに削除していました。 `move_data_directory()` メソッドは同様のジョブを実行します。つまり、WAL ディレクトリとテーブルスペースの名前を変更し、PGDATA 内のシンボリックリンクを更新します。

**pg_rewind サポートの改善**

- タイムラインの発散チェックの改善 (Alexander Kukushkin)

レプリカ上の再生位置がスイッチポイントより前でない場合、または元のプライマリー上のチェックポイント レコードの終わりがスイッチポイントと同じである場合は、巻き戻す必要はありません。チェックポイント レコードの終わりを取得するために、`pg_waldump` を使用し、その出力を解析します。

- `pg_rewind` がそれについて文句を言ったら、欠落している WAL を取得してみます。 (Alexander Kukushkin)

`pg_rewind` に必要な WAL セグメントが `pg_wal` ディレクトリに存在しないため、`pg_rewind` が分岐点より前のチェックポイントの場所を見つけることができない場合があります。 PostgreSQL 13 `pg_rewind` からは、欠落している WAL を取得するために `restore_command` を使用できるようになりました。古い PostgreSQL バージョンの場合、Patroni は、失敗した巻き戻し試行のエラーを解析し、`restore_command` を独自に呼び出して、不足している WAL を取得しようとします。

- スタンバイ クラスターで新しいタイムラインを検出し、必要に応じて巻き戻し/再初期化をトリガーします (Alexander Kukushkin)

[standby_cluster](/ja/patroni/standby_cluster#standby_cluster) はプライマリー クラスターから切り離されているため、リーダーの選出やタイムラインの切り替えについてはすぐには認識されません。この事実を検出するために、`standby_leader` は `pg_wal` 内の新しい履歴ファイルを定期的にチェックします。

- 履歴ログ出力を短縮して美しくしました (Alexander Kukushkin)

Patroni が `pg_rewind` の必要性を判断しようとすると、プライマリーからの履歴ファイルの内容がログに書き込まれる可能性があります。履歴ファイルはフェイルオーバー/スイッチオーバーのたびに増大し、最終的には多くの行を占めるようになり、そのほとんどはあまり役に立ちません。 Patroni は、生データを表示する代わりに、現在のレプリカ タイムラインより前の 3 行とその後の 2 行のみを表示します。

**K8 の改良点**

- [Kubernetes](/ja/patroni/kubernetes#kubernetes) Python モジュールを削除します (Alexander Kukushkin)

公式の Python Kubernetes クライアントには自動生成されたコードが多数含まれているため、非常に重くなっています。 Patroni は、K8 の API エンドポイントのほんの一部のみを使用しており、それらのサポートの実装は難しくありませんでした。

- [Kubernetes](/ja/patroni/kubernetes#kubernetes) サービスをバイパスできるようにしました。 (Alexander Kukushkin)

K8s で実行している場合、Patroni は通常、[Kubernetes](/ja/patroni/kubernetes#kubernetes) サービスを介して K8s API と通信します。そのアドレスは `KUBERNETES_SERVICE_HOST` 環境変数で公開されます。他のサービスと同様に、[Kubernetes](/ja/patroni/kubernetes#kubernetes) サービスは `kube-proxy` によって処理され、構成に応じてトラフィック ルーティングをユーザー空間プログラムまたは `iptables` に依存します。中間コンポーネントをスキップして K8s マスター ノードに直接接続すると、より適切な再試行戦略を実装でき、K8s マスター ノードがアップグレードされるときに Postgres を降格するリスクを軽減できます。

- Sync Patroni クラスターのすべてのポッドの HA ループ (Alexander Kukushkin)

そうしないと、障害検出時間が `ttl` から `ttl + loop_wait` に増加しました。

- K8 のサブセット アドレスに `references` と `nodename` を入力します。 (Alexander Kukushkin)

一部のロードバランサーはこの情報に依存しています。

- `update_leader()` で発生する可能性のある競合状態を修正しました。 (Alexander Kukushkin)

Patroni の外部でリーダー構成マップまたはエンドポイントの同時更新が行われると、`update_leader()` 呼び出しが失敗する可能性があります。この場合、Patroni は現在のノードがまだリーダー ロックを所有していることを再確認し、更新を繰り返します。

- 存在しない構成へのパッチ適用を明示的に禁止します (Alexander Kukushkin)

[Kubernetes](/ja/patroni/kubernetes#kubernetes) 以外の DCS では、`cluster.config` が `None` であるため、PATCH 呼び出しは例外で失敗しますが、Kubernetes では構成アノテーションが問題なく作成され、ブートストラップ終了後にブートストラップ構成を書き込むことができませんでした。

- [一時停止する](/ja/patroni/pause#pause) のバグを修正しました (Alexander Kukushkin)

リーダー キーが存在しない場合、レプリカは `primary_conninfo` を削除し、Postgres を再起動していましたが、何も行わないはずです。

**REST API の改善**

- ワーカー スレッドが開始されるまで TLS ハンドシェイクを延期します。 (Alexander Kukushkin、Ben Harris)

TLS ハンドシェイクが API スレッドで実行され、クライアント側がデータを送信しなかった場合、API スレッドはブロックされました (DoS の危険があります)。

- REST のクライアント証明書とは別に `basic-auth` をチェックする API (Alexander Kukushkin)

以前は、クライアント証明書のみが検証されていました。 2 つのチェックを独立して実行することは、完全に有効な使用例です。

- `OPTIONS` リクエストの HTTP ヘッダーの後に `CRLF` を二重に書き込みます (Sergey Burladyan)

HAProxy は 1 つの `CRLF` に満足していましたが、Consul ヘルスチェックでは接続の切断と予期しない EOF が発生したと報告されました。

- `GET /cluster` で Zookeeper の古いメンバー情報が表示されていました (Alexander Kukushkin)

エンドポイントは Patroni 内部クラスター ビューを使用していました。 Patroni 自体については問題は発生しませんでしたが、外部に公開する場合は、最新の情報、特にレプリケーション ラグを表示する必要があります。

- スタンバイ クラスターのヘルスチェックを修正しました (Alexander Kukushkin)

マスターの `GET /standby-leader` と `standby_leader` の `GET /master` が、誤って 200 で応答していました。

- 実装 `DELETE /switchover` (Alexander Kukushkin)

REST API 呼び出しは、スケジュールされたスイッチオーバーを削除します。

- `/readiness` および `/liveness` エンドポイントを作成しました (Alexander Kukushkin)

これらは、K8s サービスがラベル セレクターとともに使用されている場合に、サブセット アドレスから "unhealthy" ポッドを削除するのに役立つ可能性があります。

- 強化された `GET /replica` および `GET /async` REST API ヘルスチェック (Krishna Sarabu、Alexander Kukushkin)

チェックはオプションのキーワード `?lag=<max-lag>` をサポートし、ラグが指定された値より小さい場合にのみ 200 で応答するようになりました。この機能を利用する場合、リーダー上の WAL 位置に関する情報は `loop_wait` 秒ごとにのみ更新されることに注意してください。

- REST API 応答にユーザー定義の HTTP ヘッダーのサポートを追加しました (Yogesh Sharma)

この機能は、リクエストがブラウザから行われる場合に役立つ可能性があります。

**patronictlの改善**

- `patronictl pause` に存在しないリーダーを呼び出そうとしないでください (Alexander Kukushkin)

K8s でリーダーのないクラスターを一時停止しているときに、[patronictl](/ja/patroni/patronictl#patronictl) はメンバー「None」にアクセスできないという警告を表示していました。

- メンバー `conn_url` が欠落している場合の処理 (Alexander Kukushkin)

K8 では、Patroni がまだ実行されていないため、ポッドに必要なアノテーションがない可能性があります。 [patronictl](/ja/patroni/patronictl#patronictl) が失敗していました。

- ASCII クラスター トポロジを印刷する機能を追加しました (Maxim Fedotov、Alexander Kukushkin)

カスケード レプリケーションを使用してクラスターの概要を把握するのに非常に役立ちます。

- `patronictl flush switchover` の実装 (Alexander Kukushkin)

それ以前は、`patronictl flush` はスケジュールされた再起動のキャンセルのみをサポートしていました。

**バグ修正**

- 既存の PGDATA を使用したクラスターのブートストラップ中に Attribute エラーが発生しました (Krishna Sarabu)

`/history` キーを作成/更新しようとすると、Patroni は DCS でまだ作成されていない `ClusterConfig` オブジェクトにアクセスしていました。

- Consul の例外処理を改善しました。 (Alexander Kukushkin)

`touch_member()` メソッドの未処理の例外により、Patroni プロセス全体がクラッシュしました。

- `post_init` スクリプトに対して `synchronous_commit=local` を強制します (Alexander Kukushkin)

Patroni はユーザー (`replication`、`rewind`) を作成するときにすでにそれを行っていましたが、`post_init` の場合にそれが欠けていたのは見落としでした。その結果、スクリプトが内部で独自に実行していない場合、[synchronous_mode](/ja/patroni/replication_modes#synchronous_mode) のブートストラップを完了できませんでした。

- Consul プール マネージャーの `maxsize` を増加しました (ponvenkates)

デフォルトの `size=1` では、いくつかの警告が生成されました。

- Patroni は Postgres が実行中であると誤って報告していました (Alexander Kukushkin)

たとえば、ディスク不足エラーにより Postgres がクラッシュした場合、状態は更新されませんでした。

- 欠損値または空の値の代わりに `*` を `pgpass` に挿入します。 (Alexander Kukushkin)

たとえば、`standby_cluster.port` が指定されていない場合、`pgpass` ファイルが正しく生成されません。

- 特殊文字を使用したリーダー ノードでの物理レプリケーション スロットの作成をスキップします (Krishna Sarabu)

名前に「-」などの特殊文字が含まれている場合 ("abc-us-1" など)、Patroni はリーダー ノードの休止スロット (`slots` が定義されている場合) を作成しているように見えました。

- カスタム ブートストラップで存在しない `pg_hba.conf` を削除しないようにしました。 (Krishna Sarabu)

カスタム ブートストラップ後に `pg_hba.conf` が `pgdata` ディレクトリの外にある場合、Patroni は失敗していました。

--------

## バージョン 1.6.5 {#version-165}

2020-08-23 をリリース

**新機能**

- マスター停止タイムアウト (Krishna Sarabu)

Postgres を停止するときに Patroni が待機できる秒数。 [synchronous_mode](/ja/patroni/replication_modes#synchronous_mode) が有効な場合にのみ有効です。 0 より大きい値に設定され、[synchronous_mode](/ja/patroni/replication_modes#synchronous_mode) が有効になっている場合、停止操作が `master_stop_timeout` で設定された値を超えて実行されている場合、Patroni はポストマスターに `SIGKILL` を送信します。耐久性と可用性のトレードオフに応じて値を設定します。パラメーターが設定されていないか、正以外の値に設定されている場合、`master_stop_timeout` は効果がありません。

- プライマリーの名前で永続的な物理スロットを作成しないでください。 (Alexander Kukushkin)

レプリカが停止している間にプライマリーが WAL セグメントをリサイクルするのは一般的な問題です。これで、ノード数が固定され、名前が決して変更されない、静的クラスターに対する優れたソリューションが得られました。 `slots` 内のすべてのノードの名前をリストするだけで、ノードがダウンしている (DCS に登録されていない) ときにプライマリーがスロットを削除しないようにすることができます。

- Config Validator の初稿 (Igor Yanchenko)

Patroni 構成を検証するには、`patroni --validate-config patroni.yaml` を使用します。

- タイムライン履歴の最大長を設定できるようになりました (Krishna Sarabu)

Patroni は、フェイルオーバー/スイッチオーバーの履歴を DCS の `/history` キーに書き込みます。時間の経過とともにこのキーのサイズは大きくなりますが、ほとんどの場合、重要なのは最後の数行だけです。 `max_timelines_history` パラメーターを使用すると、DCS に保持されるタイムライン履歴アイテムの最大数を指定できます。

- Kazoo 2.7.0 の互換性 (Danyal Prout)

Kazoo の一部の非パブリック メソッドはシグネチャを変更しましたが、Patroni はそれらに依存していました。

**patronictlの改善**

- メンバー タグを表示 (Kostiantyn Nemchenko、Alexander Kukushkin)

タグはノードごとに個別に構成されており、タグの概要を簡単に把握する方法はありませんでした。

- メンバーの出力を改善しました (Alexander Kukushkin)

冗長なクラスター名は各行に表示されなくなり、テーブルのヘッダーにのみ表示されます。

``` bash
$ patronictl list
+ Cluster: batman (6813309862653668387) +---------+----+-----------+---------------------+
|    Member   |      Host      |  Role  |  State  | TL | Lag in MB | Tags                |
+-------------+----------------+--------+---------+----+-----------+---------------------+
| postgresql0 | 127.0.0.1:5432 | Leader | running |  3 |           | clonefrom: true     |
|             |                |        |         |    |           | noloadbalance: true |
|             |                |        |         |    |           | nosync: true        |
+-------------+----------------+--------+---------+----+-----------+---------------------+
| postgresql1 | 127.0.0.1:5433 |        | running |  3 |       0.0 |                     |
+-------------+----------------+--------+---------+----+-----------+---------------------+
```

- 設定ファイルが明示的に指定されているが見つからない場合は失敗します (Kaarel Moppel)

以前は、[patronictl](/ja/patroni/patronictl#patronictl) は `DEBUG` メッセージのみを報告していました。

- 初期化されていない K8s ポッドが patronictl を破壊する問題を解決しました。 (Alexander Kukushkin)

Patroni は、K8 上の特定のポッド アノテーションに依存しています。 Patroni ポッドの 1 つが停止または開始しているときは、有効なアノテーションがまだなく、[patronictl](/ja/patroni/patronictl#patronictl) が例外で失敗していました。

**安定性の向上**

- K8s API サーバーへの LIST 呼び出しが失敗した場合、1 秒のバックオフを適用します (Alexander Kukushkin)

これは主にログの氾濫を避けるために必要ですが、メインスレッドの枯渇を防ぐのにも役立ちます。

- `retry-after` HTTP ヘッダーが K8s API によって返された場合に再試行します (Alexander Kukushkin)

K8s API サーバーがリクエストで圧倒されると、再試行を要求されることがあります。

- ポストマスターからの`KUBERNETES_`環境をスクラブします (Feike Steenbergen)

`KUBERNETES_` 環境変数は PostgreSQL には必要ありませんが、環境変数をポストマスターに公開すると、バックエンドや通常のデータベース ユーザー (pl/perl などを使用) にも公開されます。

- 再初期化時にテーブルスペースをクリーンアップします (Krishna Sarabu)

再初期化中に、Patroni は `PGDATA` のみを削除し、ユーザー定義のテーブルスペース ディレクトリを残していました。これにより、Patroni が再初期化でループする原因となります。この問題に対する以前の回避策は、[カスタムブートストラップ](/ja/patroni/replica_bootstrap#custom_bootstrap) スクリプトを実装することでした。

- プロモートが行われた後に明示的に `CHECKPOINT` を実行します。 (Alexander Kukushkin)

新しいプライマリーが `pg_rewind` で使用可能になるまでの時間を短縮するのに役立ちます。

- Etcd メンバーのスマート更新 (Alexander Kukushkin)

Patroni が etcd クラスターのすべてのメンバーでリクエストの実行に失敗した場合、Patroni は、次回再試行する前に、IP/ホストの変更について `A` または `SRV` レコードを再チェックします。

- `pg_controldata` から欠損値をスキップします (Feike Steenbergen)

PGDATA と一致しないバージョンのバイナリを使用しようとすると、値が欠落します。 Patroni はとにかく Postgres を起動しようとしますが、Postgres はメジャー バージョンが一致しないと通知し、エラーで中止されます。

**バグ修正**

- 必要に応じて Consul の SSL 検証を無効にします (Julien Riou)

`urllib3` の特定のバージョン以降、SSL 検証を効果的に無効にするには、`cert_reqs` を明示的に `ssl.CERT_NONE` に設定する必要があります。

- HA ループの各サイクルでレプリケーション接続を開かないようにしました。 (Alexander Kukushkin)

回帰は 1.6.4 で導入されました。

- 失敗したプライマリーでの Call `on_role_change` コールバック (Alexander Kukushkin)

場合によっては、仮想 IP が古いプライマリーに接続されたままになる可能性があります。回帰は 1.4.5 で導入されました。

- pg_rewind が成功した後に postgres が開始された場合、巻き戻し状態をリセットします。 (Alexander Kukushkin)

このバグの結果、Patroni は一時停止モードで postgres を手動でシャットダウンして起動していました。

- `recovery.conf` をチェックするときに `recovery_min_apply_delay` を `ms` に変換します

12 よりも古い PostgreSQL 上で `recovery_min_apply_delay` が構成されている場合、Patroni はレプリカを無期限に再起動していました。

- PyInstaller の互換性 (Alexander Kukushkin)

PyInstaller は、Python アプリケーションをスタンドアロンの実行可能ファイルにフリーズ (パッケージ化) します。 `multiprocessing` の `fork` ではなく `spawn` メソッドに切り替えたときに互換性が失われていました。

--------

## バージョン 1.6.4 {#version-164}

2020-01-27 をリリース

**新機能**

- `patronictl reinit` の `--wait` オプションを実装しました (Igor Yanchenko)

`--wait` オプションが使用されている場合、Patronictl は `reinit` が完了するまで待機します。

- Windows サポートのさらなる改善 (Igor Yanchenko、Alexander Kukushkin)

  1. 統合テストに使用されるすべてのシェル スクリプトは Python で書き直されます
  2. `pg_ctl kill` は、非 posix システムで postgres を停止するために使用されます。
  3. unix ドメイン ソケットを使用しないでください

**安定性の向上**

- `unix_socket_directories` と `stats_temp_directory` が存在することを確認してください (Igor Yanchenko)

Patroni および Postgres の開始時に、`unix_socket_directories` および `stats_temp_directory` が存在することを確認するか、それらの作成を試行します。 Patroni は、作成に失敗した場合に終了します。

- Patroni が書き込みアクセスできる場所に `postgresql.pgpass` が配置されていることを確認してください。 (Igor Yanchenko)

書き込みアクセスがない場合、Patroni は例外で終了します。

- Consul `serfHealth` チェックをデフォルトで無効にします (Kostiantyn Nemchenko)

ネットワークに小さな問題が発生した場合でも、`serfHealth` が失敗すると、ノードに関連付けられたすべてのセッションが無効になります。したがって、リーダー キーは `ttl` よりもはるかに早く失われ、レプリカが不要に再起動され、場合によってはプライマリーが降格されます。

- K8 への接続のための tcp キープアライブの構成 API (Alexander Kukushkin)

TTL 秒経過してもソケットから何も取得されない場合、ソケットは停止していると見なすことができます。

- ユーザー作成時のパスワードのログ記録を回避します (Alexander Kukushkin)

パスワードが拒否された場合、またはログ記録が冗長に構成されているか、まったく構成されていない場合、パスワードが postgres ログに書き込まれる可能性があります。これを回避するために、Patroni は、ユーザーの作成/更新を試行する前に、`log_statement`、`log_min_duration_statement`、および `log_min_error_statement` を安全な値に変更します。

**バグ修正**

- カスケード レプリカで [standby_cluster](/ja/patroni/standby_cluster#standby_cluster) 構成の `restore_command` を使用します (Alexander Kukushkin)

`standby_leader` は、この機能が存在した当初からすでに実行していました。レプリカで同じことを行わないと、スタンバイ リーダーに追いつけなくなる可能性があります。

- スタンバイ クラスターによって報告される更新タイムライン (Alexander Kukushkin)

タイムライン切り替えの場合、スタンバイ クラスターはプライマリーから正しくレプリケートしていましたが、[patronictl](/ja/patroni/patronictl#patronictl) は古いタイムラインを報告していました。

- custom_conf で特定の回復パラメータを定義できるようにしました。 (Alexander Kukushkin)

レプリカでリカバリ パラメータの検証を行うとき、Patroni は、`archive_cleanup_command`、`promote_trigger_file`、`recovery_end_command`、`recovery_min_apply_delay`、および `restore_command` が Patroni 構成ではなく、`postgresql.auto.conf` または `postgresql.conf` 以外のファイルで定義されている場合、それらをスキップします。

- 名前にピリオドが含まれる PostgreSQL パラメータの処理を改善しました。 (Alexander Kukushkin)

このようなパラメーターは、単位が必ずしも文字列であるとは限らない拡張機能によって定義できます。値を変更すると、再起動が必要になる場合があります (`pg_stat_statements.max` など)。

- シャットダウン時の例外処理を改善しました (Alexander Kukushkin)

シャットダウン中、Patroni は DCS 内のステータスを更新しようとします。 DCS にアクセスできない場合は、例外が発生する可能性があります。例外処理が不足しているため、ロガー スレッドが停止できませんでした。

--------

## バージョン 1.6.3 {#version-163}

2019-12-05 をリリース

**バグ修正**

- `pg_rewind` の実行時にパスワードを公開しないでください (Alexander Kukushkin)

[\#1301](https://github.com/patroni/patroni/pull/1301) でバグが導入されました

- `postgresql.authentication` で指定された接続パラメータを `pg_basebackup` に適用し、カスタム レプリカ作成メソッドを適用します (Alexander Kukushkin)

URL のような接続文字列に依存していたため、パラメーターは適用されませんでした。

--------

## バージョン 1.6.2 {#version-162}

2019-12-05 をリリース

**新機能**

- 実装 `patroni --version` (Igor Yanchenko)

Patroni の現在のバージョンを出力して終了します。

- すべての http リクエストに `user-agent` http ヘッダーを設定します (Alexander Kukushkin)

Patroni は、http プロトコルを介して Consul、etcd、および Kubernetes API と通信しています。特別に作成された `user-agent` (例: `Patroni/1.6.2 Python/3.6.8 Linux`) を使用すると、デバッグや監視に役立つ場合があります。

- 例外トレースバックのログレベルを設定できるようにしました。 (Igor Yanchenko)

`log.traceback_level=DEBUG` を設定すると、トレースバックは `log.level=DEBUG` の場合にのみ表示されます。デフォルトの動作は変わりません。

**安定性の向上**

- 構成ファイルで必要なモジュールを検索するときに、すべての DCS モジュールをインポートしないようにしました。 (Alexander Kukushkin)

たとえば、必要なだけの場合は、etcd、Consul、および Kubernetes のモジュールをインポートする必要はありません。動物園の飼育員。これはメモリ使用量を削減し、INFO メッセージ `Failed to import smth` の問題を解決します。

- Python `requests` モジュールを明示的な要件から削除しました (Alexander Kukushkin)

これは重要なことには使用されませんでしたが、`urllib3` の新しいバージョンがリリースされると多くの問題を引き起こしました。

- YAML 配列ではなくコンマ区切り文字列として記述された `etcd.hosts` の処理を改善しました。 (Igor Yanchenko)

以前は、`host1:port1, host2:port2` (カンマの後のスペース文字) 形式で記述すると失敗していました。

**ユーザビリティの向上**

- [patronictl](/ja/patroni/patronictl#patronictl) の空のリストからメンバーを選択することをユーザーに強制しないでください (Igor Yanchenko)

ユーザーが間違ったクラスター名を指定した場合、空のリストからメンバーを選択するように求めるのではなく、例外が発生します。

- REST API がバインドできない場合のエラー メッセージをさらにわかりやすくしました。 (Igor Yanchenko)

経験の浅いユーザーにとって、Python スタックトレースから何が問題なのかを特定するのは難しいかもしれません。

**バグ修正**

- `wal_buffers` の計算を修正しました (Alexander Kukushkin)

基本単位が 8 kB ブロックから PostgreSQL 11 のバイトに変更されました。

- PostgreSQL 10+ でのみ `primary_conninfo` の `passfile` を使用する (Alexander Kukushkin)

最新バージョンの `libpq` がインストールされていない限り、古いバージョンでは `passfile` が動作する保証はありません。

--------

## バージョン 1.6.1 {#version-161}

2019-11-15 をリリース

**新機能**

- `PATRONICTL_CONFIG_FILE` 環境変数を追加しました (msvechla)

これにより、環境から [patronictl](/ja/patroni/patronictl#patronictl) の `--config-file` 引数を構成できるようになります。

- `patronictl history` の実装 (Alexander Kukushkin)

フェイルオーバー/スイッチオーバーの履歴が表示されます。

- `pg_rewind` を実行するときに `PGOPTIONS` で `-c statement_timeout=0` を渡します (Alexander Kukushkin)

これは、サーバー上の `statement_timeout` が小さな値に設定され、pg_rewind によって実行されたステートメントの 1 つがキャンセルされた場合から保護します。

- PostgreSQL 構成でより低い値を許可する (Soulou)

Patroni では、一部の PostgreSQL 構成パラメーターをハードコードされた値よりも小さく設定することができませんでした。許容される最小値が小さくなり、デフォルト値は変更されていません。

- 証明書ベースの認証を許可する (Jonathan S. Katz)

この機能により、スーパーユーザー、レプリケーション、リワインド アカウントの証明書ベースの認証が有効になり、ユーザーは接続する `sslmode` を指定できるようになります。

- パスワードの代わりに `primary_conninfo` の `passfile` を使用します (Alexander Kukushkin)

postgresql.conf に対する `600` 権限の設定を回避できます。

- 構成の変更に関係なく `pg_ctl reload` を実行します (Alexander Kukushkin)

一部の構成ファイルが Patroni によって制御されていない可能性があります。誰かが REST API を介して、または SIGHUP を Patroni プロセスに送信することによってリロードを実行している場合、通常は Postgres もリロードされることが期待されます。以前は、Patroni 構成の `postgresql` セクションに変更がない場合にはこの問題は発生しませんでした。

- `primary_conninfo` だけでなく、すべての回復パラメーターを比較します (Alexander Kukushkin)

以前は、`check_recovery_conf()` メソッドは `primary_conninfo` が変更されたかどうかのみをチェックしており、他のすべての回復パラメーターは考慮されていませんでした。

- 再起動せずにいくつかの回復パラメーターを適用できるようにしました (Alexander Kukushkin)

PostgreSQL 12 以降、`archive_cleanup_command`、`promote_trigger_file`、`recovery_end_command`、および `recovery_min_apply_delay` のリカバリ パラメーターは再起動せずに変更できます。将来の Postgres リリースでは、このリストが拡張され、Patroni が自動的にサポートする予定です。

- `use_slots` をオンラインで変更できるようにします (Alexander Kukushkin)

以前は、Patroni を再起動し、スロットを手動で削除する必要がありました。

- Postgres の起動時に、`PATRONI_` 接頭辞が付いた環境変数のみを削除します (Cody Coons)

これにより、さまざまな外部データ ラッパーの実行に関する多くの問題が解決されます。

**安定性の向上**

- K8 を使用する場合は LIST + WATCH を使用してください API (Alexander Kukushkin)

これにより、オブジェクトの変更 (ポッド、エンドポイント/構成マップ) を効率的に受信できるようになり、K8 マスター ノードのストレスが軽減されます。

- ブートストラップ中に PGDATA が空でない場合のワークフローを改善しました。 (Alexander Kukushkin)

`initdb` ソース コードによると、`lost+found` と `.dotfiles` のみが存在する場合、PGDATA は空であると見なされる可能性があります。 Patroni も同じことを行います。 `PGDATA` が空ではなく、同時に `pg_controldata` の観点から無効な場合、Patroni はエラーを出して終了します。

- すべての HA ループで高価な `os.listdir()` を呼び出すのを避けてください。 (Alexander Kukushkin)

システムが IO ストレスにさらされている場合、`os.listdir()` の実行に数秒 (または数分) かかる可能性があり、Patroni の HA ループに悪影響を及ぼします。これにより、更新がないためにリーダー キーが DCS から消える可能性もあります。 PGDATA が空でないことを確認する、より優れた、より安価な方法があります。ここで、PGDATA に `global/pg_control` ファイルが存在するかどうかを確認します。

- ロギングインフラストラクチャのいくつかの改善 (Alexander Kukushkin)

以前は、ログ スレッドが `daemon` スレッドであったため、シャットダウン時に最後の数行のログが失われる可能性がありました。

- Python で `spawn` マルチプロセッシング開始メソッドを使用する 3.4+ (Maciej Kowalczyk)

Python の [問題](https://bugs.python.org/issue6721) では、スレッド化とマルチプロセッシングがうまく組み合わせられないことが知られています。デフォルトのメソッド `fork` から `spawn` に切り替えることが推奨される回避策です。そうしないと、Postgres が実際には稼働しているにもかかわらず、ポストマスターの開始プロセスがハングし、Patroni が無期限に `INFO: restarting after failure in progress` を報告する可能性があります。

**REST API の改善**

- REST API でクライアント証明書を確認できるようにしました (Alexander Kukushkin)

`verify_client` が `required` に設定されている場合、Patroni はすべての REST API 呼び出しのクライアント証明書をチェックします。 `optional` に設定すると、クライアント証明書ですべての安全でない REST API エンドポイントがチェックされます。

- Postgres が実行されていない場合、`GET /replica` ヘルス チェック リクエストの応答コード 503 を返します。 (Alexander Anikin)

Postgres は、クライアント接続の受け入れを開始するまでの回復にかなりの時間を費やす可能性があります。

- `/history` および `/cluster` エンドポイントを実装する (Alexander Kukushkin)

`/history` エンドポイントは、DCS の `history` キーの内容を表示します。 `/cluster` エンドポイントには、すべてのクラスター メンバーと、保留中およびスケジュールされた再起動やスイッチオーバーなどのサービス情報が表示されます。

**etcd サポートの改善**

- Etcd での再試行 RAFT 内部エラー (Alexander Kukushkin)

etcd ノードがシャットダウンされると、`response code=300, data='etcdserver: server stopped'` が送信されます。これにより、Patroni がプライマリーを降格させていました。

- Etcd リクエストの再試行を早すぎて諦めないでください (Alexander Kukushkin)

ネットワークに問題が発生すると、Patroni はすぐに etcd ノードのリストを使い果たし、`retry_timeout` 全体を使用せずに諦めてしまい、プライマリーが降格される可能性がありました。

**バグ修正**

- `pg_rewind` ユーザーに実行権限を付与するときに `synchronous_commit` を無効にする (kremius)

ブートストラップが `synchronous_mode_strict: true` で行われる場合、非同期ノードが使用可能なため、`GRANT EXECUTE` ステートメントは無期限に待機していました。

- Python のメモリ リークを修正 3.7 (Alexander Kukushkin)

Patroni は `ThreadingMixIn` を使用して REST API リクエストを処理し、Python 3.7 はデフォルトで非デーモンリクエストごとにスレッドを生成します。

- 非同期アクションの競合状態を修正しました (Alexander Kukushkin)

停止した Postgres を回復しようとすると、`patronictl reinit --force` が上書きされる可能性がありました。これにより、basebackup の実行中に Patroni が Postgres を開始しようとしたという状況が発生しました。

- `postmaster_start_time()` メソッドの競合状態を修正しました (Alexander Kukushkin)

メソッドが REST API スレッドから実行される場合は、別のカーソル オブジェクトを作成する必要があります。

- 名前に大文字が含まれている同期スタンバイが昇格されない問題を修正しました。 (Alexander Kukushkin)

Postgres が `application_name` と `synchronous_standby_names` の値を比較するときに同じことを行っていたため、名前を小文字に変換しました。

- 新しいプロセスを開始する前に、コールバックプロセスとともにすべての子を強制終了します。 (Alexander Kukushkin)

そうしないと、bash でコールバックを実装することが難しくなり、最終的に 2 つのコールバックが同時に実行される状況が発生する可能性があります。

- 「起動に失敗しました」問題を修正しました (Alexander Kukushkin)

特定の条件下では、Postgres が稼働しているにもかかわらず、Postgres 状態が「開始失敗」に設定されることがあります。

--------

## バージョン 1.6.0 {#version-160}

2019-08-05 をリリース

このバージョンでは、PostgreSQL 12 との互換性が追加され、PostgreSQL 11 以降でスーパーユーザーなしで pg_rewind を実行できるようになり、IPv6 サポートが有効になります。

**新機能**

- Psycopg2 は要件から削除されたため、個別にインストールする必要があります。 (Alexander Kukushkin)

2.8.0 から、`psycopg2` は `psycopg2` と `psycopg2-binary` という 2 つの異なるパッケージに分割され、ファイル システム上の同じ場所に同時にインストールできるようになりました。依存関係による地獄の問題を減らすために、ユーザーがインストール方法を選択できるようにしました。利用可能なオプションがいくつかあります。[ドキュメント](/ja/patroni/installation#psycopg2_install_options) を参照してください。

- PostgreSQL 12 との互換性 (Alexander Kukushkin)

PostgreSQL 12 以降、`recovery.conf` はなくなり、以前のすべての回復パラメーターは [GUC](https://www.enterprisedb.com/blog/what-guc-variable) に変換されます。 `ALTER SYSTEM SET primary_conninfo` などから保護するために、Patroni は `postgresql.auto.conf` を解析し、そこからすべてのスタンバイ パラメーターとリカバリ パラメーターを削除します。 Patroni 構成には下位互換性が維持されます。たとえば、`restore_command` が GUC であるにもかかわらず、`postgresql.recovery_conf.restore_command` セクションで指定することができ、Patroni はそれを PostgreSQL 12 の `postgresql.conf` に書き込みます。

- PostgreSQL 11 以降でスーパーユーザーなしで `pg_rewind` を使用できるようにします (Alexander Kukushkin)

この機能を使用したい場合は、Patroni 構成ファイルの `postgresql.authentication.rewind` セクションで `username` および `password` を定義してください。既存のクラスターの場合は、ユーザーを手動で作成し、いくつかの機能に対する `GRANT EXECUTE` 権限を作成する必要があります。詳細については、PostgreSQL [ドキュメント](https://www.postgresql.org/docs/11/app-pgrewind.html#id-1.9.5.8.8) を参照してください。

- レプリカの実際の`primary_conninfo`と設定したい値を適切に比較するようにしました（Alexander Kukushkin）。

既存のプライマリー/スタンバイ クラスターを Patroni によって管理されるクラスターに変換するときに、レプリカの再起動を回避できる場合があります。

- IPv6 サポート (Alexander Kukushkin)

大きな問題が 2 つありました。 Patroni REST API サービスは `0.0.0.0` でのみリッスンしており、`api_url` と `conn_url` で使用される IPv6 IP アドレスは正しく引用されていませんでした。

- Kerberos サポート (Ajith Vilas、Alexander Kukushkin)

Patroni 構成ファイルでパスワードを定義する代わりに、Postgres ノード間で Kerberos 認証を使用できるようになります。

- `pg_ident.conf` の管理 (Alexander Kukushkin)

この機能は `pg_hba.conf` と同様に機能します。`postgresql.pg_ident` が構成ファイルまたは DCS で定義されている場合、Patroni はその値を `pg_ident.conf` に書き込みますが、`postgresql.parameters.ident_file` が定義されている場合、Patroni は `pg_ident` が外部から管理されているものとみなし、ファイルを更新しません。

**REST API の改善**

- `/health` エンドポイントを追加しました (Wilfried Roset)

PostgreSQL が実行されている場合にのみ、HTTP ステータス コードを返します。

- `/read-only` および `/read-write` エンドポイントを追加しました (Julien Riou)

`/read-only` エンドポイントにより、レプリカとプライマリー間で読み取りのバランスがとれます。 `/read-write` エンドポイントは、`/primary`、`/leader`、および `/master` のエイリアスです。

- `SSLContext` を使用して、REST API ソケットをラップします。 (Julien Riou)

`ssl.wrap_socket()` の使用は非推奨になりましたが、TLS 1.1 など、間もなく非推奨となるプロトコルもまだ許可されていました。

**ロギングの改善**

- 2 ステップ ロギング (Alexander Kukushkin)

すべてのログ メッセージは、最初にメモリ内のキューに書き込まれ、その後、別のスレッドから stderr またはファイルに非同期的にフラッシュされます。最大キュー サイズは制限されています (構成可能)。制限に達すると、Patroni はログを失い始めますが、HA ループをブロックするよりはまだマシです。

- GET/OPTIONS API 呼び出しとレイテンシのデバッグ ログを有効にします (Jan Tomsa)

これは、HAProxy、Consul、またはどのノードがプライマリー/レプリカであるかを決定するその他のツールによって実行されるヘルスチェックのデバッグに役立ちます。

- 再試行でキャッチされた例外をログに記録しました (Daniel Kucera)

試行回数またはタイムアウトに達したときの最後の例外をログに記録します。 DCS への通信が失敗した場合に、いくつかの問題をデバッグするのに役立つことが期待されます。

**patronictlの改善**

- スケジュールされたスイッチオーバーと再起動のためのダイアログを強化しました (Rafia Sabih)

以前のダイアログでは、スケジュールされたアクションが考慮されていなかったため、誤解を招く恐れがありました。

- 設定ファイルが存在するかどうかを確認します (Wilfried Roset)

指定されたファイル名が存在しない場合は、黙って無視するのではなく (誤解を招く可能性があります)、構成ファイルについて詳しく説明してください。

- `EDITOR` のフォールバック値を追加 (Wilfried Roset)

`EDITOR` 環境変数が定義されていない場合、`patronictl edit-config` は `PatroniCtlException` で失敗していました。新しい戦略は、ほとんどのシステムで利用できる `vi` ではなく `editor` を試すことです。

**Consul サポートの改善**

- Consul 整合性モードの指定を許可します (Jan Tomsa)

整合性モード [ここで](https://www.consul.io/api/features/consistency.html) の詳細については、こちらをご覧ください。

- SIGHUP で Consul 設定を再ロード (Cameron Daniel Kucera、Alexander Kukushkin)

これは、誰かが `token` の値を変更する場合に特に便利です。

**バグ修正**

- スイッチオーバー/フェイルオーバーの特殊なケースを修正しました (Sharoon Thomas)

REST API にアクセスできず、フォールバックとして DCS を使用している場合、変数 `scheduled_at` は未定義である可能性があります。

- カスタム ブートストラップ中に `pg_hba.conf` でローカルホストへの信頼をオープンします (Alexander Kukushkin)

以前は unix_socket に対してのみ開かれていたため、多くのエラーが発生していました: `FATAL:  no pg_hba.conf entry for replication connection from host "127.0.0.1", user "replicator"`

- 前のリーダーが先行している場合でも、同期ノードは健全であるとみなします (Alexander Kukushkin)

プライマリーが DCS へのアクセスを失った場合、Postgres を読み取り専用で再起動しますが、他のノードが REST API を介して古いプライマリーに依然としてアクセスできる可能性があります。このような状況により、古いプライマリーが同期スタンバイよりも前の WAL 位置を報告していたため、同期スタンバイが昇格しませんでした。

- スタンバイ クラスターのバグ修正 (Alexander Kukushkin)

standby_leader にアクセスできない場合にスタンバイ クラスターでレプリカをブートストラップできるようにするほか、いくつかのマイナーな修正を加えました。

--------

## バージョン 1.5.6 {#version-156}

2019-08-03 をリリース

**新機能**

- Support はプロキシのセットを介して etcd クラスターと連携します (Alexander Kukushkin)

etcd クラスターに直接アクセスできず、プロキシのセットを介してアクセスできない場合があります。この場合、Patroni は etcd トポロジ検出を実行せず、プロキシ ホストを介したラウンドロビンのみを実行します。動作は `etcd.use_proxies` によって制御されます。

- ノード上のロールが変更されたときのコールバックの動作が変更されました。 (Alexander Kukushkin)

ロールが `master` または `standby_leader` から `replica` に、または `replica` から `standby_leader` に変更された場合、`on_restart` コールバックは呼び出されなくなり、`on_role_change` コールバックが優先されます。

- postgres の起動方法を変更する (Alexander Kukushkin)

それ自体を実行する代わりに `multiprocessing.Process` を使用し、`multiprocessing.Pipe` を使用してポストマスター PID を Patroni プロセスに送信します。その前はパイプを使用していて、stdin が閉じられた状態でポストマスター プロセスを終了していました。

**バグ修正**

- スタンバイ リーダーの REST API によって返された役割を修正 (Alexander Kukushkin)

`standby_leader` ではなく、誤って `replica` を返していました。

- コールバックを強制終了できなかった場合は終了を待ちます。 (Julien Tachoires)

Patroni には、新しいコールバックをキャンセルしていた `sudo` で実行されているコールバック スクリプトを終了するのに十分な権限がありません。実行中のスクリプトを強制終了できなかった場合、Patroni は終了するまで待機し、次のコールバックを実行します。

- dcs.get_cluster メソッドにかかるロック時間を短縮しました (Alexander Kukushkin)

ロックが保持されているため、DCS の遅延が REST API ヘルス チェックに影響し、誤検知が発生していました。

- `pg_wal`/\`pg_xlog\` がシンボリックリンクである場合の PGDATA のクリーニングを改善しました。 (Julien Tachoires)

この場合、Patroni はターゲット ディレクトリからファイルを明示的に削除します。

- os.path.relpath の不要な使用を削除します (Ants Aasma)

それは、作業ディレクトリを解決できるかどうか、後でファイルシステムからリンクが解除されたディレクトリで Patroni が開始された場合に何が失敗するかによって決まります。

- Etcd と通信するときに SSL バージョンを強制しません。 (Alexander Kukushkin)

何らかの理由で、debian および ubuntu の python3-etcd はパッケージの最新バージョンに基づいていないため、etcd v3 でサポートされていない TLSv1 を強制します。この問題は Patroni 側で解決しました。

--------

## バージョン 1.5.5 {#version-155}

2019-02-15 をリリース

このバージョンでは、以前のマスターの自動再初期化の可能性が導入され、patronictl リストの出力が改善され、多くのバグが修正されています。

**新機能**

- `PATRONI_ETCD_PROTOCOL`、`PATRONI_ETCD_USERNAME`、`PATRONI_ETCD_PASSWORD` 環境変数のサポートを追加しました (Étienne M)

以前は、構成ファイル内でのみ、または `PATRONI_ETCD_URL` の一部としてのみ構成できましたが、必ずしも便利ではありませんでした。

- 以前のマスターを自動的に再初期化できるようにしました (Alexander Kukushkin)

pg_rewind が無効になっているか使用できない場合、タイムラインが分岐するため、元のマスターが新しいレプリカとして起動できない可能性があります。この場合、それを修正する唯一の方法は、データ ディレクトリを消去して再初期化することです。この動作は、`postgresql.remove_data_directory_on_diverged_timelines` を設定することで変更できます。これが設定されると、Patroni はデータ ディレクトリを消去し、元のマスターを自動的に再初期化します。

- patronictl リストのタイムラインに関する情報を表示 (Alexander Kukushkin)

古いレプリカを検出するのに役立ちます。それに加えて、ポート値がデフォルトでない場合、または同じホスト上で複数のメンバーが実行されている場合、`Host` には「:{port}」が含まれます。

- \$SCOPE-config エンドポイントに関連付けられたヘッドレス サービスを作成します (Alexander Kukushkin)

"config" エンドポイントは、クラスター全体の Patroni および Postgres 構成、履歴ファイル、そして最後に最も重要な `initialize` キーに関する情報を保持します。 Kubernetes マスター ノードが再起動またはアップグレードされると、サービスのないエンドポイントが削除されます。ヘッドレス サービスにより、削除されなくなります。

**バグ修正**

- リーダー監視ブロッキングクエリーの読み取りタイムアウトを調整しました。 (Alexander Kukushkin)

Consul ドキュメントによると、実際の応答タイムアウトは、同時要求のウェイクアップ時間を分散するために、指定された最大待機時間にランダムな少量の追加待機時間を加えることによって増加します。最大 `wait / 16` 時間の追加時間が最大期間に追加されます。この場合、どちらが大きいかに応じて、`wait / 15` または 1 を 2 番目に追加します。

- レプリケーション プロトコル経由で postgres に接続する場合は、常に replication=1 を使用します。 (Alexander Kukushkin)

Postgres 10 以降、pg_hba.conf の database=replication を含む行は、パラメーター replication=database を使用した接続を受け入れません。

- WAL 専用スタンバイ クラスターの場合は、primary_conninfo を recovery.conf に書き込まないでください。 (Alexander Kukushkin)

[standby_cluster](/ja/patroni/standby_cluster#standby_cluster) 構成で `host` も `port` も定義されていないにもかかわらず、Patroni は `primary_conninfo` を `recovery.conf` に入れていましたが、これは役に立たず、多くのエラーを生成していました。

--------

## バージョン 1.5.4 {#version-154}

2019-01-15 をリリース

このバージョンでは、柔軟なロギングが実装され、多くのバグが修正されています。

**新機能**

- ロギング インフラストラクチャの改善 (Alexander Kukushkin、Lucas Capistrant、Alexander Anikin)

ロギング構成は、環境変数からだけでなく、Patroni 構成ファイルからも構成できます。構成を更新してリロードを実行するか、SIGHUP を Patroni プロセスに送信することで、実行時にロギング構成を変更できるようになります。デフォルトでは、Patroni はログを stderr に書き込みますが、ログをファイルに直接書き込み、特定のサイズに達したときにローテーションすることが可能になりました。これに加えて、カスタム日付形式のサポートと、各 Python モジュールのログ レベルを微調整する機能が追加されました。

- リーダー選挙中に現在のタイムラインを考慮できるようにします (Alexander Kukushkin)

現在、既知の最新のタイムラインに載っていないにもかかわらず、ノードが自身を最も健全なノードであるとみなしている可能性があります。場合によっては、そのようなノードの昇格を避けたいことがあります。これは、`check_timeline` パラメーターを `true` に設定することで実現できます (デフォルトの動作は変更されません)。

- スーパーユーザー資格情報の要件の緩和

Libpq を使用すると、ユーザー名もパスワードも明示的に指定せずに接続を開くことができます。状況に応じて、pgpass ファイルまたは pg_hba.conf の信頼認証方法のいずれかに依存します。 pg_rewind も libpq を使用しているため、同じように動作します。

- Consul 環境変数を介してサービス登録とチェック間隔を設定できる機能を実装しました (Alexander Kukushkin)

Consul でのサービスの登録は 1.5.0 に追加されましたが、これまでは patroni.yaml を介してのみ有効にすることができました。

**安定性の向上**

- カスタム ブートストラップ中に archive_mode をオフに設定します (Alexander Kukushkin)

クラスターが完全に機能するまでは、WAL と履歴ファイルのアーカイブは避けたいと考えています。カスタム ブートストラップに pg_upgrade が含まれる場合、これは非常に役立ちます。

- 起動時にグローバル設定をロードするときに 5 秒のバックオフを適用します (Alexander Kukushkin)

Patroni の起動時に DCS が実行されるのを避けるのに役立ちます。

- シャットダウン時に生成されるエラー メッセージの量を削減しました (Alexander Kukushkin)

それらは無害ですが、かなり迷惑で、時には恐ろしいものでした。

- 作成時に recovery.conf の rw 権限を明示的に保護します (Lucas Capistrant)

このファイルにはレプリケーション ユーザーとパスワードが含まれているため、Patroni/postgres ユーザー以外にはこのファイルを読まないでください。

- HTTPServer 例外をロガーにリダイレクトしました (Julien Riou)

デフォルトでは、このような例外は通常のログを混乱させて標準出力に記録されていました。

**バグ修正**

- pg_ctl プロセスの stdout への stderr パイプを削除しました (Cody Coons)

メインの Patroni プロセスから stderr を継承すると、すべての Postgres ログをすべての Patroni ログとともに表示できるようになります。 Patroni および Postgres ログは標準ツール (docker ログ、kubectl など) を使用して使用できるため、これはコンテナー環境で非常に役立ちます。それに加えて、この変更により、postgres がいくつかの警告を標準エラー出力に書き込むときに Patroni がポストマスター PID をキャッチできないというバグが修正されます。

- Consul サービス チェック登録解除タイムアウトを Go 時間形式で設定します (Pavel Kirillov)

明示的に言及されていない限り、時間単位の登録は失敗していました。

- standby_cluster クラスター構成のチェックを緩める (Dmitry Dolgov、Alexander Kukushkin)

有効な値として文字列のみを受け入れていたため、ポートを整数として指定したり、create_replica_methods をリストとして指定したりすることはできませんでした。

--------

## バージョン 1.5.3 {#version-153}

2018-12-03 をリリース

互換性とバグ修正のリリース。

- 動物園飼育員に対して Python3 を使用して実行するときの安定性が向上しました (Alexander Kukushkin)

`loop_wait` の変更により、Patroni が Zookeeper から切断され、再接続できなくなりました。

- postgres との壊れた互換性を修正しました 9.3 (Alexander Kukushkin)

9.3 は replication='database' を理解できないため、レプリケーション接続を開くときは、replication=1 を指定する必要があります。

- HA ループごとに少なくとも 1 回は Consul セッションを更新し、領事セッション例外の処理を改善しました。 (Alexander Kukushkin)

ローカル領事エージェントを再起動すると、ノードに関連するすべてのセッションが無効になります。セッション更新を時間通りに呼び出さず、セッション エラーを適切に処理しなかったことが、プライマリーの降格を引き起こしていました。

--------

## バージョン 1.5.2 {#version-152}

2018-11-26 をリリース

互換性とバグ修正のリリース。

- kazoo-2.6.0 との互換性 (Alexander Kukushkin)

リクエストが適切なタイムアウトで実行されることを確認するために、Patroni は python-kazoo モジュールの create_connection メソッドを再定義します。 kazoo の最後のリリースでは、create_connection メソッドの呼び出し方法が少し変更されました。

- Consul クラスターがリーダーを失った場合の Patroni クラッシュを修正しました。 (Alexander Kukushkin)

クラッシュは touch_member メソッドの不正な実装が原因で発生していました。これはブール値を返し、例外は発生しません。

--------

## バージョン 1.5.1 {#version-151}

2018-11-01 をリリース

このバージョンでは、永続的なレプリケーション スロットのサポートが実装され、pgBackRest のサポートが追加され、いくつかのバグが修正されています。

**新機能**

- 永続レプリケーション スロット (Alexander Kukushkin)

永続的なレプリケーション スロットはフェイルオーバー/スイッチオーバーでも保持されます。つまり、新しいプライマリー上の Patroni は、プロモートの実行直後に構成済みのレプリケーション スロットを作成します。スロットは `patronictl edit-config` を使用して構成できます。初期設定は [ブートストラップ.dcs](/ja/patroni/config/yaml#yaml) で行うこともできます。

- pgbackrest サポートを追加 (Yogesh Sharma)

pgBackrest は既存の \$PGDATA フォルダーに復元できます。これにより、最後のバックアップ以降変更されていないファイルがスキップされるため、迅速な復元が可能になります。この機能をサポートするために、新しいパラメーター `keep_data` が導入されました。追加の例については、[レプリカ作成方法](/ja/patroni/replica_bootstrap#custom_replica_creation) セクションを参照してください。

**バグ修正**

- 「スタンバイ クラスター」ワークフローのいくつかのバグ修正 (Alexander Kukushkin)

詳細については、<https://github.com/patroni/patroni/pull/823> を参照してください。

- クラスター管理が一時停止され、DCS にアクセスできない場合の REST API ヘルスチェックを修正しました。 (Alexander Kukushkin)

回帰は <https://github.com/patroni/patroni/commit/90cf930036a9d5249265af15d2b787ec7517cf57> で導入されました

--------

## バージョン 1.5.0 {#version-150}

2018-09-20 をリリース

このバージョンでは、Patroni HA クラスターがスタンバイ モードで動作できるようにし、Windows での実行に対する実験的なサポートが導入され、Consul に PostgreSQL サービスを登録するための新しい構成パラメーターが提供されます。

**新機能**

- スタンバイ クラスター (Dmitry Dolgov)

1 つ以上の Patroni ノードは、プライマリー クラスターと並行して (つまり、別のデータセンター内で) 実行されるスタンバイ クラスターを形成でき、プライマリー クラスターのマスターから複製するスタンバイ ノードで構成されます。スタンバイ クラスター内のすべての PostgreSQL ノードはレプリカです。これらのレプリカの 1 つはリモート マスターから直接レプリケートすることを選択し、他のレプリカはカスケード方式でリモート マスターからレプリケートします。この機能の詳細な説明といくつかの構成例については、[ここで](/ja/patroni/standby_cluster#standby_cluster) を参照してください。

- Consul にサービスを登録する (Pavel Kirillov、Alexander Kukushkin)

コンスル [構成](/ja/patroni/config/yaml#consul_settings) の `register_service` パラメーターが有効な場合、ノードは `scope` という名前と `master`、`replica`、または `standby-leader` のタグを持つサービスを登録します。

- 実験的 Windows サポート (Pavel Golub)

今後、Patroni を Windows で実行できるようになりますが、Windows のサポートは新しく、対応する Linux ほど実際のテストは受けていません。フィードバックをお待ちしております。

**patronictlの改善**

- patronictl -k/--insecure フラグを追加し、restapi cert をサポートしました。 (Wilfried Roset)

以前は、REST API が自己署名証明書によって保護されていた場合、[patronictl](/ja/patroni/patronictl#patronictl) はそれらを検証できませんでした。その検証を無効にする方法はありませんでした。証明書検証を完全にスキップするように [patronictl](/ja/patroni/patronictl#patronictl) を構成したり、構成の [ctl:](/ja/patroni/config/yaml#patronictl_settings) セクションで CA とクライアント証明書を提供したりできるようになりました。

- patronictl スイッチオーバー/フェイルオーバー出力から nofailover タグを持つメンバーを除外します (Alexander Anikin)

以前は、patronictl を介して対話型スイッチオーバーまたはフェイルオーバーを実行するときに、これらのメンバーが候補として誤って提案されていました。

**安定性の向上**

- pg_controldata のキーと値以外の出力行を解析しないようにしました。 (Alexander Anikin)

特定の状況下では、pg_controldata はコロン文字のない行を出力します。これにより、pg_controldata 出力を解析する Patroni コードでエラーが発生し、実際の問題が隠蔽されてしまいます。多くの場合、このような行は、通常の出力の前に、つまりバイナリのメジャー バージョンが PostgreSQL データ ディレクトリのバージョンと一致しない場合に、pg_controldata によって示される警告として出力されます。

- リーダー選挙中のエラー メッセージにメンバー名を追加しました (Jan Mussler)

リーダーの選出中、Patroni はクラスターのすべての既知のメンバーに接続し、そのステータスを要求します。このようなステータスは Patroni ログに書き込まれ、メンバーの名前も含まれます。以前は、メンバーにアクセスできない場合、エラー メッセージにはその名前が示されず、URL のみが含まれていました。

- レプリケーション スロットの作成時に WAL 位置をすぐに予約します (Alexander Kukushkin)

9.6 以降、`pg_create_physical_replication_slot` 関数は追加のブール値パラメーター `immediately_reserve` を提供します。これがデフォルトでもある `false` に設定されている場合、スロットは最初のクライアント接続を受信するまで WAL 位置を予約しないため、スロットの作成と最初のクライアント接続の間の時間枠でクライアントが必要とする一部のセグメントが失われる可能性があります。

- 厳密な同期レプリケーションのバグを修正しました。 (Alexander Kukushkin)

`synchronous_mode_strict: true` で実行すると、場合によっては、Patroni が `\*` を `synchronous_standby_names` に置き、ほとんどのレプリケーション接続の同期状態を `potential` に変更します。以前は、Patroni は、`async` 状態の同期候補のみを考慮するため、このような状況では同期候補を選択できませんでした。

--------

## バージョン 1.4.6 {#version-146}

2018-08-14 をリリース

**バグ修正と安定性の向上**

このリリースでは、非マスター ノードに対して Patroni API /master エンドポイントが 200 を返すという重大な問題が修正されています。これはレポートの問題であり、実際のスプリット ブレインではありませんが、特定の状況下ではクライアントが読み取り専用ノードに誘導される可能性があります。

- 降格時に is_leader ステータスをリセット (Alexander Kukushkin、Oleksii Kliukin)

降格されたクラスター メンバーが、/master API 呼び出しでコード 200 で応答を停止することを確認します。

- 新しい "cluster_unlocked" フィールドを API 出力に追加しました (Dmitry Dolgov)

このフィールドは、クラスターでマスターが実行されているかどうかを示します。これは、レプリカの 1 つ以外の他のノードをクエリーできない場合に使用できます。

--------

## バージョン 1.4.5 {#version-145}

2018-08-03 をリリース

**新機能**

- 新しい postgres 構成を適用する際のロギングを改善しました (Don Seiler)

Patroni は、変更されたパラメータ名と値をログに記録します。

- Python 3.7 の互換性 (Christoph Berg)

async は python3.7 の予約キーワードです。

- メンバーがシャットダウンされたときに、DCS の状態を "stopped" に設定します (Tony Sorrentino)

これにより、メンバーの状態が「patronictl list」コマンドの "stopped" として表示されます。

- 古いpostmaster.pidが実行中のプロセスと一致する場合に記録されるメッセージを改善しました（Ants Aasma）

前回のものは混乱を超えていました。

- patronictl リロード機能を実装します (Don Seiler)

それまでは、REST API を呼び出すか、SIGHUP シグナルを Patroni プロセスに送信することによってのみ構成をリロードできました。

- レプリカとして開始するときに制御データからいくつかのパラメーターを取得して適用します (Alexander Kukushkin)

グローバル構成で設定される `max_connections` およびその他のパラメーターの値は、プライマリーで実際に使用される値よりも低い場合があります。この問題が発生すると、レプリカは起動できないため、手動で修正する必要があります。 Patroni は、`pg_controldata` から値を読み取って適用し、postgres を起動して `pending_restart` フラグを設定することで、これを処理します。

- 設定されている場合、postgresの起動時にLD_LIBRARY_PATHを使用します。 (Chris Fraser)

Postgres を起動するとき、Patroni は、PATH、LC_ALL、および LANG 環境変数が設定されている場合はそれらを渡していました。現在は LD_LIBRARY_PATH でも同じことを行っています。誰かが PostgreSQL を標準以外の場所にインストールすると役立つはずです。

- create_replica_method の名前を create_replica_methods に変更しました。 (Dmitry Dolgov)

それが実際には配列であることを明確にするためです。下位互換性のために古い名前も引き続きサポートされています。

**バグ修正と安定性の向上**

- 一時停止状態の pg_rewind によるレプリカ起動の条件を修正しました (Oleksii Kliukin)

以前に pg_rewind を実行したレプリカを起動しないようにしてください。

- update_lock が成功した場合にのみ、200 をマスター ヘルスチェックに応答します。 (Alexander Kukushkin)

DCS がパーティション化されている場合、Patroni が以前の (降格された) マスター上のマスターを報告しないようにします。

- 新しい領事モジュールとの互換性を修正しました (Alexander Kukushkin)

v1.1.0 から、python-consul は内部 API を変更し、クエリー パラメーターを渡すために `dict` の代わりに `list` を使用し始めました。

- シャットダウン中に Patroni REST API スレッドからの例外をキャッチします (Alexander Kukushkin)

これらのキャッチされなかった例外により、シャットダウン時に PostgreSQL が実行され続けました。

- Postgres がマスターとして実行されている場合にのみクラッシュ回復を行うようにしました。 (Alexander Kukushkin)

`pg_controldata` が「運用中」、「シャットダウン中」、または「クラッシュ回復中」を報告することを要求します。それ以外の場合はすべて、クラッシュからの回復は必要ありません。

- 構成エラーの処理を改善しました (Henning Jacobs、Alexander Kukushkin)

Patroni 構成ファイルを更新し、SIGHUP を Patroni プロセスに送信することで、実行時に多くのパラメーター (`restapi.listen` を含む) を変更することができます。この修正により、一部のパラメーターが無効な値を受け取った場合に、'restapi' スレッドから不明瞭な例外が排除されます。

--------

## バージョン 1.4.4 {#version-144}

2018-05-22 をリリース

**安定性の向上**

- poll_failover_result の競合状態を修正しました (Alexander Kukushkin)

これはフェイルオーバーにもスイッチオーバーにも直接影響しませんでしたが、まれに、元のリーダーがロックを解放したときに成功を報告するのが早すぎて、「"desired-node" にフェイルオーバーしました」メッセージの代わりに「「なし」にフェイルオーバーしました」というメッセージが生成されることがありました。

- Postgres パラメータ名を大文字と小文字を区別しないように扱います。 (Alexander Kukushkin)

Postgres パラメーターのほとんどには、snake_case 名が付いていますが、この規則には DateStyle、IntervalStyle、TimeZone の 3 つの例外があります。 Postgres は、別のケース (例: timezone = 'some/tzn') で記述された場合、これらのパラメーターを受け入れます。ただし、Patroni は、pg_settings でこれらのパラメーター名の大文字と小文字を区別しない一致を見つけることができず、結果としてそのようなパラメーターを無視しました。

- 実行中のpostgresにアタッチし、クラスターが初期化されていない場合、開始を中止します。 (Alexander Kukushkin)

Patroni は、すでに実行中の Postgres インスタンスにそれ自体をアタッチできます。レプリカにアクセスする前に、マスター ノードで Patroni の実行を開始することが不可欠です。

- patronictl scaffold の動作を修正しました (Alexander Kukushkin)

JSON でエンコードされた文字列の代わりに dict オブジェクトを `touch_member` に渡します。 DCS 実装がエンコードを処理します。

- 一時停止中にリーダーキーの更新に失敗した場合にマスターを降格しません。 (Alexander Kukushkin)

メンテナンス中、DCS は読み取り要求には応答し続けながら、書き込み要求は失敗し始める可能性があります。この場合、Patroni は、DCS のリーダー ロックの更新に失敗した後、Postgres マスター ノードを読み取り専用モードに設定していました。

- Patroni が新しいポストマスター プロセスを認識したときにレプリケーション スロットを同期するようになりました。 (Alexander Kukushkin)

Postgres が再起動された場合、Patroni はレプリケーション スロットのリストが期待どおりであることを確認する必要があります。

- 一時停止から復帰した後に sysid を確認し、レプリケーション スロットを同期します (Alexander Kukushkin)

`maintenance` モード中に、データ ディレクトリが完全に書き換えられる可能性があるため、`Database system identifier` がまだクラスターに属しており、レプリケーション スロットが Patroni の期待と同期していることを確認する必要があります。

- ポストマスター ロック ファイルが存在するデータ ディレクトリで Postgres を実行しないと開始できない可能性がある問題を修正しました。 (Alexander Kukushkin)

ポストマスター ロック ファイルから PID の再利用を検出します。 Docker コンテナーで Patroni および Postgres を実行すると、このような問題が発生する可能性が高くなります。

- DCS が誤ってワイプされた場合の保護を強化しました (Alexander Kukushkin)

Patroni には、このような場合にフェイルオーバーを防ぐためのロジックが多数組み込まれています。すべてのキーを元に戻すこともできます。ただし、この変更が行われるまでは、/config キーを誤って削除すると、HA ループの 1 サイクルの一時停止モードがオフになっていました。

- 無効なシステムが発生した場合は終了しない ID (Oleksii Kliukin)

クラスター システム ID が空の場合、または検証チェックに合格しない場合は終了しないでください。その場合、クラスターの再初期化が必要になる可能性が高くなります。結果メッセージにそれを記載してください。 Patroni を終了しないでください。終了しないと再初期化が行われません。

**Kubernetes 1.10+ との互換性**

- 空のサブセットのチェックを追加しました (Cody Coons)

Kubernetes 1.10.0+ は、`\[\]` ではなく `None` に設定された `Endpoints.subsets` を返すようになりました。

**Bootstrap の改善**

- recovery.conf の削除をオプションにします (Brad Nicholson)

<span class="title-ref">bootstrap.\<custom_bootstrap_method_name\>.keep_existing_recovery_conf</span> が定義され、`True` に設定されている場合、Patroni は既存の `recovery.conf` ファイルを削除しません。これは、適切な `recovery.conf` を生成する pgBackRest などのツールを使用してバックアップからブートストラップする場合に便利です。

- basebackup 組み込みメソッドへのオプションを許可します (Oleksii Kliukin)

カスタム レプリカ作成メソッドの定義方法と同様に、構成内で `basebackup` セクションを定義することで、組み込みの Basebackup メソッドにオプションを提供できるようになりました。違いは、`basebackup` セクションで受け入れられる形式にあります。pg_basebackup は `--key=value` オプションと `--key` オプションの両方を受け入れるため、セクションの内容は、キーと値のペアの辞書、または 1 要素の辞書のリスト、またはキー (値を受け入れないオプションの場合) のいずれかになります。追加の例については、[レプリカ作成方法](/ja/patroni/replica_bootstrap#custom_replica_creation) セクションを参照してください。

--------

## バージョン 1.4.3 {#version-143}

2018-03-05 をリリース

**ロギングの改善**

- ログ レベルを環境変数から設定できるようにしました (Andy Newton、Keyvan Hedayati)

`PATRONI_LOGLEVEL` - 一般的なログ レベルを設定します。 `PATRONI_REQUESTS_LOGLEVEL` - すべての HTTP リクエストのログ レベルを設定します。 Kubernetes API 呼び出し 可能なログ レベルの名前を取得するには、<span class="title-ref">Python ロギング \<https://docs.python.org/3.6/library/logging.html#levels\></span> のドキュメントを参照してください。

**安定性の向上とバグ修正**

- 監視がタイムアウトしたときに etcd クラスター トポロジを再検出しないようにしました。 (Alexander Kukushkin)

etcd 構成にホストが 1 つだけあり、そのホストにアクセスできない場合、Patroni はクラスター トポロジの検出を開始しましたが、決して成功しませんでした。代わりに、次の利用可能なノードに切り替える必要があります。

- カスタム ブートストラップの後に bootstrap.pg_hba の内容を pg_hba.conf に書き込みます (Alexander Kukushkin)

`initdb` を使用した通常のブートストラップと同様に動作するようになりました。

- シングル ユーザー モードはユーザー入力を待機していて終了しませんでした (Alexander Kukushkin)

回帰は <https://github.com/patroni/patroni/pull/576> で導入されました

--------

## バージョン 1.4.2 {#version-142}

2018-01-30 をリリース

**patronictlの改善**

- スケジュールされたフェイルオーバーの名前をスケジュールされたスイッチオーバーに変更しました (Alexander Kukushkin)

フェイルオーバー機能とスイッチオーバー機能はバージョン 1.4 で分離されましたが、`patronictl list` は依然として `Scheduled switchover` ではなく `Scheduled failover` を報告していました。

- 保留中の再起動に関する情報を表示する (Alexander Kukushkin)

一部の構成変更を適用するには、postgres を再起動する必要がある場合があります。 Patroni は、REST API と、ノードのステータスを DCS に書き込むときに、すでにそのヒントを提供していましたが、それを表示する簡単な方法はありませんでした。

- show-config が設定ファイルのクラスター名で動作するようにしました。 (Alexander Kukushkin)

`patronictl edit-config` と同様に機能します。

**安定性の向上**

- ブートストラップ中に pg_controldata を呼び出さないようにします。 (Alexander Kukushkin)

initdb またはカスタム ブートストラップ中に、pgdata は空ではないが、pg_controldata がまだ書き込まれていない時間帯があります。このような場合、pg_controldata 呼び出しはエラー メッセージとともに失敗していました。

- psutil から発生した例外を処理するようになりました。 (Alexander Kukushkin)

cmdline は、`cmdline()` メソッドが呼び出されるたびに読み取られて解析されます。検査対象のプロセスがすでに消滅している場合もあり、その場合は `NoSuchProcess` が発生します。

**Kubernetes サポートの改善**

- k8s からのエラーを無視しないでください API (Alexander Kukushkin)

Kubernetes API の呼び出しは、さまざまな理由で失敗する可能性があります。場合によっては、そのような呼び出しを再試行する必要がありますが、他の場合には、エラー メッセージと例外スタック トレースを記録する必要があります。ここでの変更は、Kubernetes 権限の問題のデバッグに役立ちます。

- Kubernetes サンプル Dockerfile を更新して、マスター ブランチから Patroni をインストールします (Maciej Szulik)

それまでは `feature/k8s` を使用していましたが、これは時代遅れになりました。

- k8s で Patroni を実行するために適切な RBAC を追加しました (Maciej Szulik)

クラスターのポッドに割り当てられるサービス アカウント、必要な権限のみを保持するロール、およびサービス アカウントとロールを接続するロールバインディングを追加します。

--------

## バージョン 1.4.1 {#version-141}

2018-01-17 をリリース

**patronictl の修正**

- フェイルオーバー先のメンバーの推奨リストに現在のリーダーを表示しません。 （アレクサンダー・ククシュキン）

patronictl フェイルオーバーは、クラスター内にリーダーがある場合でも機能する可能性があるため、フェイルオーバー先のメンバーのリストから除外する必要があります。

- patronictl スイッチオーバーを古い Patroni API と互換性のあるものにします (Alexander Kukushkin)

POST /switchover REST API 呼び出しがステータス コード 501 で失敗した場合、/failover エンドポイントに対して再度実行されます。

--------

## バージョン 1.4 {#version-14}

2018-01-10 をリリース

このバージョンでは、Kubernetes を DCS として使用するためのサポートが追加されており、etcd、Zookeeper、または Consul を追加展開することなく、Kubernetes でクラウドネイティブ エージェントとして Patroni を実行できるようになります。

**アップグレードのお知らせ**

pip 経由で Patroni をインストールすると、(etcd、Zookeper、Consul または Kubernetes のライブラリ、または AWS のサポートなど) の依存関係が取り込まれなくなります。それらを有効にするには、`pip install patroni\[etcd,kubernetes\]` のように、pip install コマンドで明示的にリストする必要があります。

**Kubernetes のサポート**

Kubernetes ベースの DCS を実装します。エンドポイントのメタデータは、構成とリーダー キーを保存するために使用されます。ポッド定義内のメタデータ フィールドは、メンバー関連のデータを保存するために使用されます。エンドポイントの使用に加えて、Patroni は ConfigMaps をサポートします。この機能の詳細については、[ドキュメントの Kubernetes 章](/ja/patroni/kubernetes#kubernetes) を参照してください。

**安定性の向上**

- ポストマスタープロセスを別のオブジェクトに分解します (Ants Aasma)

このオブジェクトは、pid と開始時刻を介して実行中のポストマスター プロセスを識別し、ポストマスターが背後で再起動されたとき、または postgres ディレクトリがファイル システムから消えたときの状況の検出 (および解決) を簡素化します。

- HA サイクルの各ループで Patroni によって発行される SELECT の量を最小限に抑えます。 (Alexander Kukushkin)

HA ループの反復ごとに、Patroni はリカバリ ステータスと絶対壁位置を知る必要があります。今後、Patroni はこの情報を取得するために、レプリカ上で 2 つ、マスター上で 3 つではなく、単一の SELECT のみを実行します。

- ロックがある場合にのみ、シャットダウン時にリーダー キーを削除します (Ants Aasma)

無条件の削除により、不要で誤解を招く例外が生成されていました。

**patronictlの改善**

- patronictl にバージョン コマンドを追加 (Ants Aasma)

インストールされている Patroni のバージョンと、実行中の Patroni インスタンスのバージョン (クラスター名が指定されている場合) が表示されます。

- patronictl コマンドの一部で、cluster_name 引数をオプションで指定できるようにしました (Alexander Kukushkin、Ants Aasma)

patronictl が `scope` が定義された通常の Patroni 構成ファイルを使用している場合に機能します。

- スケジュールされたスイッチオーバーとメンテナンス モードに関する情報を表示します (Alexander Kukushkin)

それ以前は、この情報は Patroni ログから、または DCS から直接のみ取得できました。

- `patronictl reinit` を改善 (Alexander Kukushkin)

Patroni が他のアクション、つまり postgres を開始しようとしてビジー状態のときに、`patronictl reinit` が続行を拒否することがありました。 [patronictl](/ja/patroni/patronictl#patronictl) には、このような長時間実行アクションをキャンセルするコマンドが提供されておらず、唯一の (危険な) 回避策はデータ ディレクトリを手動で削除することでした。 `reinit` の新しい実装は、再初期化を続行する前に、他の長時間実行アクションを強制的にキャンセルします。

- `patronictl pause` および `patronictl resume` に `--wait` フラグを実装しました (Alexander Kukushkin)

要求されたアクションがクラスター内のすべてのノードによって承認されるまで、[patronictl](/ja/patroni/patronictl#patronictl) は待機します。このような動作は、DCS のすべてのノードに対して [一時停止する](/ja/patroni/pause#pause) フラグを公開し、REST API を介して実現されます。

- `patronictl failover` を `patronictl switchover` に名前変更します (Alexander Kukushkin)

以前の `failover` は、実際にはスイッチオーバーのみを行うことができました。リーダーなしでは集団で進むことを拒否した。

- `patronictl failover` の動作を変更しました (Alexander Kukushkin)

リーダーがない場合でも機能しますが、その場合は新しいリーダーとなるノードを明示的に指定する必要があります。

**タイムラインと歴史に関する情報を公開する**

- 現在のタイムラインを DCS および API 経由で公開します (Alexander Kukushkin)

クラスターの各メンバーの現在のタイムラインに関する情報を保存します。この情報は API 経由でアクセスでき、DCS に保存されます。

- プロモーション履歴を DCS の /history キーに保存します (Alexander Kukushkin)

さらに、対応するプロモーションのタイムスタンプで強化されたタイムライン履歴を DCS の /history キーに保存し、プロモートごとに更新します。

**同期および非同期レプリカを取得するためのエンドポイントを追加する**

- 新しい /sync および /async エンドポイントを追加します (Alexander Kukushkin、Oleksii Kliukin)

> これらのエンドポイント (/synchronous および /asynchronous としてもアクセス可能) は、同期レプリカと非同期レプリカに対してのみ 200 を返します (`noloadbalance` としてマークされたものを除く)。

**etcd に対して複数のホストを許可する**

- Etcd 設定に新しい `hosts` パラメータを追加しました。 (Alexander Kukushkin)

このパラメーターには、実行中の etcd クラスター メンバーのリストを検出して設定するために使用されるホストの初期リストが含まれている必要があります。作業中に何らかの理由で、この検出されたホストのリストが使い果たされた場合 (そのリストに使用可能なホストがない場合)、Patroni は `hosts` パラメーターから初期リストに戻ります。

--------

## バージョン 1.3.6 {#version-136}

2017-11-10 をリリース

**安定性の向上**

- postgres が実行されているかどうかを確認するときに、プロセスの開始時間を確認します。 (アリズ・アスマ)

postmaster.pid をクリーンアップしないクラッシュの後は、同じ pid を持つ新しいプロセスが存在する可能性があり、その結果 is_running() の誤検出が発生し、あらゆる種類の不正な動作につながります。

- データ ディレクトリを失った場合、ブートストラップの前に PostgreSQL をシャットダウンします (ainlolcat)

マスター上のデータ ディレクトリが強制的に削除されると、postgres プロセスがしばらくの間生きたままになり、元のマスターの代わりに作成されたレプリカの起動や複製が妨げられることがあります。この修正により、Patroni はポストマスター PID とその開始時刻をキャッシュし、対応するデータ ディレクトリが削除された後も古いポストマスターがまだ実行されている場合に備えて古いポストマスターを終了できるようになります。

- postgres マスターが停止した場合にシングル ユーザー モードでクラッシュ リカバリを実行します。 (Alexander Kukushkin)

スタンバイとしてすぐに開始するのは安全ではなく、postgres が正常にシャットダウンされていない場合は `pg_rewind` を実行できません。シングル ユーザー クラッシュ リカバリは、`pg_rewind` が有効になっている場合、または現時点でマスターが存在しない場合にのみ開始されます。

**Consul の改善**

- Consul のデータセンター構成を提供できるようにします (Vilius Okockis、Alexander Kukushkin)

それまでは、Patroni は常に、それが実行されているホストのデータセンターと通信していました。

- 常に X-Consul-Token http ヘッダーでトークンを送信します (Alexander Kukushkin)

`consul.token` が Patroni 構成で定義されている場合、常に「X-Consul-Token」http ヘッダーで送信されます。 python-consul モジュールは、Consul REST API を使用して "consistent" になろうとします。これは、[セッション API](https://www.consul.io/api/session.html) のクエリー パラメーターとしてトークンを受け入れませんが、「X-Consul-Token」ヘッダーでは引き続き機能します。

- 指定された値が可能な最小値より小さい場合、セッション TTL を調整します。 (Stas Fomin、Alexander Kukushkin)

Patroni 構成で提供される TTL が、Consul でサポートされる最小値よりも小さい場合があります。その場合、Consul エージェントは新しいセッションの作成に失敗します。セッションがないと、Patroni は Consul KV ストアにメンバー キーとリーダー キーを作成できず、クラスターが異常な状態になります。

**その他の改善点**

- 環境変数 `PATRONI_LOGFORMAT` を使用してカスタム ログ形式を定義します (Stas Fomin)

システム ロガーによってすでに追加されている場合 (通常は Patroni がサービスとして実行されている場合)、Patroni ログ内のタイムスタンプやその他の同様のフィールドを無効にすることができます。

--------

## バージョン 1.3.5 {#version-135}

2017-10-12 をリリース

**バグ修正**

- データ ディレクトリが削除された場合はロールを 'uninitialized' に設定します。 (Alexander Kukushkin)

ノードがマスターとして実行されている場合、フェイルオーバーが妨げられていました。

**安定性の向上**

- postgres を起動しようとして失敗した場合は、シングルユーザー モードで postmaster を実行してみてください。 (Alexander Kukushkin)

通常、このような問題は、マスターとして実行されているノードが終了し、タイムラインが分岐したときに発生します。 `recovery.conf` に `restore_command` が定義されている場合、postgres が起動を中止し、制御データが変更されないままになる可能性が非常に高くなります。 `pg_rewind` を使用できなくなり、クリーン シャットダウンが必要になります。

**Consul の改善**

- セッション作成時にヘルスチェックを指定できるようにしました。 (Alexander Kukushkin)

指定しない場合、Consul は「serfHealth」を使用します。これにより、孤立したマスターを迅速に検出できるようになります。一方で、Patroni が短いネットワーク遅延を許容できなくなります。

**バグ修正**

- Python 3 のウォッチドッグを修正 (Ants Aasma)

ioctl() 呼び出しインターフェースの誤解。 mutable=False の場合、fcntl.ioctl() は実際に arg バッファを返します。 int と str の比較でエラーが返されなかったため、これは Python2 で誤って機能しました。エラー報告は実際には、Python2 では IOError を、Python3 では OSError を発生させることによって行われます。

--------

## バージョン 1.3.4 {#version-134}

2017-09-08 をリリース

**Consul のさまざまな改善**

- 領事トークンをヘッダーとして渡します (Andrew Colin Kissa)

ヘッダーは、トークンを領事 [API](https://www.consul.io/api/index.html#authentication) に渡すための推奨される方法になりました。

- Consul の高度な構成 (Alexander Kukushkin)

`scheme`、`token`、クライアントおよび CA 証明書 [詳細](/ja/patroni/config/yaml#consul_settings) を指定する可能性。

- python-consul-0.7.1 以降との互換性 (Alexander Kukushkin)

新しい python-consul モジュールはいくつかのメソッドのシグネチャを変更しました

- 「TTL ロックを解除できませんでした」というメッセージがログに記録されませんでした。 (Alexander Kukushkin)

重大なバグではありませんが、適切なログが記録されていないと、問題が発生した場合の調査が複雑になります。

**quote_ident を使用して synchronous_standby_names を引用する**

- `synchronous_standby_names` を `postgresql.conf` に書き込むときは、その値を引用符で囲む必要があります。 (Alexander Kukushkin)

正しく引用符で囲まれていない場合、PostgreSQL は事実上同期レプリケーションを無効にし、動作を継続します。

**一時停止状態に関するさまざまなバグ修正。主にウォッチドッグに関連します。** (アレクサンダー・ククシュキン)

- ウォッチドッグがアクティブでない場合はキープアライブを送信しない
- 一時停止モードでウォッチドッグをアクティブ化しないでください
- 一時停止モードで正しい postgres 状態を設定する
- postgres が停止している場合は、API からクエリーを実行しないでください

--------

## バージョン 1.3.3 {#version-133}

2017-08-04 をリリース

**バグ修正**

- 同期レプリケーションは、synchronous_mode_strict がオンになっている場合でも、昇格直後に無効になりました。 (Alexander Kukushkin)
- バックアップからのリストア後に`pg_ident.conf`が存在しない場合、空のファイルを作成するようにしました（Alexander Kukushkin）。
- `pg_hba.conf` で postgres だけでなくすべてのデータベースにアクセスできるようになりました (Franco Bellagamba)

--------

## バージョン 1.3.2 {#version-132}

2017-07-31 をリリース

**バグ修正**

- patronictl edit-config が ZooKeeper では動作しませんでした。 (Alexander Kukushkin)

--------

## バージョン 1.3.1 {#version-131}

2017-07-28 をリリース

**バグ修正**

- `_MemberStatus` の変更により、API 経由の  フェイルオーバーが機能しませんでした。 (Alexander Kukushkin)

--------

## バージョン 1.3 {#version-13}

2017-07-27 をリリース

バージョン 1.3 では、カスタム ブートストラップの可能性が追加され、pg_rewind のサポートが大幅に改善され、同期モードのサポートが強化され、patronictl に構成編集が追加され、Linux でウォッチドッグ サポートが実装されます。さらに、これは PostgreSQL 10 で正しく動作する最初のバージョンです。

**アップグレードのお知らせ**

新しいバージョンの Patroni との互換性に関する既知の問題はありません。バージョン 1.2 からの構成は変更せずに機能するはずです。新しいパッケージをインストールして Patroni を再起動する (PostgreSQL が再起動する) か、最初に Patroni を [一時停止モード](/ja/patroni/pause#pause) に入れてからクラスター内のすべてのノードで Patroni を再起動する (一時停止モードの Patroni は PostgreSQL の停止/開始を試行しません) ことによって、最後に一時停止モードから再開することでアップグレードできます。

**カスタムブートストラップ**

- クラスターのブートストラップのプロセスを構成可能にしました (Alexander Kukushkin)

クラスター内の最初のノードを初期化するときに、`initdb` の代わりにカスタム ブートストラップ スクリプトを許可します。ブートストラップ コマンドは、クラスターの名前とデータ ディレクトリへのパスを受け取ります。結果として得られるクラスターはリカバリを実行するように構成でき、バックアップからブートストラップしてポイントインタイムリカバリを実行できるようになります。この機能の詳細については、[ドキュメントページ](/ja/patroni/replica_bootstrap#custom_bootstrap) を参照してください。

**よりスマートな pg_rewind サポート**

- 現在のマスターとのタイムラインの違いを見て、pg_rewind を実行するかどうかを決定します。 (Alexander Kukushkin)

以前は、Patroni には、pg_rewind をトリガーする一連の固定条件がありました。つまり、元のマスターを起動するとき、クラスター内の他のすべてのノードで指定されたノードへのスイッチオーバーを実行するとき、または nofailover タグを持つレプリカが存在するときです。これらすべてのケースに共通するのは、一部のレプリカが新しいマスターよりも先に存在する可能性があるということです。場合によっては、pg_rewind が何も行わなかったり、必要なときに実行されなかったりする場合もありました。この限られたルールのリストに依存する代わりに、Patroni でマスターとレプリカの WAL 位置を (ストリーミング レプリケーション プロトコルを使用して) 比較し、レプリカに巻き戻しが必要かどうかを確実に判断します。

**同期レプリケーションモード厳密**

- 厳密モードを追加して同期レプリケーションのサポートを強化しました (James Sewell、Alexander Kukushkin)

通常、[synchronous_mode](/ja/patroni/replication_modes#synchronous_mode) が有効で、マスターにレプリカが接続されていない場合、Patroni はマスターを書き込みに使用できる状態に保つために同期レプリケーションを無効にします。 `synchronous_mode_strict` オプションは、Patroni が設定されている場合、レプリカが不足している場合でも同期レプリケーションを無効にせず、マスターにデータを書き込むすべてのクライアントを効果的にブロックするように変更します。自動フェイルオーバーによるデータ損失を防止する同期モードの保証に加えて、ストリクト モードでは、各書き込みが 2 つのノードに永続的に保存されるか、クラスター内にノードが 1 つしかない場合には完全に書き込みが行われないことが保証されます。

**patronictl を使用した構成編集**

- patronictl に構成編集を追加しました (Ants Aasma、Alexander Kukushkin)

DCS に保存されている動的クラスター構成の編集を保護する機能を追加します。コマンドラインからのパラメーター/値の指定、\$EDITOR の呼び出し、または yaml ファイルからの構成の適用のいずれかをサポートします。

**Linux ウォッチドッグのサポート**

- Linux のウォッチドッグ サポートを実装します (Ants Aasma)

Patroni が実行されていない、または応答していない (高負荷などの理由で) ノードを再起動するために、Linux ソフトウェア ウォッチドッグをサポートします。Linux ソフトウェア ウォッチドッグは、応答しないノードを再起動します。 Patroni 構成のウォッチドッグ セクションから、使用するウォッチドッグ デバイス (デフォルトでは `/dev/watchdog`) とモード (オン、自動、オフ) を構成できます。詳細については、[ウォッチドッグのドキュメント](/ja/patroni/watchdog#watchdog) から入手できます。

**PostgreSQL 10 のサポートを追加**

- Patroni は、これまでにリリースされた PostgreSQL 10 のすべてのベータ版と互換性があり、リリースされる予定の PostgreSQL 10 とも互換性があると予想されます。

**PostgreSQL 関連の軽微な改善**

- Patroni 構成ファイルまたは DCS の動的構成を介して pg_hba.conf を定義します (Alexander Kukushkin)

構成の `postgresql` セクションの `pg_hba` サブセクションで `pg_hba.conf` の内容を定義できるようにします。これにより、すべてのノードにログを記録し、手動で変更して構成をリロードするのではなく、DCS でのみ定義する必要があるため、複数のノードでの `pg_hba.conf` の管理が簡素化されます。

定義すると、このセクションの内容は現在の `pg_hba.conf` を完全に置き換えます。 `hba_file` PostgreSQL パラメータが設定されている場合、Patroni はこれを無視します。

- UNIX ソケットを介したローカル PostgreSQL クラスターへの接続をサポートしました (Alexander Kukushkin)

Patroni 構成の `postgresql` セクションに `use_unix_socket` オプションを追加します。 true に設定され、PostgreSQL `unix_socket_directories` オプションが空でない場合、Patroni はその最初の値を使用してローカル PostgreSQL クラスターに接続できます。 `unix_socket_directories` が定義されていない場合、Patroni はそのデフォルト値を想定し、PostgreSQL 接続文字列内の `host` パラメーターを完全に省略します。

- リロード時のスーパーユーザーおよびレプリケーション資格情報の変更をサポートしました (Alexander Kukushkin)

- PostgreSQL データ ディレクトリ外への構成ファイルの保存をサポート (@jouir)

新しい構成 `postgresql` 構成ディレクティブ `config_dir` を追加します。デフォルトはデータ ディレクトリであり、Patroni によって書き込み可能である必要があります。

**バグ修正と安定性の向上**

- EtcdEventIndexCleared および EtcdWatcherCleared 例外を処理します (Alexander Kukushkin)

無駄な再試行を回避することで、etcd によって監視操作が終了された場合の回復が高速化されます。

- Etcd 障害時にスピンするエラーを削除し、ログ スパムを削減します (Ants Aasma)

2 回目以降の etcd 接続失敗時に、すぐに再試行してスタック トレースをログに出力することは避けてください。

- PostgreSQL プロセスをフォークするときにロケール変数をエクスポートする (Oleksii Kliukin)

NLS で構築された PostgreSQL の英語以外のロケールでの `postmaster became multithreaded during startup` 致命的エラーを回避します。

- レプリケーション スロットを削除する際の追加チェック (Alexander Kukushkin)

場合によっては、Patroni は、WAL 送信者によってレプリケーション スロットを削除できなくなります。

- PostgreSQL 命名規則に準拠するために、レプリケーション スロット名を 63 (NAMEDATALEN - 1) 文字に切り詰めます (Nick Scott)

- Patroni から PostgreSQL クラスターに対して余分な接続が開かれるという競合状態を修正しました。 (Alexander Kukushkin)

- ノードが空のデータ ディレクトリで再起動するときにリーダー キーを解放します (Alex Kerney)

- リーダーなしでブートストラップを実行するときに非同期エグゼキュータをビジーに設定します。 (Alexander Kukushkin)

これを行わないと、Patroni はクラスター内にリーダーが存在する必要のないブートストラップ メソッドによってブートストラップされながら通常の業務を続行したため、ノードが別のクラスターに属していることを示すエラーが発生する可能性がありました。

- WAL-E レプリカ作成方法を改善しました (Joar Wandborg、Alexander Kukushkin)。

  - WAL-E ベース バックアップを解析するときに csv.DictReader を使用し、スペースで区切られた日付と時刻を持つ ISO 日付を受け入れます。
  - 、復元する WAL の量を見積もるために、レプリカから現在の WAL 位置を取得することをサポートします。以前は、コードはマスター ノードでのみ利用可能なシステム情報関数を呼び出すために使用されていました。

--------

## バージョン 1.2 {#version-12}

2016-12-13 をリリース

このバージョンでは、同期レプリケーションの処理が大幅に改善され、起動プロセスとフェイルオーバーの信頼性が向上し、PostgreSQL 9.6 サポートが追加され、多くのバグが修正されています。さらに、これらのリリース ノートを含むドキュメントは </patroni> に移動されました。

**同期レプリケーション**

- 同期レプリケーションのサポートを追加します。 (アリズ・アスマ)

新しい構成変数 [synchronous_mode](/ja/patroni/replication_modes#synchronous_mode) を追加します。有効にすると、Patroni は `synchronous_standby_names` を管理し、利用可能な正常なスタンバイがあるときは常に同期レプリケーションを有効にします。同期モードが有効な場合、Patroni はマスター障害時に同期レプリケーションを行っていたスタンバイにのみ自動的にフェイルオーバーします。これは事実上、そのような場合にユーザーに表示されるトランザクションが失われないことを意味します。詳細な説明と実装の詳細については、[機能ドキュメント](/ja/patroni/replication_modes#synchronous_mode) を参照してください。

**信頼性の向上**

- PostgreSQL が 100% 正常でない場合は、`leader optime` キーに保存されているリーダーの位置を更新しないでください。リーダーキーの更新に失敗した場合は直ちに降格します。 （アレクサンダー・ククシュキン）

- 新しいレプリカのクローンを作成するターゲットのリストから異常なノードを除外します。 （アレクサンダー・ククシュキン）

- Etcd の場合と同様に、Consul の再試行およびタイムアウト戦略を実装します。 （アレクサンダー・ククシュキン）

- `--dcs` と `--config-file` を [patronictl](/ja/patroni/patronictl#patronictl) のすべてのオプションに適用します。 （アレクサンダー・ククシュキン）

- すべての postgres パラメータを postgresql.conf に書き込みます。 （アレクサンダー・ククシュキン）

これにより、Patroni によって構成された PostgreSQL を `pg_ctl` だけで起動できます。

- 構成にユーザーが存在しない場合の例外を回避します。 （キリル・プーシキン）

- 異常なクラスターの一時停止を許可します。この修正が行われる前は、[patronictl](/ja/patroni/patronictl#patronictl) は、一時停止を実行しようとするノードが異常な場合に救済されました。 （アレクサンダー・ククシュキン）

- リーダー監視機能を改善します。 （アレクサンダー・ククシュキン）

以前は、レプリカは常にリーダー キーを監視していました (タイムアウトになるかリーダー キーが変更されるまでスリープ状態でした)。この変更により、レプリカの PostgreSQL が `running` 状態にある場合のみ監視され、PostgreSQL の停止/起動または再起動の場合は監視されません。

- SIGCHILD を PID 1 として処理するときに競合状態が発生するのを避けてください。 （アレクサンダー・ククシュキン）

以前は、Patroni 内の同じプロセスが新しいプロセスを生成し、そこから SIGCHILD を処理していたため、Docker コンテナー内で実行すると競合状態が発生する可能性がありました。この変更では、Patroni に fork/execs を使用し、元の PID 1 プロセスに子からのシグナルの処理を任せます。

- WAL-E 復元を修正します。 （オレクシー・クルーキン）

以前の WAL-E リストアでは、マスターとの協議を完全に回避するために `no_master` フラグが使用されていたため、Patroni は常に `pg_basebackup` ではなく WAL からのリストアを選択していました。この変更により、`no_master` の元の意味に戻ります。つまり、マスターが実行されていない場合、レプリケーション方法として Patroni WAL-E リストアが選択される可能性があります。後者は、メソッドに渡された接続文字列を調べることによってチェックされます。さらに、再試行メカニズムがより堅牢になり、他の細かい点も処理されます。

- 非同期 DNS リゾルバー キャッシュを実装します。 （アレクサンダー・ククシュキン）

DNS が一時的に利用できない場合 (たとえば、ノードが受信する過剰なトラフィックが原因で) 失敗することを避けてください。

- 開始状態とマスター開始タイムアウトを実装します。 （アリツ・アスマ、アレクサンダー・ククシュキン）

以前は、`pg_ctl` はタイムアウトを待ってから、PostgreSQL が実行中であるとみなして喜んで踏み続けていました。これにより、PostgreSQL が実際には実行されていないのにリストに実行中として表示され、競合状態が発生して、フェイルオーバー、クラッシュ リカバリ、またはフェイルオーバーによって中断されたクラッシュ リカバリと巻き戻しのミスが発生しました。この変更により、`master_start_timeout` パラメーターが追加され、メインの HA ループに新しい状態 (`starting`) が導入されます。 `master_start_timeout` が 0 の場合、マスターがクラッシュしたときにフェイルオーバー候補が存在するとすぐにフェイルオーバーします。それ以外の場合、Patroni はマスター上で PostgreSQL を開始しようとした後、タイムアウトの間待機します。有効期限が切れると、可能であればフェイルオーバーされます。手動フェイルオーバー要求は、マスターのクラッシュ中にタイムアウト期限が切れる前であっても受け付けられます。

`timeout` パラメーターを `restart` API エンドポイントおよび [patronictl](/ja/patroni/patronictl#patronictl) に導入します。これが設定され、再起動にタイムアウトよりも長い時間がかかると、PostgreSQL は異常とみなされ、他のノードがリーダー ロックを取得できるようになります。

- 一時停止モードでの `pg_rewind` の動作を修正しました。 (アリズ・アスマ)

Patroni が巻き戻しが必要であると考えているが巻き戻しができない場合 (つまり、`pg_rewind` が存在しない場合)、一時停止モードでの不必要な再起動を回避します。 `pg_rewind` 関連の Patroni 構成セクションに `superuser` 認証が欠落している場合、`superuser` (デフォルトの OS ユーザー) のデフォルトの `libpq` 値にフォールバックします。

- コールバックの実行をシリアル化します。新しいコールバックが実行されようとしているときに、同じタイプの前のコールバックを強制終了します。コールバックの実行時にゾンビ プロセスが生成される問題を修正します。 （アレクサンダー・ククシュキン）

- リーダー キーが DCS に設定されているにもかかわらず、このリーダー キーへの更新が失敗する場合は、以前のマスターを昇格させないでください。 （アレクサンダー・ククシュキン）

これにより、現在のマスターが etcd および「一貫性のない読み取り」を許可する他の DCS の少数のノードとともにパーティション化されている場合にその役割を維持し続けるという問題が回避されます。

**その他**

- ブートストラップに `post_init` 構成オプションを追加します。 （アレハンドロ・マルティネス）

Patroni は、`initdb` を実行し、新しいクラスターに対して PostgreSQL を起動した直後に、このオプションのスクリプト引数を呼び出します。このスクリプトは、`superuser` との接続 URL を受信し、パスワードを含む `.pgpass` ファイルを指すように `PGPASSFILE` を設定します。スクリプトが失敗すると、Patroni の初期化も失敗します。これは、新しいユーザーを追加したり、新しいクラスターに拡張機能を作成したりする場合に便利です。

- PostgreSQL 9.6 サポートを実装します。 （アレクサンダー・ククシュキン）

`wal_level = replica` を `hot_standby` の同義語として使用し、あるフラグから別のフラグに変更するときに pending_restart フラグを回避します。 （アレクサンダー・ククシュキン）

**ドキュメントの改善**

- Patroni メイン [ループワークフロー図](https://raw.githubusercontent.com/patroni/patroni/master/docs/ha_loop_diagram.png) を追加します。 （アレハンドロ・マルティネス、アレクサンダー・ククシュキン）

- README を改善し、Helm チャートとリリース ノートへのリンクを追加しました。 （ローリ・アップル）

- Patroni ドキュメントを `Read the Docs` に移動します。最新のドキュメントは </patroni> で入手できます。 （オレクシー・クルーキン）

さまざまなデバイス (スマートフォンを含む) からドキュメントを簡単に表示し、検索できるようにします。

- パッケージをセマンティック バージョニングに移動します。 （オレクシー・クルーキン）

Patroni は、小規模だが重大なバグ修正に関する新しいマイナー バージョンのリリースを回避するために、major.minor.patch バージョン スキーマに従います。すべてのパッチを含むマイナー バージョンのリリース ノートのみを公開します。

--------

## バージョン 1.1 {#version-11}

2016-09-07 をリリース

このリリースでは、一時停止モードを導入することで Patroni クラスターの管理が改善され、スケジュールされた条件付き再起動によるメンテナンスが改善され、etcd または Zookeeper との Patroni の対話の回復力が向上し、patronictl が大幅に強化されています。

**アップグレードのお知らせ**

1.0 より前のリリースからアップグレードする場合は、1.0 リリース ノートで資格情報と構成形式の変更についてお読みください。

**一時停止モード**

- 一時停止モードを導入して、Patroni を PostgreSQL インスタンスの管理から一時的に切り離します (Murat Kabilov、Alexander Kukushkin、Oleksii Kliukin)。

以前は、PostgreSQL を終了せずに、SIGKILL シグナルを Patroni に送信して停止する必要がありました。新しい一時停止モードは、Patroni を終了せずに、クラスター全体で Patroni を PostgreSQL から切り離します。これは、Pacemaker のメンテナンス モードに似ています。 Patroni は引き続き DCS のメンバー キーとリーダー キーを更新しますが、プロセス内で PostgreSQL サーバーを起動、停止、再起動することはありません。いくつかの例外があります。たとえば、手動フェイルオーバー、再初期化、再起動は引き続き許可されます。 [この機能の詳細な説明](/ja/patroni/pause#pause) と読み取れます。

さらに、patronictl は、一時停止モードを切り替えるための新しい [一時停止する](/ja/patroni/pause#pause) および `resume` コマンドをサポートしています。

**スケジュールされた再起動と条件付きの再起動**

- 再起動 API コマンドに条件を追加します (Oleksii Kliukin)

この変更により、再起動を行うために検証できるいくつかの条件が追加され、Patroni の再起動が強化されます。条件には、PostgreSQL ロールがマスターまたはレプリカの場合の再起動、PostgreSQL バージョン番号の確認、構成変更を適用するために再起動が必要な場合のみの再起動などがあります。

- スケジュールされた再起動を追加 (Oleksii Kliukin)

将来の再起動をスケジュールできるようになりました。スケジュールされた再起動はノードごとに 1 つだけサポートされます。スケジュールされた再起動が必要なくなった場合は、クリアすることができます。スケジュールされた再起動と条件付き再起動の組み合わせがサポートされているため、たとえば、夜間にスケジュールされたマイナー PostgreSQL アップグレードが可能になり、管理スクリプトに postgres 固有のロジックを追加することなく、古いマイナー バージョンを実行しているインスタンスのみを再起動できます。

- patronictl に条件付きおよびスケジュールされた再起動のサポートを追加しました (Murat Kabilov)。

patronictl restart は、いくつかの新しいオプションをサポートします。スケジュールされたアクションを消去するための patronictl flash コマンドもあります。

**堅牢な DCS インタラクション**

- loop_wait に応じて Kazoo タイムアウトを設定します (Alexander Kukushkin)

当初、ping_timeout および connect_timeout の値は、ネゴシエートされたセッション タイムアウトから計算されました。 Patroni ループ待機は考慮されていませんでした。その結果、1 回の再試行にセッション タイムアウトよりも長い時間がかかり、Patroni がロックを解放して降格する必要が生じる可能性があります。

この変更により、ping と接続のタイムアウトがloop_wait の値の半分に設定され、接続の問題の検出が高速化され、ロックが失われる前に接続試行を再試行するのに十分な時間が残されました。

- 元のリクエストが成功した後にのみ etcd トポロジを更新するようになりました。 (Alexander Kukushkin)

クライアントに認識されている etcd トポロジの更新を、元のリクエストが完了するまで延期します。クラスター トポロジを取得するときは、etcd クラスター内の既知のノード数に応じて再試行タイムアウトを実装します。これにより、クライアントは最新のノードのリストを取得するよりも、リクエストの結果を取得することを優先します。

どちらの変更も、ネットワークの問題に直面した場合でも、Patroni から DCS への接続をより堅牢にします。

**監視、監視および設定**

- API 経由でストリーミング レプリカに関する情報を返します (Feike Steenbergen)

以前は、(接続の問題などにより) 変更のストリーミングに失敗した PostgreSQL インスタンスについて Patroni をクエリーする信頼できる方法はありませんでした。この変更により、pg_stat_replication の内容が /patroni エンドポイント経由で公開されます。

- patronictl scaffold コマンドを追加 (Oleksii Kliukin)

etcd にクラスター構造を作成するコマンドを追加します。クラスターはユーザー指定の sysid とリーダーを使用して作成され、リーダー キーとメンバー キーの両方が永続化されます。このコマンドは、レプリカのみで構成される Patroni クラスターが Patroni を認識しない外部マスター ノードから複製される、いわゆるマスターレス構成を作成するのに役立ちます。その後、リーダー キーを削除し、Patroni ノードの 1 つをプロモートし、元のマスターを Patroni ベースの HA クラスターに置き換えます。

- 構成オプション `bin_dir` を追加して、PostgreSQL バイナリを見つけます (Ants Aasma)

Linux ディストリビューションが複数の PostgreSQL バージョンの同時インストールをサポートしている場合、PostgreSQL バイナリの場所を明示的に指定できると便利です。

- (Alejandro Martínez) の `custom_conf` を使用して構成ファイルのパスを上書きできるようにします

Patroni、[詳細](/ja/patroni/config/yaml#postgresql_settings) によって管理されないカスタム構成ファイル パスを許可します。

**バグ修正とコードの改善**

- Patroni を PostgreSQL 10 以降の新しいバージョンのスキーマと互換性のあるものにします (Feike Steenbergen)

PostgreSQL バージョンに基づいて条件付き再起動を行う場合、Patroni が 2 桁のバージョン番号を理解していることを確認してください。

- pkgutil を使用して DCS モジュールを検索します (Alexander Kukushkin)

DCS モジュールを見つけるためにディレクトリを手動で走査する代わりに、専用の Python モジュールを使用します。

- Patroni を開始するときに常に on_start コールバックを呼び出します。 (Alexander Kukushkin)

以前は、Patroni は、正しいロールですでに実行中のノードにアタッチするときにコールバックを呼び出しませんでした。コールバックはクライアント接続のルーティングによく使用されるため、接続ルーティング スキームで実行中のノードを登録できなくなる可能性があります。この修正により、Patroni は、既に実行中のノードに接続している場合でも on_start コールバックを呼び出します。

- アクティブなレプリケーション スロットを削除しないでください (Murat Kabilov、Oleksii Kliukin)

マスター上のアクティブな物理レプリケーション スロットをドロップしないようにします。いずれにせよ、PostgreSQL はそのようなスロットを削除できません。この変更により、Patroni 以外の管理対象レプリカ/コンシューマーをマスター上で実行できるようになります。

- PostgreSQL インスタンスの起動中に Patroni 接続を閉じます。 (Alexander Kukushkin)

PostgreSQL ノードの起動時に、Patroni が以前のすべての接続を強制的に閉じます。 postmaster が SIGKILL で強制終了された場合に、以前の接続が再利用されるという罠を回避します。

- メンバー名からスロット名を構築するときに無効な文字を置換します (Ants Aasma)

スロットの命名規則に準拠していないスタンバイ名によってスロットの作成やスタンバイの起動が失敗しないようにしてください。スロット名のダッシュをアンダースコアに置き換え、スロット名に使用できない他のすべての文字を Unicode コードポイントに置き換えます。

--------

## バージョン 1.0 {#version-10}

2016-07-05 をリリース

このリリースでは、HA クラスター全体の PostgreSQL および Patroni 構成パラメーターを動的に変更できるグローバル動的構成が導入されています。また、多数のバグ修正も提供されます。

**アップグレードのお知らせ**

v0.90 以下からアップグレードする場合は、必ずマスターより前にすべてのレプリカをアップグレードしてください。レプリケーション資格情報が DCS に保存されなくなったため、古いレプリカは新しいマスターに接続できなくなります。

**動的構成**

- 動的グローバル構成の実装 (Alexander Kukushkin)

新しい REST API エンドポイント /config を導入して、HA クラスター全体 (マスターとすべてのレプリカ) に対してグローバルに設定する必要がある PostgreSQL および Patroni 構成パラメーターを提供します。これらのパラメーターは DCS で設定され、多くの場合、PostgreSQL または Patroni を中断することなく適用できます。 Patroni は、一部の値で PostgreSQL の再起動が必要な場合に、API を介して表示される「再起動保留中」と呼ばれる特別なフラグを設定します。その場合、API を介して手動で再起動を発行する必要があります。

Patroni SIGHUP または POST から /reload を使用すると、構成ファイルが再読み取りされます。

変更できるパラメータと、異なる構成ソースを処理する順序の詳細については、[Patroni 構成](/ja/patroni/config#config) を参照してください。

v0.90 以降の構成ファイル形式は *変わった* です。 Patroni は依然として古い設定ファイルと互換性がありますが、ブートストラップ パラメータを利用するには変更する必要があります。ユーザーは、[動的構成ドキュメントページ](/ja/patroni/config/dynamic#dynamic) を参照して更新することをお勧めします。

**より柔軟な構成**\*

- postgresql 構成とデータベース名を作成します Patroni は構成可能に接続します (Misja Hoebe)

`database` および `config_base_name` 構成パラメーターを導入します。特に、Patroni を PipelineDB および他の PostgreSQL フォークで実行できるようになります。

- 環境経由で一部の Patroni 設定パラメータを設定できるように実装しました (Alexander Kukushkin)

これらには、スコープ、ノード名、名前空間、およびシークレットが含まれており、動的環境 (つまり、Kubernetes) での Patroni の実行が容易になります。詳細については、[サポートされている環境変数](/ja/patroni/config/env#env) を参照してください。

- 組み込みの Patroni Docker コンテナを更新して、環境ベースの構成を活用します (Feike Steenbergen)。

- Patroni docker イメージに Zookeeper サポートを追加しました (Alexander Kukushkin)

- Zookeeper と Exhibitionr の構成オプションを分割する (Alexander Kukushkin)

- patronictl が構成を読み取るために Patroni のコードを再利用するようにしました。 (Alexander Kukushkin)

これにより、patronictl は環境ベースの構成を利用できるようになります。

- primary_conninfo でアプリケーション名をノード名に設定しました (Alexander Kukushkin)

これにより、特定のノードの同期レプリケーションの識別と構成が簡素化されます。

**安定性、セキュリティ、使いやすさの向上**

- sysid をリセットし、バックアップの復元の進行中に pg_controldata を呼び出さないようにしました。 (Alexander Kukushkin)

この変更により、バックアップからのこのノードの長時間の初期化中に Patroni API ヘルス チェックによって生成されるノイズの量が減少します。

- pg_rewind のいくつかのコーナーケースを修正しました (Alexander Kukushkin)

ソースクラスターがマスターではない場合は、pg_rewind を実行しないでください。

さらに、新しいパラメータ *Remove_data_directory_on_rewind_failure* が true に設定されていない限り、巻き戻しが失敗したときにデータ ディレクトリを削除しないでください。デフォルトでは false です。

- DCS のレプリケーション接続文字列からパスワードを削除します。 (Alexander Kukushkin)

以前は、Patroni は常に、DCS の Postgres URL からのレプリケーション資格情報を使用していました。これは、Patroni 構成から資格情報を取得するように変更されました。シークレット (レプリケーション ユーザー名とパスワード) は DCS で公開されなくなりました。

- 降格呼び出し周りの非同期機構を修正しました。 (Alexander Kukushkin)

Demote は、DCS インタラクションをブロックすることなく、完全に非同期で実行されるようになりました。

- patronictl が設定されている場合、常に認証ヘッダーを送信するようにしました。 (Alexander Kukushkin)

これにより、Patroni がそれらに対する承認を必要とするように構成されている場合、patronictl は "protected" リクエストを発行 (つまり、再起動または再初期化) することができます。

- SystemExit 例外を正しく処理します (Alexander Kukushkin)

SIGTERM を受信したときに Patroni が適切に停止しない問題を回避します。

- confd 用のサンプル HAProxy テンプレート (Alexander Kukushkin)

confide を使用して、DCS の Patroni 状態から HAProxy 構成を生成し、動的に変更します。

- ドキュメントを改善および再構成して、新規ユーザーにとってより使いやすいものにします (Lauri Apple)

- API は、pg_ctl の停止中に role=master を報告する必要があります。 (Alexander Kukushkin)

特にクラスター停止の場合、コールバック呼び出しの信頼性が高まります。さらに、`pg_ctl_timeout` オプションを導入して、`pg_ctl` を介して呼び出しの開始、停止、再開のタイムアウトを設定します。

- etcd の再試行ロジックを修正しました。 (Alexander Kukushkin)

再試行をより予測可能かつ堅牢にします。

- Zookeeper コードの短いネットワーク障害に対する回復力を高めます (Alexander Kukushkin)

接続タイムアウトを減らして、Zookeeper の接続試行の頻度を増やします。

--------

## バージョン 0.90 {#version-090}

2016-04-27 をリリース

このリリースでは、Consul のサポートが追加され、新しい *noloadbalance* タグが含まれ、*クローンから* タグの動作が変更され、*pg_rewind* 処理が改善され、*守護者* 制御プログラムが改善されます。

**Consul のサポート**

- Consul サポートの実装 (Alexander Kukushkin)

Patroni は、etcd と Zookeeper に加えて、Consul に対して実行されます。接続パラメータは YAML ファイルで構成できます。

**新しいタグと改良されたタグ**

- *noloadbalance* タグを実装する (Alexander Kukushkin)

このタグにより、Patroni は常にレプリカがロード バランサーで利用できないことを返すようになります。

- *クローンから* タグの実装を変更します (Alexander Kukushkin)

以前は、ノード名を *クローンから* に指定する必要があり、タグ付きレプリカが特定のノードからクローンを作成する必要がありました。新しい実装では、*クローンから* がブール型タグになります。これが true に設定されている場合、レプリカは他のレプリカが複製する候補になります。複数の候補が存在する場合、レプリカはランダムに 1 つを選択します。

**安定性とセキュリティの向上**

- 数多くの信頼性の向上 (Alexander Kukushkin)

いくつかの偽のエラー メッセージを削除し、フェイルオーバーの安定性を向上させ、DCS からのデータの読み取り、シャットダウン、以前のリーダーの降格、および再接続に関するいくつかの特殊なケースに対処します。

- システム スクリプトを改善して、Patroni の子が停止中に殺されないようにする (Jan Keirse、Alexander Kukushkin)

以前は、Patroni を停止すると、*システムド* も PostgreSQL にシグナルを送信していました。 Patroni も PostgreSQL を単独で停止しようとしたため、別のシャットダウン要求 (スマート シャットダウン、その後の高速シャットダウン) が送信されることになりました。その結果、レプリカの切断が早すぎて、元のマスターが降格後に再参加できなくなりました。 Alexander による事前調査をもとに Jan によって修正されました。

- 元のマスターがレプリカとして再参加する前に pg_rewind を呼び出すことができなかったいくつかのケースを排除しました (Oleksii Kliukin)

以前は、前のマスターがクラッシュした場合にのみ *pg_rewind* を呼び出していました。 pg_rewind がシステムに存在する限り、元のマスターに対して常に pg_rewind を実行するようにこれを変更します。これにより、レプリカが最新の変更を取得する前にマスターがシャットダウンされた場合 (つまり、"smart" シャットダウン中) が修正されます。

- 単体テストと受け入れテストに対する数多くの改善により、特に Zookeeper と Consul (Alexander Kukushkin) のサポートが可能になりました。

- Travis CI を高速化し、Zookeeper (出展者) および Consul (Alexander Kukushkin) に対するテスト実行のサポートを実装します。

単体テストと受け入れテストはどちらも、各コミットまたはプルリクエストで etcd、Zookeeper、Consul に対して自動的に実行されます。

- Patroni から PostgreSQL コマンドを呼び出す前に環境変数をクリアします (Feike Steenbergen)

これにより、Patroni によって管理される PostgreSQL クラスターに接続することによってシステム環境変数が読み取られる可能性が回避されます。

**構成と制御の変更**

- patronictl と Patroni 構成を統合 (Feike Steenbergen)

patronictl は、Patroni 自体と同じ構成ファイルを使用できます。

- Patroni を有効にして環境変数から構成を読み取ります (Oleksii Kliukin)

これにより、Patroni の構成の自動生成や、異なるソースからの単一の構成のマージが簡素化されます。

- API によって返される情報にデータベース システム識別子を含めます (Feike Steenbergen)

- 利用可能なすべての DCS に *クラスターの削除* を実装します (Alexander Kukushkin)

patronictl で etcd 以外の DCS のサポートを有効にします。

--------

## バージョン 0.80 {#version-080}

2016-03-14 をリリース

このリリースでは、*カスケードレプリケーション* のサポートが追加され、*スケジュールされたフェイルオーバー* を提供することで Patroni 管理が簡素化されます。新しいリリースに移行するために、古いバージョンの Patroni (特に 0.78) をこのバージョンと組み合わせて使用​​する場合があります。スケジュールされたフェイルオーバーとカスケード レプリケーション関連の機能は、Patroni 0.80 以降でのみ動作することに注意してください。

**カスケードレプリケーション**

> - patroni ノード (Oleksii Kliukin) の *から複製する* タグと *クローンから* タグのサポートを追加します。
>
> タグ *から複製する* を使用すると、レプリカはマスターではなく任意のノードをソースとして使用できます。 *クローンから* は、最初のバックアップでも同じことを行います。これらを組み合わせることで、Patroni はカスケード レプリケーションを完全にサポートできるようになります。

- レプリケーション接続を実行していなくてもレプリカを初期化するレプリケーション メソッドの実行のサポートを追加しました (Oleksii Kliukin)。

> これは、S3 または FTP に保存されているスナップショットからレプリカを作成する場合に便利です。レプリケーション接続の実行を必要としないレプリケーション メソッドでは、yaml 設定で *no_master: true* を指定する必要があります。レプリケーション接続が存在する場合、これらのスクリプトは引き続き順番に呼び出されます。

**Patronictl、API、DCS の改善**

- スケジュールされたフェイルオーバーを実装します (Feike Steenbergen)。

patronictl または API 呼び出しを使用して、将来の特定の時刻にフェイルオーバーが発生するようにスケジュールできます。

- patronictl に *データベースユーザー* および *パスワード* パラメーターのサポートを追加しました (Feike Steenbergen)。

- PostgreSQL バージョンをヘルス チェック出力に追加します (Feike Steenbergen)。

- patronictl での Zookeeper のサポートを改善しました (Oleksandr Shulgin)

- Python への移行-etcd 0.43 (Alexander Kukushkin)

**構成**

- Patroni 用のサンプル システム構成スクリプトを追加します (Jan Keirse)。
- DB 接続の構成ファイルで指定されたスーパーユーザー名が無視される Patroni の問題を修正しました (Alexander Kukushkin)。
- Patroni (Alexander Kukushkin) によって起動されたポストマスター用に別のセッション ID とプロセス グループを作成することで、CTRL-C の処理を修正しました。

**テスト**

- Patroni を実行する実際のシナリオをチェックするために、*振る舞う* による受け入れテストを追加します (Alexander Kukushkin、Oleksii Kliukin)。

テストは、*振る舞う* コマンドを使用して手動で開始できます。また、プル リクエストやコミット後に自動的に起動されます。

一部の古いバージョンのリリース ノートは、[プロジェクトの github ページ](https://github.com/patroni/patroni/releases) にあります。
