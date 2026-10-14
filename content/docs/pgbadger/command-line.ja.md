---
title: "コマンドラインリファレンス"
linkTitle: "コマンドライン"
weight: 30
description: "完全なpgBadgerコマンド構文、オプション、リモート入力、終了コード、および例"
search_keywords: [--Jobs, --anonymize, --appname, --average, --begin, --charset, --command, --csv-separator, --day-report, --dbclient, --dbname, --dbuser, --disable-autovacuum, --disable-checkpoint, --disable-connection, --disable-error, --disable-hourly, --disable-lock, --disable-query, --disable-session, --disable-temporary, --disable-type, --dns-resolv, --dump-all-queries, --dump-raw-csv, --enable-checksum, --end, --exclude-appname, --exclude-client, --exclude-db, --exclude-file, --exclude-line, --exclude-query, --exclude-time, --exclude-user, --explain-url, --explode, --extension, --extra-files, --format, --help, --histo-average, --histogram-query, --histogram-session, --html-outdir, --ident, --include-file, --include-pid, --include-query, --include-session, --include-time, --incremental, --iso-week-number, --jobs, --journalctl, --keep-comments, --last-parsed, --log-duration, --log-timezone, --logfile-list, --maxlength, --month-report, --no-fork, --no-multiline, --no-prettify, --no-process-info, --no-progressbar, --no-week, --nocomment, --noexplain, --nograph, --noreport, --normalized-only, --outdir, --outfile, --pgbouncer-only, --pid-dir, --pid-file, --pie-limit, --prefix, --prettify-json, --query-numbering, --quiet, --rebuild, --remote-host, --retention, --sample, --select-only, --ssh-identity, --ssh-option, --ssh-port, --ssh-program, --ssh-sudo, --ssh-timeout, --ssh-user, --start-monday, --tempdir, --timezone, --title, --top, --verbose, --version, --watch-mode, --wide-char, --zcat, JSON::XS, Jobs, all, anonymize, appname, autovacuum, average, begin, char, charset, checkpoint, checksum, client, command, comments, connection, csv, csv-separator, csvlog, day, day-report, db, dbclient, dbname, dbuser, dir, disable, disable-autovacuum, disable-checkpoint, disable-connection, disable-error, disable-hourly, disable-lock, disable-query, disable-session, disable-temporary, disable-type, dns, dns-resolv, dump, dump-all-queries, dump-raw-csv, duration, enable, enable-checksum, end, error, exclude, exclude-appname, exclude-client, exclude-db, exclude-file, exclude-line, exclude-query, exclude-time, exclude-user, explain, explain-url, explode, extension, extra, extra-files, file, files, fork, format, help, histo, histo-average, histogram, histogram-query, histogram-session, host, hourly, html, html-outdir, ident, identity, include, include-file, include-pid, include-query, include-session, include-time, incremental, info, iso, iso-week-number, jobs, journalctl, json, jsonlog, keep, keep-comments, last, last-parsed, limit, line, list, lock, log, log-duration, log-timezone, log_duration, log_line_prefix, log_statement, logfile, logfile-list, logplex, maxlength, mode, monday, month, month-report, multiline, no, no-fork, no-multiline, no-prettify, no-process-info, no-progressbar, no-week, nocomment, noexplain, nograph, noreport, normalized, normalized-only, number, numbering, only, option, outdir, outfile, parsed, pgbouncer, pgbouncer-only, pid, pid-dir, pid-file, pie, pie-limit, port, prefix, prettify, prettify-json, process, program, progressbar, queries, query, query-numbering, quiet, raw, rebuild, redshift, remote, remote-host, report, resolv, retention, sample, select, select-only, separator, session, ssh, ssh-identity, ssh-option, ssh-port, ssh-program, ssh-sudo, ssh-timeout, ssh-user, start, start-monday, stderr, sudo, syslog, tempdir, temporary, time, timeout, timezone, title, top, type, url, user, verbose, version, watch, watch-mode, week, wide, wide-char, zcat]
search_boost: 8
icon: fa-solid fa-terminal
module: [PGBADGER]
categories: [リファレンス]
aliases: [/pgbadger/command-line/]
upstream_link: "https://github.com/darold/pgbadger/tree/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

