---
title: "よくある質問"
linkTitle: "FAQ"
weight: 90
description: "PgBouncer に関するよくある質問"
icon: fa-solid fa-circle-question
module: [PGBOUNCER]
categories: [リファレンス]
aliases: [/pgbouncer/faq/]
upstream_link: "https://www.pgbouncer.org/faq.html"
---

--------

## PgBouncer への接続方法 {#how-to-connect-to-pgbouncer}

PgBouncer は Postgres サーバーとして動作するため、クライアントを PgBouncer のポートに接続するだけでよい。

--------

## 複数のサーバー間でクエリを負荷分散するには？ {#how-to-load-balance-queries-between-several-servers}

PgBouncer には内部的なマルチホスト構成がありません。
外部ツールを介して実現可能です：

1.  DNS ラウンドロビン。1 つのドメイン名の背後にある複数の IP アドレスを使用します。PgBouncer は新しい接続を確立するたびに DNS を照会しません。代わりに、すべての IP アドレスをキャッシュし、内部でラウンドロビンを行います。注意：1 つの名前に 8 つ以上の IP アドレスが関連付けられている場合、DNS バックエンドは EDNS0 プロトコルをサポートしている必要があります。詳細については README を参照してください。

2.  TCP接続のロードバランサーを使用してください。[LVS](http://www.linuxvirtualserver.org/) または [HAProxy](https://www.haproxy.org/) が適した選択肢のようです。PgBouncer側では、`server_lifetime` を小さく設定し、`server_round_robin` を有効にするのが良いでしょう。デフォルトでは、アイドル状態の接続はLIFOアルゴリズムで再利用されますが、ロードバランシングが必要な状況では、この動作が十分に機能しない可能性があります。

--------

## フェイルオーバーの方法 {#how-to-failover}

PgBouncer には内部的なフェイルオーバーホストの設定や検出機能がありません。
外部ツールを用いることで可能になります：

1. DNS の再構成：DNS 名の背後にある IP アドレスが再構成された場合、PgBouncer は新しいサーバーに再接続します。この動作は、次の 2 つの設定パラメーターで調整できます。`dns_max_ttl` はホスト名の有効期間を、`dns_zone_check_period` はゾーン SOA が変更を確認するために頻繁に照会される頻度をそれぞれ調整します。ゾーン SOA レコードが変更された場合、PgBouncer はそのゾーン下のすべてのホスト名を再照会します。

2. 設定ファイルに新しいサーバーを記述し、PgBouncerが再読み込みできるようにします。
SIGHUP を送信するか、管理コンソールで `RELOAD` コマンドを実行してください。PgBouncer はホスト設定の変更を検出し、新しいサーバーに再接続します。

3.  `RECONNECT` コマンドを使用してください。これは、上記の2つのオプションのいずれも適用できない状況で使用するものです。たとえば、前述の HAProxy を使って PgBouncer から下流への接続をルーティングする場合などです。`RECONNECT` は、すべてのサーバー接続を再開するだけです。したがって、他のコンポーネントが接続ルーティング情報を変更した後に実行してください。

--------

## セッションプーリングとプリペアドステートメントをどのように使用するか？ {#how-to-use-prepared-statements-with-session-pooling}

セッションプーリングモードでは、リセットクエリが古いプリペアドステートメントをクリアする必要があります。これは `server_reset_query = DISCARD ALL;` または少なくとも `DEALLOCATE ALL;` を使用することで達成できます。

--------

## トランザクションプーリングとプリペアドステートメントをどのように使用するか？ {#how-to-use-prepared-statements-with-transaction-pooling}

バージョン 1.21.0 以降、PgBouncer はトランザクションプーリングモードでプリペアドステートメントを追跡し、関連するサーバー接続上でオンザフライで準備されるように保証できるようになりました。この機能を有効にするには、`max_prepared_statements` をゼロ以外の値に設定する必要があります。詳細については、[`max_prepared_statements`](/ja/docs/pgbouncer/config/#max_prepared_statements) のドキュメントを参照してください。

PHP/PDO を使用する場合、バージョンによっては PgBouncer のプリペアドステートメントサポートと互換性がありません ([#991])。PHP/PDO は [PHP 8.4+ **かつ** libpq 17][php-fix] を使用している場合にのみ互換性があります。したがって、古いバージョンを使用する環境では、アップグレードを推奨するか、クライアント側でプリペアドステートメントを無効にする必要があります。

[php-fix]: https://github.com/php/php-src/commit/f35ad560b468e3e0a6c289949ba9b19af4fa3e7b

[#991]: https://github.com/pgbouncer/pgbouncer/issues/991

### JDBC でのプリペアドステートメントの無効化 {#disabling-prepared-statements-in-jdbc}

JDBC で行う正しい方法は、接続文字列に `prepareThreshold=0` パラメータを追加することです。

### PHP/PDO でのプリペアドステートメントの無効化 {#disabling-prepared-statements-in-phppdo}

サーバー側のプリペアドステートメントの使用を無効にするには、PDO 属性 `PDO::ATTR_EMULATE_PREPARES` を `true` に設定する必要があります。接続時に行います：

    $db = new PDO("dsn", "user", "pass", array(PDO::ATTR_EMULATE_PREPARES => true));

またはそれ以降：

    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, true);

--------

## 接続を落とさずに PgBouncer をアップグレードする方法 {#how-to-upgrade-pgbouncer-without-dropping-connections}

ロールリング再起動は、`SHUTDOWN WAIT_FOR_CLIENTS`のドキュメントの[セクションに記載された手順に従って行うことができます。](/ja/docs/pgbouncer/usage/#shutdown-wait_for_clients)

--------

## クライアントがどのサーバー接続にあるかを確認するにはどうすればよいですか。 {#how-to-know-which-client-is-on-which-server-connection}

管理コンソール上で `SHOW CLIENTS` および `SHOW SERVERS` コマンドを使用します。

1.   クライアント接続をサーバー接続にマッピングするには、`ptr` と `link` を使用してください。

2.   クライアント接続の `addr` および `port` を使用して、クライアントからの TCP 接続を識別します。

3.   サーバーへの TCP 接続を識別するために、`local_addr` および `local_port` を使用します。

--------

## PgBouncer は Web サーバーかデータベースサーバーにインストールすべきか？ {#should-pgbouncer-be-installed-on-the-web-server-or-database-server}

状況によります。

Web サーバーに PgBouncer をインストールするのは、一時的な接続が使用される場合に適しています。この場合、接続のセットアップ遅延が最小化されます（TCP では接続が利用可能になるまで数回のパケット往復が必要です）。データベースサーバーに PgBouncer をインストールするのは、複数の異なるホスト（例：Web サーバー）が接続する場合に適しています。この場合、それらの接続をまとめて最適化できます。

Web サーバーおよびデータベース サーバーの両方に PgBouncer をインストールすることも可能です。その一方で、各 PgBouncer のホップがクエリごとにわずかな遅延を追加するという欠点があります。

最終的には、パフォーマンス要件に最も適したモデルをテストして選定する必要があります。また、ウェブサーバーまたはデータベースサーバーの障害発生時に PgBouncer を導入することでアプリケーションのフェイルオーバーにどのような影響を与えるかを検討する必要があります。
