---
title: "変更履歴"
weight: 70
description: "PgBouncer のバージョン履歴とリリースノート"
icon: fa-solid fa-scroll
module: [PGBOUNCER]
categories: [リファレンス]
aliases: [/pgbouncer/changelog/]
upstream_link: "https://www.pgbouncer.org/changelog.html"
---

--------

## PgBouncer 1.25.x {#pgbouncer-125x}

**2026-05-08  -  PgBouncer 1.25.2  -  「不確実性に満ちたタイトル争いに、新鮮な一撃が加わる」**

- セキュリティ
  * CVE-2026-6664 の修正：1.25.2 以前の PgBouncer において、ネットワークパケット解析コードに整数オーバーフローが存在し、境界チェックを回避してクラッシュを引き起こす可能性があります。認証されていないリモート攻撃者は、不正な SCRAM 認証パケットを送信することで PgBouncer をクラッシュさせることができます。
  * CVE-2026-6665 の修正：1.25.2 以前の PgBouncer における SCRAM コードは、SCRAM クライアント最終メッセージの内容を構築する際に `strlcat()` の戻り値を正しくチェックしていなかった。悪意あるバックエンドが長い nonce を含む SCRAM サーバー最終メッセージを送信すると、スタックオーバーフローを引き起こす可能性がある。
  * CVE-2026-6666 の修正：1.25.2 以前の PgBouncer では、サーバーが SQLSTATE フィールドを含まないエラー応答を送信した場合、ヌルポインタ参照の可能性があり、クラッシュを引き起こすおそれがあります。
  * CVE-2026-6667 を修正：1.25.2 以前の PgBouncer では、`KILL_CLIENT` 管理コマンドに対する適切な権限チェックが行われていませんでした。管理コンソールにアクセスできるすべてのユーザーがこのコマンドを実行できました。このコマンドは、`admin_users` パラメータにリストされたユーザーにのみ許可されるべきです。

- 修正
  * `default_pool_size` パラメータのドキュメントを明確にします。
  * ドキュメントは `client_tls13_ciphers` および `server_tls13_ciphers` に対して正しく記述されています。

**2025-12-03  -  PgBouncer 1.25.1  -  「クリスマス前に多数のバグを修正」**

- セキュリティ
  * CVE-2025-12819 の修正：このリリース以前は、認証中に悪意ある search_path パラメータを StartupMessage で提供することで、未認証の攻撃者が任意の SQL を実行できる可能性がありました。次のすべての設定を有するシステムは脆弱です：

    1. `track_extra_parameters` には search_path が含まれます（非デフォルトの設定で、おそらく Citus または PostgreSQL 18 を使用する設定でのみ構成されています）。
    2. `auth_user` が空でない文字列に設定されている（デフォルト以外の設定）
    3. `auth_query` は完全修飾オブジェクト名を指定せずに設定されています（デフォルト設定、< 演算子はスキーマ修飾されていない）