## 使い方とオプション {#usage-and-options}

使用法: pgbadger [options] logfile [...]

```text
詳細なレポートとグラフを生成するPostgreSQLログアナライザー。
```

引数:

```text
logfileには、単一のログファイル、複数のファイル、またはファイル一覧を返す
シェルコマンドを指定できます。標準入力からログを渡す場合はファイル名に-を
指定します。csvlog形式は標準入力からの読み取りに対応していません。
```

オプション:

```text
-a | --average minutes : クエリーと接続の平均グラフを作成する間隔（分）。デフォルトは5分。
-A | --histo-average min: クエリーのヒストグラムを作成する間隔（分）。デフォルトは60分。
-b | --begin datetime  : ログから解析するデータの開始日時（タイムスタンプまたは時刻）。
-c | --dbclient host   : 指定したクライアントホストのエントリーだけをレポートします。
-C | --nocomment       : クエリーから /* ... */ 形式のコメントを削除します。
-d | --dbname database : 指定したデータベースのエントリーだけをレポートします。
-D | --dns-resolv      : クライアントのIPアドレスをDNS名に置換します。pgBadgerの処理が大幅に遅くなる場合がありま
                         す。
-e | --end datetime    : ログから解析するデータの終了日時（タイムスタンプまたは時刻）。
-E | --explode         : データベースごとにレポートを生成します。データベースに関連しない全体情報はpostgresデー
                         タベースのレポートに追加します。
-f | --format logtype  : 指定可能な値はsyslog、syslog2、stderr、jsonlog、csv、pgbouncer、logplex、rds、redshift
                         です。ログ形式を自動検出できない場合に使用します。
-G | --nograph         : HTML出力のグラフを無効にします。グラフはデフォルトで有効です。
-h | --help            : このヘルプを表示して終了します。
-H | --html-outdir path: 増分モードでHTMLレポートを書き出すディレクトリ。バイナリファイルは-O、--outdir で指定し
                         たディレクトリに保持します。
-i | --ident name      : syslogの識別名に使うプログラム名。デフォルトはpostgres。
-I | --incremental     : 増分モードを使用し、日ごとのレポートを別ディレクトリに生成します。--outdir の指定が必須
                         です。
-j | --jobs number     : 単一ログファイルに対して同時に実行するジョブ数。デフォルト、またはcsvlog形式では単一ジョ
                         ブで実行します。
-J | --Jobs number     : 並列に解析するログファイル数。デフォルトでは一度に一つのファイルを処理します。
-l | --last-parsed file: 最後に解析した日時と行を記録して増分解析を可能にします。前回実行以降のエラー監視や、週
                         次ローテーションのログから日次レポートを生成する場合に便利です。
-L | --logfile-list file: 解析対象のログファイル一覧を格納したファイル。
-m | --maxlength size  : クエリーの最大長。指定した長さで切り詰めます。デフォルトの切り詰め長は100000。
-M | --no-multiline    : 複数行のステートメントを収集しません。特にエラーに伴う不要な内容でレポートが巨大になる
                         ことを防ぎます。
-N | --appname name    : 指定したアプリケーション名のエントリーだけをレポートします。
-o | --outfile filename: 出力ファイル名。形式に応じてout.html、out.txt、out.bin、out.jsonがデフォルトです。複数
                         回指定すると複数形式を出力します。JSON出力にはJSON::XSが必要です。標準出力に書く場合は
                         ファイル名に-を指定します。
-O | --outdir path     : 出力ファイルを保存するディレクトリ。
-p | --prefix string   : postgresql.confで設定した独自のlog_line_prefixの値。クライアントIPやアプリケーション名
                         などを追加し、ドキュメント記載の標準プレフィックスを使わない場合にのみ指定します。時刻
                         （%t、%m、%n）とプロセス（%p、%c）のエスケープ指定を必ず含めてください。以下の例を参照
                         してください。
-P | --no-prettify     : SQLクエリーの整形を無効にします。
-q | --quiet           : プログレスバーを含め、標準出力に何も表示しません。
-Q | --query-numbering : --dump-all-queries または --normalized-only の出力でクエリーに番号を付けます。
-r | --remote-host ip  : リモートログにcatを実行するホストを指定します。解析はローカルで行います。
-R | --retention N     : 増分モードで保持する週数。デフォルトは0（無効）。指定した週数より古い週や日のディレクト
                         リは出力ディレクトリから自動削除します。
-s | --sample number   : 保存するクエリーサンプル数。デフォルトは3。
-S | --select-only     : SELECTクエリーだけをレポートします。
-t | --top number      : 保存・表示するクエリー数。デフォルトは20。
-T | --title string    : HTMLレポートページのタイトルを変更します。
-u | --dbuser username : 指定したユーザーのエントリーだけをレポートします。
-U | --exclude-user username : 指定したユーザーのエントリーをレポートから除外します。複数回指定できます。
-v | --verbose         : 詳細・デバッグモードを有効にします。デフォルトでは無効です。
-V | --version         : pgBadgerのバージョンを表示して終了します。
-w | --watch-mode      : logwatchのようにエラーだけをレポートします。
-W | --wide-char       : クエリーのHTML出力をUTF8にエンコードし、Perlの「Wide character in print」メッセージを防
                         ぎます。
-x | --extension       : 出力形式。text、html、bin、jsonを指定できます。デフォルトはhtml。
-X | --extra-files     : 増分モードでCSSとJSを出力ディレクトリに別ファイルとして書き出します。
-z | --zcat exec_path  : zcatプログラムのフルパス。zcat、bzcat、unzipがPATHにない場合に使用します。
-Z | --timezone +/-XX  : タイムゾーンのGMTからの時差（時間）。JavaScriptグラフの日時を調整します。2のような整数、
                         または2.5のような小数を指定できます。
--anonymize            : クエリー内のすべてのリテラルを伏せ字にし、機密データを隠します。
--charset              : HTMLの文字セットを指定します。デフォルトはutf-8。
--command CMD          : 標準入力にログエントリーを取得するコマンド。pgBadgerはコマンドへのパイプを開き、コマン
                         ドが生成するログエントリーを解析します。
--csv-separator        : CSVフィールドの区切り文字。デフォルトは,。
--day-report YYYY-MM-DD: 指定した日のHTMLレポートを作成します。増分出力ディレクトリと、必要なすべてのバイナリデ
                         ータファイルが必要です。
--disable-autovacuum   : autovacuumレポートを生成しません。
--disable-checkpoint   : チェックポイント・リスタートポイントのレポートを生成しません。
--disable-connection   : 接続レポートを生成しません。
--disable-error        : エラーレポートを生成しません。
--disable-hourly       : 時間帯別レポートを生成しません。
--disable-lock         : ロックレポートを生成しません。
--disable-query        : クエリーレポート（最も遅い、高頻度、ユーザー別、データベース別など）を生成しません。
--disable-session      : セッションレポートを生成しません。
--disable-temporary    : 一時ファイルのレポートを生成しません。
--disable-type         : クエリーの種別別、データベース別、ユーザー別レポートを生成しません。
--dump-all-queries     : ログ内のすべてのクエリーを出力し、バインドパラメーターを対応するプレースホルダーの位置
                         に代入します。
--dump-raw-csv         : ログを解析して情報をCSV形式で出力します。それ以上の処理は行わず、レポートも生成しません。

--enable-checksum      : 各クエリーレポートの下にmd5チェックサムを追加します。
--exclude-appname name : 指定したアプリケーション名のエントリーを除外します。例: "pg_dump"。複数回指定できます。
--exclude-client name  : 指定したクライアントIPのログエントリーを除外します。複数回指定できます。
--exclude-db name      : 指定したデータベースのエントリーを除外します。例: "postgres"。複数回指定できます。
--exclude-file filename: 除外するクエリーの正規表現を格納したファイルのパス。一行に一つの正規表現を記述します。
--exclude-line regex   : 指定した正規表現に一致するログエントリーを除外します。複数回指定できます。
--exclude-query regex  : 指定した正規表現に一致するクエリーを除外します。例: "^(VACUUM|COMMIT)"。複数回指定でき
                         ます。
--exclude-time  regex  : 指定した正規表現に一致するタイムスタンプを除外します。例: "2013-04-12 .*"。複数回指定で
                         きます。
--explain-url URL      : 実行計画をグラフィカルに表示するツールのURLを変更します。デフォルトは
                         https://explain.depesz.com/。
--histogram-query VAL  : クエリー実行時間ヒストグラムの境界値を指定します。デフォルト（ミリ秒）:
                     0,1,5,10,25,50,100,500,1000,10000
--histogram-session VAL: セッション時間ヒストグラムの境界値を指定します。デフォルト（ミリ秒）:
                     0,500,1000,30000,60000,600000,1800000,3600000,28800000
--include-file filename: 含めるクエリーの正規表現を格納したファイルのパス。一行に一つの正規表現を記述します。
--include-query regex  : 指定した正規表現に一致しないクエリーを除外します。複数回指定できます。例: "(tbl1|tbl2)"。

--include-pid PID      : セッションのpid（%p）に関連するイベントだけをレポートします。複数回指定できます。
--include-session ID   : セッションID（%c）に関連するイベントだけをレポートします。複数回指定できます。
--include-time  regex  : 指定した正規表現に一致するタイムスタンプだけを含めます。例: "2013-04-12 .*"。複数回指定
                         できます。
--iso-week-number      : 増分モードで週を月曜始まりとし、ISO 8601の週番号（01～53）を使用します。第1週は新年の日
                         が少なくとも4日含まれる最初の週です。
--keep-comments        : 正規化したクエリーからコメントを削除しません。同じ正規化結果を持つクエリーを区別したい
                         場合に便利です。
--journalctl command   : PostgreSQLログファイルの代わりにjournalctlを呼び出すコマンド。例:
                            journalctl -u postgresql-9.5
--log-duration         : log_duration = onとlog_statement = 'all'の両方が生成したログエントリーを、pgBadgerで強
                         制的に関連付けます。
--log-timezone +/-XX   : GMTからの時差（時間）を指定し、解析前にログから読んだ日時を調整します。日時によるログ検
                         索が難しくなります。2のような整数、または2.5のような小数を指定できます。
--month-report YYYY-MM : 指定した月の累積HTMLレポートを作成します。増分出力ディレクトリと、必要なすべてのバイナ
                         リデータファイルが必要です。
--noexplain            : auto_explainが生成した行を処理しません。
--no-fork              : デバッグ用に、プロセスを一切フォークしません。
--no-process-info      : pgbadgerプロセスを識別しやすくするプロセスタイトルの変更を無効にします。一部のシステム
                         ではサポートされていません。
--no-progressbar       : プログレスバーを無効にします。
--noreport             : 増分モードでレポートを生成しません。
--no-week              : 増分モードで週次レポートを作成しません。生成に時間がかかりすぎる場合に便利です。
--normalized-only      : 正規化したすべてのクエリーだけをout.txtに出力します。
--pgbouncer-only       : ヘッダーにPgBouncer関連のメニューだけを表示します。
--pid-dir path         : pidファイルの保存先ディレクトリ。デフォルトは/tmp。
--pid-file file        : pgBadgerの同時実行を管理するpidファイル名。デフォルトはpgbadger.pid。
--pie-limit num        : num%未満の円グラフデータを合算して表示します。
--prettify-json        : JSON出力を読みやすく整形します。
--rebuild              : バイナリデータが残っている増分出力ディレクトリのHTMLレポートをすべて再生成します。
--start-monday         : 増分モードでは週が日曜日に始まります。このオプションで月曜始まりに変更します。
--tempdir DIR          : 一時ファイルを書き出すディレクトリ。デフォルトはFile::Spec->tmpdir() || '/tmp'。
```

pgBadgerは、パスワードなしのSSH接続でリモートログファイルを解析できます。-rまたは --remote-host でホストのIPアドレスまたはホスト名を指定します。SSH接続を細かく制御する追加オプションもあります。

```text
--ssh-identity file      使用する認証鍵ファイルのパス。
--ssh-option  options    SSH接続に渡す-oオプションの一覧。
                         常に使用されるオプション:
                             -o ConnectTimeout=$ssh_timeout
                             -o PreferredAuthentications=hostbased,publickey
--ssh-port port          接続するSSHポート。デフォルトは22。
--ssh-program ssh        SSHプログラムのパス。デフォルトはssh。
--ssh-timeout second     SSH接続失敗までのタイムアウト。デフォルトは10秒。
--ssh-user username      接続先のログイン名。デフォルトは実行ユーザー。
```

`--ssh-sudo`は、リモートでファイルを一覧表示・読み取りするコマンドの先頭に`sudo`を付けます。リモートのSSHユーザーは、対話的な入力なしでこれらのコマンドを`sudo`経由で実行できる必要があります。

解析するログファイルは、URIを使用して指定することもできます。サポートされているプロトコルはhttp[s]および [s]ftpです。ファイルのダウンロードにはcurlコマンドが使用され、ダウンロード中にファイルが解析されます。 sshプロトコルもサポートされており、リモートホストの使用と同様にsshコマンドを使用します。以下の例を参照してください。