- 修正
    - 1.25.0 で導入された、サーバーへの再接続後に一時的な SCRAM 認証で発生するエラーを修正しました ([#1432])
    - SIMD 対応なしの特殊アーキテクチャ向けに欠落している typedef を追加しました（[#1414]、1.25.0 で導入）
    - クライアントがデータを送信する前に接続を閉じた場合のノイズとなる警告ログを削除する（[#1420]、1.25.0 で導入）
    - NULL ポインタ参照の可能性を防止します（[#1423]、1.25.0 で導入）
    - 1.25.0 で導入された潜在的なメモリリークを修正しました ([#1422])
    - SCRAM のサーバーメッセージ解析を修正しました（[#1431]、1.25.0 で導入）

[#1414]: https://github.com/pgbouncer/pgbouncer/pull/1414
[#1420]: https://github.com/pgbouncer/pgbouncer/pull/1420
[#1422]: https://github.com/pgbouncer/pgbouncer/pull/1422
[#1423]: https://github.com/pgbouncer/pgbouncer/pull/1423
[#1431]: https://github.com/pgbouncer/pgbouncer/pull/1431
[#1432]: https://github.com/pgbouncer/pgbouncer/pull/1432

**2025-11-09  -  PgBouncer 1.25.0  -  「LDAPサポート付きのバージョン」**

- 機能
    * LDAP 認証を追加できます。HBA ファイルまたは `auth_ldap_options` を使用して設定できます。([#731])
    * クライアント側の直接TLS接続をサポートしました。これにより、PostgreSQL 17で導入されたより高速なTLS接続セットアップがクライアントで利用可能になります。PgBouncerは現在、このより高速な接続セットアップを使用してPostgreSQLサーバーに接続することはできません。([#1359])
    *  クライアント接続のアイドル状態を `SHOW CLIENTS` に追加します。 ([#1191])
    *  `transaction_timeout` の設定を、グローバルおよびユーザー単位で追加します。([#1242])
    *  5 秒以上接続を受け取らずにキューに積まれた場合、クライアントに NOTICE メッセージを送信します。この期間は `query_wait_notify` を使用して変更または無効化できます。([#1264])
    *  認証の速度を向上させるためにセキュリティを犠牲にすることができるよう、`scram_iterations` 設定を追加しました ([#1339])
    * TLSv1.3 の暗号スイートを有効にするために、`client_tls13_ciphers` および `server_tls13_ciphers` を指定します。([#1352])
- 変更点
    *  一時的な SCRAM 認証のパフォーマンスを大幅に向上。([#1338])
    * `KILL` をデータベース指定なしで実行できるようにしました。この場合、すべてのデータベースに対して `KILL` を実行します。([#1317])
    * ヘルスチェッククエリは、`SELECT 1`ではなく空のクエリを送信するようにデフォルトで設定されています。 ([#1233])
    * PAMキューが満杯になったことを警告としてログ出力する。これにより、この原因で遅延が発生しているクエリの原因を特定しやすくなる。([#1297])
    *  `RELOAD` コマンドは、再読み込み中に発生したエラーを報告するようになりました。([#1231])
    * シャットダウン中に管理者接続用に PgBouncer の UNIX ソケットへのアクセスを有効化します。これにより、オペレーターが PgBouncer プロセスがシャットダウンしない原因を確認しやすくなり、スタックした接続に対して手動で `KILL_CLIENT` を実行できるようになります。([#1305])
    * `mkauth.py` を変更して、不要な第三フィールドを追加しなくなるようにする ([#1365])
    *  `FATAL` メッセージを `disconnect_client` および `disconnect_server` 関数で改善しました。 ([#1382])
    * 非推奨となった OpenSSL 関数 `EVP_PKEY_get0_EC_KEY` の使用を停止してください。これにより、特定の FIPS 実装で問題が発生する可能性があります。([#1384])
- 修正内容
    * 長さ 1024 文字以上のパスワードを含むクラッシュを修正しました。([#1215])
    * 複数ホスト接続を `server_tls_sslmode=verify-full` を使用する際に修正しました。 ([#1303])
    * キャンセル要求を転送する際の稀な `FATAL` エラーを修正しました。([#1383])
    * パラメータの並べ替えを `SHOW CONFIG` で修正しました。([#1403])
    * スタートアップパケットの解析を強化します。([#1407])

[#731]: https://github.com/pgbouncer/pgbouncer/pull/731
[#1191]: https://github.com/pgbouncer/pgbouncer/pull/1191
[#1215]: https://github.com/pgbouncer/pgbouncer/pull/1215
[#1231]: https://github.com/pgbouncer/pgbouncer/pull/1231
[#1233]: https://github.com/pgbouncer/pgbouncer/pull/1233
[#1242]: https://github.com/pgbouncer/pgbouncer/pull/1242
[#1264]: https://github.com/pgbouncer/pgbouncer/pull/1264
[#1297]: https://github.com/pgbouncer/pgbouncer/pull/1297
[#1303]: https://github.com/pgbouncer/pgbouncer/pull/1303
[#1305]: https://github.com/pgbouncer/pgbouncer/pull/1305
[#1317]: https://github.com/pgbouncer/pgbouncer/pull/1317
[#1338]: https://github.com/pgbouncer/pgbouncer/pull/1338
[#1339]: https://github.com/pgbouncer/pgbouncer/pull/1339
[#1352]: https://github.com/pgbouncer/pgbouncer/pull/1352
[#1359]: https://github.com/pgbouncer/pgbouncer/pull/1359
[#1365]: https://github.com/pgbouncer/pgbouncer/pull/1365
[#1382]: https://github.com/pgbouncer/pgbouncer/pull/1382
[#1383]: https://github.com/pgbouncer/pgbouncer/pull/1383
[#1384]: https://github.com/pgbouncer/pgbouncer/pull/1384
[#1403]: https://github.com/pgbouncer/pgbouncer/pull/1403
[#1407]: https://github.com/pgbouncer/pgbouncer/pull/1407

--------

## PgBouncer 1.24.x {#pgbouncer-124x}

**2025-04-16  -  PgBouncer 1.24.1  -  "CVE-2025-2291 VALID UNTIL yesterday**

- セキュリティ
  * CVE-2025-2291 の修正：以前、PgBouncer は auth_query を使用してパスワードハッシュを照会する際に、ユーザーのパスワードの VALID UNTIL を考慮していませんでした。したがって、Postgres の前に透明なプロキシとして PgBouncer を使用している場合、すでに有効期限が切れたパスワードが許可される可能性がありました。この問題を解決するため、デフォルトの auth_query およびドキュメント内のカスタム auth_query 関数の例が、VALID UNTIL を考慮するように変更されました。カスタム auth_query を使用している場合は、それに合わせて更新してください。デフォルトの auth_query を使用している場合、PgBouncer 1.24.1 にアップグレードするか、以前のバージョンの PgBouncer で設定を変更して新しいデフォルトの auth_query を使用できます。

- 修正
  * PAM 認証を修正するために、HBA ファイル内の `pam` 認証サポートを元に戻してください。([#1291]) (1.24.0 で導入されたバグ)
  * ユーザ接続数を減算する際のバグを修正しました。この修正は GitHub のタグ 1.24.0 に含まれていましたが、リリース用の tarball にはこの修正が含まれていませんでした。 ([#1238]) (1.24.0 で導入されたバグ)
  * `test_load_balance_hosts.py` をリリース tarball に追加しました。([#1282])
  * テストの問題を修正し、Debian パッケージャーがテストを実行できるようにします。([#1266], [#1250])

- ドキュメント
  * `auth_query` で安全な `search_path` を設定する例を更新しました。([#1245])

[#1238]: https://github.com/pgbouncer/pgbouncer/pull/1238
[#1291]: https://github.com/pgbouncer/pgbouncer/pull/1291
[#1282]: https://github.com/pgbouncer/pgbouncer/pull/1282
[#1266]: https://github.com/pgbouncer/pgbouncer/pull/1266
[#1250]: https://github.com/pgbouncer/pgbouncer/pull/1250
[#1245]: https://github.com/pgbouncer/pgbouncer/pull/1245

**2025-01-10  -  PgBouncer 1.24.0  -  "New year, new bouncer**

- 機能
  * systemd 用に `Type=notify-reload` をサポート。この機能には systemd バージョン 253 以降が必要です。([#1148])
  * 管理コンソールに `KILL_CLIENT` コマンドを追加します。これにより、クライアント接続を強制的に終了できます。([#1147])
  * にグローバルおよびユーザー単位で `max_user_client_connections` 設定を追加します。([#1137])
  * に `max_db_client_connections` 設定を、グローバルレベルおよびデータベースレベルで追加します。([#1138])
  * `current_client_connections`カウンタを`SHOW USERS`および`SHOW DATABASES`の出力に追加します。([#1137], [#1138])
  * に `load_balance_hosts` パラメータを追加し、ホスト間のロードバランシングを**行わない**ようにサポートします。([#736])
  * で準備済みステートメントの使用カウンタを `SHOW STATS` に公開する。([#1192])
  * に `client_idle_timeout` 設定を追加します。 ([#1189])
  * ユーザーレベルで `query_timeout` および `reserve_pool_size` を追加します。 ([#1180], [#1228])
  * HBA ファイルで `pam` 認証サポートを有効化します。([#326])

- 変更
  * RELOAD の際、TLS 設定が変更されていない場合は接続を再利用しない。以前は TLS 接続がある場合、すべての接続が RELOAD で再利用され、一時的に深刻なパフォーマンス低下を引き起こしていた。現在は TLS 設定が実際に変更された場合にのみ、この再利用が行われる。([#1157])
  * プリペアドステートメントのサポートをデフォルトで有効化し、`max_prepared_statements` のデフォルト値は now 200 に設定されています。このデフォルト値の変更は、実際にプリペアドステートメントを使用するクライアントにのみ影響します。プリペアドステートメントを使用する場合は、[ドキュメント][prepared-docs] でプリペアドステートメントサポートの制限事項について確認することを推奨します ([#1144])
  * ソケット/クライアント/サーバーは、管理者出力で一意の ID で識別できるようになりました。以前はポインタで識別されていましたが、切断後に新しいクライアントがそのポインタを再利用することがよくありました。([#1172])
  * pidfile が空の場合のエラーを明確にしました。([#1195])
  * クライアントに `server_login_retry` の障害発生時に元のエラーを返します。([#1152])
  * エラーが `auth_query` から発生した場合、元のサーバーのエラーをログに記録します。 ([#1187])
  * `default_pool_size` を 0 に設定すると、サイズ制限なしになります。([#1227])
  * データベース用の `reserve_pool` 設定の名前を `reserve_pool_size` に変更します。以前の名前は新しい名前の別名として引き続き使用可能です。([#1232])

- 修正
  * メモリ不足（OOM）エラーを含む、まれなエラー状況をより適切に処理するように改善しました。これにより、以前はクラッシュやメモリリークを引き起こしていた状況が軽減されました。([#1108], [#1101], [#1099], [#1169], [#1202])
  * サンプル構成ファイルにおける `server_tls_sslmode` のデフォルト値を修正。([#1133])
  * ドキュメントから無効なエイリアスについての記述を削除しました。(`server_tls_protocols`)[#1155]
  * `auth_query` とレプリケーション接続を併用する際に発生するバグを修正しました。このバグにより、このような設定で接続エラーが発生していました。([#1166])
  * PgBouncer がサーバー設定を構成している間、クライアントのキャンセル要求を無視します。 ([#298])

[prepared-docs]: /ja/docs/pgbouncer/config/#max_prepared_statements

[#1148]: https://github.com/pgbouncer/pgbouncer/pull/1148
[#1147]: https://github.com/pgbouncer/pgbouncer/pull/1147
[#1137]: https://github.com/pgbouncer/pgbouncer/pull/1137
[#1138]: https://github.com/pgbouncer/pgbouncer/pull/1138
[#736]: https://github.com/pgbouncer/pgbouncer/pull/736
[#1192]: https://github.com/pgbouncer/pgbouncer/pull/1192
[#1189]: https://github.com/pgbouncer/pgbouncer/pull/1189
[#1180]: https://github.com/pgbouncer/pgbouncer/pull/1180
[#1228]: https://github.com/pgbouncer/pgbouncer/pull/1228
[#326]: https://github.com/pgbouncer/pgbouncer/pull/326
[#1157]: https://github.com/pgbouncer/pgbouncer/pull/1157
[#1144]: https://github.com/pgbouncer/pgbouncer/pull/1144
[#1172]: https://github.com/pgbouncer/pgbouncer/pull/1172
[#1195]: https://github.com/pgbouncer/pgbouncer/pull/1195
[#1152]: https://github.com/pgbouncer/pgbouncer/pull/1152
[#1187]: https://github.com/pgbouncer/pgbouncer/pull/1187
[#1227]: https://github.com/pgbouncer/pgbouncer/pull/1227
[#1232]: https://github.com/pgbouncer/pgbouncer/pull/1232
[#1108]: https://github.com/pgbouncer/pgbouncer/pull/1108
[#1101]: https://github.com/pgbouncer/pgbouncer/pull/1101
[#1099]: https://github.com/pgbouncer/pgbouncer/pull/1099
[#1169]: https://github.com/pgbouncer/pgbouncer/pull/1169
[#1202]: https://github.com/pgbouncer/pgbouncer/pull/1202
[#1133]: https://github.com/pgbouncer/pgbouncer/pull/1133
[#1155]: https://github.com/pgbouncer/pgbouncer/pull/1155
[#1166]: https://github.com/pgbouncer/pgbouncer/pull/1166
[#298]: https://github.com/pgbouncer/pgbouncer/pull/298

--------

## PgBouncer 1.23.x {#pgbouncer-123x}

**2024-08-02  -  PgBouncer 1.23.1  -  「すべてが整然と戻された」**

- 修正
  * PgBouncer が設定を再読み込みした後に発生する可能性のあるセグメンテーションフォールトを修正しました。([#1105]) (1.23.0 で導入されたバグ)
  * 既知の put_in_order のクラッシュをすべて修正しました。([#1120])
    (1.23.0 で新たなクラッシュが導入されました)
  * テストに必要なファイルをリリース用 tarball に追加してください。
    ([#1124]) (これらのファイルは 1.23.0 で導入されました)

[#1120]: https://github.com/pgbouncer/pgbouncer/pull/1120
[#1105]: https://github.com/pgbouncer/pgbouncer/pull/1105
[#1124]: https://github.com/pgbouncer/pgbouncer/pull/1124

**2024-07-03  -  PgBouncer 1.23.0  -  "Into the new beginnings**

- 機能
  * ローリング再起動のサポートを追加しました。SIGTERM はもはや PgBouncer プロセスの即時シャットダウンを引き起こしなくなりました。代わりに「スーパー安全シャットダウン」を実行します。すべてのクライアントが切断されるのを待ってからシャットダウンを行います。新しい SIGTERM の振る舞いにより、ロードバランサーの背後にある複数の PgBouncer プロセスのローリング再起動、または `so_reuseport` で同じポートをリッスンしている場合の再起動が可能になります。これは **マイナーな破壊的変更** です。Dockerfile や Systemd サービスファイルで旧来の SIGTERM の振る舞いに依存していた場合は、今後は SIGQUIT を使用する必要があります。([#902])
  * `cert`および`peer`認証方法に対するユーザー名マップのサポートを追加しました。
      この機能により、接続を開始するユーザーがデータベースユーザーでなくてもよい柔軟性が得られます。
      PgBouncerのユーザー名マップサポートは、ドキュメントに記載された例外を除き、PostgreSQLとほぼ同じ動作をします。([#996])
  * PgBouncer を介したレプリケーション接続のサポートを追加しました。([#876])

- 変更
  * `SHOW USERS`接続の出力リストを改善します。([#1040])
  * ユーザーごとの `pool_size` 設定を許可します。([#1049])
  * データベースごとに `server_lifetime` 設定を許可する。([#1057])
  * `SHOW USERS` の出力で動的に作成されたユーザーを一覧表示する機能を追加しました。([#1052])
  * HBA 設定で `all` アドレス型のサポートを追加しました。([#1078])
  * systemd を使用する際の自動再起動をサポートする。([#1080])
  * c-ares の最低バージョン要件を 1.9.0 に引き上げる ([#1076])

- 修正
  * 大容量および部分的なスタートアップパケットの処理に関する問題を修正しました。([#1058])
  * 起動パラメータの options に `--config=value` 形式のサポートを追加します。([#1064])
  * `avg_wait_time`のメトリクス計算を修正しました。([#727])
  * クライアントとの間でポストグレSQLプロトコルバージョンのネゴシエーションをサポートする。([#1007])
  * に `auth_query` の保留中のリクエストを追加します。 ([#1034])
  * ドキュメントおよびCIの改善を複数実施。

[#996]: https://github.com/pgbouncer/pgbouncer/pull/996
[#1040]: https://github.com/pgbouncer/pgbouncer/pull/1040
[#1049]: https://github.com/pgbouncer/pgbouncer/pull/1049
[#1057]: https://github.com/pgbouncer/pgbouncer/pull/1057
[#1052]: https://github.com/pgbouncer/pgbouncer/pull/1052
[#1058]: https://github.com/pgbouncer/pgbouncer/pull/1058
[#1007]: https://github.com/pgbouncer/pgbouncer/pull/1007
[#876]: https://github.com/pgbouncer/pgbouncer/pull/876
[#902]: https://github.com/pgbouncer/pgbouncer/pull/902
[#1064]: https://github.com/pgbouncer/pgbouncer/pull/1064
[#1078]: https://github.com/pgbouncer/pgbouncer/pull/1078
[#1080]: https://github.com/pgbouncer/pgbouncer/pull/1080
[#727]: https://github.com/pgbouncer/pgbouncer/pull/727
[#1076]: https://github.com/pgbouncer/pgbouncer/pull/1076
[#1034]: https://github.com/pgbouncer/pgbouncer/pull/1034

--------

## PgBouncer 1.22.x {#pgbouncer-122x}

**2024-03-04  -  PgBouncer 1.22.1  -  「バンガロールでは夏だ」**

- 修正
  * クライアントが `COPY FROM STDIN` クエリを使用することによって引き起こされる問題を修正します。このようなクエリはメモリリーク、パフォーマンスの低下、およびプリペアドステートメントの不具合を引き起こす可能性があります。([#1025])
      (1.21.0 で導入されたバグ)
  * リリース用tarボールに欠落しているテストを追加しました ([#1026])
    (欠落していたテストは 1.19.0 および 1.21.0 で導入されました)

[#1025]: https://github.com/pgbouncer/pgbouncer/pull/1025
[#1026]: https://github.com/pgbouncer/pgbouncer/pull/1026

**2024-01-31  -  PgBouncer 1.22.0  -  "DEALLOCATE ALL**

- 機能
  * 、`max_prepared_statements` が非ゼロ値に設定されている場合に `DEALLOCATE ALL` および `DISCARD ALL` をサポートします（通常の `DEALLOCATE` は依然として非対応）([#972])
  * データベースごとに `auth_query` の設定をサポートしています ([#979])

- 変更
  * 推奨される systemd ユニットファイル内の設定を改善しました ([#983])
  * 失敗を速やかに処理するロジックを、データベースへの接続がすべて失われていて、新たに接続できなくなった状況をすべて処理するように修正しました ([#998])
  * 複数のドキュメント改善

- 修正
  * トランザクションごとに PG14+ が `SET DateStyle='ISO'` を送信する問題を修正しました ([#879])
  * 空の `application_name` の処理を修正しました ([#999])
  * Windows で OpenSSL 3.2.0 を使用したビルドを修正しました ([#1009])

[#972]: https://github.com/pgbouncer/pgbouncer/pull/972
[#979]: https://github.com/pgbouncer/pgbouncer/pull/979
[#983]: https://github.com/pgbouncer/pgbouncer/pull/983
[#998]: https://github.com/pgbouncer/pgbouncer/pull/998
[#879]: https://github.com/pgbouncer/pgbouncer/pull/879
[#999]: https://github.com/pgbouncer/pgbouncer/pull/999
[#1009]: https://github.com/pgbouncer/pgbouncer/pull/1009

--------

## PgBouncer 1.21.x {#pgbouncer-121x}

**2023-10-16  -  PgBouncer 1.21.0  -  「プリペアドステートメント対応版」**

- 機能
  * プロトコルレベルの名前付き準備ステートメントをサポートしました！これは PgBouncer で最も要望の多かった機能の一つです。準備ステートメントを PgBouncer と併用することで、システムの CPU 負荷を大幅に削減できます（PgBouncer 側および PostgreSQL 側の両方で）。合成ベンチマークでは、ワークロードによってはクエリスループットを 15% から 250% まで向上させることが確認されています。この新機能の恩恵を受けるには、新しい `max_prepared_statements` 設定を 0 以外の値に変更する必要があります（正確な値はワークロードによりますが、100 が妥当な値である可能性があります）。この機能の動作方法、制限事項、および値のチューニング方法については、[`max_prepared_statements`](/ja/docs/pgbouncer/config/#max_prepared_statements) のドキュメントを参照してください。設定後は、クライアントライブラリが実際に準備ステートメントを使用していることを確認する必要があります。その方法は各クライアントごとに異なりますので、使用しているクライアントのドキュメントを確認してください。この機能はリリース前に十分なテストを実施していますが、機能の複雑さからパフォーマンス上の問題やバグが存在する可能性は十分にあります。そのような問題を発見した場合は、報告してください。([#845])

- 変更
  * OpenSSL の設定のセキュリティを向上させました。従来のデフォルト値は非常に古く、不適切でした。
      このリリースでは、デフォルト値を、PgBouncer を実行しているシステムの OpenSSL のデフォルト値と同一にしました。([#948] & [libusual/#41])
  * PgBouncer は、可能な限り OpenSSL を使用して MD5 ハッシュを計算するようになりました。これは PgBouncer を FIPS 準拠の方法で使用するために必要です。([#949])
  * クライアントが接続されていなくても、強制ユーザーを設定したプールに対しては `min_pool_size` を維持する ([#947])
  * PgBouncer がキャンセルトークンに `peer_id` をエンコードする方法が変更されたため、バージョン 1.21.0 の境界をまたぐ異なる PgBouncer バージョン間でのピアリングは、すべてのバージョンが同じ側にない限り動作しません。([#945])

- 修正
  * 1.18.0 で導入されたバグにより、エラーメッセージ "FATAL in function client_proto(): bad client state: 6/7" が発生する問題を修正しました ([#928])
  * 1.18.0 で導入されたバグにより、エラーメッセージ "FATAL in function server\_proto(): server in bad state: 11" が発生する問題を修正しました ([#927])
  * キャンセル送信のログレベルを低減する ([#903])
  * peers のログプレフィックスを slog で修正 ([#922])
  * ドキュメントのタイポを修正しました ([#932])
  * 静的解析器が指摘したエラーを修正しました ([#943])
  * ログイン中に一時的な FATAL エラーが発生しても、待機中のすべてのクライアントを終了しないようにする ([#946])
  * 、`auth_dbname` でデータベースが明示的に設定されていない場合、自動データベース機能を使用する。
    ([#921])

- クリーンアップ
  * udns のサポートを削除しました ([#938])

[#845]: https://github.com/pgbouncer/pgbouncer/pull/845
[#948]: https://github.com/pgbouncer/pgbouncer/pull/948
[#949]: https://github.com/pgbouncer/pgbouncer/pull/949
[#947]: https://github.com/pgbouncer/pgbouncer/pull/947
[#945]: https://github.com/pgbouncer/pgbouncer/pull/945
[#903]: https://github.com/pgbouncer/pgbouncer/pull/903
[#922]: https://github.com/pgbouncer/pgbouncer/pull/922
[#932]: https://github.com/pgbouncer/pgbouncer/pull/932
[#928]: https://github.com/pgbouncer/pgbouncer/pull/928
[#927]: https://github.com/pgbouncer/pgbouncer/pull/927
[#943]: https://github.com/pgbouncer/pgbouncer/pull/943
[#946]: https://github.com/pgbouncer/pgbouncer/pull/946
[#921]: https://github.com/pgbouncer/pgbouncer/pull/921
[#938]: https://github.com/pgbouncer/pgbouncer/pull/938
[libusual/#41]: https://github.com/libusual/libusual/pull/41

--------

## PgBouncer 1.20.x {#pgbouncer-120x}

**2023-08-09  -  PgBouncer 1.20.1  -  「オプションの設定」**

- 修正
  * 1.20.0 で導入されたバグ修正の再現を修正しました。`options` を `ignore_startup_parameters` 内に配置した場合、`options` スタートアップパラメータ内に含まれる未知のパラメータを無視しなくなる問題を解消しました。([#908])
  * ドキュメント内の誤ったタイプミスを修正しました ([#917])

[#908]: https://github.com/pgbouncer/pgbouncer/pull/908
[#917]: https://github.com/pgbouncer/pgbouncer/pull/917

**2023-07-20  -  PgBouncer 1.20.0  -  "A funny name goes here**

- 非推奨事項
  * オンライン再起動オプションはもはや非推奨とされています。近年はほとんど開発が行われていません。この機能には複数の既知の問題があり、新しく追加された機能の多くはこれをサポートしていません。現在、オンライン再起動を行う推奨方法は、`so_reuseport` および `peers` 機能を使用することです。これにより、同じポート上で複数の異なる PgBouncer プロセスを実行できます。その後、これらのプロセスを1つずつ再起動することで、常に目的のポートで PgBouncer プロセスがリスニングしていることを保証できます。([#894])

- 機能
  * トランザクションプーリングモードでより多くのパラメータを追跡できるようにする `track_extra_parameters` を導入しました。以前は PgBouncer は `application_name`、`DateStyle`、`TimeZone` および `standard_conforming_strings` のみを追跡していました。現在はデフォルトで `IntervalStyle` も追跡するようになっています。また、`track_extra_parameters` を変更することで、さらに多くの設定を追跡できますが、[PostgreSQL がクライアントに報告するもの][guc_report] に限られます。Citus 12.0+ を使用している場合、Citus が PostgreSQL が `search_path` をクライアントに報告するよう保証します。したがって、Citus を使用する場合は `search_path` を `track_extra_parameters` 設定に追加できます。([#867])
  * 認証フェーズで SQLSTATE を転送する。これにより、データベースが存在しないことを検出可能となり、Npgsql（PostgreSQL の .NET データプロバイダ）で利用される。([#814])
  * デフォルト `server_tls_sslmode` を `prefer` に変更します。 ([#866])
  * `options` パラメータをサポートしました。これにより、[`PGOPTIONS` 環境変数を用いることが可能になります。`psql` および `libpq` が認識しているもの][pgoptions]。この変数を使用することで、起動時に任意の PostgreSQL パラメータを設定できます。これは `track_extra_parameters` を通じて PgBouncer が追跡する PostgreSQL パラメータに限られます。([#878])

- 修正
  * `pgbouncer` が auth_dbname として使用された場合にクラッシュしないようにしました。まだサポートされていませんが、クラッシュする代わりに明確なエラーが表示されるようになりました。([#817])
  * `peer_cache` の名前を `SHOW MEM` で修正しました。以前は `db_cache` として正しく表示されていませんでした。([#864])
  * ログ内のソース/宛先の混同を修正しました。PgBouncer は宛先IPを意図していたのに、ソースIPをログに記録していました。([#880])
  * UNIX ソケット経由の管理者接続ログは、`log_connections` が `1` に設定されている場合にのみ出力する。 ([#883])

[guc_report]: https://www.postgresql.org/docs/15/protocol-flow.html#PROTOCOL-ASYNC
[pgoptions]: https://www.postgresql.org/docs/current/config-setting.html#id-1.6.7.4.5
[#867]: https://github.com/pgbouncer/pgbouncer/pull/867
[#814]: https://github.com/pgbouncer/pgbouncer/pull/814
[#866]: https://github.com/pgbouncer/pgbouncer/pull/866
[#878]: https://github.com/pgbouncer/pgbouncer/pull/878
[#817]: https://github.com/pgbouncer/pgbouncer/pull/817
[#864]: https://github.com/pgbouncer/pgbouncer/pull/864
[#880]: https://github.com/pgbouncer/pgbouncer/pull/880
[#883]: https://github.com/pgbouncer/pgbouncer/pull/883
[#894]: https://github.com/pgbouncer/pgbouncer/pull/894

--------

## PgBouncer 1.19.x {#pgbouncer-119x}

**2023-05-31  -  PgBouncer 1.19.1  -  "Sunny Spring**

これは最近導入されたバグを修正するマイナーリリースです：

- 修正
  * 修正: 関数 disconnect_client() で FATAL が発生: クライアントの状態が無効: 0 ([#846])
    (1.18.0 で導入されたバグ)
  * 修正: 関数 server_proto() で FATAL: サーバーが異常状態: 14 ([#849])
    (1.18.0 で導入されたバグ)
  * Python によるテストを実行するのに必要なファイルをリリース用ターボールに追加しました ([#852])
    (1.19.0 で導入された新しいテスト)

[#846]: https://github.com/pgbouncer/pgbouncer/pull/846
[#849]: https://github.com/pgbouncer/pgbouncer/pull/849
[#852]: https://github.com/pgbouncer/pgbouncer/pull/852

**2023-05-04  -  PgBouncer 1.19.0  -  「昔ながらの、人間が手作業で生成するタイプ」**

- 機能
  * に `auth_dbname` オプションを追加し、`auth_query` を実行する対象のデータベースを指定します。([#764])
  * `SHOW STATE` コマンドを追加し、PgBouncer がアクティブ、一時停止中、または一時停止状態かどうかを表示します。([#528])
  * PgBouncer プロセス間のピアリングをサポートしました。これにより、複数の異なる PgBouncer プロセスが単一のロードバランサーの背後にある場合でも、キャンセルリクエストが正常に動作し続けるように設定できるようになります。([#666])
  * 専用の `cancel_wait_timeout` 設定を追加し、キャンセル要求の転送を放棄するまでの時間を決定します。デフォルトは 10 秒です。([#833])
  * 新しいテストフレームワーク ([#792])

- 修正
  * TLSハンドシェイクの失敗時に可能性のあるメモリリークを修正しました。([#796])
  * Windows でのサポートされていないコマンドラインオプションに対して、より正確なエラーメッセージを表示する。([#620])
  * サーバーが `BEING_CANCELED` 状態にあるときに `disconnect_server` を呼び出す問題を修正しました。 ([#815]) (1.18.0 で導入)
  * `SIGTERM` が受信されたときに非ゼロステータスで終了しないでください。([#834])
  * 起動時に `unix_socket_dir` でソケットの作成に失敗した場合は、強制的に終了する。 ([#830])
  * 起動時に `listen_addr` のアドレスのいずれもリスンできなかった場合、強制的に失敗する。 ([#838])
  * `sbuf_connect` が失敗したときに、より詳細な情報を持つ警告メッセージを出力する。特に Unix ソケットの作成に失敗した際に有用である。([#837])

- クリーンアップ
  * パフォーマンス向上のための各種 CI の更新
  * AppVeyor を削除

[#528]: https://github.com/pgbouncer/pgbouncer/issues/528
[#620]: https://github.com/pgbouncer/pgbouncer/pull/620
[#666]: https://github.com/pgbouncer/pgbouncer/pull/666
[#764]: https://github.com/pgbouncer/pgbouncer/pull/764
[#792]: https://github.com/pgbouncer/pgbouncer/pull/792
[#796]: https://github.com/pgbouncer/pgbouncer/pull/796
[#815]: https://github.com/pgbouncer/pgbouncer/pull/815
[#830]: https://github.com/pgbouncer/pgbouncer/pull/830
[#833]: https://github.com/pgbouncer/pgbouncer/pull/833
[#834]: https://github.com/pgbouncer/pgbouncer/pull/834
[#837]: https://github.com/pgbouncer/pgbouncer/pull/837
[#838]: https://github.com/pgbouncer/pgbouncer/pull/838

--------

## PgBouncer 1.18.x {#pgbouncer-118x}

**2022-12-12  -  PgBouncer 1.18.0  -  「実に明白なこと」**

- 機能
  * `application_name` を `SHOW CLIENTS`/`SERVERS`/`SOCKETS` に追加
    出力 ([#449](https://github.com/pgbouncer/pgbouncer/pull/449))
  * キャンセル要求に関する情報を `SHOW
    CLIENTS `/` SERVERS `/` POOLS` 出力に追加
    ([#782](https://github.com/pgbouncer/pgbouncer/pull/782))

- 修正
  * 宛先ソケットが閉じられている場合、`sbuf_send_pending` 操作を失敗させる
    ([#652](https://github.com/pgbouncer/pgbouncer/pull/652))
  * いくつかの可能性のあるクラッシュを修正
    ([#700](https://github.com/pgbouncer/pgbouncer/pull/700)、
    [#730](https://github.com/pgbouncer/pgbouncer/pull/730))
  * コンマ区切りホストリスト機能におけるオーバーフローバグの修正により、
    接続がUnixソケットに再ルーティングされる問題が解消されました
    ([#747](https://github.com/pgbouncer/pgbouncer/pull/747))
  * 接続を解放して `min_pool_size` を達成するべきではありません
    ([#648](https://github.com/pgbouncer/pgbouncer/pull/648))
  * PostgreSQL 15 での `SHOW HELP` の修正
    ([#769](https://github.com/pgbouncer/pgbouncer/issues/769))
  * クライアントのクエリキャンセル処理におけるレースコンディションを修正しました。
      あるクライアントのクエリキャンセル要求が、別のクライアントのクエリをキャンセルする可能性がありました。
      これは、PgBouncer がクエリのキャンセルを意図していたクライアントのクエリがすでに自身で完了していた場合に発生する可能性がありました。
      ([#717](https://github.com/pgbouncer/pgbouncer/pull/717))

- クリーンアップ
  * さまざまな CI の更新

--------

## PgBouncer 1.17.x {#pgbouncer-117x}

**2022-03-23  -  PgBouncer 1.17.0  -  「一線が引かれた」**

- 機能
  * データベース定義では、コンマ区切りのホストリストを指定できます。
      ホストはラウンドロビン方式で接続されます。
  * 非存在のデータベースに接続する場合、エラー（"no such database"）が認証後に報告されるようになりました。これにより、認証されていないクライアントが存在するデータベースを調べるのを防ぎます。（これはバージョン 1.15.0 でユーザーが存在しない場合に認証後にエラーを報告する変更と同様です。）
  * ログイン前にクライアントにサーバー切断エラーを送信しないでください。
      これは、ログインしていないクライアントに、設定情報など公開されていない情報を漏らす可能性があります。
  * パスワード長を再度最大値に増加します。明らかに、前回の増加では長期間にわたって十分ではなかったようです。
  * 自動的な `auth_file` 再読み込みを削除しました。`auth_file` は設定ファイルの再読み込み時のみ再読み込みされ、変更された直後に自動的に再読み込みされるようではありません。
  * Windows ビルドには、バージョン情報リソースファイルが含まれるようになりました。
  * Windows で CI によって作成されたビルドはもはや静的リンクされているため、依存関係を必要とせずに直接使用できます。

- 修正
  * OpenSSL 3 のサポートが修正されました。以前のリリースではクラッシュしていました。
  * 接続時に迅速な失敗を適用しない。これは、認証前にサーバーのエラーを報告しないという前述の変更の一部である。また、SCRAM パススルー認証における特定の状況を修正する。この状況では、クライアント側の認証交信を許可して、再認証によりサーバー側の接続を修正できるようにする必要がある。迅速な失敗メカニズムは認証直後には依然として適用されるため、ほとんどの状況では実際の観察される動作は同じになる。
  * サンプル `pgbouncer.ini` における `auth_type` を `md5` に変更し、組み込みのデフォルトと一致させます。このファイルをデフォルトの設定ファイルとして展開する場合があるため、変更後の設定がご自身の環境に適しているか確認してください。
  * アサート有効ビルドでの終了時クラッシュを修正。
  * `tcp_defer_accept` のドキュメントおよび動作を改善しました。
      デフォルト値についてのドキュメントは誤りがあり、誤解を招く内容でした。
      一部のケースでは、「show config」で誤った値が表示されていました。
      また、設定はされているがサポートされていない場合、無視するのではなくエラーを発生させるようにしました。
      これは、他のプラットフォーム固有のソケットオプションと同様の処理です。
  * Windows での c-ares によるビルドを修正。Windows では c-ares >=1.18.0 が必須になりました。

- クリーンアップ
  * Autoconf 2.70 以降の大部分の非推奨警告が削除されました。古い Autoconf のバージョンも引き続きサポートされています。
  * Cirrus CI の利用が、より多くのプラットフォームに拡張されました。
  * Travis CI のサポートは削除されました。
  * デフォルトのルートCAファイルを検索する場所を更新し、Fedora/RHEL/CentOSなど、より多くのプラットフォームをカバーする。
  * Python スクリプトはすべて、デフォルトで `python3` を使用するようになりました。Python 2 互換性はもはや維持されません。
  * テストスクリプトは、非推奨となった `which` の代わりに `command -v` を使用しています。
  * いくつかのエラーメッセージを再構成し、それらがどのコマンドや設定項目に関連しているかが明確になるようにしました。
  * テストスクリプトはもはや GNU sed を必要としなくなりました。
  * `make check` は Windows でも動作します（ただし SSL テストスイートはまだ対応していません）。
  * 管理コンソールはシンプルなクエリプロトコルのみをサポートしており、この点に関するより良いエラーメッセージを提供します。

--------

## PgBouncer 1.16.x {#pgbouncer-116x}

**2021-11-11  -  PgBouncer 1.16.1  -  「静かさの効率性に対する深さのテスト」**

これはセキュリティ修正を含むマイナーリリースです。

* PgBouncer をサーバーとして動作させ、SSL または GSS 暗号化ハンドシェイク後に不要なデータを拒否する。

中間者攻撃者がTCP接続にデータを挿入できる場合、暗号化保護されたデータベースセッションの開始部分に平文データを注入できる可能性があります。この攻撃は、PgBouncerが認証データを要求しない設定の場合に、サーバーに偽のSQLコマンドを送信する目的で悪用される可能性があります。（ただし、SSL証明書認証に依存するPgBouncerの設定では、この攻撃が成立しない可能性があります。）（CVE-2021-3935）

**2021-08-09  -  PgBouncer 1.16.0  -  「ジャガーを撃退」**

- 機能
  * TLS 設定のホットリロードをサポートします。設定ファイルを再読み込みすると、変更された TLS 設定が自動的に有効になります。
  * 抽象的な Unix ドメインソケットをサポート。
      Unix ドメインソケットのパスの前に `@` を付けることで、抽象名前空間内のソケットを使用できます。
      これは PostgreSQL 14 の対応機能と一致します。
  * パスワードとユーザー名の最大長はそれぞれ 996 および 128 に増加されました。さまざまなクラウドサービスでこの要件が求められます。
  * データベースごとに最小プールサイズを設定できるようになりました。これは通常のプールサイズおよび予約プールサイズと同様です。
  * 保留中のクエリキャンセルの数は `SHOW
    POOLS` に表示されます。

- 修正
  * 設定パースでは、多くの場所でより厳密なエラー処理が導入されました。以前はエラーをログに記録して続行していた場所でも、設定エラーは現在、起動失敗を引き起こすようになっています。これは常にそうすべきだったはずですが、一部のコードでは正しく処理されていませんでした。一部のユーザーは、これまでずっと不正な設定を使用していたことに気づき、もはや動作しなくなるかもしれません。
  * クエリのキャンセル処理が修正されました。一部の状況下では、キャンセル要求が長時間スタックするように見えました。これにより、もはや発生しなくなります。実際、キャンセル要求はプールサイズの2倍まで超過可能となり、スタックする心配はほとんどありません。 ([#542](https://github.com/pgbouncer/pgbouncer/pull/542), [#543](https://github.com/pgbouncer/pgbouncer/pull/543))
  * HBA を介した md5 と scram の混在使用が修正されました。
  * Windows での c-ares を使用したビルドが修正されました。
  * 「FIXME: クエリの終了だが query_start == 0」メッセージは解消されました。発生原因が判明し、これ以上表示されないはずです。([#565](https://github.com/pgbouncer/pgbouncer/pull/565))
  * 再読み込みを修正しました。`default_pool_size`、`min_pool_size`、および `res_pool_size` を再読み込みしても、以前は機能していませんでした。

- クリーンアップ
  * Cirrus CI は now
    [使用](https://cirrus-ci.com/github/pgbouncer/pgbouncer) され
    代わりに Travis CI が使用されません。
  * 通常通り、多数のテストが追加されています。
  * 「unclean server」のログメッセージを若干明確化しました。現在は、「クライアントがサーバーが準備できていない間に切断された」または「クライアントがサーバーへのすべてのデータ送信前に切断された」と表示されます。後者は、サーバーでトランザクションブロックが開いている状態でクライアント接続が閉じられた場合に発生し、一部のユーザーを混乱させていた問題です。
  * 「pgbouncer」をデータベース名として使用できなくなりました。この名前は管理コンソール用に予約されており、通常のデータベース名として使用しても正しく動作していませんでした。これにより、明示的に禁止されています。
  * 接続が閉じられる前にクライアントに送信されるエラーは、もはや単に ERROR ではなく FATAL としてラベル付けされるようになりました。これにより、一部のクライアントが以前は混乱していた問題が解消されました。 ([#564](https://github.com/pgbouncer/pgbouncer/pull/564))
  * GCC 11 でのコンパイラ警告を修正しました。
    ([#623](https://github.com/pgbouncer/pgbouncer/issues/623))

--------

## PgBouncer 1.15.x {#pgbouncer-115x}

**2020-11-19  -  PgBouncer 1.15.0  -  "Ich hab noch einen Koffer in Berlin**

- 機能
  * 認証失敗の報告を改善しました。認証失敗のメッセージはクライアントに送信される際、失敗したことを示すのみで、詳細は含まれません。詳細は PgBouncer のログで確認できます。また、要求されたユーザーが存在しない場合でも、認証処理は終了まで実行され、同じ汎用的な失敗メッセージになります。これにより、クライアントが PgBouncer インスタンスに対してユーザー名や認証関連の情報を探るのを防ぎます。これは PostgreSQL の動作と同様です。
  * クライアントが即座に切断された場合、何もログに出力しない。モニタリングシステムがTCP/IP接続を開くだけで、データを送信せずに切断する場合にログの雑多な出力を防ぐためである。
  * systemd ジャーナルを使用する場合は、ログ出力に systemd ジャーナルを利用します。標準エラー出力が systemd ジャーナルに送信されることが検出された場合、ログ出力に systemd のネイティブ関数を使用します。これにより、タイムスタンプや PID の重複出力が回避され、ログが若干きれいになります。また、ログに重大度などのメタデータが追加されるため、ジャーナルが syslog に転送された場合でも、メッセージに有用なメタデータが付与されます。
  * テストスイートの一部は now Windows で実行できるようになりました。
  * `SHOW CONFIG` は設定のデフォルト値も表示するようになりました。

- 修正
  * FreeBSD で `so_reuseport` オプションを修正しました。PgBouncer 1.12.0 の元のコードは FreeBSD では実際に動作していませんでした。 ([#504](https://github.com/pgbouncer/pgbouncer/pull/504))
  * 1.14.0 で破損した、古い systemd バージョンを搭載したシステムでのコンパイルを修復しました。
      ([#505](https://github.com/pgbouncer/pgbouncer/issues/505))
  * Windows用バイナリzipパッケージをビルドするmakefileターゲットを修復しました。
  * 長時間のコマンドラインオプションは、Windowsでも現在動作します。
  * `auth_user` 設定の動作を修正しました。従来の動作は、設定ファイル内の順序に依存していたため、混乱しやすく脆弱でした。これ以上はそのような状態にはなりません。([#391](https://github.com/pgbouncer/pgbouncer/issues/391), [#393](https://github.com/pgbouncer/pgbouncer/issues/393))

- クリーンアップ
  * テストの安定性と移植性を向上させます。
  * Autoconf 関連のコードを現代化する。
  * OpenSSL 3.0.0 からの非推奨コンパイラ警告を無効化します。

--------

## PgBouncer 1.14.x {#pgbouncer-114x}

**2020-06-11  -  PgBouncer 1.14.0  -  "La ritrovata magia**

- 機能
  * SCRAM 認証のパススルーを追加します。これにより、PgBouncer 内で `userlist.txt` または `auth_query` から取得した暗号化された SCRAM シークレットを使用してサーバーにログインできます。
  * systemd のソケット活性化をサポートしました。これは、`/var/run/postgresql` へのアクセスが制限されているシステムで、systemd が Unix ドメインソケットの作成を担当する場合に特に有用です。
  * Windows で Unix ドメインソケットのサポートを追加。

- クリーンアップ
  * テストまたはデプロイ用に、代替の小さな設定ファイルを追加します。
    `pgbouncer-minimal.ini`

--------

## PgBouncer 1.13.x {#pgbouncer-113x}

**2020-04-27  -  PgBouncer 1.13.0  -  "My favourite game**

- 機能
  * 設定キーワード `tcp_user_timeout` を追加し、対応するソケットオプションを設定します。
  * `client_tls_protocols` および `server_tls_protocols` は now default to `secure` となり、TLS 1.2 および TLS 1.3 のみが有効になります。古いバージョンは引き続きサポートされていますが、デフォルトでは有効になっていません。
  * systemd サービス通知をサポートする。現在のところ、これにより `Type=notify` サービスユニットの使用が可能である。今後、より深い統合が計画されている。

- 修正
  * 複数行のログメッセージを修正
    ([libusual #24](https://github.com/libusual/libusual/pull/24))
  * `auth_query` から返される null ユーザ名を適切に処理する
      ([#340](https://github.com/pgbouncer/pgbouncer/pull/340))

- クリーンアップ
  * `debian` にある Debian パッケージファイルは削除されました。
      https://apt.postgresql.org/. からのパッケージを使用することを推奨します。
  * テストスイートにおける多数の修正と改善
  * テストはもはやデフォルトで sudo を使用しようとしません。この機能は、環境変数 `USE_SUDO` を設定することで明示的に有効化できます。
  * libevent API の使用が、バージョン 2 形式のインターフェースを採用し、バージョン 1 で非推奨となったインターフェースの使用をやめました。

--------

## PgBouncer 1.12.x {#pgbouncer-112x}

**2019-10-17  -  PgBouncer 1.12.0  -  「学び、より良くなること」**

このリリースでは、多数の軽微な機能強化および修正が含まれています。

- 機能
  * `SO_REUSEPORT` ソケットオプションを有効にする設定を追加します。一部のオペレーティングシステムでは、同じホスト上で同じポートをリッスンする複数の PgBouncer インスタンスを実行可能となり、カーネルが接続を自動的に分散します。
  * OS とは別個の `resolv.conf` ファイルを使用する設定を追加します。これにより、カスタムの DNS サーバーおよび他の DNS オプションを設定できます。
  * `SHOW VERSION` の出力を通常の結果行として送信し、NOTICE メッセージとして送信しない。これにより、出力の利用が容易になり、他の `SHOW` コマンドと一貫性が保たれる。

- 修正
  * 統計カラムを `numeric` として送信し、`bigint` として送信するのを回避します。これにより、`bigint` の範囲を超える値でクライアントライブラリが失敗するのを防ぎます。([#360](https://github.com/pgbouncer/pgbouncer/pull/360), [#401](https://github.com/pgbouncer/pgbouncer/pull/401))
  * PAM ユーザーがパスワードを失う問題を修正しました。 ([#285](https://github.com/pgbouncer/pgbouncer/issues/285))
  * で SCRAM チャネルバインディングを有効にしたクライアントを受け入れます。以前は、チャネルバインディングをサポートするクライアント（つまり PostgreSQL 11 以降）が、特定の状況下で PgBouncer への接続に失敗していました（PgBouncer はチャネルバインディングをサポートしていません。この変更は、チャネルバインディングを提供するクライアントのサポートを修正するものです）。
  * musl-libc の最新バージョン（Alpine Linux で使用）とのコンパイルを修正。

- クリーンアップ
  * に `make check` のターゲットを追加します。これにより、1 つのコマンドからすべてのテストを実行できるようになります。
  * PostgreSQL wiki への参照を削除しました。すべての情報は now 、PgBouncer のドキュメントまたはウェブサイトにあります。
  * Libevent 1.x のサポートを削除しました。Libevent 2.x が必須です。Libevent の検出は now pkg-config を使用して行われます。
  * macOS および Windows でのコンパイラ警告を修正しました。これらのプラットフォームでのビルドは now 警告が発生しなくなりました。
  * LLVM scan-build からの警告を修正。

--------

## PgBouncer 1.11.x {#pgbouncer-111x}

**2019-08-27  -  PgBouncer 1.11.0  -  "Instinct for Greatness**

- 機能
  * クライアントおよびサーバーに対する SCRAM 認証のサポートを追加しました。新しい認証タイプ `scram-sha-256` が追加されました。
  * 保存されたパスワードが md5 の場合、`auth_type=password` を処理し、PostgreSQL サーバーが行うのと同様に処理します。([#129](https://github.com/pgbouncer/pgbouncer/pull/129))
  * `log_stats` を追加して、統計情報をログに出力しないようにします。 ([#287](https://github.com/pgbouncer/pgbouncer/pull/287))
  * ログタイムスタンプにタイムゾーンを追加します。
  * ログプレフィックスにPIDを[カッコ]で囲んで出力する。
- 修正内容
  * OpenSSL の configure テストを、`-Werror` と互換性がある新しい OpenSSL で実行する際に修正します。
  * `auth_user` における待機時間の計算を修正しました。これにより、待機時間がクラッシュするか、不正な値が報告される問題が解消されました。([#393](https://github.com/pgbouncer/pgbouncer/pull/393))
  * GSSENCRequest パケットの処理。PostgreSQL 12 で追加。現在は何も実行しないが、「不正なパケットヘッダー」という誤ったエラーメッセージを避けるために存在する。
- クリーンアップ
  * テストスイートの多数の改善と、いくつかの新規テスト
  * Windows でのコンパイラ警告を複数修正。
  * `[users]` セクションのドキュメントを拡張し、例の設定ファイルに追加する。 ([#330](https://github.com/pgbouncer/pgbouncer/pull/330))

--------

## PgBouncer 1.10.x {#pgbouncer-110x}

**2019-07-01  -  PgBouncer 1.10.0  -  "Afraid of the World**

- 機能
  * TLS 1.3 の有効化および無効化をサポートする。 (TLS 1.3 はすでに OpenSSL ライブラリに依存してサポートされていたが、今や TLS プロトコルバージョンを選択する設定項目もこれに対応している。)
- 修正
  * TLS 1.3 のサポートを修正しました。これは OpenSSL 1.1.1 および 1.1.1a で破損していました（それ以前や以降では問題ありません）。
  * `SHOW FDS` での稀なクラッシュを修正しました ([#311](https://github.com/pgbouncer/pgbouncer/issues/311))。
  * 多数のキャンセルリクエストが到着した場合、長時間の停止が発生する可能性を修正しました
    ([#329](https://github.com/pgbouncer/pgbouncer/issues/329)).
  * PostgreSQL の再読み込み後に「ログインクエリからの予期しない応答」を回避する
      ([#220](https://github.com/pgbouncer/pgbouncer/issues/220)).
  * `idle_transaction_timeout`の計算を修正
    ([#125](https://github.com/pgbouncer/pgbouncer/issues/125))。
    このバグにより、特定の状況で過剰なタイムアウトが発生していました。
- クリーンアップ
  * さまざまなログおよびエラーメッセージをより明確にします。
  * Coverity で発見された問題を修正しました（実際の運用において重大な影響を及ぼすものはありませんでした）。
  * すべてのテストスクリプトの改善とドキュメント化を実施する。
  * ドキュメントに追加の SHOW コマンドを追加する。
  * ドキュメントを rst から Markdown に変換する。
  * ソースツリー内の Python スクリプトはすべて Python 3 と互換性があります。

--------

## PgBouncer 1.9.x {#pgbouncer-19x}

**2018-08-13  -  PgBouncer 1.9.0  -  "Chaos Survival**

- 機能
  * RECONNECT コマンド
  * WAIT_CLOSE コマンド
  * 即時切断 - セッションプールモードで、サーバーが "close_needed"（再接続）モードにある場合、直ちに接続を切断します。
  * SHOW SERVERS に close_needed 列を追加
- 修正
  * parse_filename における二重解放を回避
  * parse_line での NULL ポインタ参照を回避
- クリーンアップ
  * ポート mkauth.py を Python 3 に移行する
  * シグナルのドキュメントを改善
  * クイックスタートドキュメントの改善
  * Document SET コマンド
  * 必須ソフトウェアのリスト
  * 警告を修正-Wimplicit-fallthrough
  * 各種 SHOW フィールドのドキュメントを追加
  * 再読み込みおよびDNS変更時の再接続動作の説明
  * KILL が実行された後は RESUME が必要なドキュメント
  * サーバーのライフタイムに関するドキュメントを明確化
  * メッセージおよびドキュメント内のスペルミスと大文字小文字の修正
  * テストでの psql 実行を修正
  * その他のテスト環境設定の改善

--------

## PgBouncer 1.8.x {#pgbouncer-18x}

**2017-12-20 - PgBouncer 1.8.1 - "Ground-and-pound Mentality**

- 修正
  * ディストリビューションの tar パッケージに `include/pam.h` を含めるようにした。これにより、1.8 バージョンの tar パッケージがまったくビルドできなくなっていた。

**2017-12-19 - PgBouncer 1.8 - "Confident at the Helm**

- 機能
  * PAM 認証をサポートします。 (有効にするには `--with-pam` を使用してください。)
  * `SHOW DATABASES` の出力に `paused` および `disabled` フィールドを追加します。
  * に `maxwait_us` フィールドを `SHOW POOLS` 出力に追加します。
  * `wait` および `wait_us` フィールドを `SHOW` コマンドの出力に追加します。
  * に新しいコマンド `SHOW STATS_TOTALS` と `SHOW STATS_AVERAGES` を追加します。
  * `SHOW STATS` でクエリとトランザクションを個別に追跡します。`total_requests`、`avg_req`、および `avg_query` フィールドは、新しいフィールドに置き換えられました。
  * に `wait_time` を `SHOW STATS` に追加します。
- 修正内容
  * libusual が OpenSSL 1.1 をサポートするようになりました。
  * Unix ソケット上で TLS を使用しようとしないでください。
  * `pg_hba.conf` を解析する際は、誤った行があってもファイル全体を拒否せず、解析を継続してください。
      ([#118](https://github.com/pgbouncer/pgbouncer/issues/118))
  * その他の HBA パースの修正。
  * クエリのキャンセル時に競合状態を修正。
    ([#141](https://github.com/pgbouncer/pgbouncer/issues/141))
- 整備作業
  * `auth_user` 設定は、データベースごとの設定に加えて、グローバルに指定することも可能になりました。
      ([#142](https://github.com/pgbouncer/pgbouncer/issues/142))
  * 管理コンソールのクライアントおよびサーバーのエンコーディングを `UTF8` に設定します。

--------

## PgBouncer 1.7.x {#pgbouncer-17x}

**2016-02-26  -  PgBouncer 1.7.2  -  "Finally Airborne**

- 修正
  * 古い pidfile の削除時にクラッシュする問題を修正。この問題は 1.7.1 で導入された。
  * クリーンアップを無効化する — これはフェイルオーバーを破壊し、本番負荷では有用でない。1.7.1 で導入された問題。
  * トーキーク後は、pidfileが消えるまで待ってから起動してください。
      メモリクリーンアップによる遅延シャットダウンが、既存のレースを露呈しました。
      ([#113](https://github.com/pgbouncer/pgbouncer/issues/113))
- クリーンアップ
  * ビルド時に DBGVER の処理を削除して再現性を確保する。
    ([#112](https://github.com/pgbouncer/pgbouncer/issues/112))
  * Antimake: $(wildcard) から取得したファイルリストを並べ替える。新しい gmake ではもはや並べ替えを行わない。
    ([#111](https://github.com/pgbouncer/pgbouncer/issues/111))
  * ログに libssl のバージョンを表示します。
  * deb: 完全なハードニングを有効化します。

**2016-02-18  -  PgBouncer 1.7.1  -  「5人の友人に転送しないと……」**

警告： バージョン 1.7 以降、データベースがトランザクションプーリングモードにある場合、`server_reset_query` は実行されません。この点は 1.7 のリリース通知で十分に強調されていなかったようです。アプリケーションでこの動作に依存している場合、以前の動作を復元するには `server_reset_query_always` を使用してください。

このリリースの主な作業は、TLS関連のメモリリークを追跡することでしたが、実際にはリークは存在しません。代わりに、Debian/wheezy に組み込まれた libssl には、接続あたり600kのオーバーヘッドがあり（リークはしない）、期待される20〜30kよりも大幅に高いです。TLSを使用する際は、この点に注意が必要です。

- 修正
  * TLS：sslmode の "disabled" を "disable" に名称変更。PostgreSQL が使用している名称に合わせる。
  * TLS: `client_tls_sslmode=verify-ca/-full` はクライアント証明書のない接続を拒否するようになりました。
    ([#104](https://github.com/pgbouncer/pgbouncer/issues/104))
  * TLS: `client_tls_sslmode=allow/require` クライアント証明書の検証を実行する
    送信された場合。以前は検証設定が無効だったため、クライアント証明書を用いた接続が失敗していた。
    ([#105](https://github.com/pgbouncer/pgbouncer/issues/105))
  * データベースを解放する際のメモリリークを修正。
  * TLS ハンドシェイク中のメモリリークを修正。
  * EOF処理を tls_handshake() で修正。
  * memset のサイズが小さすぎる問題を asn1_time_parse 互換性用に修正。
  * TLS 以外の (`--without-openssl`) ビルドを修正。
    ([#101](https://github.com/pgbouncer/pgbouncer/issues/101))
  * Windowsビルドに関するさまざまな問題を修正しました。
    ([#100](https://github.com/pgbouncer/pgbouncer/issues/100))
- 整備作業
  * TLS: 不活性な接続のメモリ使用量を削減するには SSL_MODE_RELEASE_BUFFERS を使用してください。
  * 終了時に割り当てられたメモリをクリーンアップします。メモリリークチェッカーの実行を支援します。
  * `server_reset_query`のドキュメントを改善します。
    ([#110](https://github.com/pgbouncer/pgbouncer/issues/110))
  * TLS オプションをサンプル構成ファイルに追加します。

**2015-12-18  -  PgBouncer 1.7  -  「復活後に色が変化する」**

- 機能
  * TLS 接続をサポートします。バックエンド実装として OpenSSL/LibreSSL が使用されます。
  * TLS クライアント証明書による認証をサポートします。
  * Unix ソケットでの "peer" 認証をサポートします。
  * PostgreSQL と同様に、ホストベースのアクセス制御ファイルをサポートしています。
    [pg_hba.conf](http://www.postgresql.org/docs/9.4/static/auth-pg-hba-conf.html)
    これにより、ネットワーク接続に対する TLS 設定や、ローカル接続に対する "peer" 認証を構成できます。
- クリーンアップ
  * `query_wait_timeout` のデフォルト値を 120s に設定します。現在のデフォルト値（0）はキューイングを無限に許可するため、実用性がありません。つまり、クライアントが未処理のクエリを保持している状態でサーバー接続に割り当てられていない場合、クライアント接続は切断されます。
  * `server_reset_query_always` をデフォルトで無効化します。現在、reset クエリはセッションモードにあるプールでのみ使用されます。
  * pkt_buf を 4096 バイトに増加します。TLS との組み合わせでパフォーマンスが向上します。
      動作はおそらく負荷に依存しますが、v1.2 以降ではパケットバッファが接続から分離され、プールから遅延して使用されるため、安全に実行できます。
  * パイプライン化されたコマンドの数が、ReadyForQueryパケットの受信を期待している状態をサポートします。
      これにより、サーバーが早めに解放されるのを防ぎます。
      修正対象：[#52](https://github.com/pgbouncer/pgbouncer/issues/52)。
  * sbuf_loopcnt のロジックを改善しました。ソケットにイベントがなくても、ソケットの再処理が保証されます。TLS では独自のバッファリングがあるため、この改善が必要です。
  * システムテストを、最新のBSDおよびMacOSで動作するように調整。
    (Eric Radman)
  * **crypt** 認証を削除してください。この認証方式は古く、PostgreSQL 8.4 以降ではサポートされていません。
  * --with-cares の設定オプション（引数なし）を修正
      引数なしの設定で動作が不正だったため。

--------

## PgBouncer 1.6.x {#pgbouncer-16x}

**2015-09-03  -  PgBouncer 1.6.1  -  "Studio Audience Approves**

- 機能
  * 新しい設定: `server_reset_query_always`。設定すると、
      セッション以外のプールでの `server_reset_query` の使用を無効化します。
      PgBouncer ではプールごとの pool_mode を導入しましたが、
      セッションプールとトランザクションプールは同じリセットクエリを使用すべきではありません。
      実際、トランザクションプールはリセットクエリを使用すべきではありません。

    1.6.x で設定されていますが、1.7 で無効になります。

- 修正
  * [セキュリティ]  `auth_user` の無効な割当を削除する。(#69)
      `auth_user` が設定されており、クライアントが存在しないユーザー名を要求した場合、
      クライアントは `auth_user` としてログインする。これは好ましくない。

    [CVE-2015-6817](https://access.redhat.com/security/cve/cve-2015-6817)

  * 認証応答の処理中に NoticeResponse をスキップする。そうでなければ、サーバーでの詳細ログ出力がログイン失敗を引き起こす。

  * 管理コンソール: auth_type=any の場合、`auth_user` を指定してください。それ以外の場合、ログ出力がクラッシュする可能性があります（#67）。

  * OpenBSD、Solaris、OSX での各種ポータビリティ修正。

**2015-08-01  -  PgBouncer 1.6  -  「未来のゾンビ」**

- 機能

  * ユーザーのパスワードハッシュを PostgreSQL データベースから読み込みます。
    新しいパラメータ:

    auth_user
        データベースに接続し、ユーザー情報を取得するために使用するユーザー。
        データベースごとに設定することもできます。

    auth_query
        認証ユーザー下で実行する SQL クエリ。
        デフォルト： "SELECT usename, passwd FROM pg_shadow WHERE usename=$1"

    (Cody Cutrer)

  * プールモードは、データベースごとおよびユーザーごとに設定できます。
    (Cody Cutrer)

  * データベースおよびユーザーごとの接続制限：max_db_connections および max_user_connections。

  * 新規接続を防止するための DISABLE/ENABLE コマンドを追加します。
    (William Grant)

  * 新しいDNSバックエンド: c-ares。すべての有用な機能をサポートする唯一のDNSバックエンドです: /etc/hostsのリフレッシュ、SOA照会、大容量の応答（TCP/EDNS+UDP経由）、IPv6。現在は推奨されるバックエンドであり、将来的には**唯一**のバックエンドになる可能性が高く、不十分なライブラリの多数をサポートする意義がないためです。

    SNAFU: c-ares バージョン 1.10 以下では、IPv6 を有効にした状態で CNAME サポートが破損するバグがあります。（既に上流で修正済み。） 一時的な対策として、c-ares 1.10 以下では IPv4 のみを使用します。したがって、PgBouncer は c-ares >1.10（まだリリースされていない）が公開されてからある程度時間が経過した場合にのみ、他のバックエンドを切断します。

  * SHOW CLIENTS/SERVERS でリモート PID を表示します。Unix ソケット経由で接続するクライアントおよび TCP および Unix ソケットの両方に対応するサーバーで利用可能です。TCP サーバーの場合、PID はキャンセルキーから取得されます。

  * 負の DNS キャッシュを制御するための別々の設定パラメータ（dns_nxdomain_ttl）を追加。
    (Cody Cutrer)

  * クライアントのホストIPアドレスとポートを application_name に追加します。
      これは設定パラメータ application_name_add_host によって有効化され、デフォルトでは 'off' です。
    (Andrew Dunstan)

  * 設定ファイルには、設定を複数のファイルに分割できるようにする '%include FILENAME' 指令があります。
    (Andrew Dunstan)

- クリーンアップ

  * log: IPv6 アドレスを [] で囲む
  * log: サーバーへの接続時、ローカルIPアドレスとポートを表示
  * win32: 長引く引数には GNU スタイルを使用してください: --foo
  * ホスト名に数値を許可し、常に inet_pton でパースを試行する
  * deallocate_all() の修正についての FAQ
  * 例の設定ファイルに誤ったキーワードを修正
    (Magnus Hagander)
  * 認証ファイルにコメント（';' を用いて）を許可する。
    (Guillaume Aubert)
  * ログメッセージおよびコメント内のスペルミスを修正します。
    (Dmitriy Olshevskiy)

- 修正

  * メンテナンス中に新しい接続の起動を修正
    (Cody Cutrer)
  * 起動時に認証ファイルを2回読み込まない。
    (Cody Cutrer)
  * 自動DBの適切な無効化
  * ipv6: リスンソケットに IPV6_V6ONLY を設定します。
  * win32: リスンソケットに SO_REUSEADDR を設定しないでください。
  * IPv6 アドレスの memcpy 修正
  * 待機中のクライアントのキャンセルを修正。
    (Mathieu Fenniak)
  * 小さなバグ修正、calloc の結果を確認する必要があります
    (Heikki Linnakangas)
  * PID ファイルの末尾に改行を追加する
    (Peter Eisentraut)
  * PAUSE <db> が実行された場合、新しいサーバー接続を許可しない。
    (Petr Jelinek)
  * ログイン時にヘッダーが遅延する場合の「bad packet」を修正。
      (Michal Trojnara, Marko Kreen)
  * Coverty で検出されたエラーを修正。
    (Euler Taveira)
  * サーバー数が min_pool を下回った場合、server_idle_timeout を無効にする (#60)
    (Marko Kreen)

--------

## PgBouncer 1.5.x {#pgbouncer-15x}

**2015-04-09  -  PgBouncer 1.5.5  -  "Play Dead To Win**

- 修正
  * リモートクラッシュを修正 - 無効なパケット順序により NULL ポインタの参照が発生する問題を解消。悪用可能ではなく、DoS にのみ影響。

**2012-11-28  -  PgBouncer 1.5.4  -  「リークなし、訓練成功」**

- 修正
  * DNS：getaddrinfo_a() バックエンドにおけるメモリリークを修正。
  * DNS：udns バックエンドにおけるメモリリークを修正。
  * DNS：統計の計算を修正。
  * DNS：getaddrinfo_a() におけるエラーメッセージの処理を改善。
  * Win32 のコンパイルを修正。
  * コンパイラの依存関係サポートチェックを configure で修正。
  * ドキュメントの修正をいくつか実施。

**2012-09-12  -  PgBouncer 1.5.3  -  "Quantum Toaster**

- 重大な修正

  * データベース名が長すぎるとクラッシュする可能性があり、自動データベース作成が有効な場合、リモートからトリガーされることがあります。

    - 元のチェックはすべての名前が設定ファイルから来ると想定していたため、fatal() を使用しても問題なかったが、autodbs が有効な場合、[databases] セクションで  から '*' に設定されたデータベース名はネットワーク経由で取得される可能性があり、リモートシャットダウンが可能になる。

    [CVE-2012-4575](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2012-4575)

- マイナー機能

  * max_packet_size - クライアントとサーバー間で許可される最大パケットサイズを調整する設定パラメータ。
      デフォルト値は (2G-1) と同一ですが、現在はこれを小さく設定できます。
  * パケットヘッダーが解析できない場合、ログおよびエラーメッセージに16進数で表示する。

- 修正

  * AntiMake：パス名の操作に $(relpath) および $(abspath) を使用していたが、ソースツリーのパスにシンボリックリンクが含まれる場合にビルドが失敗していた。コードは現在、平文の文字列のみを扱うように変更された。
  * console: now SET コマンドを使用して空文字列の値を設定できます。
  * config.txt：タイムアウトは浮動小数点数で設定可能であることを示す。
      これは 1.4 で導入された、あまり知られていない機能である。

**2012-05-29  -  PgBouncer 1.5.2  -  「噛まずに、ただ飲み込む」**

- 修正
  * 誤って、reserve_pool_timeout がマイクロ秒単位で扱われていたため、プールが満杯になった際に即座に予約プールが有効化されていました。現在は意図した通り、秒単位で扱うように修正しました。
    (Noticed by Keyur Govande)

**2012-04-17  -  PgBouncer 1.5.1  -  "Abort, Retry, Ignore?**

- 機能
  * UNIXソケットの権限を調整するためのパラメータ:
    unix_socket_mode=0777, unix_socket_group=''.
- 修正事項
  * サーバー側変数に空文字列を許可する — これは "application_name" が正しく動作するために必要であり、サーバー側のデフォルト値を持たない唯一のパラメーターだからである。
  * 接続文字列が変更された場合、サーバーのパラメーターの再読み込みが必要です。
      以前は PgBouncer は古いパラメーターで続行していましたが、Postgres のアップグレード時にはこれにより障害が発生します。
  * autodb の接続文字列が変更された場合、古い接続を切断します。
  * cf_setint: 整数設定パラメータの解析に atoi() の代わりに strtol() を使用します。これにより16進数、8進数のサポートおよびより良いエラー検出が可能になります。
  * sigqueue() を使用して union sigval の存在を検出 - HPUX でのコンパイルを修正。
  * Makefile から 'git' コマンドを削除し、プレーンなtarボールビルド時に発生するランダムなエラーを回避する。
  * stats_period パラメータ。このパラメータは、統計出力の周期を調整します。
  * Asciidoc 8.4 以上を必要とします。以前のバージョンとの互換性は失われているようです。
  * close() からの EINTR に対する再試行をやめます。

**2012-01-05  -  PgBouncer 1.5  -  「2007 年よりクライアントの接続を最適化しています」**

1 つの DNS 名に 8 個を超える IP アドレスを関連付ける場合、EDNS0 プロトコルで照会する必要があります。
この機能をサポートするのは getaddrinfo_a()/getaddrinfo() と UDNS バックエンドだけで、libevent 1.x/2.x はサポートしません。
libc で有効にするには、/etc/resolv.conf に 'options edns0' を追加してください。

GNU Make 3.81 以上が必要です。

- 機能
  * DNS の応答変更を検出し、最新の応答に存在しない IP アドレスへの接続を無効化します。
    (Petr Jelinek)
  * DNS ゾーンシリアルに基づくホスト名の無効化。オプション dns_zone_check_period が設定されている場合、すべての DNS ゾーンに対して SOA を照会し、シリアルが変更された時点ですべてのホスト名を照会します。これは、接続の無効化を確定的に実行するため必要です。なぜなら、照会が行われない状態では、照会時の無効化は無意味だからです。新しい UDNS バックエンドでのみ動作します。
  * DNS キャッシュを確認するための新しい SHOW DNS_HOSTS および SHOW DNS_ZONES コマンドを追加。
  * 新しいパラメータ: min_pool_size - ロードがなければ接続をすべて切断しないようにする
    (Filip Rembialkowski)
  * idle_in_transaction_timeout - トランザクションが長時間アイドル状態になると終了する。
    デフォルトでは設定されない。
  * DNS ルックアップ用に libudns バックエンドを追加。evdns よりも機能が豊富。
      --with-udns を使用して有効化してください。現時点では IPv6 に対応していません。
  * KILL コマンドは、特定のデータベースのすべての接続を即座に終了します。
    (Michael Tharp)
  * Antimake ビルドシステムに移行して、より見やすい Makefile を得る。
    今後は GNU Make 3.81 以上が必要です。
- 修正
  * DNS は IPv6 ホスト名に対応しています。
  * サーバーから NOTIFY が到着しても接続状態を変更しない。
  * さまざまなドキュメントの修正。
    (Dan McGee)
  * 管理コンソールで "" を使った識別子の引用をサポートしました。当初はデータベース名を引数に取るコマンドがなかったため、引用は不要でした。
  * 管理コンソール：単語の正規表現の先頭に数字を許可する。厳密なパーサーを使用しようとすると、ここでは複雑になりすぎる。
  * 自動データベースが一時停止されている場合、期限を切らないでください。
    (Michael Tharp)
  * PAUSE を実行する際に必要に応じて自動でデータベースを作成します。
    (Michael Tharp)
  * RESUME コマンドによって発行される誤ったログメッセージを修正。
    (Peter Eisentraut)
  * user= に password= を指定しない場合、パスワードは userlist から取得されます。
  * takeover コードで '*' を正しく解析する。
  * autogen.sh: 古い autoconf/automake と互換性を持つ。
  * Win32 で mingw/msvc ランタイムの basename() が不正なため、サービス実行時にクラッシュする問題を修正。現在は常に互換性のある basename() が使用される。

--------

## PgBouncer 1.4.x {#pgbouncer-14x}

**2011-06-16  -  PgBouncer 1.4.2  -  "先制アルゴリズム**

影響を受ける OS: \*BSD、Solaris、Win32。

- ポータビリティ修正
  * リンカーに CFLAGS を渡します。pthread ベースの getaddrinfo_a() フォールバックを使用する場合に必要です。
  * lib/find_modules.sh: split() を index()+substr() に置き換えます。
    これにより、古い AWK でも動作するようになります。
  * <usual/endian.h>：システムの htoX/Xtoh 定義を無視します。マクロは部分的に定義されている可能性があります。
  * <usual/signal.h>：compat sigval と compat sigevent を分離する
  * <usual/socket.h>：iovec を取得するには <sys/uio.h> を含めてください。
  * <usual/time.h>：win32 での関数の自動検出を改善
  * <usual/base_win32.h>：重複する sigval/sigevent の宣言を削除

**2011-04-01  -  PgBouncer 1.4.1  -  「すべては演技だった」**

- 機能

  * IPv6 アドレスのリスニング/接続をサポートします。
    (Hannu Krosing)
  * で複数のリスニングアドレスを指定する場合、'listen_addr' では各 getaddrinfo() が呼び出されるため、名前も使用可能である。
  * 管理コンソール: クライアントに 'server_version' を送信して PgBouncer のバージョンを通知します。

- 重要な修正

  * glibc < 2.9 では getaddrinfo_a() を無効化する。古いバージョンでクラッシュするため。

    影響を受ける主要な OS 一覧: RHEL/CentOS 5.x (glibc 2.5)、Ubuntu 8.04 (glibc 2.7)。
    また、Debian/lenny (glibc 2.7) も影響を受けるが、getaddrinfo_a() はクラッシュしない。
    ただし、その状態を検出する適切な方法が存在しない。

    このような OS では libevent 2.x を使用してください。fallback の getaddrinfo_a() は本番システム向けではありません。DNS バックエンドの選択方法については、README の「DNS ルックアップサポート」セクションを参照してください。

    (Hubert Depesz Lubaczewski, Dominique Hermsdorff, David Sommerseth)

  * libevent 2.x を使用する場合、--enable-evdns をデフォルトで有効にします。

  * デフォルトで tcp_keepalive を有効にします。これは Postgres も同様に実行しているためです。
    (Hubert Depesz Lubaczewski)

  * Postgres との互換性を保つため、server_reset_query のデフォルトを DISCARD ALL に設定しました。

  * win32: NULL の Unix ソケットアドレスで発生するクラッシュを修正。
    (Hiroshi Saito)

  * autodb のクリーンアップを修正：古いクリーンアップコードはデータベースとプールを混同していた。
      空のプールが見つかった瞬間、データベースが「アイドル」とマークされ、
      後にアクティブなユーザーがいるデータベースを終了する可能性があった。

    Reported-By: Hubert Depesz Lubaczewski

- 修正

  * getaddrinfo_a() を非ブロッキングにするために、並列にリクエストを処理する単一のスレッドを使用して、アドレス解決を行う。
  * pthread コンパイルを有効にしてください。compat getaddrinfo_a が使用される場合。
  * release_server がライフタイム切断時に ->last_lifetime_disconnect の設定を失った。
    (Emmanuel Courreges)
  * win32: DOS形式の改行コードに対応した認証ファイルの修正 — load_file() はファイルの短縮を考慮していなかった。
    (Rich Schaaf)
  * <usual/endian.h>：enc/dec 関数の autoconf 検出を追加
      BSD での競合を回避するため。
    (James Pye)
  * 設定ファイルが存在しない場合にクラッシュしない。
    (Lou Picciano)
  * ログレベルがノイズのとき、DNS ルックアップの失敗でクラッシュしないようにする (-v -v)。
      (Hubert Depesz Lubaczewski, Dominique Hermsdorff)
  * find_modules.sh では、$(cmd) の代わりにバッククォートを使用して、よりポータブルにする。
    (Lou Picciano)
  * find_modules.sh では、互換性を高めるために 'sed' の代わりに 'awk' を使用してください。
    (Giorgio Valoti)
  * 起動時に非同期DNSバックエンドの情報をアクティブログに出力します。
  * で --disable-evdns を 'yes' ではなく 'no' に設定します。
  * ドキュメントに -R が unix_socket_dir を必要とする点を記載してください。
  * server_reset_query を faq.txt で説明します。
  * memset のスラブアロケータで失われた機能を復元
  * libusual におけるいくつかの小さなポータビリティ修正。

**2011-01-11  -  PgBouncer 1.4  -  "Gore Code**

- 機能

  * 非同期DNS照合 — リロード時にホスト名を解決するのではなく、接続時に解決し、設定可能なキャッシュをサポートします。
      (参照: dns_max_ttl パラメータ。)

    デフォルトでは、バックエンドとして getaddrinfo_a() (glibc) を使用します。存在しない場合、getaddrinfo_a() はブロッキング(!) な getaddrinfo() を使ってエミュレートされます。

    --enable-evdns を configure に指定すると、libevent の evdns がバックエンドとして使用されます。デフォルトでは使用されません。これは libevent 1.3/1.4 にバグのある実装が含まれているためです。libevent 2.0 の evdns だけが問題ないとされています。

  * 新しい設定変数: syslog_ident は、syslog の名前を調整するために使用します。

  * `application_name` 起動パラメータに対する適切なサポート。

  * コマンドラインの長オプション (Guillaume Lelarge)

  * Solaris 互換性の修正 (Hubert Depesz Lubaczewski)

  * 新しい設定変数: disable_pqexec。非常に厳格な環境では、この設定で Simple Query Protocol を無効化できます。これには、Extended Query Protocol のみを使用するアプリケーションが必要です。

  * Postgres互換性: スタートアップパケット内のデータベース名が空の場合、ユーザー名をデータベース名として使用する。

- 修正

  * DateStyle および TimeZone サーバー設定パラメーターは、正確な大文字・小文字を使用する必要があります。
  * 管理コンソール：クライアントに日時、タイムゾーンおよび標準出力サーバー設定を送信します。

- 内部のクリーンアップ

  * 低レベルなユーティリティ関数には libusual ライブラリを使用します。
  * サーバー パラメータの固定長制限を削除します。

--------

## PgBouncer 1.3.x {#pgbouncer-13x}

**2010-09-09  -  PgBouncer 1.3.4  -  "Bouncer is always right**

- 修正
  * 接続時に迅速な失敗ロジックを適用します。サーバーが障害状態の場合、クライアントは接続時にエラーを受け取ります。
  * 再読み込み時にチェックするため、自動生成されたデータベースにタグを付けないでください。それらは設定に存在しないため、殺されてしまいます。
  * アプリケーション名パラメータをデフォルトで無視します。これにより、Postgres 9.0 のすべてのユーザーが、ignore_startup_parameters= に手動で追加する必要がなくなります。
  * pg_auth の引用を正しく修正しました。 '\' はその場で使用されていません。
  * 管理コンソールでのエラー報告を改善し、ユーザーに受信したクエリを表示します。
  * 対応 OS（OpenBSD）では、tv_sec が time_t でない場合があります。
  * gcc 4.5 での警告を多すぎないようにする。

**2010-05-10  -  PgBouncer 1.3.3  -  "NSFW**

- 改善
  * listen(2) の引数を設定可能にする: listen_backlog。これは、システムの最大許容値が設定可能な OS で有用です。
  * ログイン失敗の原因となったユーザー名やデータベース名を明示するように、切断メッセージを改善します。
- 修正内容
  * クライアントがログインを試みない状態でも、再起動を繰り返すという従来の高速失敗再起動ロジックを変更しました。永続的に破損したデータベースやユーザーの場合、この動作は不快でした。
  * ログ出力関数が古い errno を保持するようにし、そうでない場合、ログレベルが高くなると pgbouncer が不具合を起こす可能性があります。
  * 起動関連のバッファサイズを増やして、EDB のノイズの多い起動を処理する。
  * V2 プロトコルの起動リクエストを検出し、切断の明確な理由を提示する。

**2010-03-15  -  PgBouncer 1.3.2  -  "Boomerang Bullet**

- 修正

  * 新しい設定変数 'query_wait_timeout'。クライアントがこの秒数以内にサーバー接続を取得できない場合、クライアントは終了されます。

  * クライアント接続プールにサーバー接続が存在せず、直前の接続が失敗した場合、クライアント接続を保留せず、直ちにエラーを送信する。

    これにより、前の修正と併せて、データベースが停止した場合の不要な停止を回避できます。

  * libevent の状態を sbuf.c で追跡して、二重の event_del() を回避します。
      通常は安全ですが、100% 効果があるとは限りません。
      今後は常に event_del() が呼び出されたかどうかを明確に把握できるようになります。

  * SUSPEND中にメンテナンスを無効化してください。そうでない場合、短いタイムアウト設定では、古いpgBouncerが接続を転送した後にいくつかの接続を閉じてしまう可能性があります。

  * クライアントがウェルカムパケットを待っている間（最初のサーバー接続時）に client_login_timeout を適用する。そうでなければ、query_timeout が設定されていない限り、無限に待機し続ける可能性がある。

  * win32: -U/-P オプションを -regservice に追加し、ユーザーがサービスの実行に使用するアカウントを選択できるようにします。従来のローカルサービスとローカルシステムの自動選択は信頼性が低かったためです。

  * console：テキスト列の末尾から \0 を削除します。C クライアントでは問題なかったため、気づきにくかったためです。

  * ドキュメントの改善。  (Greg Sabino Mullane)

  * ログメッセージのログイン関連の記述を明確化しました。

  * プーラーが送信したエラー（通常は切断時）のログレベルを INFO から WARNING に変更し、問題を示すことを明示します。

  * query_timeout のログメッセージを「query timeout」に変更します。

**2009-07-06  -  PgBouncer 1.3.1  -  「NSA監視要件を完全に準拠」**

- 修正
  * sbuf_loopcnt の問題を修正しました。接続がフリーズする原因となる場合があります。
      クエリまたは結果の長さが (pktlen * sbuf_loopcnt) [デフォルトで 10k] の倍数に近い場合、存在しないデータを待機し続ける可能性があります。
  * データベースの再構成を即時に行います。現在、SIGHUP 後に古い接続が再利用される可能性があります。
  * SHOW DATABASES のカラム追加により破損していた問題を修正。
  * 管理コンソールへのアクセスは、「auth_type=any」の場合、ユーザー名がドロップされたため無効化されました。
      修正：「auth_type=any」の場合、任意のユーザーが管理者として管理コンソールにアクセスできるようにします。
  * 不具合のある CUSTOM_ALIGN マクロを修正。幸いにも、OS が ALIGN マクロを定義している場合、このマクロは使用されないため、実際の環境では問題が発生していなかったと思われる。
  * win32: WSAStartup() を常に呼び出し、デーモンモード時のみでない
    なぜなら、設定の解析時にホストを解決する必要があるため。
  * win32: サービスのコマンドラインで、パスにスペースを含む場合に備えて設定ファイル名を引用符で囲みます。実行可能ファイルのパスについては、win32 の仕様上、引用符の必要性がありません。
  * SHOW HELP テキストに STATS を追加。
  * doc/usage.txt: 管理コンソールの結果における時間単位はミリ秒ではなくマイクロ秒です。

**2009-02-18  -  PgBouncer 1.3 -  "New Ki-Smash Finishing Move**

- 機能

  * IANA は PgBouncer の公式ポートとしてポート 6432 を割り当てました。
      したがって、デフォルトのポート番号は 6432 に変更されました。
      既存の個別ユーザーは変更する必要はありませんが、
      PgBouncer のパッケージを配布する場合は、パッケージのデフォルトを公式ポートに変更してください。

  * による動的データベース作成 (David Galoyan)

    これで、データベース名 "*" を定義できます。定義された場合、未定義のデータベースすべてに対してその接続文字列が使用されます。主にテスト／開発環境で有用です。

  * Windows でのサポート (斎藤浩史)

    PgBouncer は現在、Windows 2000 以降で動作します。コマンドラインの使用方法は従来と同様ですが、デーモンとして実行できず、オンライン再起動もできません。サービスとして実行するには、設定ファイルに service_name パラメータを定義します。その後、以下の手順を実行します。

        > pgbouncer.exe config.ini -regservice
        > net start SERVICE_NAME

    To stop and unregister:

        > net stop SERVICE_NAME
        > pgbouncer.exe config.ini -unregservice

    Windows イベントログを使用するには、事前にイベント DLL を登録する必要があります。

        > regsrv32 pgbevent.dll

    その後、設定ファイルで syslog = 1 を設定できます。

- マイナー機能

  * 設定ファイル内のデータベース名は、標準SQLの識別子クォートを使用して引用できるようになり、データベース名に非標準文字を含められるようになりました。

  * 新しい設定項目: 'reserve_pool_size' および 'reserve_pool_timeout'。
      クライアントが 'reserve_pool_timeout' 秒以上待機している場合、'reserve_pool_size' はプールに追加可能な接続数を指定します。また、'reserve_pool' 接続変数でプールごとに設定することもできます。

  * ソケット1つで費やされる時間を制限するための新しい設定 'sbuf_loopcnt'。

    一部の状況（例：SMP サーバー、ローカル Postgres、高速ネットワーク）では、pgbouncer は recv()->send() ループをブロッキングせずに多数回実行できます。しかし、これは他の接続が長時間スタックする原因になります。処理の公平性を高めるため、1 つのソケットに対して recv()->send() を実行する回数を制限します。回数制限に達した場合、他のソケットの処理に進みます。そのソケットの処理は次のイベントループで再開されます。

    Alexander Schocke による報告およびテストのおかげで。

  * crypt() 認証は現在オプションになりました。これは Postgres から削除されたためです。
      OS で提供されていなくても、pgbouncer は問題なく動作します。

  * ログタイムスタンプにミリ秒を追加します。

  * 旧来的な MD5 実装を、よりコンパクトな実装に置き換えます。

  * ISC ライセンスを FSF の説明で更新。

- 修正

  * event_del() が失敗を報告した場合、ただクリーンアップを続行してください。
      以前は、失敗が ENOMEM によるものだった場合に pgbouncer が再試行していました。
      しかし、これにより無限ループによるログの洪水が発生していたため、
      libevent がこれを好まないようです。

    Why event_del() report failure first time is still mystery.

  * --enable-debug はもはやバイナリからデバッグ情報を削除するかどうかを切り替えるだけです。
      これ以上 -fomit-frame-pointer に影響を与えることはなく、危険なためです。

  * include の順序を修正し、そうでなければシステムの include が内部のものより前に来る場合があります。これは新しい md5.h include ファイルで問題となりました。

  * COPYRIGHT ファイルを .tgz に含める...

--------

## PgBouncer 1.2.x {#pgbouncer-12x}

**2008-08-08  -  PgBouncer 1.2.3  -  "Carefully Selected Bytes**

- 修正
  * BSD 用に動作しなかった SO_ACCEPTFILTER コードを無効化します。
  * 例として etc/userlist.txt を tgz に含める。
  * 再帰には '$(MAKE)' を 'make' の代わりに使用してください (Jorgen Austvik)
  * glibc が無意味になるため、_GNU_SOURCE を定義してください。
  * libevent 1.1 のリンクテストを通過させ、後に「1.3b+ が必要」を報告できるようにする
  * 古い pidfile を検出し、削除する。

Devrim GUNDUZ および Bjoern Metzdorf による問題報告およびテストのおかげで。

**2008-08-06  -  PgBouncer 1.2.2  -  「バーフバッグ付属」**

- 修正
  * 'drop_on_error' を削除してください。これは誤ったアイデアでした。PostgreSQL の破損したプランキャッシュ動作を回避するための暫定対策として追加されたものですが、通常のケースで一部のクエリが常にエラーを返す場合に、損害を引き起こす可能性があります。

**2008-08-04  -  PgBouncer 1.2.1  -  "Waterproof**

- 機能
  * 新しいパラメータ 'drop_on_error' — サーバーがエラーを発生させた場合、接続は再利用されず、クライアントが処理を終了した後に破棄されます。これはプランキャッシュを更新するために必要です。自動更新は 8.3 でも動作しません。デフォルトは 1 です。
- 修正事項
  * SHOW SOCKETS/CLIENTS/SERVERS: ソケットにバッファがない場合にクラッシュしない。
  * SUSPEND で suspend_timeout が発動した場合の無限ループを修正。
- 軽微な整備
  * struct iovec に <sys/uio.h> を使用してください。
  * 中断停止（SIGINT からの再開）を RESUME/SIGUSR2 で実行する場合、次回の PAUSE 時に発動しないようにする。
  * 管理コンソール操作がキャンセルされた場合の適切なログメッセージ。

**2008-07-29  -  PgBouncer 1.2  -  "Ordinary Magic Flute**

PgBouncer 1.2 では、libevent バージョン 1.3b 以降が必要です。
古い libevent バージョンでは、新しい再起動コードでクラッシュします。

- 機能

  * コマンドラインオプション (-u) および設定パラメータ (user=) を、起動時にユーザー切り替えをサポートするためのものとして導入しました。また、現在、pgbouncer は root として実行されることを拒否します。

    (Jacob Coby)

  * より詳細な使用説明テキスト (-h)。 (Jacob Coby)

  * 新しいデータベースオプション：接続開始前に新しい接続でクエリを実行できるようにする connect_query。

    (Teodor Sigaev)

  * 新しい設定変数 'ignore_startup_parameters' を導入し、起動パケット内の追加パラメータを許可または無視できるようにしました。デフォルトでは 'database' と 'user' のみが許可され、それ以外のパラメータはエラーを発生させます。これは、過剰に積極的な JDBC が起動パケット内で 'extra_float_digits=2' を無条件に設定しようとする場合に耐えられるようにするためです。

  * syslog へのログ出力: syslog=0/1 および syslog_facility=daemon/user/local0 の新パラメータ。

  * より安全なオンライン再起動 (-R)

    - fork の前で FD の読み込みを移動し、管理コンソールにログ出力できるようにし、^C で中断できるようにする

    - fork後にSHUTDOWNを保持し、^Cが安全になるようにする

    -  、接続先の Unix ソケットがリスニングしているか確認するために試行されます。
        これにより、-R は、以前のプロセスが実行されていなくても使用可能になります。
        以前のプロセスが存在する場合でも、-R が使用されない限り、起動は失敗します。

  * 新しい管理コンソールコマンド：

    - SHOW TOTALS は、ログに出力される統計の要約に加えてメモリ使用量を表示します。

    - SHOW ACTIVE_SOCKETS は、ソケットを表示するものと同様ですが、アクティブなソケットのみをフィルタリングして表示します。

- 目に見えにくい機能

  * suspend_timeout - スタックした接続と長時間のログインを切断します。再起動時の追加の安全性を提供します。

  * リモートデータベースがログイン時にエラーを発生させた場合、クライアントに通知する。

  * 設定からデータベースを削除して再読み込みすると、すべての接続が切断され、データベースが削除されます。

  * 管理コンソールの SHOW/SET コマンドで、PostgreSQL に似た動作を実現するため、仮のパラメータを設定します。
      これは psycopg が管理コンソールに接続できるようにするため必要でした。
      (client_encoding/default_transaction_isolation/datestyle/timezone)

  * server_lifetime=0 を設定すると、最初の使用後すぐにサーバー接続を切断します。以前は「0」を設定すると PgBouncer がサーバーの年齢を無視していました。この動作は非文書化されていたため、依存しているユーザーは存在しないはずです。

  * 内部の改善事項：

    - パケットバッファは遅延割り当てされ、再利用されます。これによりメモリ使用量が大幅に削減されます。また、多数の接続で大きな pktbuf を使用することも現実的になります。

    - OOM状況でも正常に動作するよう、多数のエラー処理の改善が行われました。

    - メモリ管理にスラブ割り当てを使用します。

    - 多数のコードクリーンアップ。

- 修正

  * イベントループごとに1回だけ accept() が実行される仕様により、接続試行の数が多い場合に接続バックログが発生する可能性がありました。現在はリスニングソケットを常に完全にドレインするようにしたため、この問題が解消されます。
  * connect からの EINTR を処理する。
  * configure.ac を autoconf 2.59 と互換性を持たせる。
  * Solaris互換性の修正 (Magne Maehre)

--------

## PgBouncer 1.1.x {#pgbouncer-11x}

**2007-12-10  -  PgBouncer 1.1.2  -  "The Hammer**

- 機能
  * server_lifetime による切断は、(server_lifetime / pool_size) 秒ごとに分離されるようになりました。これにより、pgbouncer が再接続の洪水を引き起こすのを回避できます。
- 修正
  * オンラインアップグレード 1.0 → 1.1 の問題：
    - 1.0 ではサーバーのパラメーターを追跡しないため、それらは NULL のままになりますが、1.1 ではこれを想定しておらず、クラッシュしました。
    -  サーバーのパラメータが不明な場合でも、クライアントのパラメータが設定されているなら、エラーを出力する代わりにそれらに対して SET を実行する。
  * INFO レベルで誤って残された一時的なデバッグ出力を削除し、ログが汚染されないようにする。
  * debian/changelog の修正を元に戻す。
- 整理作業。
  * バッファのアライメントを改善するために、構造体 SBuf のフィールドの順序を再配置する。

**2007-10-26  -  PgBouncer 1.1.1  -  "Breakdancing Bee**

- 修正
  * サーバーのパラメーター・キャッシュが初期化されないまま残る場合があり、これにより不要な SET が発生しました。これは 8.1 では standard_conforming_strings を変更できないため問題を引き起こしました。
      （報告およびテストの協力にディミトリ・フォンタインに感謝します。）
  * ドキュメントの修正。
  * doc/fixman.py を .tgz に含める。

**2007-10-09  -  PgBouncer 1.1  -  "Mad-Hat Toolbox**

- 機能

  * 次のサーバー設定パラメーターを追跡してください：

        client_encoding  datestyle, timezone, standard_conforming_strings

  * データベース接続文字列の拡張機能：

    -  host= で指定されたホスト名を受け入れます。
    - ホストにカスタム Unix ソケットの場所を許可する
    - クォートされた値を許可: password=' asd''foo'

  * 新しい設定変数: server_reset_query は、リリース直後にすぐに送信されます
  * 新しい設定変数: サーバーの接続割り当て方式を LIFO と RR の間で切り替えるための server_round_robin。
  * でアイドル状態の接続に対して送信された Cancel パケットは、もはや接続を切断しなくなりました。
  * からの ^C によるキャンセルは、SUSPEND / PAUSE に対して有効です。
  * 起動時に FD 制限を出力する。
  * 一時停止時に、できるだけ早くパケット境界に到達するように試みます。
  * データベースパラメータに 'timezone' を追加します。
  * 長寿命のログファイルディスクリプタを使用。SIGHUP / RELOAD で再オープンする。
  * SHOW SERVERS/CLIENTS/SOCKETS で表示されるローカル接続エンドポイントの情報。

- コードの整理

  * デバッグログメッセージにソケット情報が含まれます。
  * マジックナンバーの削除とエラーメッセージの整理。 (David Fetter)
  * 現在のパケット情報用のラッパー構造体です。複雑さを大幅に削減します。

- 修正

  * パケットヘッダーの無効な値をより正確に検出する。
  * auth_file の変更チェックが不具合だったため、pgbouncer が頻繁に再読み込みを行っていました。

--------

## PgBouncer 1.0.x {#pgbouncer-10x}

**2007-06-18  -  PgBouncer 1.0.8  -  "Undead Shovel Jutsu**

- 修正
  * キャンセルパケット処理でのクラッシュを修正。(^C による psql からの中断)
- 機能
  * 一時停止 <db>；再開 <db>；正常に動作しています。
  * 管理コンソールコマンドの解析のクリーンアップ。
  * 価格の高い in-list アサートチェックを無効化します。

**2007-04-19  -  PgBouncer 1.0.7  -  "With Vitamin A-Z**

- 修正
  * send() の間にエラー/通知パケットが発生し、アサートがトリガーされる。バッファリングのロジックを完全に削除することで修正する。pgbouncer は明示的にバッファを保持しないため、この処理は不要である。これは MSG_MORE でバッファリングをカーネルに押し出していた時代の残骸である。
  * また、送信がブロック解除されたときに recv() のロジックを呼び出さないようにしてください。
  * admin_users および stats_users の検索コードで部分一致が正しく処理されない問題を修正。
  * UNIX ソケットのピア UID を取得する方法を標準化し、getpeereid() を使用する。

**2007-04-12  -  PgBouncer 1.0.6  -  "Daily Dose**

- 修正
  * 「トーケイ中におけるメンテナンスの無効化」の修正により、メンテナンスが完全に無効化される可能性がある。修正する。
  * 用の FreeBSD へのコンパイル修正、<sys/ucred.h> は <sys/param.h> が必要です。
      Robert Gogolok による報告に感謝します。

**2007-04-11  -  PgBouncer 1.0.5  -  「今日はこれで十分」**

- 修正
  * オンライン再起動のバグを修正：
    - Set -> サーバーのアイドル状態を待機可能にします。
    - use_client_socket() から不要なコードを削除します
    - トーキーイン中にメンテナンスを無効化します。

**2007-04-11  -  PgBouncer 1.0.4  -  「最後の 'last' バグ」**

- 修正
  * アイドル状態のサーバーが「dirty」とタグ付けされたための通知。
      release_server() はこれを想定していなかった。
      これを修正するには、それらを破棄してください。

**2007-04-11  -  PgBouncer 1.0.3  -  "Fearless Fork**

- 修正
  * ログインパスにエラー処理が不足していたため、接続が終了した際にアサーションが発生する可能性がありました。
  * アサートを sbuf.c でクリーンアップし、問題を早期に検出する。
  * Assert() がトリガーされたときにコアを生成する。

- 新機能
  * 新しい設定変数: log_connections、log_disconnections、log_pooler_errors は、ログ出力を有効または無効にするために使用します。
  * 設定変数: client_login_timeout
      ログインフェーズで、SUSPEND がスタックする可能性があるため、無応答の接続を切断するタイムアウト時間。

**2007-03-28  -  PgBouncer 1.0.2  -  "Supersonic Spoon**

- 修正
  * libevent は、同じループ内で削除されたイベントを報告する可能性があります。
      1 つのループ内でソケットの再利用を回避してください。
  * release_server() は、disconnect_client() から呼び出された際に、パケットが実際に送信されたかどうかを確認していなかった。

**2007-03-15  -  PgBouncer 1.0.1  -  "Alien technology**

- 修正
  * キャッシュ済みとキャッシュ未使用の時刻の混在、および unsigned usec_t の型定義の使用により、誤った query_timeout エラーが発生していた。
  * 送信待機からソケットが起床したが、依然としてスタールする稀なケースを修正。
  * サーバー接続のより公正なキューイング。以前は、新しいクエリが古いクエリより先にサーバー接続を取得することができた。
  * サーバーの解放を、すべてのデータが確実に送信された後に遅らせる。

- 機能
  * SHOW SOCKETS コマンドで、状態に関する詳細情報を取得できます。
  * 接続の追跡を支援するため、ログに PgSocket ポインタを出力します。
  * 管理コンソールで、SHOW の代わりに SELECT を許可します。
  * さまざまなコードの整備。

**2007-03-13  -  PgBouncer 1.0  -  "Tuunitud bemm**

- 初の公開リリース。