終了コード:

```text
0: 正常終了
1: エラーで終了
2: Ctrl+Cなどで中断
3: pidファイルがすでに存在するか、作成できない
4: コマンドラインでログファイルが指定されていない
```

例:

```text
pgbadger /var/log/postgresql.log
pgbadger /var/log/postgres.log.2.gz /var/log/postgres.log.1.gz /var/log/postgres.log
pgbadger /var/log/postgresql/postgresql-2012-05-*
pgbadger --exclude-query="^(COPY|COMMIT)" /var/log/postgresql.log
pgbadger -b "2012-06-25 10:56:11" -e "2012-06-25 10:59:11" /var/log/postgresql.log
cat /var/log/postgres.log | pgbadger -
# stderrログ出力のログ行プレフィックス
pgbadger --prefix '%t [%p]: user=%u,db=%d,client=%h' /pglog/postgresql-2012-08-21*
pgbadger --prefix '%m %u@%d %p %r %a : ' /pglog/postgresql.log
# syslogログ出力のログ行プレフィックス
pgbadger --prefix 'user=%u,db=%d,client=%h,appname=%a' /pglog/postgresql-2012-08-21*
# 8 CPUで10GBのファイルを高速に解析
pgbadger -j 8 /pglog/postgresql-10.1-main.log
```

リモートログファイルにはURI表記を使用します。

```text
pgbadger http://172.12.110.1//var/log/postgresql/postgresql-10.1-main.log
pgbadger ftp://username@172.12.110.14/postgresql-10.1-main.log
pgbadger ssh://username@172.12.110.14:2222//var/log/postgresql/postgresql-10.1-main.log*
```

ローカルPostgreSQLログファイルとリモートpgbouncerログファイルを一緒に使用して解析できます。

```text
pgbadger /var/log/postgresql/postgresql-10.1-main.log ssh://username@172.12.110.14/pgbouncer.log
```

cronジョブで毎週エラーをレポートします。

```text
30 23 * * 1 /usr/bin/pgbadger -q -w /var/log/postgresql.log -o /var/reports/pg_errors.html
```

増分動作を使用して毎週レポートを生成します。

```text
0 4 * * 1 /usr/bin/pgbadger -q `find /var/log/ -mtime -7 -name "postgresql.log*"` -o /var/reports/pg_errors-`date +\%F`.html -l /var/reports/pgbadger_incremental_file.dat
```

これは、ログファイルとHTMLレポートも毎週ローテーションされることを前提としています。

あるいは、自動生成された増分レポートを使用することをお勧めします。

```text
0 4 * * * /usr/bin/pgbadger -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

日ごとおよび週ごとにレポートが生成されます。

増分モードでは、レポートに保存する週数を指定することもできます。

```text
/usr/bin/pgbadger --retention 2 -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

毎日30分間、23:00および13:00にpg_dumpがある場合、次のようにpgBadgerを使用して、これらの期間をレポートから除外できます。

```text
pgbadger --exclude-time "2013-09-.* (23|13):.*" postgresql.log
```

この式は、該当する時間帯の1時間全体を除外するため、30分のダンプ処理以外の時間も除外されます。ダンプの実行時間だけを除外する場合は、分のパターンを絞り込んでください。

これにより、pg_dumpによって生成されたCOPYステートメントが最も遅いクエリーのリストの上位に表示されるのを避けることができます。 --exclude-appname "pg_dump" を使用して、この問題をより簡単な方法で解決することもできます。

また、journalctl出力をログファイルであるかのように解析することもできます。

```text
pgbadger --journalctl 'journalctl -u postgresql-9.5'
```

リモートホストから呼び出すこともできます。

```text
pgbadger -r 192.168.1.159 --journalctl 'journalctl -u postgresql-9.5'
```

コマンドラインでログファイルを指定する必要はありませんが、解析する他のPostgreSQLログファイルがある場合は、通常どおり追加できます。

すべての増分HTMLレポートを後で再構築するには、次の手順を実行します。

```text
rm /path/to/reports/*.js
rm /path/to/reports/*.css
pgbadger -X -I -O /path/to/reports/ --rebuild
```

また、すべてのリソースファイル(JSおよびCSS)も更新されます。このオプションを使用してレポートが作成された場合は、-Eまたは --explode を使用します。

pgBadgerは、logplex形式を使用したHeroku PostgreSQLログもサポートしています。

```text
heroku logs -p postgres | pgbadger -f logplex -o heroku.html -
```

これにより、標準入力を介してHeroku PostgreSQLログがpgbadgerにストリーミングされます。

pgBadgerは、rds形式を使用してRDSおよびCloudWatch PostgreSQLログを自動検出できます。

```text
pgbadger -f rds -o rds_out.html rds.log
```

各Cloud SQL PostgreSQLログはごく普通のPostgreSQLログですが、JSON形式でカプセル化されています。これはpgBadgerによって自動検出されますが、ログ形式を強制する必要がある場合には `jsonlog`を使用します。

```text
pgbadger -f jsonlog -o cloudsql_out.html cloudsql.log
```

jsonlog拡張機能のログとはJSONの構造が異なりますが、pgBadgerは両方を解析できます。

pgBadgerは、KubernetesのCloudNativePG Postgresオペレーターによって生成されたログもサポートします。

```text
pgbadger -f jsonlog -o cnpg_out.html cnpg.log
```

1か月にわたる累積レポートを作成するには、次のコマンドを使用します。

```text
pgbadger --month-report 2019-05 /path/to/incremental/reports/
```

これにより、増分レポートのカレンダービューに月名へのリンクが追加され、2019年5月のレポートが表示されます。このオプションを使用してレポートが作成された場合は、-Eまたは --explode を使用します。
